export type TileResult = "correct" | "present" | "absent";

export interface Guess {
	word: string;
	result: TileResult[];
	time: number;
}

export interface FinishedInfo {
	solved: boolean;
	guesses: number;
	finish_time: number;
}

export interface PlayerScore {
	"1st": number;
	"2nd": number;
	"3rd": number;
}

export interface OtherPlayer {
	tile_pattern: TileResult[][];
	guesses_used: number;
	finished: boolean;
	finished_info: FinishedInfo | null; // only populated when round_over
}

export interface WordleState {
	round: number;
	round_over: boolean;
	secret_word: string | null; // only populated when round_over
	guesses: Guess[];
	guesses_remaining: number;
	finished: boolean;
	finished_info: FinishedInfo | null;
	scores: Record<string, PlayerScore>;
	other_players: Record<string, OtherPlayer>;
}

export function defaultWordleState(): WordleState {
	return {
		round: 1,
		round_over: false,
		secret_word: null,
		guesses: [],
		guesses_remaining: 6,
		finished: false,
		finished_info: null,
		scores: {},
		other_players: {},
	};
}
