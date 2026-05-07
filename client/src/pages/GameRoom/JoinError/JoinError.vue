<template>
  <div class="error-screen">
    <span class="error-icon">✕</span>
    <p class="error-title">Something went wrong</p>
    <p class="error-message">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{ error: string }>();
</script>

<style scoped>
.error-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  animation: fadeUp 0.5s ease both;
}

.error-icon {
  font-size: 28px;
  color: var(--color-error, #e05555);
  line-height: 1;
}

.error-title {
  font-family: var(--font-display);
  font-size: 32px;
  letter-spacing: 0.08em;
  color: var(--text-primary);
}

.error-message {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-error, #e05555);
  opacity: 0.85;
}
</style>