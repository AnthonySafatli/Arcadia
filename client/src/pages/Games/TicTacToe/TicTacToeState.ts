export interface TicTacToeState {
	board: (string | null)[]; // 9 cells, null = empty, string = player_id
	current_turn: string; // player_id of whoever's turn it is
	marks: Record<string, "X" | "O">; // player_id -> mark
	winner: string | "draw" | null;
	scores: Record<string, number>;
}
