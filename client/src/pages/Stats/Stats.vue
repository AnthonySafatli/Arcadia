<template>
    <Page back-btn>
        <div class="content">
            <div class="page-header">
                <span class="label">system</span>
                <h2 class="title">Stats</h2>
            </div>

            <!-- Top stats row -->
            <div class="stats-grid">
                <div class="stat-card" v-for="stat in topStats" :key="stat.label">
                    <div class="stat-value" :class="{ green: stat.green }">{{ stat.value }}</div>
                    <div class="stat-label">{{ stat.label }}</div>
                    <div
                        class="stat-delta"
                        :class="stat.delta > 0 ? 'up' : 'down'"
                        v-if="stat.delta !== undefined"
                    >
                        {{ stat.delta > 0 ? '↑' : '↓' }} {{ Math.abs(stat.delta) }} today
                    </div>
                </div>
            </div>

            <!-- Active rooms table -->
            <div class="section">
                <div class="section-header">
                    <span class="section-title">Active Rooms</span>
                    <span class="badge">{{ activeRooms.length }} live</span>
                </div>
                <div class="table-wrap card">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Room</th>
                                <th>Game</th>
                                <th>Players</th>
                                <th>Status</th>
                                <th>Uptime</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="room in activeRooms" :key="room.id">
                                <td class="mono green">{{ room.id }}</td>
                                <td>{{ room.game }}</td>
                                <td>{{ room.players }}/{{ room.maxPlayers }}</td>
                                <td>
                                    <span class="status-pill" :class="room.status">{{
                                        room.status
                                    }}</span>
                                </td>
                                <td class="mono muted">{{ room.uptime }}</td>
                            </tr>
                            <tr v-if="activeRooms.length === 0">
                                <td colspan="5" class="empty">No active rooms</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Game breakdown -->
            <div class="section">
                <div class="section-header">
                    <span class="section-title">Games Played</span>
                </div>
                <div class="game-bars card">
                    <div class="bar-row" v-for="game in gameBreakdown" :key="game.name">
                        <span class="bar-label">{{ game.name }}</span>
                        <div class="bar-track">
                            <div class="bar-fill" :style="{ width: game.pct + '%' }" />
                        </div>
                        <span class="bar-count mono">{{ game.count }}</span>
                    </div>
                </div>
            </div>
        </div>
    </Page>
</template>

<script setup>
import Page from '@/components/Page.vue'

// Mock data — replace with real socket/API calls
const topStats = [
    { label: 'Online Players', value: '12', green: true, delta: 4 },
    { label: 'Active Rooms', value: '5', green: true, delta: 2 },
    { label: 'Games Today', value: '38', green: false, delta: 12 },
    { label: 'All-time Games', value: '412', green: false },
]

const activeRooms = [
    {
        id: 'X7K2PQ',
        game: 'Tic-tac-toe',
        players: 2,
        maxPlayers: 2,
        status: 'playing',
        uptime: '4m 12s',
    },
    { id: 'B3NNLW', game: 'Pong', players: 1, maxPlayers: 2, status: 'waiting', uptime: '0m 48s' },
    {
        id: 'QT90AS',
        game: 'Chess',
        players: 2,
        maxPlayers: 2,
        status: 'playing',
        uptime: '11m 03s',
    },
]

const gameBreakdown = [
    { name: 'Tic-tac-toe', count: 180, pct: 100 },
    { name: 'Pong', count: 120, pct: 67 },
    { name: 'Chess', count: 72, pct: 40 },
    { name: 'Checkers', count: 40, pct: 22 },
]
</script>

<style scoped>
.content {
    position: relative;
    z-index: 1;
    width: 100%;
    max-width: 720px;
    display: flex;
    flex-direction: column;
    gap: 32px;
    padding-top: 48px;
}

.page-header {
    animation: fadeUp 0.5s ease both;
}

.label {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--green-mid);
}

.title {
    font-family: var(--font-display);
    font-size: clamp(36px, 6vw, 56px);
    letter-spacing: 0.05em;
    color: var(--text-primary);
    line-height: 1.1;
    margin-top: 4px;
}

/* Top stats */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    animation: fadeUp 0.5s 0.1s ease both;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--bg-border);
    border-radius: var(--radius-md);
    padding: 20px;
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.stat-value {
    font-family: var(--font-display);
    font-size: 48px;
    line-height: 1;
    color: var(--text-secondary);
    letter-spacing: 0.05em;
}

.stat-value.green {
    color: var(--green-bright);
    text-shadow: 0 0 20px var(--green-glow);
}

.stat-label {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}

.stat-delta {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    margin-top: 4px;
}
.stat-delta.up {
    color: var(--green-mid);
}
.stat-delta.down {
    color: #e05252;
}

/* Sections */
.section {
    animation: fadeUp 0.5s 0.2s ease both;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
}

.section-title {
    font-family: var(--font-mono);
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-secondary);
}

.badge {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    background: var(--green-dim);
    color: var(--green-bright);
    border-radius: 3px;
    padding: 2px 8px;
}

/* Table */
.table-wrap {
    padding: 0;
    overflow: hidden;
}

.table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.875rem;
}

.table th {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    text-align: left;
    padding: 12px 20px;
    border-bottom: 1px solid var(--bg-border);
}

.table td {
    padding: 14px 20px;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--bg-border);
}

.table tr:last-child td {
    border-bottom: none;
}
.table tr:hover td {
    background: var(--bg-raised);
}

.mono {
    font-family: var(--font-mono);
    font-size: 0.85rem;
}
.green {
    color: var(--green-bright);
}
.muted {
    color: var(--text-muted);
}

.status-pill {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 3px;
}

.status-pill.playing {
    background: var(--green-dim);
    color: var(--green-bright);
}
.status-pill.waiting {
    background: rgba(245, 197, 24, 0.12);
    color: #f5c518;
}

.empty {
    text-align: center;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 0.8rem;
    padding: 32px !important;
}

/* Bar chart */
.game-bars {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.bar-row {
    display: grid;
    grid-template-columns: 100px 1fr 48px;
    align-items: center;
    gap: 16px;
}

.bar-label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    text-align: right;
}

.bar-track {
    height: 6px;
    background: var(--bg-base);
    border-radius: 3px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    background: var(--green-bright);
    border-radius: 3px;
    box-shadow: 0 0 8px var(--green-glow);
    transition: width 0.8s cubic-bezier(0.4, 0, 0.2, 1);
}

.bar-count {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-align: right;
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
