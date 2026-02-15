<script setup lang="ts">
const auth = useAuth();

const signOutUrl = computed(() => {
  if (auth.status.value !== "authenticated") return "";
  try {
    return auth.buildHostedUiSignOutUrl();
  } catch {
    return "";
  }
});
</script>

<template>
  <div v-if="auth.status === 'authenticated'" class="app-shell">
    <header class="app-header">
      <div class="brand">S3 Media Browser</div>
      <nav class="app-nav">
        <NuxtLink class="nav-link" to="/">Home</NuxtLink>
        <NuxtLink class="nav-link" to="/">Browse</NuxtLink>
      </nav>
      <a
        class="nav-link signout"
        :href="signOutUrl"
        :aria-disabled="!signOutUrl"
      >
        Sign out
      </a>
    </header>
    <main class="app-main">
      <NuxtPage />
    </main>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: grid;
  grid-template-rows: auto 1fr;
  background: var(--color-background);
}

.app-header {
  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}

.brand {
  font-size: 18px;
  font-weight: 600;
}

.app-nav {
  display: flex;
  gap: var(--space-3);
}

.nav-link {
  color: inherit;
  text-decoration: none;
  font-weight: 500;
}

.nav-link:hover {
  text-decoration: underline;
}

.signout {
  color: var(--color-accent);
}

.app-main {
  padding: var(--space-4);
}

@media (max-width: 720px) {
  .app-header {
    grid-template-columns: 1fr;
    align-items: start;
  }

  .app-nav {
    flex-wrap: wrap;
  }
}
</style>
