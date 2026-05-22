from abc import ABC, abstractmethod
from typing import Callable

class BaseGame(ABC):
    MIN_PLAYERS: int = 1
    MAX_PLAYERS: int = 1
    NAME: str = "The Game"
    TAGS: list[str] = []
    ICON_NAME: str = "base-game"

    def __init__(self, room_code: str, players: list[dict], host_id: str):
        self.room_code = room_code
        self.players = players  # ordered list
        self.host_id = host_id

    @abstractmethod
    def on_start(self) -> Callable[[str], dict]:
        """Return the initial game state broadcast to all players."""

    @abstractmethod
    def on_action(self, player_id: str, action: dict) -> Callable[[str], dict]:
        """
        Handle a player action. Mutate internal state, return new state.
        Raise ValueError with a message if the action is invalid.
        """

    @abstractmethod
    def is_over(self) -> str | None:
        """Return winning player_id, 'draw', or None if game is still going."""

    @abstractmethod
    def get_state(self, player_id: str) -> Callable[[str], dict]:
        """Return current state of the game"""

    @property
    def player_ids(self) -> list[str]:
        return [p["player_id"] for p in self.players]