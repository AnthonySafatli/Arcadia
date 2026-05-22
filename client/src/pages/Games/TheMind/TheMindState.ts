export interface TheMindState {
	hand: number[];
	placed: number[];
	discarded: number[];

	level: number;
	lives: number;
	throwing_stars: number;

	player_hands: Record<string, number>;
	player_hovering: Record<string, boolean>;
	player_throwing_stars: Record<string, boolean>;
	player_focus: Record<string, boolean>;
}

export function defaultTheMindState(): TheMindState {
	return {
		hand: [],
		placed: [],
		discarded: [],
		level: 1,
		lives: 0,
		throwing_stars: 0,
		player_hands: {},
		player_hovering: {},
		player_throwing_stars: {},
		player_focus: {},
	};
}
