type AuthStatus = "unknown" | "authenticated" | "unauthenticated";

type StoredTokens = {
  accessToken: string;
  idToken: string;
  refreshToken: string | null;
  tokenType: string;
  expiresAt: number;
};

type TokenResponse = {
  access_token: string;
  id_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
};

const STORAGE_KEY = "s3mb.auth.tokens";
const PKCE_VERIFIER_KEY = "s3mb.auth.pkce_verifier";
const OAUTH_STATE_KEY = "s3mb.auth.state";

const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null;

const isStoredTokens = (value: unknown): value is StoredTokens => {
  if (!isRecord(value)) return false;
  return (
    typeof value.accessToken === "string" &&
    typeof value.idToken === "string" &&
    typeof value.tokenType === "string" &&
    typeof value.expiresAt === "number" &&
    (typeof value.refreshToken === "string" || value.refreshToken === null)
  );
};

const isTokenResponse = (value: unknown): value is TokenResponse => {
  if (!isRecord(value)) return false;
  if (typeof value.access_token !== "string") return false;
  if (typeof value.id_token !== "string") return false;
  if (typeof value.token_type !== "string") return false;
  if (typeof value.expires_in !== "number") return false;
  if (value.refresh_token !== undefined && typeof value.refresh_token !== "string") {
    return false;
  }
  return true;
};

const normalizeBaseUrl = (value: string) =>
  value.endsWith("/") ? value.slice(0, -1) : value;

const toBase64Url = (bytes: Uint8Array) => {
  let binary = "";
  bytes.forEach((value) => {
    binary += String.fromCharCode(value);
  });
  const base64 = btoa(binary);
  return base64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/g, "");
};

const generateRandomString = (length: number) => {
  const bytes = new Uint8Array(length);
  crypto.getRandomValues(bytes);
  return toBase64Url(bytes);
};

const createCodeChallenge = async (verifier: string) => {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const digest = await crypto.subtle.digest("SHA-256", data);
  return toBase64Url(new Uint8Array(digest));
};

const readStoredTokens = (): StoredTokens | null => {
  if (!process.client) return null;
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return null;
  try {
    const parsed: unknown = JSON.parse(raw);
    if (!isStoredTokens(parsed)) {
      localStorage.removeItem(STORAGE_KEY);
      return null;
    }
    return parsed;
  } catch {
    localStorage.removeItem(STORAGE_KEY);
    return null;
  }
};

const isExpired = (tokens: StoredTokens) => tokens.expiresAt <= Date.now();

export const useAuth = () => {
  const tokens = useState<StoredTokens | null>("auth.tokens", () => null);
  const status = useState<AuthStatus>("auth.status", () => "unknown");
  const config = useRuntimeConfig();

  const hostedUiDomain = (config.public.authHostedUiDomain ?? "").trim();
  const clientId = (config.public.authClientId ?? "").trim();
  const callbackUrl = (config.public.authCallbackUrl ?? "").trim();
  const logoutUrl = (config.public.authLogoutUrl ?? "").trim();

  const resolveCallbackUrl = () => {
    if (callbackUrl) return callbackUrl;
    if (process.client) return `${window.location.origin}/auth/callback`;
    return "";
  };

  const resolveLogoutUrl = () => {
    if (logoutUrl) return logoutUrl;
    if (process.client) return `${window.location.origin}/`;
    return "";
  };

  const getRequiredConfig = () => {
    if (!hostedUiDomain) {
      throw new Error("authHostedUiDomain is not set.");
    }
    if (!clientId) {
      throw new Error("authClientId is not set.");
    }
    const redirectUri = resolveCallbackUrl();
    if (!redirectUri) {
      throw new Error("Callback URL is not available.");
    }
    return {
      baseUrl: normalizeBaseUrl(hostedUiDomain),
      clientId,
      redirectUri,
      logoutUri: resolveLogoutUrl(),
    };
  };

  const setTokens = (next: StoredTokens) => {
    tokens.value = next;
    status.value = "authenticated";
    if (process.client) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    }
  };

  const clearTokens = () => {
    tokens.value = null;
    status.value = "unauthenticated";
    if (process.client) {
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  const loadFromStorage = () => {
    if (!process.client) return;
    const stored = readStoredTokens();
    if (stored && !isExpired(stored)) {
      tokens.value = stored;
      status.value = "authenticated";
      return;
    }
    if (stored) {
      localStorage.removeItem(STORAGE_KEY);
    }
    tokens.value = null;
    status.value = "unauthenticated";
  };

  const storeAuthRequest = (state: string, verifier: string) => {
    if (!process.client) return;
    sessionStorage.setItem(OAUTH_STATE_KEY, state);
    sessionStorage.setItem(PKCE_VERIFIER_KEY, verifier);
  };

  const consumeAuthVerifier = (state: string) => {
    if (!process.client) return null;
    const storedState = sessionStorage.getItem(OAUTH_STATE_KEY);
    const verifier = sessionStorage.getItem(PKCE_VERIFIER_KEY);
    sessionStorage.removeItem(OAUTH_STATE_KEY);
    sessionStorage.removeItem(PKCE_VERIFIER_KEY);
    if (!storedState || storedState !== state) return null;
    return verifier;
  };

  const buildHostedUiSignInUrl = async () => {
    const { baseUrl, clientId, redirectUri } = getRequiredConfig();
    const state = generateRandomString(32);
    const verifier = generateRandomString(64);
    const challenge = await createCodeChallenge(verifier);
    storeAuthRequest(state, verifier);
    const params = new URLSearchParams({
      response_type: "code",
      client_id: clientId,
      redirect_uri: redirectUri,
      scope: "openid email profile",
      state,
      code_challenge: challenge,
      code_challenge_method: "S256",
    });
    return `${baseUrl}/oauth2/authorize?${params.toString()}`;
  };

  const buildHostedUiSignOutUrl = () => {
    const { baseUrl, clientId, logoutUri } = getRequiredConfig();
    const params = new URLSearchParams({
      client_id: clientId,
      logout_uri: logoutUri,
    });
    return `${baseUrl}/logout?${params.toString()}`;
  };

  const exchangeCodeForTokens = async (code: string, state: string) => {
    const { baseUrl, clientId, redirectUri } = getRequiredConfig();
    const verifier = consumeAuthVerifier(state);
    if (!verifier) {
      throw new Error("Invalid authentication state.");
    }
    const body = new URLSearchParams({
      grant_type: "authorization_code",
      client_id: clientId,
      code,
      redirect_uri: redirectUri,
      code_verifier: verifier,
    });

    const response = await $fetch<unknown>(`${baseUrl}/oauth2/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: body.toString(),
    });

    if (!isTokenResponse(response)) {
      throw new Error("Unexpected token response.");
    }

    const expiresAt = Date.now() + response.expires_in * 1000;
    setTokens({
      accessToken: response.access_token,
      idToken: response.id_token,
      refreshToken: response.refresh_token ?? null,
      tokenType: response.token_type,
      expiresAt,
    });
  };

  const isAuthenticated = () => status.value === "authenticated";

  const isAuthenticatedWithFreshToken = () => {
    const current = tokens.value;
    if (!current) return false;
    if (isExpired(current)) {
      clearTokens();
      return false;
    }
    return status.value === "authenticated";
  };

  return {
    status,
    tokens,
    loadFromStorage,
    clearTokens,
    buildHostedUiSignInUrl,
    buildHostedUiSignOutUrl,
    exchangeCodeForTokens,
    isAuthenticated,
    isAuthenticatedWithFreshToken,
  };
};
