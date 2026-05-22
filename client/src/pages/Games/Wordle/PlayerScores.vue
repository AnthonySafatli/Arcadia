<template>
	<div class="scores-row">
		<div v-for="(score, pid) in props.scores" :key="pid">
			<div
				v-if="pid !== playerId"
				class="player-score"
				:class="{
					'player-score--me': pid === playerId,
					'player-score--done': isPlayerDone(pid),
				}">
				<span class="player-name">{{ playerName(pid) }}</span>
				<TallyRow :score="score" />

				<!-- opponent mini grid -->
				<div v-if="pid !== playerId" class="mini-grid">
					<div v-for="(row, ri) in opponentTiles(pid)" :key="ri" class="mini-row">
						<div
							v-for="(tile, ti) in row"
							:key="ti"
							class="mini-tile"
							:class="tile"></div>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import type { PlayerScore, OtherPlayer, TileResult } from "./WordleState";

import TallyRow from "./TallyRow.vue";

import { usePlayerId } from "@/composables/usePlayerId";

const props = defineProps<{
	scores: Record<string, PlayerScore>;
	allPlayers: {
		player_id: string;
		nickname: string;
		connected: boolean;
	}[];
	finished: boolean;
	otherPlayers: Record<string, OtherPlayer>;
}>();

const playerId = usePlayerId();

function playerName(pid: string) {
	if (pid === playerId) return "you";
	return props.allPlayers.find((p) => p.player_id === pid)?.nickname ?? "???";
}

function isPlayerDone(pid: string) {
	if (pid === playerId) return props.finished;
	return props.otherPlayers[pid]?.finished ?? false;
}

function opponentTiles(pid: string): (TileResult | "empty" | "filled")[][] {
	const op = props.otherPlayers[pid];
	if (!op) return [];
	const rows: (TileResult | "empty" | "filled")[][] = [];
	for (let r = 0; r < 6; r++) {
		const row = op.tile_pattern[r];
		if (row !== undefined) {
			rows.push(row);
		} else if (r < op.guesses_used) {
			rows.push(Array(5).fill("absent"));
		} else {
			rows.push(Array(5).fill("empty"));
		}
	}
	return rows;
}
</script>

<style scoped>
.scores-row {
	display: flex;
	gap: 8px;
	width: 100%;
	flex-wrap: wrap;
	justify-content: center;
}

.player-score {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 6px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	padding: 10px 12px;
	flex: 1;
	min-width: 72px;
	max-width: 120px;
	transition: border-color 200ms ease;
}

.player-score--me {
	border-color: var(--green-dim);
	box-shadow: 0 0 10px rgba(57, 255, 138, 0.12);
}

.player-score--done {
	opacity: 0.7;
}

.player-name {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.2em;
	text-transform: uppercase;
	color: var(--text-secondary);
	white-space: nowrap;
	overflow: hidden;
	text-overflow: ellipsis;
	max-width: 90px;
}

.player-score--me .player-name {
	color: var(--green-bright);
}

/* ── Mini grid ── */
.mini-grid {
	display: flex;
	flex-direction: column;
	gap: 2px;
	margin-top: 2px;
}

.mini-row {
	display: flex;
	gap: 2px;
}

.mini-tile {
	width: 8px;
	height: 8px;
	border-radius: 1px;
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
}

.mini-tile.correct {
	background: var(--green-bright);
	border-color: var(--green-bright);
}
.mini-tile.present {
	background: #f5c518;
	border-color: #f5c518;
}
.mini-tile.absent {
	background: var(--bg-raised);
	border-color: var(--text-muted);
}
.mini-tile.empty {
	background: transparent;
}
</style>
