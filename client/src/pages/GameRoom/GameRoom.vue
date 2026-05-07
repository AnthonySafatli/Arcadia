<template>
	<div class="game-room">
		<header class="room-header">
			<router-link to="/" class="wordmark">arcadia</router-link>

			<div class="room-info">
				<span class="room-label">room</span>
				<span class="room-code">{{ roomId }}</span>
			</div>

			<StatusBadge :status="statusClass" :label="roomStatus" />
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
				@changeNickname="showNicknameModal = true" />

			<!-- Game canvas placeholder -->
			<div v-else class="game-canvas">
				<p class="placeholder-text">Game component renders here</p>
				<!-- <component :is="gameComponent" :state="state" /> -->
			</div>
		</main>
	</div>
	<NicknameModal v-model="showNicknameModal" :onNicknameChanged="onNicknameChange" />
</template>

<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useQuery } from "@tanstack/vue-query";
import { toast } from "vue3-toastify";

import { useSocket } from "@/composables/useSocket";
import { usePlayerId } from "@/composables/usePlayerId";
import { useNickname } from "@/composables/useNickname";

import type { Room } from "@/dtos/RoomDto";

import StatusBadge from "./StatusBadge.vue";
import JoinError from "./JoinError/JoinError.vue";
import PreJoinScreen from "./PreJoinScreen/PreJoinScreen.vue";
import WaitingLobby from "./WaitingLobby/WaitingLobby.vue";
import Spinner from "@/components/Spinner.vue";
import NicknameModal from "@/components/NicknameModal.vue";

const { socket, connect, joinRoom, changeNickname } = useSocket();
const playerId = usePlayerId();
const nickname = useNickname();

const showNicknameModal = ref(false);

const route = useRoute();
const roomId = computed(() => route.params.id);

socket.on("joined", (data) => {
	connected.value = true;
	room.value = data.room;
});

socket.on("game_start", (data) => {});

socket.on("game_over", (data) => {});

socket.on("game_state", (data) => {});

socket.on("player_joined", (data) => {
	room.value = data.room;
});

socket.on("player_reconnected", (data) => {
	room.value = data.room;
});

socket.on("player_disconnected", (data) => {
	room.value = data.room;
});

socket.on("player_renamed", (data) => {
	console.log("here");
	console.log(data);
	const player = room.value?.players.find((x) => x.player_id == data.player_id);
	if (player) {
		player.nickname = data.nickname;
	}
});

socket.on("error", (data) => {
	console.error(data.message);
	toast(data.message, {
		theme: "dark",
		type: "error",
		position: "bottom-center",
	});
});

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
	if (newData) {
		room.value = newData;
		if (room.value.host_player_id == playerId) onConnect();
	}
});

const room = ref<Room | null>(null);
const connected = ref(false);

const roomStatus = computed(
	() => room.value?.status ?? (isPending.value ? "loading" : isError.value ? "error" : null)
);
const statusClass = computed(
	() =>
		({
			nothing: "",
			error: "red",
			loading: "yellow",
			waiting: "yellow",
			playing: "green",
			over: "red",
		})[roomStatus.value ?? "nothing"]
);

function onConnect() {
	connect();
	joinRoom(roomId.value as string, playerId, nickname.value);
}

function onNicknameChange(nickname: string) {
	changeNickname(room.value?.code!, playerId, nickname);
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

.game-canvas {
	width: 100%;
	height: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
}

.placeholder-text {
	font-family: var(--font-mono);
	color: var(--text-muted);
	font-size: 0.85rem;
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
