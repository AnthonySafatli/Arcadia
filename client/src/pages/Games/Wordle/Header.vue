<template>
	<div class="wordle-header">
		<div class="header-left">
			<span class="round-label">round {{ props.round }}</span>
			<TallyRow :score="props.playerScore" />
		</div>
		<div class="header-right">
			<span class="wordle-status" :class="statusClass">{{ statusText }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import TallyRow from "./TallyRow.vue";

import type { FinishedInfo, PlayerScore } from "./WordleState";

const props = defineProps<{
	round: number;
	playerScore: PlayerScore | undefined | null;
	roundOver: boolean;
	finished: boolean;
	finishedInfo: FinishedInfo | null;
	guessesRemaining: number;
}>();

const statusText = computed(() => {
	if (props.roundOver) return "round over";
	if (props.finished) {
		return props.finishedInfo?.solved ? "solved!" : "out of guesses";
	}
	return `${props.guessesRemaining} left`;
});

const statusClass = computed(() => ({
	"status--win": props.finishedInfo?.solved && !props.roundOver,
	"status--lose": props.finished && !props.finishedInfo?.solved,
	"status--over": props.roundOver,
}));
</script>

<style scoped>
.wordle-header {
	display: flex;
	align-items: baseline;
	justify-content: space-between;
	width: 100%;
	padding-bottom: 8px;
	border-bottom: 1px solid var(--bg-border);
}

.header-left {
	display: flex;
	align-items: baseline;
	gap: 12px;
}

.round-label {
	font-family: var(--font-mono);
	font-size: 0.65rem;
	letter-spacing: 0.2em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.wordle-status {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--text-muted);
	transition: color 200ms ease;
}

.status--win {
	color: var(--green-bright);
}
.status--lose {
	color: #ff6b6b;
}
.status--over {
	color: var(--text-secondary);
	animation: blink 1s ease-in-out 3;
}

@keyframes blink {
	0%,
	100% {
		opacity: 1;
	}
	50% {
		opacity: 0.3;
	}
}
</style>
