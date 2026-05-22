<template>
	<div class="wordle-wrap">
		<div class="grid-bg" aria-hidden="true">
			<div class="grid-bg-inner"></div>
		</div>

		<div class="wordle">
			<!-- HEADER -->
			<div class="wordle-header">
				<div class="header-left">
					<span class="round-label">round {{ state.round }}</span>
					<div class="tally-row">
						<span class="tally tally--1st" :title="'1st place'">
							<span class="tally-icon">🥇</span>
							<span class="tally-num">{{ state.scores[playerId]?.["1st"] }}</span>
						</span>
						<span class="tally tally--2nd" :title="'2nd place'">
							<span class="tally-icon">🥈</span>
							<span class="tally-num">{{ state.scores[playerId]?.["2nd"] }}</span>
						</span>
						<span class="tally tally--3rd" :title="'3rd place'">
							<span class="tally-icon">🥉</span>
							<span class="tally-num">{{ state.scores[playerId]?.["3rd"] }}</span>
						</span>
					</div>
				</div>
				<div class="header-right">
					<span class="wordle-status" :class="statusClass">{{ statusText }}</span>
				</div>
			</div>

			<!-- PLAYER SCORES -->
			<div class="scores-row">
				<div v-for="(score, pid) in state.scores" :key="pid">
					<div
						v-if="pid !== playerId"
						class="player-score"
						:class="{
							'player-score--me': pid === playerId,
							'player-score--done': isPlayerDone(pid),
						}">
						<span class="player-name">{{ playerName(pid) }}</span>
						<div class="tally-row">
							<span class="tally tally--1st" :title="'1st place'">
								<span class="tally-icon">🥇</span>
								<span class="tally-num">{{ score["1st"] }}</span>
							</span>
							<span class="tally tally--2nd" :title="'2nd place'">
								<span class="tally-icon">🥈</span>
								<span class="tally-num">{{ score["2nd"] }}</span>
							</span>
							<span class="tally tally--3rd" :title="'3rd place'">
								<span class="tally-icon">🥉</span>
								<span class="tally-num">{{ score["3rd"] }}</span>
							</span>
						</div>
						<!-- opponent tile preview -->
						<div v-if="pid !== playerId" class="mini-grid">
							<div v-for="(row, ri) in opponentTiles(pid)" :key="ri" class="mini-row">
								<div
									v-for="(tile, ti) in row"
									:key="ti"
									class="mini-tile"
									:class="tile"></div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- GUESS BOARD -->
			<div class="board">
				<div
					v-for="rowIndex in 6"
					:key="rowIndex"
					class="board-row"
					:class="{
						'board-row--active':
							rowIndex - 1 === state.guesses.length && !state.finished,
						'board-row--shake': shakeRow === rowIndex - 1,
					}">
					<div
						v-for="colIndex in 5"
						:key="colIndex"
						class="tile"
						:class="tileClass(rowIndex - 1, colIndex - 1)">
						<span class="tile-letter">{{
							tileLetter(rowIndex - 1, colIndex - 1)
						}}</span>
					</div>
				</div>
			</div>

			<!-- ROUND OVER REVEAL -->
			<div v-if="state.round_over" class="round-over-banner">
				<span class="reveal-label">the word was</span>
				<span class="reveal-word">{{ state.secret_word }}</span>
			</div>

			<!-- ERROR -->
			<div v-if="errorMsg" class="error-toast">{{ errorMsg }}</div>

			<!-- HOST CONTROLS -->
			<div v-if="isHost" class="host-controls">
				<button v-if="!state.round_over && allFinished" class="btn-ctrl" @click="endRound">
					end round
				</button>
				<button
					v-if="state.round_over"
					class="btn-ctrl btn-ctrl--primary"
					@click="nextRound">
					next round
				</button>
				<button class="btn-ctrl btn-ctrl--ghost" @click="resetGame">
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
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from "vue";

import type { WordleState, TileResult } from "./WordleState";
import { defaultWordleState } from "./WordleState";

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

const isHost = computed(() => room.value?.host_player_id === playerId);

const allPlayers = computed(() => room.value?.players ?? []);

const allFinished = computed(() => {
	const me = state.value.finished;
	const others = Object.values(state.value.other_players).every((p) => p.finished);
	return me && others;
});

function playerName(pid: string) {
	if (pid === playerId) return "you";
	return allPlayers.value.find((p) => p.player_id === pid)?.nickname ?? "???";
}

function isPlayerDone(pid: string) {
	if (pid === playerId) return state.value.finished;
	return state.value.other_players[pid]?.finished ?? false;
}

function opponentTiles(pid: string): (TileResult | "empty" | "filled")[][] {
	const op = state.value.other_players[pid];
	if (!op) return [];
	const rows: (TileResult | "empty" | "filled")[][] = [];
	for (let r = 0; r < 6; r++) {
		const row = op.tile_pattern[r];
		if (row !== undefined) {
			rows.push(row);
		} else if (r < op.guesses_used) {
			rows.push(Array(5).fill("absent"));
		} else {
			rows.push(Array(5).fill("empty"));
		}
	}
	return rows;
}

const statusText = computed(() => {
	if (state.value.round_over) return "round over";
	if (state.value.finished) {
		return state.value.finished_info?.solved ? "solved!" : "out of guesses";
	}
	return `${state.value.guesses_remaining} left`;
});

const statusClass = computed(() => ({
	"status--win": state.value.finished_info?.solved && !state.value.round_over,
	"status--lose": state.value.finished && !state.value.finished_info?.solved,
	"status--over": state.value.round_over,
}));

