export default defineNuxtRouteMiddleware(() => {
  const auth = useAuth();

  if (process.client && auth.status.value === "unknown") {
    auth.loadFromStorage();
  }

  if (!auth.isAuthenticatedWithFreshToken()) {
    return navigateTo("/signin");
  }
});
