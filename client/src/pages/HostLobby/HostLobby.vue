<template>
	<Page back-btn>
		<div class="content">
			<div class="page-header">
				<span class="label">host a game</span>
				<h2 class="title">Choose your game</h2>
			</div>

			<Select v-if="selectOptions.length > 0" v-model="selected" :items="selectOptions" />

			<button class="btn btn-primary launch-btn" :disabled="!selected" @click="launch">
				Launch Room
			</button>
		</div>
	</Page>
</template>

<script setup lang="ts">
import { computed, watch } from "vue";
import { useQuery, useMutation } from "@tanstack/vue-query";
import { usePlayerId } from "@/composables/usePlayerId";
import { useNickname } from "@/composables/useNickname";

import type { Game } from "@/dtos/GameDto";
import type { NewRoom, Room } from "@/dtos/RoomDto";

import type { SelectItem } from "@/types/SelectItem";

import Page from "@/components/Page.vue";
import Select from "./Select.vue";

import { ref } from "vue";
import { useRouter } from "vue-router";

const { data } = useQuery<Game[]>({
	queryKey: ["games"],
	queryFn: (): Promise<Game[]> => fetch("/api/games").then((r) => r.json()),
});

const { mutate } = useMutation<Room, Error, NewRoom>({
	mutationFn: (newRoom: NewRoom) =>
		fetch("/api/rooms", {
			method: "POST",
			body: JSON.stringify(newRoom),
		}).then((r) => r.json()),
});

const router = useRouter();
const selected = ref<string | null>(null);

const selectOptions = computed<SelectItem[]>(
	() =>
		data.value?.map((x) => ({
			id: x.slug,
			name: x.name,
			icon: "⊞",
			tags: [
				x.min_players === x.max_players
					? `${x.min_players} Players`
					: `${x.min_players}-${x.max_players} Players`,
				...x.tags,
			],
		})) ?? []
);

function launch() {
	if (!selected.value) return;

	const playerId = usePlayerId();
	const nickname = useNickname();

	const newRoom: NewRoom = {
		game_slug: selected.value,
		player_id: playerId,
		nickname: nickname.value,
	};
	mutate(newRoom, {
		onSuccess: (room) => {
			router.push(`/room/${room.code}`);
		},
	});
}
</script>

<style scoped>
.content {
	position: relative;
	z-index: 1;
	width: 100%;
	max-width: 560px;
	display: flex;
	flex-direction: column;
	gap: 32px;
}

.page-header {
	animation: fadeUp 0.5s ease both;
}

.label {
	font-family: var(--font-mono);
	font-size: 0.75rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--green-mid);
}

.title {
	font-family: var(--font-display);
	font-size: clamp(36px, 6vw, 56px);
	letter-spacing: 0.05em;
	color: var(--text-primary);
	line-height: 1.1;
	margin-top: 4px;
}

.launch-btn {
	width: 100%;
	padding: 16px;
	font-size: 0.9rem;
	animation: fadeUp 0.5s 0.2s ease both;
}

.launch-btn:disabled {
	opacity: 0.35;
	cursor: not-allowed;
	box-shadow: none;
	transform: none;
}

@keyframes fadeUp {
	from {
		opacity: 0;
		transform: translateY(16px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}
</style>
