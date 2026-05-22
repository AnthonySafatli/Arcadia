<template>
	<div class="ttt-wrap">
		<div class="grid-bg" aria-hidden="true">
			<div class="grid-bg-inner"></div>
		</div>

		<div class="ttt">
			<div class="ttt-header">
				<div
					class="score-block"
					:class="[
						{
							'score-block--active': state.current_turn === playerId && !state.winner,
						},
						markForClass(playerId),
					]">
					<span class="score-you">you</span>
					<div class="score-main">
						<span class="score-mark">{{ markFor(playerId) }}</span>
						<span class="score-value">{{ state.scores[playerId] }}</span>
					</div>
				</div>

				<div class="ttt-title-block">
					<span class="ttt-title">tic tac toe</span>
					<span class="ttt-status" :class="statusClass">{{ statusText }}</span>
				</div>

				<div
					class="score-block"
					:class="[
						{ 'score-block--active': isOpponentTurn && !state.winner },
						markForClass(opponent?.player_id!),
					]">
					<span class="score-you">&nbsp;</span>
					<div class="score-main">
						<span class="score-value">{{
							state.scores[opponent?.player_id ?? ""]
						}}</span>
						<span class="score-mark">{{ markFor(opponent?.player_id!) }}</span>
					</div>
				</div>
			</div>

			<div class="board" :class="{ 'board--disabled': !!state.winner || isOpponentTurn }">
				<button
					v-for="(cell, i) in state.board"
					:key="i"
					class="cell"
					:class="{
						'cell--x': markFor(cell) === 'X',
						'cell--o': markFor(cell) === 'O',
						'cell--win': false,
						'cell--empty': !cell,
					}"
					:disabled="!!cell || !!state.winner || isOpponentTurn"
					@click="playerMove(i)"
					:aria-label="`cell ${i + 1}${cell ? ', ' + (markFor(cell) === 'X' ? 'your mark' : 'cpu mark') : ', empty'}`">
					<svg v-if="markFor(cell) === 'X'" class="mark mark-x" viewBox="0 0 40 40">
						<line x1="8" y1="8" x2="32" y2="32" />
						<line x1="32" y1="8" x2="8" y2="32" />
					</svg>
					<svg v-else-if="markFor(cell) === 'O'" class="mark mark-o" viewBox="0 0 40 40">
						<circle cx="20" cy="20" r="11" />
					</svg>
				</button>
			</div>

			<div class="ttt-footer">
				<button
					class="ttt-reset"
					v-if="room?.host_player_id === playerId"
					@click="resetGame">
					<svg
						width="14"
						height="14"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true">
						<polyline points="23 4 23 10 17 10"></polyline>
						<path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"></path>
					</svg>
					new game
				</button>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
// TODO: Full screen win screen

import { computed } from "vue";

import type { TicTacToeState } from "./TicTacToeState";
import { defaultTicTacToeState } from "./TicTacToeState";

import { usePlayerId } from "@/composables/usePlayerId";
import { useGameRoom } from "@/composables/useGameRoom";
import { useSocket } from "@/composables/useSocket";

const playerId = usePlayerId();

const { sendAction } = useSocket();
const { room, state: socketState } = useGameRoom();
const state = computed(() => (socketState.value as TicTacToeState) ?? defaultTicTacToeState());
const opponent = computed(() => room.value?.players.find((x) => x.player_id != playerId));

const youWin = computed(() => state.value.winner === playerId);
const opponentWin = computed(() => state.value.winner === opponent.value?.player_id);
const isDraw = computed(() => state.value.winner === "draw");
const isOpponentTurn = computed(() => state.value.current_turn !== playerId);

const statusText = computed(() => {
	if (youWin.value) return "you win!";
	if (opponentWin.value) return `${opponent.value?.nickname} wins`;
	if (isDraw.value) return "draw";
	if (isOpponentTurn.value) return `${opponent.value?.nickname} thinking...`;
	return "your turn";
});

const statusClass = computed(() => ({
	"status--win": youWin.value,
	"status--lose": opponentWin.value,
	"status--draw": isDraw.value,
	"status--thinking": isOpponentTurn.value,
}));

function markFor(cell: string | null) {
	return cell ? state.value.marks[cell] : null;
}

function markForClass(cell: string | null) {
	return markFor(cell)?.toLowerCase();
}

function playerMove(i: number) {
	if (state.value.board[i] || state.value.winner || isOpponentTurn.value) return;
	sendAction(room.value?.code!, playerId, { type: "cell", cell: i });
}

function resetGame() {
	sendAction(room.value?.code!, playerId, { type: "reset" });
}
</script>

