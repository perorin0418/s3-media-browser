export default defineNuxtConfig({
  ssr: false,
  typescript: {
    strict: true,
  },
  app: {
    head: {
      title: "S3 Media Browser",
      meta: [{ name: "viewport", content: "width=device-width, initial-scale=1" }],
    },
  },
  css: ["~/styles/tokens.css", "~/styles/base.css", "~/styles/utilities.css"],
  runtimeConfig: {
    public: {
      authHostedUiDomain: "",
      authClientId: "",
      authCallbackUrl: "http://localhost:3000/auth/callback",
      authLogoutUrl: "http://localhost:3000/",
    },
  },
});
