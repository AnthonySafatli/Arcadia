<!-- PlayerPill.vue -->
<template>
	<div class="player-pill" :class="{ me: isMe }" @click="changeNickname">
		<span class="player-avatar">{{ initials(player.nickname) }}</span>
		<span class="player-name">{{ player.nickname }}</span>
		<span v-if="isHost" class="host-badge">host</span>
	</div>
</template>

<script setup lang="ts">
import { computed } from "vue";

const props = defineProps({
	player: { type: Object, required: true },
	playerId: { type: String, required: true },
	hostPlayerId: { type: String, required: true },
});
const emit = defineEmits<{ changeNickname: [] }>();

const isMe = computed(() => props.player.player_id === props.playerId);
const isHost = computed(() => props.player.player_id === props.hostPlayerId);

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

function changeNickname() {
	if (!isMe) return;
	emit("changeNickname");
}
</script>

<style scoped>
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

.player-pill.me {
	border-color: var(--green-dim);
	box-shadow:
		0 0 6px var(--green-glow-sm),
		0 0 12px var(--green-glow);
	animation: pill-pulse 3s ease-in-out infinite;
	cursor: pointer;
}

@keyframes pill-pulse {
	0%,
	100% {
		box-shadow:
			0 0 6px var(--green-glow-sm),
			0 0 12px var(--green-glow);
	}
	50% {
		box-shadow:
			0 0 10px var(--green-glow),
			0 0 20px var(--green-glow);
	}
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
</style>
