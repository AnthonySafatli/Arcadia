<template>
	<div class="btn-group">
		<button v-if="props.hostPlayerId == playerId" class="action-btn" @click="$emit('reset')">
			reset game
		</button>
		<button class="action-btn" @click="$emit('focus')">reset focus</button>
		<button class="action-btn" @click="$emit('throwingStar')">
			{{ playerThrowingStar ? "cancel" : "suggest" }} throwing star
		</button>
	</div>

	<Transition name="star-fade">
		<div v-if="throwingStarsCount > 0" class="throwing-star-banner">
			<StarIcon :active="true" :size="14" class="star-icon" />
			<span class="star-text">throwing star</span>
			<span class="star-count">{{ throwingStarsCount }} / {{ props.playerCount }}</span>
		</div>
	</Transition>
</template>

<script setup lang="ts">
import { computed } from "vue";

import { usePlayerId } from "@/composables/usePlayerId";

const playerId = usePlayerId();

const props = defineProps<{
	hostPlayerId: string;
	playerCount: number;
	playerThrowingStars: Record<string, boolean> | undefined;
}>();

const emit = defineEmits<{
	(e: "focus"): void;
	(e: "reset"): void;
	(e: "throwingStar"): void;
}>();

const playerThrowingStar = computed(() => props.playerThrowingStars?.[playerId]);
const throwingStarsCount = computed(
	() => Object.values(props.playerThrowingStars ?? {}).filter((v) => v).length
);
</script>

<style scoped>
.btn-group {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 12px;
	margin-top: 20px;
}

.action-btn {
	font-family: var(--font-mono);
	font-size: 0.75rem;
	font-weight: 500;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	padding: 10px 24px;
	background: transparent;
	color: var(--green-bright);
	border: 1px solid var(--green-dim);
	border-radius: var(--radius-md);
	cursor: pointer;
	transition: all 200ms ease;
}

.action-btn:hover {
	background: rgba(57, 255, 138, 0.06);
	box-shadow: 0 0 20px rgba(57, 255, 138, 0.12);
}

.btn-primary {
	margin-top: 10px;
}

.throwing-star-banner {
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 10px;
	margin-top: 12px;
	padding: 10px 24px;
	border: 1px solid var(--green-dim);
	border-radius: var(--radius-md);
	background: rgba(57, 255, 138, 0.04);
	font-family: var(--font-mono);
	font-size: 0.78rem;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--green-bright);
	animation: star-pulse 1.4s ease-in-out infinite;
}

.star-icon {
	animation: star-spin 2s linear infinite;
	display: inline-block;
	font-size: 0.9rem;
}

.star-count {
	color: var(--green-bright);
	font-weight: 500;
}

.star-text {
	color: var(--text-secondary);
}

@keyframes star-pulse {
	0%,
	100% {
		box-shadow: 0 0 8px rgba(57, 255, 138, 0.1);
		border-color: var(--green-dim);
	}
	50% {
		box-shadow: 0 0 20px rgba(57, 255, 138, 0.25);
		border-color: var(--green-mid);
	}
}

@keyframes star-spin {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}

.star-fade-enter-active,
.star-fade-leave-active {
	transition:
		opacity 300ms ease,
		transform 300ms ease;
}
.star-fade-enter-from,
.star-fade-leave-to {
	opacity: 0;
	transform: translateY(6px);
}
</style>
