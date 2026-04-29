export function usePlayerId() {
    let id = localStorage.getItem('player_id')
    if (!id) {
        id = window.crypto.randomUUID()
        localStorage.setItem('player_id', id)
    }
    return id
}
