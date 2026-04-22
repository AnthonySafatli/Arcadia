<template>
  <div class="game-room">
    <header class="room-header">
      <router-link to="/" class="wordmark">arcadia</router-link>

      <div class="room-info">
        <span class="room-label">room</span>
        <span class="room-code">{{ roomId }}</span>
      </div>

      <div class="room-status">
        <span class="status-dot" :class="statusClass" />
        <span class="status-text">{{ statusText }}</span>
      </div>
    </header>

    <main class="room-body">
      <!-- Waiting state -->
      <div v-if="gameState === 'waiting'" class="waiting-screen">
        <div class="waiting-animation"><span /><span /><span /></div>
        <p class="waiting-title">Waiting for players</p>
        <p class="waiting-sub">Share your room code</p>
        <div class="share-code">
          <span class="share-code-text">{{ roomId }}</span>
          <button class="btn btn-ghost copy-btn" @click="copyCode">
            {{ copied ? 'Copied!' : 'Copy' }}
          </button>
        </div>
      </div>

      <!-- Game canvas placeholder -->
      <div v-else class="game-canvas">
        <p class="placeholder-text">Game component renders here</p>
        <!-- <component :is="gameComponent" :state="state" /> -->
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const roomId = computed(() => route.params.id)

const gameState = ref('waiting') // 'waiting' | 'playing' | 'over'
const copied = ref(false)

const statusClass = computed(
  () =>
    ({
      waiting: 'yellow',
      playing: 'green',
      over: 'red',
    })[gameState.value],
)

const statusText = computed(
  () =>
    ({
      waiting: 'Waiting',
      playing: 'Live',
      over: 'Ended',
    })[gameState.value],
)

async function copyCode() {
  await navigator.clipboard.writeText(roomId.value)
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<style scoped>
.game-room {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-base);
}

.room-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 32px;
  border-bottom: 1px solid var(--bg-border);
  background: var(--bg-card);
  flex-shrink: 0;
}

.wordmark {
  font-family: var(--font-display);
  font-size: 24px;
  letter-spacing: 0.1em;
  color: var(--text-primary);
  text-decoration: none;
  transition: color var(--transition);
}
.wordmark:hover {
  color: var(--green-bright);
}

.room-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}

.room-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.room-code {
  font-family: var(--font-mono);
  font-size: 1.1rem;
  font-weight: 500;
  color: var(--green-bright);
  letter-spacing: 0.2em;
  text-shadow: 0 0 12px var(--green-glow);
}

.room-status {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-dot.green {
  background: var(--green-bright);
  box-shadow: 0 0 6px var(--green-bright);
  animation: pulse-dot 2s infinite;
}
.status-dot.yellow {
  background: #f5c518;
  box-shadow: 0 0 6px #f5c518;
  animation: pulse-dot 2s infinite;
}
.status-dot.red {
  background: #ff4444;
}

@keyframes pulse-dot {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.4;
  }
}

.status-text {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-secondary);
}

.room-body {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.waiting-screen {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  animation: fadeUp 0.5s ease both;
}

.waiting-animation {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.waiting-animation span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--green-bright);
  animation: bounce 1.2s ease-in-out infinite;
}

.waiting-animation span:nth-child(2) {
  animation-delay: 0.2s;
}
.waiting-animation span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-12px);
    opacity: 1;
  }
}

.waiting-title {
  font-family: var(--font-display);
  font-size: 32px;
  letter-spacing: 0.08em;
  color: var(--text-primary);
}

.waiting-sub {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-muted);
}

.share-code {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--bg-card);
  border: 1px solid var(--bg-border);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  margin-top: 8px;
}

.share-code-text {
  font-family: var(--font-mono);
  font-size: 1.4rem;
  font-weight: 500;
  letter-spacing: 0.3em;
  color: var(--green-bright);
}

.copy-btn {
  padding: 8px 16px;
  font-size: 0.75rem;
}

.game-canvas {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-text {
  font-family: var(--font-mono);
  color: var(--text-muted);
  font-size: 0.85rem;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
