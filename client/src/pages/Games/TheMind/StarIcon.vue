<template>
	<svg viewBox="0 0 16 16" :width="size" :height="size">
		<polygon
			points="8,1 10,6 15,6 11,9.5 12.5,15 8,12 3.5,15 5,9.5 1,6 6,6"
			:fill="active ? 'currentColor' : 'none'"
			:stroke="active ? 'none' : 'currentColor'"
			stroke-width="1.2" />
	</svg>
</template>

<script setup lang="ts">
defineProps<{ active?: boolean; size?: number }>();
</script>
