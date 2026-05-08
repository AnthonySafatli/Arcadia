<template>
	<Teleport to="body">
		<Transition name="overlay">
			<div class="overlay" v-if="visible">
				<div class="overlay-backdrop" @click="emit('backdropClick')" />
				<div class="overlay-content">
					<p v-if="subtitle" class="overlay-subtitle">{{ subtitle }}</p>
					<h1 class="overlay-title">{{ title }}</h1>
					<div v-if="$slots.default" class="overlay-actions">
						<slot />
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup lang="ts">
defineProps<{
	visible: boolean;
	title: string;
	subtitle?: string;
}>();

const emit = defineEmits(["backdropClick"]);
</script>

<style scoped>
.overlay {
	position: fixed;
	inset: 0;
	z-index: 100;
	display: flex;
	align-items: center;
	justify-content: center;
}

.overlay-backdrop {
	position: absolute;
	inset: 0;
	background: rgba(8, 12, 10, 0.85);
	backdrop-filter: blur(4px);
}

.overlay-content {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 16px;
	text-align: center;
	padding: 48px 56px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-lg);
	box-shadow:
		0 0 0 1px var(--bg-border),
		0 32px 64px rgba(0, 0, 0, 0.6),
		0 0 80px rgba(57, 255, 138, 0.04);
}

.overlay-subtitle {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.2em;
	text-transform: uppercase;
	color: var(--text-muted);
}

.overlay-title {
	font-family: var(--font-display);
	font-size: clamp(3rem, 8vw, 5.5rem);
	letter-spacing: 0.08em;
	line-height: 1;
	color: var(--text-primary);
	text-transform: uppercase;
}

.overlay-actions {
	display: flex;
	align-items: center;
	gap: 12px;
	margin-top: 8px;
	flex-wrap: wrap;
	justify-content: center;
}

/* Transition */
.overlay-enter-active {
	transition: opacity 300ms ease;
}
.overlay-enter-active .overlay-content {
	transition:
		opacity 300ms ease 80ms,
		transform 300ms cubic-bezier(0.4, 0, 0.2, 1) 80ms;
}

.overlay-leave-active {
	transition: opacity 200ms ease;
}
.overlay-leave-active .overlay-content {
	transition:
		opacity 200ms ease,
		transform 200ms ease;
}

.overlay-enter-from,
.overlay-leave-to {
	opacity: 0;
}
.overlay-enter-from .overlay-content,
.overlay-leave-to .overlay-content {
	opacity: 0;
	transform: translateY(12px) scale(0.97);
}
</style>
