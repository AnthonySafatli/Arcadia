<template>
	<div>
		<div id="modals"></div>
		<div class="game-room">
			<header class="room-header">
				<div class="logo-section">
					<router-link to="/" class="wordmark">arcadia</router-link>
					<div v-if="room?.host_player_id == playerId" class="host-badge">host</div>
				</div>

				<div class="room-info">
					<span class="room-label">room</span>
					<span class="room-code">{{ roomId }}</span>
				</div>

				<div class="room-status-div">
					<p class="room-game-name" v-if="room">{{ room.game_name }}</p>
					<StatusBadge :label="roomStatus" />
				</div>
			</header>

			<main class="room-body">
				<!-- Loading -->
				<Spinner v-if="roomStatus === 'loading'" />

				<!-- Join Error -->
				<JoinError v-else-if="isError" :error="error?.message ?? ''" />

				<!-- Yet To Join -->
				<PreJoinScreen
					v-else-if="!connected && roomStatus === 'waiting'"
					:room="room!"
					@join="onConnect" />

				<!-- Waiting state -->
				<WaitingLobby
					v-else-if="roomStatus === 'waiting'"
					:room="room!"
					@changeNickname="showNicknameModal = true"
					@onStartGame="startGameEvent" />

				<!-- Game Canvas -->
				<GameCanvas v-else />
			</main>
		</div>
		<NicknameModal v-model="showNicknameModal" :onNicknameChanged="onNicknameChange" />
	</div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useQuery } from "@tanstack/vue-query";

import { useSocket } from "@/composables/useSocket";
import { useGameRoom } from "@/composables/useGameRoom";
import { usePlayerId } from "@/composables/usePlayerId";
import { useNickname } from "@/composables/useNickname";

import type { Room } from "@/dtos/RoomDto";

import GameCanvas from "./GameCanvas.vue";
import StatusBadge from "./StatusBadge.vue";
import JoinError from "./JoinError/JoinError.vue";
import PreJoinScreen from "./PreJoinScreen/PreJoinScreen.vue";
import WaitingLobby from "./WaitingLobby/WaitingLobby.vue";
import Spinner from "@/components/Spinner.vue";
import NicknameModal from "@/components/NicknameModal.vue";

const route = useRoute();
const roomId = computed(() => route.params.id);

const playerId = usePlayerId();
const nickname = useNickname();

const { connect, joinRoom, changeNickname, startGame } = useSocket();
const { room, connected } = useGameRoom();

const showNicknameModal = ref(false);

const { data, isError, error, isPending } = useQuery<Room>({
	queryKey: ["rooms", roomId],
	queryFn: async (): Promise<Room> => {
		const r = await fetch(`/api/rooms/${roomId.value}`);
		if (!r.ok) {
			const body = await r.json();
			throw new Error(body.message ?? body.error ?? `${r.status}`);
		}
		return r.json();
	},
});

watch(data, (newData) => {
	if (!newData) return;
	room.value = newData;
	if (!connected.value) {
		onConnect();
	}
});

const roomStatus = computed(
	() => room.value?.status ?? (isPending.value ? "loading" : isError.value ? "error" : null)
);

function onConnect() {
	connect();
	joinRoom(roomId.value as string, playerId, nickname.value);
}

function onNicknameChange(nickname: string) {
	changeNickname(room.value?.code!, playerId, nickname);
}

function startGameEvent() {
	startGame(room.value?.code!, playerId);
}
</script>

<style scoped>
.game-room {
	min-height: 100vh;
	display: flex;
	flex-direction: column;
	background: var(--bg-base);
}

.room-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 16px 32px;
	border-bottom: 1px solid var(--bg-border);
	background: var(--bg-card);
	flex-shrink: 0;
	z-index: 101;
}

.wordmark {
	font-family: var(--font-display);
	font-size: 24px;
	letter-spacing: 0.1em;
	color: var(--text-primary);
	text-decoration: none;
	transition: color var(--transition);
}
.wordmark:hover {
	color: var(--green-bright);
}

.room-info {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 2px;
}

.room-label {
	font-family: var(--font-mono);
	font-size: 0.65rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.room-code {
	font-family: var(--font-mono);
	font-size: 1.1rem;
	font-weight: 500;
	color: var(--green-bright);
	letter-spacing: 0.2em;
	text-shadow: 0 0 12px var(--green-glow);
}

.room-body {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
}

.room-status-div {
	display: flex;
	flex-direction: column;
	justify-content: end;
	gap: 5px;
}

.room-game-name {
	font-family: var(--font-mono);
	font-size: 1rem;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.logo-section {
	display: flex;
	align-items: center;
	gap: 20px;
}

.host-badge {
	display: inline-flex;
	align-items: center;
	gap: 5px;
	font-family: var(--font-mono);
	font-size: 0.62rem;
	font-weight: 500;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--bg-base);
	background: var(--green-bright);
	padding: 3px 7px;
	border-radius: 4px;
	box-shadow: 0 0 10px var(--green-glow);
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
