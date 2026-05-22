from dataclasses import dataclass, field
import time
import random
import string

from server.models.player import Player
from server.engine.base_game import BaseGame

@dataclass
class Room:
    code: str
    game_slug: str
    host_player_id: str
    status: str = "waiting"   # waiting | playing | finished
    players: dict[str, Player] = field(default_factory=dict)  # player_id → Player
    game: BaseGame | None = None
    created_at: float = field(default_factory=time.time)

    def generate_code(rooms: dict[str, "Room"]) -> str:
        chars = string.ascii_uppercase + string.digits
        while True:
            code = "".join(random.choices(chars, k=6))
            if code not in rooms:
                return code
