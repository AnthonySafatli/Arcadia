<template>
	<div class="tally-row">
		<span class="tally tally--1st" :title="'1st place'">
			<span class="tally-icon">🥇</span>
			<span class="tally-num">{{ props.score?.["1st"] }}</span>
		</span>
		<span class="tally tally--2nd" :title="'2nd place'">
			<span class="tally-icon">🥈</span>
			<span class="tally-num">{{ props.score?.["2nd"] }}</span>
		</span>
		<span class="tally tally--3rd" :title="'3rd place'">
			<span class="tally-icon">🥉</span>
			<span class="tally-num">{{ props.score?.["3rd"] }}</span>
		</span>
	</div>
</template>

<script setup lang="ts">
import type { PlayerScore } from "./WordleState";

const props = defineProps<{
	score: PlayerScore | null | undefined;
}>();
</script>

<style scoped>
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
</style>
