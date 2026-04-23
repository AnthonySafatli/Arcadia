<template>
    <Page back-btn>
        <div class="content">
            <div class="page-header">
                <span class="label">host a game</span>
                <h2 class="title">Choose your game</h2>
            </div>

            <Select v-model="selected" :items="selectOptions" />

            <button class="btn btn-primary launch-btn" :disabled="!selected" @click="launch">
                Launch Room
            </button>
        </div>
    </Page>
</template>

<script setup lang="ts">
import type { SelectItem } from '@/types/SelectType'

import Page from '@/components/Page.vue'
import Select from './Select.vue'

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const selected = ref<string | null>(null)

const games = [
    { id: 'tictactoe', name: 'Tic-tac-toe', icon: '⊞', players: '2 players', type: 'Classic' },
    { id: 'pong', name: 'Pong', icon: '◈', players: '2 players', type: 'Arcade' },
    { id: 'chess', name: 'Chess', icon: '♟', players: '2 players', type: 'Strategy' },
    { id: 'checkers', name: 'Checkers', icon: '●', players: '2 players', type: 'Classic' },
]

const selectOptions: SelectItem[] = games.map((x) => ({
    id: x.id,
    name: x.name,
    icon: x.icon,
    tags: [x.players, x.type],
}))

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
