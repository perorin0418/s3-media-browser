<script setup lang="ts">
definePageMeta({
  middleware: ["requireAuth"],
});
</script>

<template>
  <section class="home-page">
    <div class="home-card">
      <h1 class="home-title">Welcome</h1>
      <p class="home-text">Authentication is confirmed.</p>
    </div>
  </section>
</template>

<style scoped>
.home-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: var(--space-4);
}

.home-card {
  width: min(520px, 100%);
  background: var(--color-surface);
  border-radius: var(--radius-2);
  padding: var(--space-5);
  box-shadow: var(--shadow-card);
}

.home-title {
  margin: 0 0 var(--space-2);
  font-size: 26px;
}

.home-text {
  margin: 0;
  color: var(--color-muted);
}
</style>
