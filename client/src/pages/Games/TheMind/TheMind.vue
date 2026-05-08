<template>
	<div class="mind-wrap">
		<div class="grid-bg" aria-hidden="true"><div class="grid-bg-inner"></div></div>

		<div class="mind">
			<!-- Top HUD -->
			<div class="hud">
				<div class="hud-block">
					<span class="hud-label">level</span>
					<span class="hud-value hud-level">{{ state.level }}</span>
				</div>

				<div class="hud-center">
					<div class="hud-pips-group">
						<span class="hud-label">lives</span>
						<div class="hud-pips">
							<span
								v-for="i in 5"
								:key="i"
								class="pip pip-life"
								:class="{ 'pip--active': i <= state.lives }" />
						</div>
					</div>
					<div class="hud-divider" />
					<div class="hud-pips-group">
						<span class="hud-label">stars</span>
						<div class="hud-pips">
							<span
								v-for="i in 3"
								:key="i"
								class="pip pip-star"
								:class="{ 'pip--active': i <= state.throwing_stars }">
								<svg
									v-if="i <= state.throwing_stars"
									viewBox="0 0 16 16"
									width="10"
									height="10">
									<polygon
										points="8,1 10,6 15,6 11,9.5 12.5,15 8,12 3.5,15 5,9.5 1,6 6,6"
										fill="currentColor" />
								</svg>
								<svg v-else viewBox="0 0 16 16" width="10" height="10">
									<polygon
										points="8,1 10,6 15,6 11,9.5 12.5,15 8,12 3.5,15 5,9.5 1,6 6,6"
										fill="none"
										stroke="currentColor"
										stroke-width="1.2" />
								</svg>
							</span>
						</div>
					</div>
				</div>

				<div class="hud-block hud-block--right">
					<span class="hud-label">players</span>
					<span class="hud-value">{{ Object.keys(state.player_hands).length }}</span>
				</div>
			</div>

			<!-- Play Area -->
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
								:class="[
									`pile-card--${card.type}`,
									`pile-card--depth-${Math.min(idx, 4)}`,
								]"
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
						<span
							class="pile-label-text"
							:class="topCard.type === 'discarded' ? 'pile-label--red' : ''">
							{{ topCard.type === "discarded" ? "last: mistake" : "last played" }}
						</span>
						<span
							class="pile-label-value"
							:class="topCard.type === 'discarded' ? 'pile-label--red' : ''">
							{{ topCard.value }}
						</span>
					</div>
				</div>

				<!-- Other players -->
				<div class="players-ring">
					<div
						v-for="[id, count] in otherPlayers"
						:key="id"
						class="player-node"
						:class="{
							'player-node--hovering': state.player_hovering[id],
						}">
						<div class="player-avatar">
							<span class="player-initial">{{ id.charAt(0).toUpperCase() }}</span>
							<div v-if="state.player_hovering[id]" class="player-hover-ring" />
						</div>
						<div class="player-cards-count">
							<div class="player-card-pips">
								<span
									v-for="c in Math.min(count, 8)"
									:key="c"
									class="player-card-pip" />
								<span v-if="count > 8" class="player-card-overflow"
									>+{{ count - 8 }}</span
								>
							</div>
						</div>
						<span class="player-name">{{ id }}</span>
					</div>
				</div>
			</div>

			<!-- Your Hand -->
			<div class="hand-zone">
				<div class="hand-label">
					<span>your hand</span>
					<span class="hand-count"
						>{{ state.hand.length }} card{{ state.hand.length !== 1 ? "s" : "" }}</span
					>
				</div>
				<div class="hand-cards" :style="{ '--card-count': state.hand.length }">
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
					<div v-if="state.hand.length === 0" class="hand-empty">no cards</div>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import { ref, computed } from "vue";

