import random
import string
import time
from dataclasses import dataclass, field
from engine.base_game import BaseGame

# TODO: No room cleanup, remove stale rooms
# TODO: Host reassignment logic for when host leaves

# How long (seconds) a disconnected player has to reconnect before being removed
RECONNECT_GRACE_PERIOD = 60

@dataclass
class Player:
    player_id: str                  # Persistent token stored in browser (localStorage)
    nickname: str
    socket_id: str | None = None    # Current socket connection (changes on reconnect)
    connected: bool = False
    disconnected_at: float | None = None

@dataclass
class Room:
    code: str
    game_slug: str
    host_player_id: str
    status: str = "waiting"   # waiting | playing | finished
    players: dict[str, Player] = field(default_factory=dict)  # player_id → Player
    game: BaseGame | None = None
    created_at: float = field(default_factory=time.time)

# In-memory store. Replace with Redis for multi-process deployments.
# TODO: Replace with not in-memory dict
_rooms: dict[str, Room] = {}
# socket_id → player_id (for fast lookup on disconnect)
_socket_to_player: dict[str, tuple[str, str]] = {}  # socket_id → (room_code, player_id)

# Room lifecycle

def generate_code() -> str:
    chars = string.ascii_uppercase + string.digits
    while True:
        code = "".join(random.choices(chars, k=6))
        if code not in _rooms:
            return code

def create_room(game_slug: str, host_player_id: str, host_nickname: str) -> Room:
    code = generate_code()
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

    from engine.game_registry import get_game_class
    game_cls = get_game_class(room.game_slug)

    is_reconnect = player_id in room.players

    if is_reconnect:
        player = room.players[player_id]
        player.socket_id = socket_id
        player.connected = True
        player.disconnected_at = None
    else:
        if room.status == "playing":
            raise ValueError("Game already in progress.")
        if game_cls and len(room.players) >= game_cls.MAX_PLAYERS:
            raise ValueError("Room is full.")
        player = Player(player_id=player_id, nickname=nickname, socket_id=socket_id, connected=True)
        room.players[player_id] = player

    _socket_to_player[socket_id] = (room.code, player_id)
    return room, player, is_reconnect

def player_disconnect(socket_id: str) -> tuple[Room, Player] | None:
    """Called when a socket disconnects. Marks player as disconnected."""
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
    return room, player


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
    room.game = game_cls(room.code, players_list)
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