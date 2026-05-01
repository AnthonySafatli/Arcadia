<template>
    <div class="waiting-screen">
        <p class="waiting-title">Ready to play?</p>
        <p class="waiting-sub">{{ room.game_name }}</p>
        <button class="btn btn-primary" @click="$emit('join')">Join Lobby</button>
    </div>
</template>

<script setup lang="ts">
import type { Room } from '@/dtos/RoomDto'

defineProps<{ room: Room }>()
defineEmits<{ join: [] }>()
</script>

<style scoped>
.waiting-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
    animation: fadeUp 0.5s ease both;
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
</style>
