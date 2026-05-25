<template>
	<div class="board" @click="hiddenInput?.focus()">
		<input
			ref="hiddenInput"
			class="hidden-input"
			autocomplete="off"
			autocorrect="off"
			autocapitalize="off"
			spellcheck="false"
			@keydown="handleKey" />
		<div
			v-for="rowIndex in 6"
			:key="rowIndex"
			class="board-row"
			:class="{
				'board-row--active': rowIndex - 1 === guesses.length && !finished,
				'board-row--shake': shakeRow === rowIndex - 1,
			}">
			<div
				v-for="colIndex in 5"
				:key="colIndex"
				class="tile"
				:class="tileClass(rowIndex - 1, colIndex - 1)">
				<span class="tile-letter">{{ tileLetter(rowIndex - 1, colIndex - 1) }}</span>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import type { Guess } from "./WordleState";

const props = defineProps<{
	guesses: Guess[];
	finished: boolean;
	currentInput: string;
	shakeRow: number | null;
}>();

const emit = defineEmits<{
	(e: "key", key: string): void;
}>();

const hiddenInput = ref<HTMLInputElement | null>(null);

onMounted(() => hiddenInput.value?.focus());

function handleKey(e: KeyboardEvent) {
	e.preventDefault();
	if (e.key === "Enter" || e.key === "Backspace") {
		emit("key", e.key);
	} else if (/^[a-zA-Z]$/.test(e.key)) {
		emit("key", e.key.toUpperCase());
	}
}

function tileLetter(row: number, col: number): string {
	if (row < props.guesses.length) {
		return props.guesses[row]?.word[col] ?? "";
	}
	if (row === props.guesses.length && !props.finished) {
		return props.currentInput[col] ?? "";
	}
	return "";
}

function tileClass(row: number, col: number): string[] {
	const classes: string[] = [];
	if (row < props.guesses.length) {
		const g = props.guesses[row];
		classes.push("tile--revealed", `tile--${g?.result[col]}`);
		classes.push(`tile--delay-${col}`);
	} else if (row === props.guesses.length && !props.finished) {
		if (props.currentInput[col]) classes.push("tile--filled");
		else classes.push("tile--empty");
	} else {
		classes.push("tile--empty");
	}
	return classes;
}
</script>

<style scoped>
.hidden-input {
	position: absolute;
	opacity: 0;
	width: 1px;
	height: 1px;
	pointer-events: none;
}

/* rest of styles unchanged */
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
</style>
