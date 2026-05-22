<template>
	<div class="room-status">
		<span class="status-dot" :class="statusClass" />
		<span class="status-text">{{ label }}</span>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({ label: String });

const statusClass = computed(
	() =>
		({
			nothing: "",
			error: "red",
			loading: "yellow",
			waiting: "yellow",
			playing: "green",
			over: "red",
			disconnected: "red",
		})[props.label ?? "nothing"]
);
</script>

<style scoped>
.room-status {
	display: flex;
	justify-content: end;
	align-items: center;
	gap: 8px;
}

.status-dot {
	width: 8px;
	height: 8px;
	border-radius: 50%;
}

.status-dot.green {
	background: var(--green-bright);
	box-shadow: 0 0 6px var(--green-bright);
	animation: pulse-dot 2s infinite;
}
.status-dot.yellow {
	background: #f5c518;
	box-shadow: 0 0 6px #f5c518;
	animation: pulse-dot 2s infinite;
}
.status-dot.red {
	background: #ff4444;
	box-shadow: 0 0 6px #ff4444;
	animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
	0%,
	100% {
		opacity: 1;
	}
	50% {
		opacity: 0.4;
	}
}

.status-text {
	font-family: var(--font-mono);
	font-size: 0.75rem;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--text-secondary);
}
</style>
