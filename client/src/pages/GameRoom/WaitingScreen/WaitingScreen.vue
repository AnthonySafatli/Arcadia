<template>
    <div class="waiting-screen">
        <LoadingAnimation />
        <p class="waiting-title">Waiting for players</p>
        <p class="waiting-sub">Share your room code</p>
        <ShareCode :code="roomId" />
    </div>
</template>

<script setup>
import LoadingAnimation from './LoadingAnimation.vue'
import ShareCode from './ShareCode.vue'
defineProps({ roomId: String })
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
