<template>
	<div class="spinner" :style="{ '--size': sizePx }" :aria-label="label" role="status">
		<svg
			:width="size"
			:height="size"
			viewBox="0 0 40 40"
			fill="none"
			xmlns="http://www.w3.org/2000/svg">
			<!-- Track ring -->
			<circle cx="20" cy="20" r="16" stroke="var(--green-dim)" stroke-width="2.5" />
			<!-- Spinning arc -->
			<circle
				class="spinner__arc"
				cx="20"
				cy="20"
				r="16"
				stroke="var(--green-bright)"
				stroke-width="2.5"
				stroke-linecap="round"
				stroke-dasharray="40 60"
				stroke-dashoffset="0" />
			<!-- Glow arc (duplicate, blurred) -->
			<circle
				class="spinner__arc spinner__arc--glow"
				cx="20"
				cy="20"
				r="16"
				stroke="var(--green-bright)"
				stroke-width="4"
				stroke-linecap="round"
				stroke-dasharray="40 60"
				stroke-dashoffset="0"
				filter="url(#glow)" />
			<defs>
				<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
					<feGaussianBlur stdDeviation="2.5" result="blur" />
				</filter>
			</defs>
		</svg>
		<!-- Optional label slot -->
		<span v-if="$slots.default" class="spinner__label">
			<slot />
		</span>
	</div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
	/**
	 * Size in pixels. Accepts a number or a string like '48' or '48px'.
	 * @default 40
	 */
	size: {
		type: [Number, String],
		default: 40,
	},
	/**
	 * Accessible label for screen readers.
	 */
	label: {
		type: String,
		default: "Loading…",
	},
});

const sizePx = computed(() => {
	const raw = String(props.size);
	return raw.endsWith("px") ? raw : `${raw}px`;
});
</script>

<style scoped>
.spinner {
	display: inline-flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	gap: 10px;
	width: var(--size);
	height: var(--size);
}

.spinner__arc {
	transform-origin: 20px 20px;
	animation: spin 900ms cubic-bezier(0.4, 0, 0.2, 1) infinite;
}

.spinner__arc--glow {
	opacity: 0.45;
}

@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

.spinner__label {
	font-family: var(--font-mono, "DM Mono", monospace);
	font-size: 0.7em;
	letter-spacing: 0.1em;
	text-transform: uppercase;
	color: var(--text-secondary, #7a9e84);
	white-space: nowrap;
	/* label sits outside the fixed size box */
	position: absolute;
	margin-top: calc(var(--size) + 8px);
}
</style>
