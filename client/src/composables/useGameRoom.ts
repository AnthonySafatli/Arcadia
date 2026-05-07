import { ref } from "vue";
import { toast } from "vue3-toastify";
import { useSocket } from "@/composables/useSocket";
import type { Room } from "@/dtos/RoomDto";

export function useGameRoom() {
	const { socket } = useSocket();
	const room = ref<Room | null>(null);
	const connected = ref(false);

	socket.on("joined", (data) => {
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
	const onGameStart = ref<(data: any) => void>(() => {});
	const onGameOver = ref<(data: any) => void>(() => {});
	const onGameState = ref<(data: any) => void>(() => {});

	socket.on("game_start", (data) => onGameStart.value(data));
	socket.on("game_over", (data) => onGameOver.value(data));
	socket.on("game_state", (data) => onGameState.value(data));

	return { room, connected, onGameStart, onGameOver, onGameState };
}
