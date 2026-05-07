import { ref } from "vue";
import { toast } from "vue3-toastify";
import { useSocket } from "@/composables/useSocket";
import type { Room } from "@/dtos/RoomDto";

const { socket } = useSocket();
const room = ref<Room | null>(null);
const state = ref<unknown | null>(null);
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

socket.on("game_start", (data) => {
	room.value = data.room;
	state.value = data.state;
});

socket.on("game_over", (data) => {
	room.value = data.room;
});
socket.on("game_state", (data) => {
	state.value = data.state;
});

export function useGameRoom() {
	return { room, state, connected };
}
