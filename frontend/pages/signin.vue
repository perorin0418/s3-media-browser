<script setup lang="ts">
definePageMeta({});

const auth = useAuth();
const errorMessage = ref<string | null>(null);
const isRedirecting = ref(false);

const getErrorMessage = (error: unknown) =>
  error instanceof Error ? error.message : "Failed to start sign-in.";

const startSignIn = async () => {
  errorMessage.value = null;
  try {
    const url = await auth.buildHostedUiSignInUrl();
    isRedirecting.value = true;
    window.location.assign(url);
  } catch (error: unknown) {
    isRedirecting.value = false;
    errorMessage.value = getErrorMessage(error);
  }
};
</script>

<template>
  <section class="signin-page">
    <div class="signin-card">
      <h1 class="signin-title">S3 Media Browser</h1>
      <p class="signin-lead">Sign in with Hosted UI to continue.</p>
      <button
        class="signin-button"
        type="button"
        :disabled="isRedirecting"
        @click="startSignIn"
      >
        {{ isRedirecting ? "Redirecting..." : "Sign in" }}
      </button>
      <p v-if="errorMessage" class="signin-error">{{ errorMessage }}</p>
    </div>
  </section>
</template>

<style scoped>
.signin-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: var(--space-4);
}

.signin-card {
  width: min(420px, 100%);
  background: var(--color-surface);
  border-radius: var(--radius-2);
  padding: var(--space-5);
  box-shadow: var(--shadow-card);
}

.signin-title {
  margin: 0 0 var(--space-2);
  font-size: 28px;
}

.signin-lead {
  margin: 0 0 var(--space-4);
  color: var(--color-muted);
}

.signin-button {
  width: 100%;
  border: none;
  border-radius: var(--radius-1);
  padding: var(--space-2) var(--space-3);
  background: var(--color-accent);
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.signin-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.signin-error {
  margin-top: var(--space-3);
  color: var(--color-danger);
}
</style>
