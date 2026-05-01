<template>
	<div class="waiting-screen">
		<LoadingAnimation />
		<p class="waiting-title">Waiting for players</p>
		<p class="waiting-sub">{{ players.length }} / {{ room.max_players }} joined</p>

		<div class="player-grid">
			<div
				v-for="player in players"
				:key="player.player_id"
				class="player-pill"
				:class="{ host: player.player_id === room.host_player_id }">
				<span class="player-avatar">{{ initials(player.nickname) }}</span>
				<span class="player-name">{{ player.nickname }}</span>
				<span v-if="player.player_id === room.host_player_id" class="host-badge">host</span>
			</div>
		</div>

		<div class="lobby-footer">
			<p class="waiting-sub">Share your room code</p>
			<ShareCode :code="room.code" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import LoadingAnimation from "./LoadingAnimation.vue";
import ShareCode from "./ShareCode.vue";

import type { Room } from "@/dtos/RoomDto";

const props = defineProps<{ room: Room }>();

const players = computed(() => props.room?.players ?? []);

function initials(name: string) {
	return (
		name
			?.split(" ")
			.map((w) => w[0])
			.join("")
			.toUpperCase()
			.slice(0, 2) ?? "?"
	);
}
</script>

<style scoped>
.waiting-screen {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 16px;
	animation: fadeUp 0.5s ease both;
}

.waiting-title {
	font-family: var(--font-display);
	font-size: 32px;
	letter-spacing: 0.08em;
	color: var(--text-primary);
}

.waiting-sub {
	font-family: var(--font-mono);
	font-size: 0.8rem;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.player-grid {
	display: flex;
	flex-wrap: wrap;
	gap: 10px;
	justify-content: center;
	max-width: 480px;
	margin-top: 8px;
}

.player-pill {
	display: flex;
	align-items: center;
	gap: 8px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: 999px;
	padding: 6px 14px 6px 6px;
	transition: border-color var(--transition);
}

.player-pill.host {
	border-color: var(--green-dim);
}

.player-avatar {
	width: 28px;
	height: 28px;
	border-radius: 50%;
	background: var(--green-dim);
	color: var(--green-bright);
	font-family: var(--font-mono);
	font-size: 0.7rem;
	font-weight: 500;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-shrink: 0;
}

.player-name {
	font-family: var(--font-mono);
	font-size: 0.8rem;
	color: var(--text-primary);
	letter-spacing: 0.05em;
}

.host-badge {
	font-family: var(--font-mono);
	font-size: 0.6rem;
	letter-spacing: 0.12em;
	text-transform: uppercase;
	color: var(--green-bright);
	opacity: 0.7;
}

.lobby-footer {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8px;
	margin-top: 8px;
}
</style>
