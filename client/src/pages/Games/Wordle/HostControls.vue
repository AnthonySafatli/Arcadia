<template>
	<div v-if="isHost" class="host-controls">
		<button v-if="!roundOver && allFinished" class="btn-ctrl" @click="$emit('endRound')">
			end round
		</button>
		<button v-if="roundOver" class="btn-ctrl btn-ctrl--primary" @click="$emit('nextRound')">
			next round
		</button>
		<button class="btn-ctrl btn-ctrl--ghost" @click="$emit('resetGame')">
			<svg
				width="12"
				height="12"
				viewBox="0 0 24 24"
				fill="none"
				stroke="currentColor"
				stroke-width="2"
				stroke-linecap="round"
				stroke-linejoin="round">
				<polyline points="23 4 23 10 17 10"></polyline>
				<path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
			</svg>
			reset
		</button>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import type { OtherPlayer } from "./WordleState";

import { usePlayerId } from "@/composables/usePlayerId";

const props = defineProps<{
	roundOver: boolean;
	finished: boolean;
	hostPlayerId: string | undefined | null;
	otherPlayers: Record<string, OtherPlayer>;
}>();

const emit = defineEmits<{
	(e: "endRound"): void;
	(e: "nextRound"): void;
	(e: "resetGame"): void;
}>();

const playerId = usePlayerId();

const isHost = computed(() => props.hostPlayerId === playerId);

const allFinished = computed(() => {
	const me = props.finished;
	const others = Object.values(props.otherPlayers).every((p) => p.finished);
	return me && others;
});
</script>

<style scoped>
.host-controls {
	display: flex;
	gap: 8px;
	align-items: center;
}

.btn-ctrl {
	display: inline-flex;
	align-items: center;
	gap: 6px;
	font-family: var(--font-mono);
	font-size: 0.7rem;
	font-weight: 500;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	padding: 10px 20px;
	border-radius: var(--radius-md);
	cursor: pointer;
	transition: all 200ms ease;
	background: transparent;
	color: var(--text-muted);
	border: 1px solid var(--bg-border);
}

.btn-ctrl:hover {
	border-color: var(--green-dim);
	color: var(--green-bright);
}

.btn-ctrl--primary {
	background: var(--green-bright);
	color: var(--bg-base);
	border-color: var(--green-bright);
	box-shadow: 0 0 20px rgba(57, 255, 138, 0.3);
}

.btn-ctrl--primary:hover {
	box-shadow: 0 0 32px rgba(57, 255, 138, 0.5);
	transform: translateY(-1px);
}

.btn-ctrl--ghost {
	color: var(--text-muted);
}
</style>