<style scoped>
.ttt-wrap {
	position: relative;
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 40px 24px;
	width: 100%;
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

.ttt {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 32px;
	width: 100%;
	max-width: 420px;
}

.ttt-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	width: 100%;
}

.ttt-title-block {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 6px;
}

.ttt-title {
	font-family: var(--font-display);
	font-size: 1.5rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--text-secondary);
}

.ttt-status {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--text-muted);
	transition: color 200ms ease;
	min-height: 1em;
}

.status--win {
	color: var(--green-bright);
}
.status--lose {
	color: #ff6b6b;
}
.status--draw {
	color: var(--text-secondary);
}
.status--thinking {
	animation: blink 1s ease-in-out infinite;
}

@keyframes blink {
	0%,
	100% {
		opacity: 1;
	}
	50% {
		opacity: 0.35;
	}
}

.board {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 3px;
	background: var(--bg-border);
	border-radius: var(--radius-md);
	overflow: hidden;
	border: 1px solid var(--bg-border);
	width: 100%;
	max-width: 360px;
	aspect-ratio: 1;
}

.cell {
	background: var(--bg-card);
	border: none;
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: background 150ms ease;
	padding: 0;
}

.cell--empty:not(:disabled):hover {
	background: var(--bg-raised);
}

.cell:disabled {
	cursor: default;
}

.cell--win.cell--x {
	background: rgba(57, 255, 138, 0.06);
}
.cell--win.cell--o {
	background: rgba(255, 107, 107, 0.06);
}

.mark {
	width: 42%;
	height: 42%;
	overflow: visible;
}

.mark-x line {
	stroke: var(--green-bright);
	stroke-width: 3.5;
	stroke-linecap: round;
	stroke-dasharray: 34;
	stroke-dashoffset: 34;
	animation: draw 180ms ease forwards;
}

.mark-x line:nth-child(2) {
	animation-delay: 60ms;
}

.mark-o circle {
	fill: none;
	stroke: #ff6b6b;
	stroke-width: 3.5;
	stroke-linecap: round;
	stroke-dasharray: 70;
	stroke-dashoffset: 70;
	animation: draw 220ms ease forwards;
}

@keyframes draw {
	to {
		stroke-dashoffset: 0;
	}
}

.cell--win .mark-x line {
	filter: drop-shadow(0 0 4px rgba(57, 255, 138, 0.7));
}
.cell--win .mark-o circle {
	filter: drop-shadow(0 0 4px rgba(255, 107, 107, 0.7));
}

.ttt-footer {
	width: 100%;
	display: flex;
	justify-content: center;
}

.ttt-reset {
	display: inline-flex;
	align-items: center;
	gap: 8px;
	font-family: var(--font-mono);
	font-size: 0.75rem;
	font-weight: 500;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	padding: 10px 24px;
	background: transparent;
	color: var(--text-muted);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	cursor: pointer;
	transition: all 200ms ease;
}

.ttt-reset:hover {
	border-color: var(--green-dim);
	color: var(--green-bright);
}

.score-main {
	display: flex;
	align-items: center;
	gap: 8px;
}

.score-mark {
	font-family: var(--font-display);
	font-size: 1.4rem;
	line-height: 1;
	opacity: 0.4;
	transition: opacity 200ms ease;
}

.x .score-mark {
	color: var(--green-bright);
}

.o .score-mark {
	color: #ff6b6b;
}

.score-block--active .score-mark {
	opacity: 1;
}

.x.score-block.score-block--active {
	border-color: var(--green-dim);
	box-shadow: 0 0 12px rgba(57, 255, 138, 0.2);
}

.o.score-block.score-block--active {
	border-color: rgba(255, 107, 107, 0.5);
	box-shadow: 0 0 12px rgba(255, 107, 107, 0.2);
}

.score-block {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 4px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	padding: 12px 24px;
	min-width: 72px;
	transition:
		border-color 200ms ease,
		box-shadow 200ms ease;
}

.score-value {
	font-family: var(--font-display);
	font-size: 2rem;
	line-height: 1;
	color: var(--text-secondary);
	text-shadow: 0 0 12px rgba(57, 255, 138, 0.35);
}

.score-you {
	font-family: var(--font-mono);
	font-size: 0.55rem;
	letter-spacing: 0.3em;
	text-transform: uppercase;
	padding: 2px 8px;
	opacity: 0.7;
	transition: opacity 200ms ease;
}

.x .score-you {
	color: var(--green-bright);
}

.o .score-you {
	color: #ff6b6b;
}

.score-block--active .score-you {
	opacity: 1;
}
</style>
