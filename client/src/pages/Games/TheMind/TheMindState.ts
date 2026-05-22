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
