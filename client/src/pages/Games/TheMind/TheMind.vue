<template>
	<div class="mind-wrap">
		<div class="grid-bg" aria-hidden="true"><div class="grid-bg-inner"></div></div>

		<div class="mind">
			<TopHud
				:level="state.level"
				:lives="state.lives"
				:throwing-stars="state.throwing_stars"
				:player-hands="state.player_hands" />

			<PlayArea
				:placed="state.placed"
				:discarded="state.discarded"
				:player-hands="state.player_hands"
				:player-hovering="state.player_hovering"
				:players="room?.players ?? []" />

			<YourHand
				:hand="state.hand"
				:next-level-btn="showNextLevelBtn"
				@place="place"
				@hover="hover"
				@next-level="nextLevel" />

			<!-- <GameOverlay visible title="Throwing Star" subtitle="wanted by mr man"/> -->
		</div>
	</div>
</template>
<script setup lang="ts">
import { computed } from "vue";

import type { TheMindState } from "./TheMindState";

import GameOverlay from "@/components/GameOverlay.vue";
import TopHud from "./TopHud.vue";
import PlayArea from "./PlayArea.vue";
import YourHand from "./YourHand.vue";

import { usePlayerId } from "@/composables/usePlayerId";
import { useGameRoom } from "@/composables/useGameRoom";
import { useSocket } from "@/composables/useSocket";

const playerId = usePlayerId();

const { sendAction } = useSocket();
const { room, state: socketState } = useGameRoom();
const state = computed(() => socketState.value as TheMindState);

const showNextLevelBtn = computed(
	() =>
		room.value?.host_player_id === playerId &&
		Object.values(state.value.player_hands).every((x) => x === 0)
);

function hover(state: boolean) {
	sendAction(room.value?.code!, playerId, { type: "hover", state: state });
}

function place() {
	sendAction(room.value?.code!, playerId, { type: "place" });
}

function nextLevel() {
	sendAction(room.value?.code!, playerId, { type: "next_level" });
}

function throwingStar(state: boolean) {
	sendAction(room.value?.code!, playerId, { type: "throwing_star", state: state });
}

function focus(state: boolean) {
	sendAction(room.value?.code!, playerId, { type: "focus", state: state });
}

function reset() {
	sendAction(room.value?.code!, playerId, { type: "reset" });
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
</style>
