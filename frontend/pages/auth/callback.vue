<script setup lang="ts">
definePageMeta({});

const auth = useAuth();
const route = useRoute();
const errorMessage = ref<string | null>(null);
const isProcessing = ref(true);

const getErrorMessage = (error: unknown) =>
  error instanceof Error ? error.message : "Authentication failed.";

onMounted(async () => {
  const code = typeof route.query.code === "string" ? route.query.code : null;
  const state = typeof route.query.state === "string" ? route.query.state : null;
  const error = typeof route.query.error === "string" ? route.query.error : null;
  const description =
    typeof route.query.error_description === "string"
      ? route.query.error_description
      : null;

  if (error) {
    errorMessage.value = description ? `${error}: ${description}` : error;
    auth.clearTokens();
    isProcessing.value = false;
    return;
  }

  if (!code) {
    errorMessage.value = "Authorization code is missing.";
    auth.clearTokens();
    isProcessing.value = false;
    return;
  }

  if (!state) {
    errorMessage.value = "Authentication state is missing.";
    auth.clearTokens();
    isProcessing.value = false;
    return;
  }

  try {
    await auth.exchangeCodeForTokens(code, state);
    await navigateTo("/", { replace: true });
  } catch (error: unknown) {
    errorMessage.value = getErrorMessage(error);
    auth.clearTokens();
    isProcessing.value = false;
  }
});
</script>

<template>
  <section class="callback-page">
    <div class="callback-card">
      <h1 class="callback-title">Completing sign-in</h1>
      <p v-if="isProcessing" class="callback-text">Processing authentication...</p>
      <p v-else-if="errorMessage" class="callback-error">{{ errorMessage }}</p>
      <NuxtLink v-if="errorMessage" class="callback-link" to="/signin">
        Back to sign-in
      </NuxtLink>
    </div>
  </section>
</template>

<style scoped>
.callback-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: var(--space-4);
}

.callback-card {
  width: min(420px, 100%);
  background: var(--color-surface);
  border-radius: var(--radius-2);
  padding: var(--space-5);
  box-shadow: var(--shadow-card);
}

.callback-title {
  margin: 0 0 var(--space-2);
  font-size: 24px;
}

.callback-text {
  margin: 0;
  color: var(--color-muted);
}

.callback-error {
  margin: 0 0 var(--space-3);
  color: var(--color-danger);
}

.callback-link {
  color: var(--color-accent);
  font-weight: 600;
}
</style>
