from engine.base_game import BaseGame
from engine.game_registry import register

@register("the-mind")
class TheMind(BaseGame):
    NAME = "The Mind"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 5
    TAGS = ["Thinking", "Difficult"]

    def __init__(self, room_code, players, host_id):
        super().__init__(room_code, players, host_id)

    def on_start(self) -> dict:
        return self._state()
    
    def on_action(self, player_id: str, action: dict) -> dict:
        """
        Action format:

        """

    def is_over(self) -> str | None:
        return None
    
    def get_state(self, player_id):
        return self._state()

    def _state(self) -> dict:
        pass