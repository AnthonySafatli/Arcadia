import type { Player } from './PlayerDto'

export interface NewRoom {
    game_slug: string;
    player_id: string;
    nickname: string;
}

export interface Room {
    code: string
    game_slug: string
    game_name: string
    status: string
    host_player_id: string
    players: Player[]
    min_players: number
    max_player: number
}