// Temporary local state instead of props
const state = {
	hand: [3, 17, 42, 68, 91],
	placed: [1, 5, 8, 12, 20, 25, 33],
	discarded: [15, 37],
	level: 3,
	lives: 3,
	throwing_stars: 1,
	player_hands: { alice: 3, bob: 2, carol: 4 },
	player_hovering: { alice: true, bob: false, carol: false },
	player_throwing_star: { alice: false, bob: false, carol: false },
	player_focus: { alice: false, bob: false, carol: false },
};

const hoveredCard = ref(null);

const sortedHand = computed(() => [...state.hand].sort((a, b) => a - b));

const allCards = computed(() => {
	const placed = state.placed.map((v) => ({ value: v, type: "placed" }));
	const discarded = state.discarded.map((v) => ({ value: v, type: "discarded" }));
	return [...placed, ...discarded].sort((a, b) => a.value - b.value);
});

const visiblePileCards = computed(() => {
	const cards = allCards.value;
	return cards.slice(-5).reverse();
});

const topCard = computed(() => visiblePileCards.value[0] ?? null);

const otherPlayers = computed(() => Object.entries(state.player_hands));

function cardRotation(idx) {
	const rotations = [0, -2, 2, -3, 3];
	return `${rotations[idx] ?? (Math.random() > 0.5 ? 2 : -2)}deg`;
}
</script>

<style scoped>
.mind-wrap {
	position: relative;
	width: 100%;
	height: 100%;
	min-height: 600px;
	display: flex;
	align-items: stretch;
	justify-content: center;
}

.grid-bg {
	position: absolute;
	inset: 0;
	background-image:
		linear-gradient(var(--bg-border) 1px, transparent 1px),
		linear-gradient(90deg, var(--bg-border) 1px, transparent 1px);
	background-size: 48px 48px;
	opacity: 0.35;
	pointer-events: none;
}

.grid-bg-inner {
	position: absolute;
	inset: 0;
	background: radial-gradient(ellipse 80% 80% at 50% 40%, transparent 20%, var(--bg-base) 100%);
}

.mind {
	position: relative;
	z-index: 1;
	width: 100%;
	max-width: 680px;
	display: flex;
	flex-direction: column;
	gap: 0;
	padding: 20px 24px 28px;
}

/* ── HUD ── */
.hud {
	display: flex;
	align-items: center;
	justify-content: space-between;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	padding: 12px 20px;
	gap: 16px;
	margin-bottom: 20px;
}

.hud-block {
	display: flex;
	flex-direction: column;
	align-items: flex-start;
	gap: 3px;
	min-width: 48px;
}

.hud-block--right {
	align-items: flex-end;
}

.hud-label {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.14em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.hud-value {
	font-family: var(--font-display);
	font-size: 1.6rem;
	line-height: 1;
	color: var(--text-primary);
}

.hud-level {
	color: var(--green-bright);
	text-shadow: 0 0 10px rgba(57, 255, 138, 0.3);
}

.hud-center {
	display: flex;
	align-items: center;
	gap: 20px;
	flex: 1;
	justify-content: center;
}

.hud-divider {
	width: 1px;
	height: 28px;
	background: var(--bg-border);
}

.hud-pips-group {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 6px;
}

.hud-pips {
	display: flex;
	align-items: center;
	gap: 6px;
}

.pip {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 14px;
	height: 14px;
	border-radius: 50%;
	transition: all 200ms ease;
}

.pip-life {
	border: 1.5px solid var(--bg-border);
	background: var(--bg-base);
}

.pip-life.pip--active {
	background: #ff6b6b;
	border-color: #ff6b6b;
	box-shadow: 0 0 6px rgba(255, 107, 107, 0.4);
}

.pip-star {
	color: var(--text-muted);
	border: none;
	background: none;
}

.pip-star.pip--active {
	color: #f5c842;
	filter: drop-shadow(0 0 4px rgba(245, 200, 66, 0.5));
}

/* ── Play Area ── */
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

/* ── Hand ── */
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
