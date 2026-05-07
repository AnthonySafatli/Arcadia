import { io, Socket } from "socket.io-client";

import type {
	JoinedEvent,
	GameStartEvent,
	GameOverEvent,
	GameStateEvent,
	PlayerEvent,
} from "@/dtos/SocketEventDto";

export interface ServerToClientEvents {
	joined: (data: JoinedEvent) => void;
	game_start: (data: GameStartEvent) => void;
	game_over: (data: GameOverEvent) => void;
	game_state: (data: GameStateEvent) => void;
	player_joined: (data: PlayerEvent) => void;
	player_reconnected: (data: PlayerEvent) => void;
	player_disconnected: (data: PlayerEvent) => void;
	player_renamed: (data: PlayerEvent) => void;
	error: (data: ErrorEvent) => void;
}

export interface ClientToServerEvents {
	join_room: (data: { room_code: string; player_id: string; nickname: string }) => void;
	start_game: (data: { room_code: string; player_id: string }) => void;
	change_nickname: (data: { room_code: string; player_id: string; nickname: string }) => void;
	action: (data: { room_code: string; player_id: string; action: unknown }) => void;
}

// ---- Singleton ----
const socket: Socket<ServerToClientEvents, ClientToServerEvents> = io("http://localhost:5000", {
	autoConnect: false,
});

// ---- Composable ----
export function useSocket() {
	const connect = () => socket.connect();
	const disconnect = () => socket.disconnect();

	const joinRoom = (roomCode: string, playerId: string, nickname: string) => {
		socket.emit("join_room", { room_code: roomCode, player_id: playerId, nickname });
	};

	const startGame = (roomCode: string, playerId: string) => {
		socket.emit("start_game", { room_code: roomCode, player_id: playerId });
	};

	const changeNickname = (roomCode: string, playerId: string, nickname: string) => {
		socket.emit("change_nickname", {
			room_code: roomCode,
			player_id: playerId,
			nickname: nickname,
		});
	};

	const sendAction = (roomCode: string, playerId: string, action: unknown) => {
		socket.emit("action", { room_code: roomCode, player_id: playerId, action });
	};

	return { socket, connect, disconnect, joinRoom, startGame, changeNickname, sendAction };
}
