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

			<ExtraActions
				:host-player-id="room?.host_player_id ?? ''"
				:player-count="room?.players.length ?? 0"
				:player-throwing-stars="state.player_throwing_stars"
				@focus="focus"
				@throwing-star="throwingStar"
				@reset="reset" />

			<GameOverlay
				:visible="focusCount > 0"
				title="Restart Focus"
				subtitle="Someone has suggested resetting the focus">
				<p>{{ focusCount }} / {{ room?.players.length }} players are focused</p>
				<button class="btn btn-primary" v-if="!playerFocus" @click="focus">Focus</button>
			</GameOverlay>

			<GameOverlay
				:visible="gameOverStatus == 'win'"
				title="You Win!"
				subtitle="Congratulations! You have completed the mind">
				<button
					class="btn btn-primary"
					v-if="room?.host_player_id == playerId"
					@click="reset">
					Restart
				</button>
			</GameOverlay>

			<GameOverlay
				:visible="gameOverStatus == 'loss'"
				title="You Loose!"
				subtitle="You have run out of lives">
				<button
					class="btn btn-primary"
					v-if="room?.host_player_id == playerId"
					@click="reset">
					Restart
				</button>
			</GameOverlay>
		</div>
	</div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";

import type { TheMindState } from "./TheMindState";
import { defaultTheMindState } from "./TheMindState";

import GameOverlay from "@/components/GameOverlay.vue";
import TopHud from "./TopHud.vue";
import PlayArea from "./PlayArea.vue";
import YourHand from "./YourHand.vue";
import ExtraActions from "./ExtraActions.vue";

import { usePlayerId } from "@/composables/usePlayerId";
import { useGameRoom } from "@/composables/useGameRoom";
import { useSocket } from "@/composables/useSocket";

import type { GameOverEvent } from "@/dtos/SocketEventDto";

const playerId = usePlayerId();

const gameOverStatus = ref<string | null>(null);

function gameOver(data: GameOverEvent) {
	gameOverStatus.value = data.winner;
}

const { sendAction } = useSocket();
const { room, state: socketState } = useGameRoom(gameOver);
const state = computed(() => (socketState.value as TheMindState) ?? defaultTheMindState());

const focusCount = computed(
	() => Object.values(state.value.player_focus ?? {}).filter((v) => v).length
);
const playerFocus = computed(() => state.value.player_focus?.[playerId]);

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

function throwingStar() {
	sendAction(room.value?.code!, playerId, {
		type: "throwing_star",
		state: !state.value.player_throwing_stars[playerId],
	});
}

function focus() {
	sendAction(room.value?.code!, playerId, { type: "focus", state: true });
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
</style>
