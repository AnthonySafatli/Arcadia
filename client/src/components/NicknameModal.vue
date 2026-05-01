<template>
	<Modal v-model="show" title="Identity" width="380px">
		<div class="nickname-form">
			<label class="field-label" for="nickname-input">Set nickname:</label>
			<div class="input-wrap">
				<input
					id="nickname-input"
					ref="inputRef"
					v-model="draft"
					class="nickname-input"
					type="text"
					placeholder="enter handle..."
					maxlength="24"
					spellcheck="false"
					@keydown.enter="confirm" />
				<span class="char-count">{{ draft.length }}/24</span>
			</div>
			<div class="actions">
				<button class="btn btn-ghost" @click="show = false">cancel</button>
				<button class="btn btn-primary" :disabled="!draft.trim()" @click="confirm">
					confirm
				</button>
			</div>
		</div>
	</Modal>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from "vue";
import Modal from "./Modal.vue";
import { useNickname, useSetNickname } from "@/composables/useNickname";

const props = defineProps<{ modelValue: boolean }>();
const emit = defineEmits<{ "update:modelValue": [value: boolean] }>();

const nickname = useNickname();
const show = ref(props.modelValue);
const draft = ref(nickname.value);
const inputRef = ref<HTMLInputElement | null>(null);

watch(
	() => props.modelValue,
	(v) => {
		show.value = v;
		if (v) {
			draft.value = nickname.value ?? "";
			nextTick(() => inputRef.value?.select());
		}
	}
);

watch(show, (v) => emit("update:modelValue", v));

function confirm() {
	const trimmed = draft.value.trim();
	if (!trimmed) return;
	useSetNickname(trimmed);
	show.value = false;
}
</script>

<style scoped>
.nickname-form {
	display: flex;
	flex-direction: column;
	gap: 20px;
}

.field-label {
	font-family: var(--font-mono);
	font-size: 0.7rem;
	letter-spacing: 0.15em;
	text-transform: uppercase;
	color: var(--text-secondary);
}

.input-wrap {
	position: relative;
}

.nickname-input {
	width: 100%;
	background: var(--bg-raised);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	padding: 12px 48px 12px 16px;
	font-family: var(--font-mono);
	font-size: 0.95rem;
	color: var(--text-primary);
	outline: none;
	transition: var(--transition);
	letter-spacing: 0.05em;
}

.nickname-input::placeholder {
	color: var(--text-muted);
}

.nickname-input:focus {
	border-color: var(--green-dim);
	box-shadow: 0 0 0 3px rgba(57, 255, 138, 0.06);
}

.char-count {
	position: absolute;
	right: 12px;
	top: 50%;
	transform: translateY(-50%);
	font-family: var(--font-mono);
	font-size: 0.65rem;
	color: var(--text-muted);
	pointer-events: none;
}

.actions {
	display: flex;
	gap: 10px;
	justify-content: flex-end;
}

.btn:disabled {
	opacity: 0.35;
	cursor: not-allowed;
	pointer-events: none;
}
</style>
