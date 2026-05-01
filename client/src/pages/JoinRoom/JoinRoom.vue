<template>
	<Page back-btn>
		<div class="content">
			<div class="page-header">
				<span class="label">join a game</span>
				<h2 class="title">Enter room code</h2>
			</div>

			<div class="code-input-block card" @click="inputRef?.focus()">
				<div class="code-display">
					<span
						v-for="(char, i) in paddedCode"
						:key="i"
						class="code-char"
						:class="{
							filled: char !== '·',
							cursor: i === code.length && code.length < 6,
						}">
						{{ char }}
					</span>
				</div>

				<!-- Hidden actual input -->
				<input
					ref="inputRef"
					v-model="code"
					maxlength="6"
					class="hidden-input"
					@keydown.enter="join"
					@blur="inputRef?.focus()"
					autofocus />
			</div>

			<button class="btn btn-primary join-btn" :disabled="code.length < 6" @click="join">
				Join Room
			</button>
		</div>
	</Page>
</template>

<script setup>
import Page from "@/components/Page.vue";

import { ref, computed } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();
const inputRef = ref(null);
const code = ref("");

const paddedCode = computed(() => {
	const chars = code.value.toUpperCase().split("");
	while (chars.length < 6) chars.push("·");
	return chars;
});

function join() {
	if (code.value.length < 6) return;
	router.push(`/room/${code.value.toUpperCase()}`);
}
</script>

<style scoped>
.content {
	position: relative;
	z-index: 1;
	width: 100%;
	max-width: 400px;
	display: flex;
	flex-direction: column;
	gap: 24px;
}

.page-header {
	animation: fadeUp 0.5s ease both;
}

.label {
	font-family: var(--font-mono);
	font-size: 0.75rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--green-mid);
}

.title {
	font-family: var(--font-display);
	font-size: clamp(36px, 6vw, 56px);
	letter-spacing: 0.05em;
	color: var(--text-primary);
	line-height: 1.1;
	margin-top: 4px;
}

.code-input-block {
	animation: fadeUp 0.5s 0.1s ease both;
	position: relative;
	cursor: text;
}

.code-display {
	display: flex;
	gap: 10px;
	justify-content: center;
}

.code-char {
	font-family: var(--font-mono);
	font-size: 2rem;
	font-weight: 500;
	width: 44px;
	height: 56px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: var(--bg-base);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-sm);
	color: var(--text-muted);
	transition: var(--transition);
	letter-spacing: 0;
}

.code-char.filled {
	color: var(--green-bright);
	border-color: var(--green-dim);
	text-shadow: 0 0 12px var(--green-glow);
}

.code-char.cursor {
	border-color: var(--green-bright);
}

.hidden-input {
	position: absolute;
	opacity: 0;
	width: 1px;
	height: 1px;
	pointer-events: none;
}

.hint {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	color: var(--text-muted);
	text-align: center;
	letter-spacing: 0.1em;
	text-transform: uppercase;
}

.join-btn {
	width: 100%;
	padding: 16px;
	font-size: 0.9rem;
	animation: fadeUp 0.5s 0.2s ease both;
}

.join-btn:disabled {
	opacity: 0.35;
	cursor: not-allowed;
	box-shadow: none;
	transform: none;
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
