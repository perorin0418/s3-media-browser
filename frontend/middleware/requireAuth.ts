export default defineNuxtRouteMiddleware(() => {
  const auth = useAuth();

  const status = auth.resolveAuthStatus();

  if (status !== "authenticated" || !auth.isAuthenticatedWithFreshToken()) {
    return navigateTo("/signin");
  }
});
