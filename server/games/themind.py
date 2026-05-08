import random

from engine.base_game import BaseGame
from engine.game_registry import register

@register("the-mind")
class TheMind(BaseGame):
    NAME = "The Mind"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 4
    TAGS = ["thinking", "difficult", "telepathy"]

    MAX_LEVEL = {
        2: 8,
        3: 10,
        4: 12
    }
    MAX_LIVES = 5
    MAX_THROWING_STARS = 3
    REWARDS = {
        2: "l",
        3: "ts",
        5: "l",
        6: "ts",
        8: "l",
        9: "ts",
    }

    def __init__(self, room_code, players, host_id):
        super().__init__(room_code, players, host_id)
        self._set_initial_state()

    def on_start(self) -> dict:
        return self._state()
    
    def on_action(self, player_id: str, action: dict) -> dict:
        """
        Action format:
            { "type": "hover" }
                — hover over their card
            { "type": "place" }
                — place their smallest card
            { "type": "throwing_star" }  
                — toggles votes to place throwing star
            { "type": "focus" }
                — toggles votes to restart focus
        """

    def _handle_hover(self, player_id: str) -> dict:
        pass

    def _handle_place(self, player_id: str) -> dict:
        pass

    def _handle_throwing_star(self, player_id: str) -> dict:
        pass

    def _handle_focus(self, player_id: str) -> dict:
        pass

    def is_over(self) -> str | None:
        return None
    
    def get_state(self, player_id):
        return self._state(player_id)

    def _pick_card_from_deck(self) -> int:
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def _set_initial_state(self):
        self.deck = [i+1 for i in range(100)]
        self.level = 1
        self.lives = len(self.players)
        self.throwing_stars = 1

        self.player_decks = {player["player_id"]: self._pick_card_from_deck() for player in self.players}
        self.is_hovering = {player["player_id"]: False for player in self.players}
        self.wants_throwing_star = {player["player_id"]: False for player in self.players}
        self.wants_focus = {player["player_id"]: False for player in self.players}

    def _state(self, player_id: str) -> dict:
        pass