import time
import threading

from engine.game_registry import get_game_class
from models.room import Room
from models.player import Player

# In-memory store. Replace with Redis for multi-process deployments.
# TODO: Replace with not in-memory dict
_rooms: dict[str, Room] = {}
# socket_id → player_id (for fast lookup on disconnect)
_socket_to_player: dict[str, tuple[str, str]] = {}  # socket_id → (room_code, player_id)

# Room lifecycle

def create_room(game_slug: str, host_player_id: str, host_nickname: str) -> Room:
    code = Room.generate_code(_rooms)
    room = Room(code=code, game_slug=game_slug, host_player_id=host_player_id)
    host = Player(player_id=host_player_id, nickname=host_nickname)
    room.players[host_player_id] = host
    _rooms[code] = room
    return room

def get_room(code: str) -> Room | None:
    return _rooms.get(code.upper())

def list_rooms() -> list[Room]:
    return list(_rooms.values())

# Player join / reconnect

def join_room(code: str, player_id: str, nickname: str, socket_id: str) -> tuple[Room, Player, bool]:
    """
    Returns (room, player, is_reconnect).
    Raises ValueError on invalid state.
    """
    room = get_room(code)
    if not room:
        raise ValueError("Room not found.")
    if room.status == "finished":
        raise ValueError("Game has already ended.")

    game_cls = get_game_class(room.game_slug)

    is_reconnect = player_id in room.players

    if is_reconnect:
        player = room.players[player_id]
        if player.socket_id and player.socket_id in _socket_to_player:
            del _socket_to_player[player.socket_id]
        player.socket_id = socket_id
        player.connected = True
        player.disconnected_at = None
    else:
        if room.status == "playing":
            raise ValueError("Game already in progress.")
        if game_cls and sum(1 for p in room.players.values() if p.connected) >= game_cls.MAX_PLAYERS:
            raise ValueError("Room is full.")
        player = Player(player_id=player_id, nickname=nickname, socket_id=socket_id, connected=True)
        room.players[player_id] = player
        if len(room.players) > game_cls.MAX_PLAYERS:
            disconnected = [p for p in room.players.values() if not p.connected]
            if disconnected:
                longest_disconnected = min(disconnected, key=lambda x: x.disconnected_at)
                del room.players[longest_disconnected.player_id]

    _socket_to_player[socket_id] = (room.code, player_id)
    return room, player, is_reconnect

def player_disconnect(socket_id: str) -> tuple[Room, Player] | None:
    entry = _socket_to_player.pop(socket_id, None)
    if not entry:
        return None
    room_code, player_id = entry
    room = _rooms.get(room_code)
    if not room or player_id not in room.players:
        return None
    
    player = room.players[player_id]
    player.connected = False
    player.disconnected_at = time.time()

    # Reassign host if needed
    if room.host_player_id == player_id and room.status == "waiting":
        next_host = next(
            (p for p in room.players.values() if p.player_id != player_id and p.connected),
            None
        )
        if next_host:
            room.host_player_id = next_host.player_id

    return room, player

def change_nickname(room_code: str, player_id: str, nickname: str) -> Player:
    room = get_room(room_code)
    if not room:
        raise ValueError("Room not found.")
    print(player_id)
    print(list(room.players.keys()))
    if player_id not in room.players:
        raise ValueError("Player not in room.")
    if not nickname or len(nickname) > 20:
        raise ValueError("Nickname must be 1-20 characters.")
    room.players[player_id].nickname = nickname
    return room.players[player_id]

def register_socket(socket_id: str, room_code: str, player_id: str):
    _socket_to_player[socket_id] = (room_code, player_id)

# Game start

def start_game(room: Room) -> dict:
    """Instantiate the game and return initial state. Raises on bad state."""
    from engine.game_registry import get_game_class
    if room.status != "waiting":
        raise ValueError("Game already started.")
    game_cls = get_game_class(room.game_slug)
    if not game_cls:
        raise ValueError(f"Unknown game: {room.game_slug}")
    if len(room.players) < game_cls.MIN_PLAYERS:
        raise ValueError(f"Need at least {game_cls.MIN_PLAYERS} players.")

    players_list = [
        {"player_id": p.player_id, "nickname": p.nickname}
        for p in room.players.values()
    ]
    room.game = game_cls(room.code, players_list, room.host_player_id)
    room.status = "playing"
    return room.game.on_start()

# Helpers

def room_to_dict(room: Room) -> dict:
    from engine.game_registry import get_game_class
    game_cls = get_game_class(room.game_slug)
    return {
        "code": room.code,
        "game_slug": room.game_slug,
        "game_name": game_cls.NAME if game_cls else room.game_slug,
        "status": room.status,
        "host_player_id": room.host_player_id,
        "players": [
            {
                "player_id": p.player_id,
                "nickname": p.nickname,
                "connected": p.connected,
            }
            for p in room.players.values()
        ],
        "min_players": game_cls.MIN_PLAYERS if game_cls else 2,
        "max_players": game_cls.MAX_PLAYERS if game_cls else 2,
    }

DISCONNECT_TIMEOUT = 30  # seconds

def _cleanup_loop():
    while True:
        time.sleep(10)
        now = time.time()
        for room in list(_rooms.values()):
            if room.status != "waiting":
                continue
            for player_id, player in list(room.players.items()):
                if not player.connected and player.disconnected_at and \
                        now - player.disconnected_at > DISCONNECT_TIMEOUT:
                    del room.players[player_id]
            
            if len(room.players) == 0:
                del _rooms[room.code]
                continue

            # Reassign host if needed
            if room.host_player_id not in room.players:
                next_host = next(
                    (p for p in room.players.values() if p.connected), None
                )
                if next_host:
                    room.host_player_id = next_host.player_id

# Start background thread
_cleanup_thread = threading.Thread(target=_cleanup_loop, daemon=True)
_cleanup_thread.start()
