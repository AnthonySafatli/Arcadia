import type { Room } from './RoomDto'

export interface JoinedEvent {
    is_reconnect: boolean
    player_id: string
    room: Room
}

export interface GameStartEvent {
    state: unknown
    room: Room
}

export interface GameStateEvent {
    state: unknown
}

export interface GameOverEvent {
    winner: string
    room: Room
}

export interface PlayerEvent {
    player_id: string
    nickname: string
    room: Room
}

export interface ErrorEvent {
    message: string
}
