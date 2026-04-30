<template>
    <div class="waiting-animation"><span /><span /><span /></div>
</template>

<style scoped>
.waiting-animation {
    display: flex;
    gap: 8px;
    margin-bottom: 8px;
}

.waiting-animation span {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--green-bright);
    animation: bounce 1.2s ease-in-out infinite;
}

.waiting-animation span:nth-child(2) {
    animation-delay: 0.2s;
}
.waiting-animation span:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes bounce {
    0%,
    100% {
        transform: translateY(0);
        opacity: 0.4;
    }
    50% {
        transform: translateY(-12px);
        opacity: 1;
    }
}
</style>
