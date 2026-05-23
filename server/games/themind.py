import random
from typing import Callable

from engine.base_game import BaseGame
from engine.game_registry import register

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

@register("the-mind")
class TheMind(BaseGame):
    NAME = "The Mind"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 4
    TAGS = ["cooperative", "card game", "telepathy"]
    ICON_NAME = "the-mind"


    def __init__(self, room_code, players, host_id):
        super().__init__(room_code, players, host_id)
        self._set_initial_state()

    def on_start(self) -> Callable[[str], dict]:
        return self._state
    
    def on_action(self, player_id: str, action: dict) -> Callable[[str], dict]:
        """
        Action format:
            { "type": "hover", "state": bool }
                — hover over their card
            { "type": "place" }
                — place their smallest card
            { "type": "throwing_star", "state": bool }  
                — sets vote to place throwing star
            { "type": "focus", "state": bool }
                — sets vote to restart focus
            { "type": "reset" }              
                — restart the game
        """
        action_type = action.get("type")
        if action_type == "hover":
            return self._handle_hover(player_id, action)
        elif action_type == "place":
            return self._handle_place(player_id)
        elif action_type == "next_level":
            return self._handle_next_level(player_id)
        elif action_type == "throwing_star":
            return self._handle_throwing_star(player_id, action)
        elif action_type == "focus":
            return self._handle_focus(player_id, action)
        elif action_type == "reset":
            return self._handle_reset(player_id)
        else:
            raise ValueError(f"Unknown action type: {action_type!r}")

    def _handle_hover(self, player_id: str, action: dict) -> Callable[[str], dict]:
        if self.is_over():
            raise ValueError("Game is over")
        
        state = bool(action.get("state"))
        if state is None or type(state) is not bool:
            raise ValueError("Invalid action.")
        
        self.is_hovering[player_id] = state
        return self._state

    def _handle_place(self, player_id: str) -> Callable[[str], dict]:
        if self.is_over():
            raise ValueError("Game is over")
        
        if len(self.player_hands[player_id]) == 0:
            raise ValueError("You have no cards in your hand.")

        self.placed.sort()

        lowest_card = min(self.player_hands[player_id])
        self.player_hands[player_id].remove(lowest_card)

        self.placed.append(lowest_card)

        all_hands = [
            card
            for hand in self.player_hands.values()
            for card in hand
        ]

        discarded_cards = [
            card for card in all_hands
            if card < lowest_card
        ]

        if discarded_cards:
            self.lives -= 1
            self.discarded.extend(discarded_cards)
            self.player_hands = {
                p: [
                    card for card in hand
                    if card > lowest_card
                ]
                for p, hand in self.player_hands.items()
            }

        return self._state
    
    def _handle_next_level(self, player_id: str):
        if self.is_over():
            raise ValueError("Game is over")
        
        if player_id != self.host_id:
            raise ValueError("Only the host can move to the next level.")
        
        reward = REWARDS.get(self.level)
        if reward == "ts":
            self.throwing_stars = min(self.throwing_stars + 1, MAX_THROWING_STARS)
        elif reward == "l":
            self.lives = min(self.lives + 1, MAX_LIVES)

        self.level += 1
        self._set_initial_state(full_reset=False, level=self.level)

        return self._state
    
    def _handle_throwing_star(self, player_id: str, action: dict) -> Callable[[str], dict]:
        if self.is_over():
            raise ValueError("Game is over")
        
        state = bool(action.get("state"))
        if state is None or type(state) is not bool:
            raise ValueError("Invalid action.")
        
        self.wants_throwing_star[player_id] = state
        if all(ts == True for ts in self.wants_throwing_star.values()):
            for player in self.players:
                id = player["player_id"]

                if len(self.player_hands[id]) == 0:
                    continue

                lowest_card = min(self.player_hands[id])
                self.player_hands[id].remove(lowest_card)
                self.placed.append(lowest_card)

            self.placed.sort()
            self.wants_throwing_star = {player["player_id"]: False for player in self.players}            

        return self._state

    def _handle_focus(self, player_id: str, action: dict) -> Callable[[str], dict]:
        if self.is_over():
            raise ValueError("Game is over")
        
        state = bool(action.get("state"))
        if state is None or type(state) is not bool:
            raise ValueError("Invalid action.")
        
        self.wants_focus[player_id] = state
        if all(f == True for f in self.wants_focus.values()):
            self.wants_focus = {p: False for p in self.wants_focus}
        
        return self._state

    def _handle_reset(self, player_id: str) -> Callable[[str], dict]:
        if player_id != self.host_id:
            raise ValueError("Only the host can reset the game.")
        
        self._set_initial_state()
        return self._state

    def is_over(self) -> str | None:
        max_level = MAX_LEVEL[len(self.players)]
        if max_level == self.level:
            if all(len(hand) == 0 for hand in self.player_hands.values()):
                return "win"
        if self.lives == 0:
            return "loss"
        return None
    
    def get_state(self, player_id):
        return self._state(player_id)

    def _pick_card_from_deck(self) -> int:
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def _set_initial_state(self, full_reset=True, level=1):
        self.deck = [i+1 for i in range(100)]
        self.placed = []
        self.discarded = []
        self.level = level

        self.player_hands = {
            player["player_id"]: [self._pick_card_from_deck() for _ in range(level)]
            for player in self.players
        }

        if full_reset:
            self.lives = len(self.players)
            self.throwing_stars = 1

            self.is_hovering = {player["player_id"]: False for player in self.players}
            self.wants_throwing_star = {player["player_id"]: False for player in self.players}
            self.wants_focus = {player["player_id"]: False for player in self.players}

    def _state(self, player_id: str) -> dict:
        return {
            "hand": self.player_hands[player_id],
            "placed": self.placed,
            "discarded": self.discarded,
            "level": self.level,
            "lives": self.lives,
            "throwing_stars": self.throwing_stars,
            "player_hands": {k: len(v) for k, v in self.player_hands.items()},
            "player_hovering": self.is_hovering,
            "player_throwing_stars": self.wants_throwing_star,
            "player_focus": self.wants_focus
        }