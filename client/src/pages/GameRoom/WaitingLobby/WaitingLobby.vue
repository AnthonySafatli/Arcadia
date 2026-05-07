<template>
	<div class="waiting-screen">
		<LoadingAnimation />
		<p class="waiting-title">Waiting for players</p>
		<p class="waiting-sub">{{ players.length }} / {{ room.max_players }} joined</p>

		<div class="player-grid">
			<PlayerPill
				v-for="player in players.filter((x) => x.connected)"
				:key="player.player_id"
				:player="player"
				:player-id="playerId"
				:host-player-id="room.host_player_id"
				@changeNickname="$emit('changeNickname')" />
		</div>

		<div class="lobby-footer">
			<p class="waiting-sub">Share your room code</p>
			<ShareCode :code="room.code" />
		</div>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";

import { usePlayerId } from "@/composables/usePlayerId";

import PlayerPill from "./PlayerPill.vue";
import LoadingAnimation from "./LoadingAnimation.vue";
import ShareCode from "./ShareCode.vue";

import type { Room } from "@/dtos/RoomDto";

const props = defineProps<{ room: Room }>();
defineEmits<{ changeNickname: [] }>();

const players = computed(() => props.room?.players ?? []);

const playerId = usePlayerId();
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

.lobby-footer {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 8px;
	margin-top: 8px;
}
</style>
