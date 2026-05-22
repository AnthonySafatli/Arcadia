<template>
	<div class="play-area">
		<div class="pile-zone">
			<!-- Empty state -->
			<div v-if="allCards.length === 0" class="pile-empty">
				<span class="pile-empty-text">play begins</span>
			</div>

			<!-- Stacked cards -->
			<div v-else class="pile-stack">
				<TransitionGroup name="card-in">
					<div
						v-for="(card, idx) in visiblePileCards"
						:key="card.value + card.type"
						class="pile-card"
						:class="[`pile-card--${card.type}`, `pile-card--depth-${Math.min(idx, 4)}`]"
						:style="{
							'--card-idx': idx,
							'--pile-rotation': cardRotation(idx),
						}">
						<span class="pile-card-number">{{ card.value }}</span>
					</div>
				</TransitionGroup>
			</div>

			<!-- Top card label -->
			<div v-if="topCard" class="pile-label">
				<span class="pile-label-text">last played</span>
				<span class="pile-label-value">
					{{ topCard.value }}
					<template v-if="recentDiscards.length > 0">
						<span class="pile-label--red"> · {{ recentDiscards.join(" · ") }}</span>
					</template>
				</span>
			</div>
		</div>

		<!-- Other players -->
		<div class="players-ring">
			<div
				v-for="player in otherPlayers"
				:key="player.player_id"
				class="player-node"
				:class="{
					'player-node--hovering': playerHovering[player.player_id],
				}">
				<div class="player-avatar">
					<span class="player-initial">{{ player.nickname }}</span>
					<div v-if="playerHovering[player.player_id]" class="player-hover-ring" />
				</div>
				<div class="player-cards-count">
					<div class="player-card-pips">
						<span
							v-for="c in Math.min(getPlayerHandCount(player.player_id), 8)"
							:key="c"
							class="player-card-pip" />
						<span
							v-if="getPlayerHandCount(player.player_id) > 8"
							class="player-card-overflow"
							>+{{ getPlayerHandCount(player.player_id) - 8 }}</span
						>
					</div>
				</div>
				<span class="player-name">{{ player.player_id }}</span>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed, watch, ref } from "vue";

import type { Player } from "@/dtos/PlayerDto";

import { usePlayerId } from "@/composables/usePlayerId";

const props = defineProps<{
	placed: number[];
	discarded: number[];
	playerHands: Record<string, number>;
	playerHovering: Record<string, boolean>;
	players: Player[];
}>();

const playerId = usePlayerId();

const allCards = computed(() => {
	const placed = props.placed.map((v) => ({ value: v, type: "placed" }));
	const discarded = props.discarded.map((v) => ({ value: v, type: "discarded" }));
	return [...placed, ...discarded].sort((a, b) => a.value - b.value);
});

const visiblePileCards = computed(() => {
	const cards = allCards.value;
	return cards.slice(-5).reverse();
});

const topCard = computed(() => visiblePileCards.value[0] ?? null);
const otherPlayers = computed(() => props.players.filter((x) => x.player_id !== playerId));

function getPlayerHandCount(id: string) {
	return props.playerHands[id] ?? 0;
}

function cardRotation(idx: number) {
	const rotations = [0, -2, 2, -3, 3];
	return `${rotations[idx] ?? (Math.random() > 0.5 ? 2 : -2)}deg`;
}

const recentDiscards = ref<number[]>([]);
let prevDiscarded: number[] = [];

watch(
	() => props.discarded,
	(newVal) => {
		const added = newVal.filter((v) => !prevDiscarded.includes(v));
		if (added.length > 0) recentDiscards.value = added;
		prevDiscarded = [...newVal];
	}
);

watch(
	() => props.placed,
	() => {
		recentDiscards.value = [];
	}
);
</script>

<style scoped>
.play-area {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	gap: 40px;
	padding: 20px 0;
	position: relative;
}

.pile-zone {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 12px;
	flex-shrink: 0;
}

.pile-empty {
	width: 110px;
	height: 154px;
	border: 2px dashed var(--bg-border);
	border-radius: var(--radius-md);
	display: flex;
	align-items: center;
	justify-content: center;
}

.pile-empty-text {
	font-family: var(--font-mono);
	font-size: 0.65rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.pile-stack {
	position: relative;
	width: 110px;
	height: 154px;
}

.pile-card {
	position: absolute;
	inset: 0;
	border-radius: var(--radius-md);
	display: flex;
	align-items: center;
	justify-content: center;
	transform: rotate(var(--pile-rotation));
	transition: transform 200ms ease;
}

.pile-card--placed {
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
}

.pile-card--discarded {
	background: rgba(255, 60, 60, 0.08);
	border: 1px solid rgba(255, 107, 107, 0.25);
}

.pile-card--depth-0 {
	z-index: 5;
}
.pile-card--depth-1 {
	z-index: 4;
	box-shadow: -2px 2px 0 var(--bg-border);
}
.pile-card--depth-2 {
	z-index: 3;
	box-shadow: -4px 4px 0 var(--bg-border);
}
.pile-card--depth-3 {
	z-index: 2;
	box-shadow: -6px 6px 0 var(--bg-border);
}
.pile-card--depth-4 {
	z-index: 1;
	box-shadow: -8px 8px 0 var(--bg-border);
}

.pile-card-number {
	font-family: var(--font-display);
	font-size: 2.8rem;
	line-height: 1;
	color: var(--text-primary);
}

.pile-card--discarded .pile-card-number {
	color: #ff6b6b;
}

.pile-label {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 2px;
}

.pile-label-text {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.pile-label-value {
	font-family: var(--font-mono);
	font-size: 0.85rem;
	color: var(--text-secondary);
}

.pile-label--red {
	color: #ff6b6b !important;
}

/* ── Players Ring ── */
.players-ring {
	display: flex;
	flex-wrap: wrap;
	gap: 16px;
	justify-content: center;
	align-items: flex-start;
	flex: 1;
}

.player-node {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8px;
	transition: transform 200ms ease;
}

.player-node--hovering {
	transform: translateY(-2px);
}

.player-avatar {
	position: relative;
	width: 44px;
	height: 44px;
	border-radius: 50%;
	background: var(--bg-raised);
	border: 1.5px solid var(--bg-border);
	display: flex;
	align-items: center;
	justify-content: center;
	transition: border-color 200ms ease;
}

.player-node--hovering .player-avatar {
	border-color: var(--green-dim);
}

.player-hover-ring {
	position: absolute;
	inset: -4px;
	border-radius: 50%;
	border: 1.5px solid var(--green-bright);
	opacity: 0.5;
	animation: ring-pulse 1.4s ease-in-out infinite;
}

@keyframes ring-pulse {
	0%,
	100% {
		transform: scale(1);
		opacity: 0.5;
	}
	50% {
		transform: scale(1.08);
		opacity: 0.25;
	}
}

.player-initial {
	font-family: var(--font-mono);
	font-size: 0.9rem;
	font-weight: 500;
	color: var(--text-secondary);
}

.player-cards-count {
	display: flex;
	align-items: center;
}

.player-card-pips {
	display: flex;
	gap: 3px;
	align-items: center;
	flex-wrap: wrap;
	justify-content: center;
	max-width: 64px;
}

.player-card-pip {
	width: 8px;
	height: 11px;
	border-radius: 2px;
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
	display: block;
	transition: all 200ms ease;
}

.player-node--hovering .player-card-pip {
	border-color: var(--green-dim);
	background: rgba(57, 255, 138, 0.06);
}

.player-card-overflow {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	color: var(--text-muted);
}

.player-name {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--text-muted);
	max-width: 64px;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}
</style>
