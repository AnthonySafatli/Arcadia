<template>
	<div class="hud">
		<div class="hud-block">
			<span class="hud-label">level</span>
			<span class="hud-value hud-level">{{ level }}</span>
		</div>

		<div class="hud-center">
			<div class="hud-pips-group">
				<span class="hud-label">lives</span>
				<div class="hud-pips">
					<span
						v-for="i in 5"
						:key="i"
						class="pip pip-life"
						:class="{ 'pip--active': i <= lives }" />
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
						:class="{ 'pip--active': i <= throwingStars }">
						<StarIcon :active="i <= throwingStars" :size="10" />
					</span>
				</div>
			</div>
		</div>

		<div class="hud-block hud-block--right">
			<span class="hud-label">players</span>
			<span class="hud-value">{{ Object.keys(playerHands).length }}</span>
		</div>
	</div>
</template>

<script setup lang="ts">
import StarIcon from "./StarIcon.vue";

const props = defineProps<{
	level: number;
	lives: number;
	throwingStars: number;
	playerHands: Record<string, number>;
}>();
</script>

<style scoped>
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
</style>
