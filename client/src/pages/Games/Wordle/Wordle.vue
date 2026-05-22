<template>
	<div class="wordle-wrap">
		<div class="grid-bg" aria-hidden="true">
			<div class="grid-bg-inner"></div>
		</div>

		<div class="wordle">
			<Header
				:round="state.round"
				:player-score="state.scores[playerId]"
				:round-over="state.round_over"
				:finished="state.finished"
				:finished-info="state.finished_info"
				:guesses-remaining="state.guesses_remaining" />

			<PlayerScores
				:scores="state.scores"
				:all-players="allPlayers"
				:finished="state.finished"
				:other-players="state.other_players" />

			<GuessBoard
				:guesses="state.guesses"
				:finished="state.finished"
				:current-input="currentInput"
				:shake-row="shakeRow" />

			<!-- ROUND OVER REVEAL -->
			<div v-if="state.round_over" class="round-over-banner">
				<span class="reveal-label">the word was</span>
				<span class="reveal-word">{{ state.secret_word }}</span>
			</div>

			<!-- ERROR -->
			<div v-if="errorMsg" class="error-toast">{{ errorMsg }}</div>

			<HostControls
				:round-over="state.round_over"
				:finished="state.finished"
				:host-player-id="room?.host_player_id"
				:other-players="state.other_players"
				@end-round="endRound"
				@next-round="nextRound"
				@reset-game="resetGame" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";

import type { WordleState } from "./WordleState";
import { defaultWordleState } from "./WordleState";

import Header from "./Header.vue";
import PlayerScores from "./PlayerScores.vue";
import GuessBoard from "./GuessBoard.vue";
import HostControls from "./HostControls.vue";

import { usePlayerId } from "@/composables/usePlayerId";
import { useGameRoom } from "@/composables/useGameRoom";
import { useSocket } from "@/composables/useSocket";

const playerId = usePlayerId();
const { sendAction } = useSocket();
const { room, state: socketState } = useGameRoom();
const state = computed(() => (socketState.value as WordleState) ?? defaultWordleState());

const currentInput = ref("");
const errorMsg = ref<string | null>(null);
const shakeRow = ref<number | null>(null);
let errorTimeout: ReturnType<typeof setTimeout> | null = null;

const allPlayers = computed(() => room.value?.players ?? []);

function showError(msg: string) {
	errorMsg.value = msg;
	if (errorTimeout) clearTimeout(errorTimeout);
	errorTimeout = setTimeout(() => (errorMsg.value = null), 1800);
}

function triggerShake() {
	const row = state.value.guesses.length;
	shakeRow.value = row;
	setTimeout(() => (shakeRow.value = null), 500);
}

function handleKey(e: KeyboardEvent) {
	if (state.value.finished || state.value.round_over) return;
	const key = e.key;

	if (key === "Enter") {
		if (currentInput.value.length < 5) {
			showError("not enough letters");
			triggerShake();
			return;
		}
		sendAction(room.value?.code!, playerId, { type: "guess", word: currentInput.value });
		currentInput.value = "";
		return;
	}

	if (key === "Backspace") {
		currentInput.value = currentInput.value.slice(0, -1);
		return;
	}

	if (/^[a-zA-Z]$/.test(key) && currentInput.value.length < 5) {
		currentInput.value += key.toUpperCase();
	}
}

onMounted(() => window.addEventListener("keydown", handleKey));
onUnmounted(() => window.removeEventListener("keydown", handleKey));

function endRound() {
	sendAction(room.value?.code!, playerId, { type: "end_round" });
}

function nextRound() {
	sendAction(room.value?.code!, playerId, { type: "next_round" });
}

function resetGame() {
	sendAction(room.value?.code!, playerId, { type: "reset" });
}
</script>

<style scoped>
.wordle-wrap {
	position: relative;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 32px 24px;
	width: 100%;
	min-height: 100%;
}

.grid-bg {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(var(--bg-border) 1px, transparent 1px),
		linear-gradient(90deg, var(--bg-border) 1px, transparent 1px);
	background-size: 48px 48px;
	opacity: 0.4;
	pointer-events: none;
}

.grid-bg-inner {
	position: absolute;
	inset: 0;
	background: radial-gradient(ellipse 70% 70% at 50% 50%, transparent 30%, var(--bg-base) 100%);
}

.wordle {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20px;
	width: 100%;
	max-width: 480px;
}

/* ── Round over banner ── */
.round-over-banner {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 4px;
	padding: 16px 32px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	animation: fade-up 300ms ease;
}

@keyframes fade-up {
	from {
		opacity: 0;
		transform: translateY(8px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

.reveal-label {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.25em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.reveal-word {
	font-family: var(--font-display);
	font-size: 2.5rem;
	letter-spacing: 0.3em;
	text-transform: uppercase;
	color: var(--green-bright);
	text-shadow: 0 0 24px rgba(57, 255, 138, 0.5);
}

/* ── Error toast ── */
.error-toast {
	position: absolute;
	top: 80px;
	left: 50%;
	transform: translateX(-50%);
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	background: var(--text-primary);
	color: var(--bg-base);
	padding: 8px 20px;
	border-radius: var(--radius-sm);
	white-space: nowrap;
	animation: toast-in 200ms ease;
	z-index: 10;
}

@keyframes toast-in {
	from {
		opacity: 0;
		transform: translateX(-50%) translateY(-6px);
	}
	to {
		opacity: 1;
		transform: translateX(-50%) translateY(0);
	}
}
</style>
