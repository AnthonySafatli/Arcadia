<script setup>
import Page from "@/components/Page.vue";
</script>

<template>
	<Page page-class="home" glow-orb>
		<div class="content">
			<!-- Logo -->
			<div class="logo-block">
				<div class="logo-icon">
					<img src="/icon.svg" alt="Logo" width="40" height="40" />
				</div>
				<h1 class="wordmark">arcadia</h1>
			</div>

			<p class="tagline">online. multiplayer. anytime.</p>

			<div class="actions">
				<router-link to="/host" class="btn btn-primary action-btn">
					<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
						<path
							d="M8 1a7 7 0 100 14A7 7 0 008 1zm3.5 7.5h-3v3a.5.5 0 01-1 0v-3h-3a.5.5 0 010-1h3v-3a.5.5 0 011 0v3h3a.5.5 0 010 1z" />
					</svg>
					Host Game
				</router-link>
				<router-link to="/join" class="btn btn-ghost action-btn">
					<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
						<path
							d="M11 8a3 3 0 11-6 0 3 3 0 016 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z" />
					</svg>
					Join Game
				</router-link>
			</div>

			<div class="version-tag">v0.0.1 — early access</div>
		</div>
	</Page>
</template>

<style scoped>
@keyframes pulse {
	0%,
	100% {
		opacity: 0.6;
		transform: translate(-50%, -50%) scale(1);
	}
	50% {
		opacity: 1;
		transform: translate(-50%, -50%) scale(1.1);
	}
}

.content {
	position: relative;
	z-index: 1;
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 0;
	text-align: center;
}

.logo-block {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 20px;
	margin-bottom: 16px;
	animation: fadeUp 0.6s ease both;
}

.logo-icon {
	filter: drop-shadow(0 0 20px var(--green-bright));
}

.wordmark {
	font-family: var(--font-display);
	font-size: clamp(72px, 14vw, 140px);
	letter-spacing: 0.12em;
	color: var(--text-primary);
	line-height: 1;
	text-shadow: 0 0 80px var(--green-glow);
}

.tagline {
	font-family: var(--font-mono);
	font-size: 0.8rem;
	letter-spacing: 0.2em;
	text-transform: uppercase;
	color: var(--green-mid);
	margin-bottom: 52px;
	animation: fadeUp 0.6s 0.1s ease both;
}

.actions {
	display: flex;
	flex-direction: column;
	gap: 12px;
	width: 100%;
	max-width: 280px;
	animation: fadeUp 0.6s 0.2s ease both;
}

.action-btn {
	width: 100%;
	padding: 16px 32px;
	font-size: 0.9rem;
}

.version-tag {
	margin-top: 48px;
	font-family: var(--font-mono);
	font-size: 0.7rem;
	color: var(--text-muted);
	letter-spacing: 0.1em;
	animation: fadeUp 0.6s 0.3s ease both;
}

@keyframes fadeUp {
	from {
		opacity: 0;
		transform: translateY(20px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}
</style>
