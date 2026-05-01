<template>
	<Teleport to="body">
		<Transition name="modal">
			<div v-if="modelValue" class="modal-backdrop" @click.self="onBackdropClick">
				<div class="modal-panel" :style="{ maxWidth: width }">
					<div class="modal-header">
						<span v-if="title" class="modal-title">{{ title }}</span>
						<button
							class="modal-close"
							@click="$emit('update:modelValue', false)"
							aria-label="Close">
							<svg width="14" height="14" viewBox="0 0 14 14" fill="none">
								<path
									d="M1 1l12 12M13 1L1 13"
									stroke="currentColor"
									stroke-width="1.5"
									stroke-linecap="round" />
							</svg>
						</button>
					</div>
					<div class="modal-body">
						<slot />
					</div>
				</div>
			</div>
		</Transition>
	</Teleport>
</template>

<script setup lang="ts">
const props = withDefaults(
	defineProps<{
		modelValue: boolean;
		title?: string;
		width?: string;
		closeOnBackdrop?: boolean;
	}>(),
	{
		width: "420px",
		closeOnBackdrop: true,
	}
);

const emit = defineEmits<{
	"update:modelValue": [value: boolean];
}>();

function onBackdropClick() {
	if (props.closeOnBackdrop) emit("update:modelValue", false);
}
</script>

<style scoped>
.modal-backdrop {
	position: fixed;
	inset: 0;
	background: rgba(4, 6, 5, 0.92);
	backdrop-filter: blur(6px);
	-webkit-backdrop-filter: blur(6px);
	display: flex;
	align-items: center;
	justify-content: center;
	padding: 24px;
	z-index: 1000;
}

.modal-panel {
	width: 100%;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-lg);
	box-shadow:
		0 0 0 1px rgba(57, 255, 138, 0.04),
		0 24px 64px rgba(0, 0, 0, 0.6),
		0 0 80px rgba(57, 255, 138, 0.04);
	overflow: hidden;
}

.modal-header {
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 20px 24px 16px;
	border-bottom: 1px solid var(--bg-border);
}

.modal-title {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	font-weight: 500;
	letter-spacing: 0.18em;
	text-transform: uppercase;
	color: var(--text-secondary);
}

.modal-close {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 28px;
	height: 28px;
	background: transparent;
	border: 1px solid transparent;
	border-radius: var(--radius-sm);
	color: var(--text-muted);
	cursor: pointer;
	transition: var(--transition);
	padding: 0;
	margin-left: auto;
}

.modal-close:hover {
	border-color: var(--bg-border);
	color: var(--green-bright);
}

.modal-body {
	padding: 24px;
}

/* Transition */
.modal-enter-active,
.modal-leave-active {
	transition: opacity 180ms ease;
}
.modal-enter-active .modal-panel,
.modal-leave-active .modal-panel {
	transition:
		opacity 180ms ease,
		transform 220ms cubic-bezier(0.4, 0, 0.2, 1);
}
.modal-enter-from,
.modal-leave-to {
	opacity: 0;
}
.modal-enter-from .modal-panel {
	opacity: 0;
	transform: translateY(12px) scale(0.97);
}
.modal-leave-to .modal-panel {
	opacity: 0;
	transform: translateY(8px) scale(0.98);
}
</style>
