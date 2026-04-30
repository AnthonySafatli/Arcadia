<template>
    <div class="game-room">
        <header class="room-header">
            <router-link to="/" class="wordmark">arcadia</router-link>

            <div class="room-info">
                <span class="room-label">room</span>
                <span class="room-code">{{ roomId }}</span>
            </div>

            <StatusBadge :status="statusClass" :label="roomStatus" />
        </header>

        <main class="room-body">
            <!-- Loading -->
            <Spinner v-if="roomStatus === 'loading'" />

            <!-- Waiting state -->
            <WaitingLobby
                v-else-if="roomStatus === 'waiting'"
                :room="room!"
                :on-connect="onConnect"
            />

            <!-- Game canvas placeholder -->
            <div v-else class="game-canvas">
                <p class="placeholder-text">Game component renders here</p>
                <!-- <component :is="gameComponent" :state="state" /> -->
            </div>
        </main>
    </div>
</template>

<script setup lang="ts">
import StatusBadge from './StatusBadge.vue'
import WaitingLobby from './WaitingLobby/WaitingLobby.vue'
import Spinner from '@/components/Spinner.vue'

import type { Room } from '@/dtos/RoomDto'

import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useQuery } from '@tanstack/vue-query'

const route = useRoute()
const roomId = computed(() => route.params.id)

// TODO: Display error
const { data, isError, isPending } = useQuery<Room>({
    queryKey: ['rooms', roomId],
    queryFn: (): Promise<Room> => fetch(`/api/rooms/${roomId.value}`).then((r) => r.json()),
})

watch(data, (newData) => {
    if (newData) room.value = newData
})

const room = ref<Room | null>(null)

const roomStatus = computed(
    () => room.value?.status ?? (isPending ? 'loading' : isError ? 'error' : null),
)
const statusClass = computed(
    () =>
        ({
            nothing: '',
            error: 'red',
            loading: 'yellow',
            waiting: 'yellow',
            playing: 'green',
            over: 'red',
        })[roomStatus.value ?? 'nothing'],
)

function onConnect() {
    console.log('connected!')
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

.room-body {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
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
