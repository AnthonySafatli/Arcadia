<template>
	<div class="page" :class="pageClass">
		<!-- Background Effects -->
		<div class="grid-bg" />
		<div v-if="glowOrb" class="glow-orb" />

		<!-- Headers -->
		<router-link v-if="backBtn" to="/" class="back-link">back</router-link>

		<!-- Content -->
		<slot />
	</div>
</template>

<script setup>
defineProps({
	pageClass: { type: String, default: "" },
	backBtn: { type: Boolean, default: false },
	glowOrb: { type: Boolean, default: false },
});
</script>

<style>
.home {
	overflow: hidden;
}

.glow-orb {
	position: fixed;
	width: 600px;
	height: 600px;
	background: radial-gradient(circle, var(--green-glow) 0%, transparent 70%);
	top: 50%;
	left: 50%;
	transform: translate(-50%, -50%);
	pointer-events: none;
	animation: pulse 6s ease-in-out infinite;
}
</style>
