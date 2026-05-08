<template>
	<div class="hand-zone">
		<div class="hand-label">
			<span>your hand</span>
			<span class="hand-count">{{ hand.length }} card{{ hand.length !== 1 ? "s" : "" }}</span>
		</div>
		<div class="hand-cards" :style="{ '--card-count': hand.length }">
			<div
				v-for="(card, idx) in sortedHand"
				:key="card"
				class="hand-card"
				:class="{ 'hand-card--lowest': idx === 0 }"
				:style="{ '--hand-idx': idx }"
				@mouseenter="hoveredCard = card"
				@mouseleave="hoveredCard = null">
				<div class="hand-card-inner">
					<span class="hand-card-number">{{ card }}</span>
				</div>
				<div v-if="idx === 0" class="hand-card-glow" />
			</div>
			<div v-if="hand.length === 0" class="hand-empty">no cards</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";

const props = defineProps<{
	hand: number[];
}>();

const { hand } = props;

const hoveredCard = ref<null | number>(null);

const sortedHand = computed(() => [...hand].sort((a, b) => a - b));
</script>

<style scoped>
.hand-zone {
	margin-top: 12px;
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.hand-label {
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-family: var(--font-mono);
	font-size: 0.65rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--text-muted);
	padding: 0 4px;
}

.hand-count {
	color: var(--text-muted);
}

.hand-cards {
	display: flex;
	align-items: flex-end;
	justify-content: center;
	gap: 10px;
	padding: 8px 4px 4px;
	min-height: 110px;
}

.hand-card {
	position: relative;
	cursor: default;
	transition: transform 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.hand-card--lowest {
	transform: translateY(-6px);
}

.hand-card:hover {
	transform: translateY(-14px) !important;
	z-index: 10;
}

.hand-card-inner {
	width: 68px;
	height: 96px;
	border-radius: var(--radius-md);
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
	display: flex;
	align-items: center;
	justify-content: center;
	transition: border-color 200ms ease;
}

.hand-card--lowest .hand-card-inner {
	border-color: rgba(57, 255, 138, 0.3);
	background: rgba(57, 255, 138, 0.04);
}

.hand-card:hover .hand-card-inner {
	border-color: rgba(57, 255, 138, 0.5);
}

.hand-card-number {
	font-family: var(--font-display);
	font-size: 2.2rem;
	line-height: 1;
	color: var(--text-primary);
	transition: color 200ms ease;
}

.hand-card--lowest .hand-card-number {
	color: var(--green-bright);
}

.hand-card-glow {
	position: absolute;
	inset: 0;
	border-radius: var(--radius-md);
	box-shadow:
		0 0 20px rgba(57, 255, 138, 0.15),
		0 0 40px rgba(57, 255, 138, 0.06);
	pointer-events: none;
}

.hand-empty {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--text-muted);
	align-self: center;
}

/* ── Transitions ── */
.card-in-enter-active {
	transition: all 280ms cubic-bezier(0.4, 0, 0.2, 1);
}
.card-in-enter-from {
	opacity: 0;
	transform: translateY(-20px) rotate(var(--pile-rotation));
}
</style>
