<template>
	<div class="select">
		<button
			v-for="item in items"
			:key="item.id"
			class="select-card"
			:class="{ selected: modelValue === item.id }"
			@click="$emit('update:modelValue', item.id)">
			<div class="select-icon">
				<component :is="item.icon" width="24" height="24" />
			</div>

			<div class="select-info">
				<div class="select-name">{{ item.name }}</div>

				<div class="select-tags">
					<span v-for="tag in item.tags" :key="tag" class="badge">
						{{ tag }}
					</span>
				</div>
			</div>

			<div class="select-indicator" />
		</button>
	</div>
</template>

<script setup lang="ts">
import type { SelectItem } from "@/types/SelectItem";

defineProps<{
	items: SelectItem[];
	modelValue: string | null;
}>();

defineEmits<{
	(e: "update:modelValue", value: string): void;
}>();
</script>

<style scoped>
.select {
	display: flex;
	flex-direction: column;
	gap: 10px;
}

.select-card {
	display: flex;
	align-items: center;
	gap: 16px;
	padding: 18px 20px;
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-md);
	cursor: pointer;
	transition: var(--transition);
	text-align: left;
	position: relative;
	overflow: hidden;
}

.select-card::before {
	content: "";
	position: absolute;
	left: 0;
	top: 0;
	bottom: 0;
	width: 3px;
	background: var(--green-bright);
	transform: scaleY(0);
	transition: transform var(--transition);
}

.select-card:hover {
	border-color: var(--green-dim);
	background: var(--bg-raised);
}

.select-card.selected {
	border-color: var(--green-dim);
	background: var(--bg-raised);
	box-shadow:
		0 0 0 1px var(--green-dim),
		inset 0 0 40px var(--green-glow-sm);
}

.select-card.selected::before {
	transform: scaleY(1);
}

.select-icon {
	font-size: 24px;
	width: 44px;
	height: 44px;
	display: flex;
	align-items: center;
	justify-content: center;
	background: var(--bg-base);
	border-radius: var(--radius-sm);
	border: 1px solid var(--bg-border);
	flex-shrink: 0;
	color: var(--text-muted);
}

.select-info {
	flex: 1;
}

.select-name {
	font-weight: 500;
	color: var(--text-primary);
	font-size: 0.95rem;
}

.select-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
	margin-top: 4px;
}

.badge {
	font-family: var(--font-mono);
	font-size: 0.68rem;
	letter-spacing: 0.08em;
	color: var(--text-muted);
	background: var(--bg-base);
	border: 1px solid var(--bg-border);
	border-radius: 3px;
	padding: 2px 6px;
	text-transform: uppercase;
	white-space: nowrap;
}

.select-indicator {
	width: 18px;
	height: 18px;
	border-radius: 50%;
	border: 1.5px solid var(--bg-border);
	transition: var(--transition);
	flex-shrink: 0;
}

.select-card.selected .select-indicator {
	border-color: var(--green-bright);
	background: var(--green-bright);
	box-shadow: 0 0 8px var(--green-glow);
}

.select-card.selected .select-icon {
	color: var(--green-bright);
}
</style>
