<template>
    <div class="share-code">
        <span class="share-code-text">{{ code }}</span>
        <button class="btn btn-ghost copy-btn" @click="copy">
            {{ copied ? 'Copied!' : 'Copy' }}
        </button>
    </div>
</template>

<script setup>
import { ref } from 'vue'
const props = defineProps({ code: String })
const copied = ref(false)

async function copy() {
    await navigator.clipboard.writeText(props.code)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
}
</script>

<style scoped>
.share-code {
    display: flex;
    align-items: center;
    gap: 12px;
    background: var(--bg-card);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-md);
    padding: 12px 16px;
    margin-top: 8px;
}

.share-code-text {
    font-family: var(--font-mono);
    font-size: 1.4rem;
    font-weight: 500;
    letter-spacing: 0.3em;
    color: var(--green-bright);
}

.copy-btn {
    padding: 8px 16px;
    font-size: 0.75rem;
}
</style>
