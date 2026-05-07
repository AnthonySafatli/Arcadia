import { ref, onUnmounted } from "vue";
import { toast } from "vue3-toastify";
import { useSocket } from "@/composables/useSocket";
import type { Room } from "@/dtos/RoomDto";
import type { GameStartEvent, GameOverEvent, GameStateEvent } from "@/dtos/SocketEventDto";

export function useGameRoom() {
	const { socket } = useSocket();
	const room = ref<Room | null>(null);
	const connected = ref(false);

	socket.on("joined", (data) => {
		console.log("here");
		connected.value = true;
		room.value = data.room;
	});

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
		const player = room.value?.players.find((x) => x.player_id == data.player_id);
		if (player) player.nickname = data.nickname;
	});

	socket.on("error", (data) => {
		console.error(data.message);
		toast(data.message, { theme: "dark", type: "error", position: "bottom-center" });
	});

	// Game-specific handlers — override/extend these per game
	const onGameStart = ref<(data: GameStartEvent) => void>(() => {});
	const onGameOver = ref<(data: GameOverEvent) => void>(() => {});
	const onGameState = ref<(data: GameStateEvent) => void>(() => {});

	socket.on("game_start", (data) => onGameStart.value(data));
	socket.on("game_over", (data) => onGameOver.value(data));
	socket.on("game_state", (data) => onGameState.value(data));

	onUnmounted(() => {
		socket.off("joined");
		socket.off("player_joined");
		socket.off("player_reconnected");
		socket.off("player_disconnected");
		socket.off("player_renamed");
		socket.off("error");
		socket.off("game_start");
		socket.off("game_over");
		socket.off("game_state");
		socket.disconnect();
	});

	return { room, connected, onGameStart, onGameOver, onGameState };
}