function tileLetter(row: number, col: number): string {
	if (row < state.value.guesses.length) {
		return state.value.guesses[row]?.word[col] ?? "";
	}
	if (row === state.value.guesses.length && !state.value.finished) {
		return currentInput.value[col] ?? "";
	}
	return "";
}

function tileClass(row: number, col: number): string[] {
	const classes: string[] = [];
	if (row < state.value.guesses.length) {
		const g = state.value.guesses[row];
		classes.push("tile--revealed", `tile--${g?.result[col]}`);
		// stagger reveal animation
		classes.push(`tile--delay-${col}`);
	} else if (row === state.value.guesses.length && !state.value.finished) {
		if (currentInput.value[col]) classes.push("tile--filled");
		else classes.push("tile--empty");
	} else {
		classes.push("tile--empty");
	}
	return classes;
}

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

/* ── Header ── */
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

/* ── Scores row ── */
.scores-row {
	display: flex;
	gap: 8px;
	width: 100%;
	flex-wrap: wrap;
	justify-content: center;
}

.player-score {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 6px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	padding: 10px 12px;
	flex: 1;
	min-width: 72px;
	max-width: 120px;
	transition: border-color 200ms ease;
}

.player-score--me {
	border-color: var(--green-dim);
	box-shadow: 0 0 10px rgba(57, 255, 138, 0.12);
}

.player-score--done {
	opacity: 0.7;
}

.player-name {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.2em;
	text-transform: uppercase;
	color: var(--text-secondary);
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	max-width: 90px;
}

.player-score--me .player-name {
	color: var(--green-bright);
}

.tally-row {
	display: flex;
	gap: 6px;
	align-items: center;
}

.tally {
	display: flex;
	align-items: center;
	gap: 2px;
}

.tally-icon {
	font-size: 0.7rem;
	line-height: 1;
}

.tally-num {
	font-family: var(--font-display);
	font-size: 1.1rem;
	line-height: 1;
	color: var(--text-secondary);
}

/* ── Mini opponent grid ── */
.mini-grid {
	display: flex;
	flex-direction: column;
	gap: 2px;
	margin-top: 2px;
}

.mini-row {
	display: flex;
	gap: 2px;
}

.mini-tile {
	width: 8px;
	height: 8px;
	border-radius: 1px;
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
}

.mini-tile.correct {
	background: var(--green-bright);
	border-color: var(--green-bright);
}
.mini-tile.present {
	background: #f5c518;
	border-color: #f5c518;
}
.mini-tile.absent {
	background: var(--bg-raised);
	border-color: var(--text-muted);
}
.mini-tile.empty {
	background: transparent;
}

/* ── Board ── */
.board {
	display: flex;
	flex-direction: column;
	gap: 6px;
	width: 100%;
	max-width: 330px;
}

.board-row {
	display: flex;
	gap: 6px;
	justify-content: center;
}

.board-row--shake {
	animation: shake 0.45s cubic-bezier(0.36, 0.07, 0.19, 0.97);
}

@keyframes shake {
	0%,
	100% {
		transform: translateX(0);
	}
	15% {
		transform: translateX(-6px);
	}
	35% {
		transform: translateX(6px);
	}
	55% {
		transform: translateX(-4px);
	}
	75% {
		transform: translateX(4px);
	}
}

/* ── Tile ── */
.tile {
	width: 58px;
	height: 58px;
	display: flex;
	align-items: center;
	justify-content: center;
	border: 2px solid var(--bg-border);
	border-radius: var(--radius-sm);
	background: var(--bg-card);
	position: relative;
	transition: border-color 80ms ease;
}

.tile--filled {
	border-color: var(--text-secondary);
	animation: pop 80ms ease;
}

@keyframes pop {
	0% {
		transform: scale(1);
	}
	50% {
		transform: scale(1.08);
	}
	100% {
		transform: scale(1);
	}
}

.tile-letter {
	font-family: var(--font-display);
	font-size: 2rem;
	line-height: 1;
	color: var(--text-primary);
	letter-spacing: 0.05em;
}

/* Revealed tiles — flip in */
.tile--revealed {
	animation: flip-in 300ms ease forwards;
	border-color: transparent;
}

.tile--delay-0 {
	animation-delay: 0ms;
}
.tile--delay-1 {
	animation-delay: 80ms;
}
.tile--delay-2 {
	animation-delay: 160ms;
}
.tile--delay-3 {
	animation-delay: 240ms;
}
.tile--delay-4 {
	animation-delay: 320ms;
}

@keyframes flip-in {
	0% {
		transform: rotateX(0deg);
	}
	50% {
		transform: rotateX(-90deg);
	}
	100% {
		transform: rotateX(0deg);
	}
}

.tile--correct {
	background: var(--green-dim);
	border-color: var(--green-bright);
	box-shadow: 0 0 8px rgba(57, 255, 138, 0.25);
}

.tile--correct .tile-letter {
	color: var(--green-bright);
}

.tile--present {
	background: #3d2f00;
	border-color: #f5c518;
	box-shadow: 0 0 8px rgba(245, 197, 24, 0.2);
}

.tile--present .tile-letter {
	color: #f5c518;
}

.tile--absent {
	background: var(--bg-raised);
	border-color: var(--text-muted);
	opacity: 0.6;
}

.tile--absent .tile-letter {
	color: var(--text-muted);
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

/* ── Host controls ── */
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
