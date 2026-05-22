<template>
	<div class="game-canvas">
		<TicTacToe v-if="room.game_slug === 'tic-tac-toe'" />
		<TheMind v-else-if="room.game_slug === 'the-mind'" />
		<p v-else class="placeholder-text">Game not found</p>
	</div>
</template>

<script setup>
import TicTacToe from "@/pages/Games/TicTacToe/TicTacToe.vue";
import TheMind from "@/pages/Games/TheMind/TheMind.vue";

import { useGameRoom } from "@/composables/useGameRoom";

const { room } = useGameRoom();
</script>

<style scoped>
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
</style>
