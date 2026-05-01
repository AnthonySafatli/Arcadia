<template>
	<div class="page">
		<div class="grid-bg" />

		<div class="content">
			<div class="error-code">404</div>
			<h1 class="title">Page not found</h1>
			<p class="attempted">
				<span class="mono">{{ route.path }}</span> doesn't exist
			</p>
			<router-link to="/" class="btn btn-primary">Back to arcadia</router-link>
		</div>
	</div>
</template>

<script setup>
import { useRoute } from "vue-router";
const route = useRoute();
</script>

<style scoped>
.content {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 16px;
	text-align: center;
	animation: fadeUp 0.5s ease both;
}

.error-code {
	font-family: var(--font-display);
	font-size: clamp(120px, 20vw, 200px);
	line-height: 1;
	color: var(--text-secondary);
	letter-spacing: 0.1em;
	text-shadow: 0 0 80px var(--green-glow-sm);
	user-select: none;
}

.title {
	font-family: var(--font-display);
	font-size: clamp(28px, 5vw, 48px);
	letter-spacing: 0.08em;
	color: var(--text-primary);
	margin-top: -24px;
}

.attempted {
	font-family: var(--font-body);
	color: var(--text-primary);
	font-size: 0.9rem;
}

.mono {
	font-family: var(--font-mono);
	color: var(--green-mid);
	background: var(--bg-card);
	border: 1px solid var(--bg-border);
	border-radius: var(--radius-sm);
	padding: 2px 8px;
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
