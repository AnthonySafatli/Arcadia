<template>
  <div class="page">
    <div class="grid-bg" />
    <router-link to="/" class="back-link">← back</router-link>

    <div class="content">
      <div class="page-header">
        <span class="label">host a game</span>
        <h2 class="title">Choose your game</h2>
      </div>

      <div class="games-grid">
        <button
          v-for="game in games"
          :key="game.id"
          class="game-card"
          :class="{ selected: selected === game.id }"
          @click="selected = game.id"
        >
          <div class="game-icon">{{ game.icon }}</div>
          <div class="game-info">
            <div class="game-name">{{ game.name }}</div>
            <div class="game-meta">
              <span class="badge">{{ game.players }}</span>
              <span class="badge">{{ game.type }}</span>
            </div>
          </div>
          <div class="game-select-indicator" />
        </button>
      </div>

      <button class="btn btn-primary launch-btn" :disabled="!selected" @click="launch">
        Launch Room
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selected = ref(null)

const games = [
  { id: 'tictactoe', name: 'Tic-tac-toe', icon: '⊞', players: '2 players', type: 'Classic' },
  { id: 'pong', name: 'Pong', icon: '◈', players: '2 players', type: 'Arcade' },
  { id: 'chess', name: 'Chess', icon: '♟', players: '2 players', type: 'Strategy' },
  { id: 'checkers', name: 'Checkers', icon: '●', players: '2 players', type: 'Classic' },
]

function launch() {
  if (!selected.value) return
  // TODO: create room via server, get room ID back
  const mockRoomId = Math.random().toString(36).slice(2, 8).toUpperCase()
  router.push(`/room/${mockRoomId}`)
}
</script>

<style scoped>
.content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 560px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.page-header {
  animation: fadeUp 0.5s ease both;
}

.label {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--green-mid);
}

.title {
  font-family: var(--font-display);
  font-size: clamp(36px, 6vw, 56px);
  letter-spacing: 0.05em;
  color: var(--text-primary);
  line-height: 1.1;
  margin-top: 4px;
}

.games-grid {
  display: flex;
  flex-direction: column;
  gap: 10px;
  animation: fadeUp 0.5s 0.1s ease both;
}

.game-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 18px 20px;
  background: var(--bg-card);
  border: 1px solid var(--bg-border);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: var(--transition);
  text-align: left;
  position: relative;
  overflow: hidden;
}

.game-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: var(--green-bright);
  transform: scaleY(0);
  transition: transform var(--transition);
}

.game-card:hover {
  border-color: var(--green-dim);
  background: var(--bg-raised);
}

.game-card.selected {
  border-color: var(--green-dim);
  background: var(--bg-raised);
  box-shadow:
    0 0 0 1px var(--green-dim),
    inset 0 0 40px var(--green-glow-sm);
}

.game-card.selected::before {
  transform: scaleY(1);
}

.game-icon {
  font-size: 24px;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--bg-base);
  border-radius: var(--radius-sm);
  border: 1px solid var(--bg-border);
  flex-shrink: 0;
}

.game-info {
  flex: 1;
}

.game-name {
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.95rem;
}

.game-meta {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.badge {
  font-family: var(--font-mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  color: var(--text-muted);
  background: var(--bg-base);
  border: 1px solid var(--bg-border);
  border-radius: 3px;
  padding: 2px 6px;
  text-transform: uppercase;
}

.game-select-indicator {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid var(--bg-border);
  transition: var(--transition);
  flex-shrink: 0;
}

.game-card.selected .game-select-indicator {
  border-color: var(--green-bright);
  background: var(--green-bright);
  box-shadow: 0 0 8px var(--green-glow);
}

.launch-btn {
  width: 100%;
  padding: 16px;
  font-size: 0.9rem;
  animation: fadeUp 0.5s 0.2s ease both;
}

.launch-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
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
