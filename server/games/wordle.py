import random
import time

from engine.base_game import BaseGame
from engine.game_registry import register

WORD_LIST = [
    "crane", "slate", "audio", "stare", "raise", "arose", "snare", "least",
    "feast", "beast", "react", "trace", "place", "grace", "space", "brace",
    "plane", "blend", "block", "clock", "clown", "crown", "blown", "brown",
    "drape", "drive", "grove", "grope", "globe", "glove", "grave", "brave",
    "shale", "share", "shame", "shade", "shake", "shape", "shore", "score",
    "store", "stole", "stone", "stove", "spoke", "smoke", "smote", "slope",
    "scope", "spore", "snore", "swore", "those", "chose", "close", "prose",
    "prune", "prone", "prove", "trove", "drove", "drown", "frown", "grown",
    "green", "greed", "greet", "creek", "cheek", "check", "chess", "chest",
    "crest", "press", "dress", "bless", "flesh", "fresh", "trend", "blend",
]

MAX_GUESSES = 6
WORD_LENGTH = 5

@register("wordle")
class Wordle(BaseGame):
    NAME = "Wordle"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 5
    TAGS = ["word game", "competitive"]
    ICON_NAME = "wordle"

    def __init__(self, room_code, players, host_id):
        super().__init__(room_code, players, host_id)
        self._set_initial_state()
        self.scores = {
            player["player_id"]: {"1st": 0, "2nd": 0, "3rd": 0}
            for player in self.players
        }

    def on_start(self) -> callable[str, dict]:
        return self._state

    def on_action(self, player_id: str, action: dict) -> callable[str, dict]:
        """
        Action format:
            { "type": "guess", "word": str }
                — submit a 5-letter guess
            { "type": "end_round" }
                — host ends the round and awards points
            { "type": "next_round" }
                — host starts a new round
            { "type": "reset" }
                — host resets the entire game
        """
        action_type = action.get("type")
        if action_type == "guess":
            return self._handle_guess(player_id, action)
        elif action_type == "next_round":
            return self._handle_next_round(player_id)
        elif action_type == "reset":
            return self._handle_reset(player_id)
        else:
            raise ValueError(f"Unknown action type: {action_type!r}")

    def _handle_guess(self, player_id: str, action: dict) -> callable[str, dict]:
        if self.round_over:
            raise ValueError("Round is over.")

        if player_id in self.finished_players:
            raise ValueError("You have already finished this round.")

        word = action.get("word", "").lower().strip()
        if len(word) != WORD_LENGTH or not word.isalpha():
            raise ValueError(f"Guess must be a {WORD_LENGTH}-letter word.")

        result = self._score_guess(word, self.secret_word)
        guess_time = time.time()

        self.player_guesses[player_id].append({
            "word": word,
            "result": result,
            "time": guess_time,
        })

        solved = all(r == "correct" for r in result)
        exhausted = len(self.player_guesses[player_id]) >= MAX_GUESSES

        if solved or exhausted:
            self.finished_players[player_id] = {
                "solved": solved,
                "guesses": len(self.player_guesses[player_id]),
                "finish_time": guess_time,
            }

            if len(self.finished_players) == len(self.players):
                self.round_over = True
                self._award_points()

        return self._state

    def _handle_next_round(self, player_id: str) -> callable[str, dict]:
        if player_id != self.host_id:
            raise ValueError("Only the host can start the next round.")
        if not self.round_over:
            raise ValueError("Current round is not over yet.")

        self.round += 1
        self._set_initial_state(full_reset=False)
        return self._state

    def _handle_reset(self, player_id: str) -> callable[str, dict]:
        if player_id != self.host_id:
            raise ValueError("Only the host can reset the game.")

        self.scores = {
            player["player_id"]: {"1st": 0, "2nd": 0, "3rd": 0}
            for player in self.players
        }
        self._set_initial_state(full_reset=True)
        return self._state

    def _award_points(self):
        # Only solved players are eligible for placement
        solved = [
            (pid, info)
            for pid, info in self.finished_players.items()
            if info["solved"]
        ]

        # Sort by guesses asc, then finish_time asc as tiebreaker
        solved.sort(key=lambda x: (x[1]["guesses"], x[1]["finish_time"]))

        placements = ["1st", "2nd", "3rd"]
        awarded = []
        prev_guesses = None
        prev_time = None
        place_index = 0

        for pid, info in solved:
            if place_index >= len(placements):
                break

            # Advance place only if not a tie
            if prev_guesses is not None:
                is_tie = (
                    info["guesses"] == prev_guesses
                    and abs(info["finish_time"] - prev_time) < 1.0  # within 1s = tie
                )
                if not is_tie:
                    place_index += 1
                    if place_index >= len(placements):
                        break

            self.scores[pid][placements[place_index]] += 1
            awarded.append(pid)
            prev_guesses = info["guesses"]
            prev_time = info["finish_time"]

    def _score_guess(self, guess: str, secret: str) -> list[str]:
        result = ["absent"] * WORD_LENGTH
        secret_chars = list(secret)
        guess_chars = list(guess)

        # First pass: mark correct
        for i in range(WORD_LENGTH):
            if guess_chars[i] == secret_chars[i]:
                result[i] = "correct"
                secret_chars[i] = None
                guess_chars[i] = None

        # Second pass: mark present
        for i in range(WORD_LENGTH):
            if guess_chars[i] is None:
                continue
            if guess_chars[i] in secret_chars:
                result[i] = "present"
                secret_chars[secret_chars.index(guess_chars[i])] = None

        return result

    def is_over(self) -> str | None:
        return None  # No hard game-over; host resets manually

    def get_state(self, player_id: str) -> dict:
        return self._state(player_id)

    def _set_initial_state(self, full_reset=True):
        self.secret_word = random.choice(WORD_LIST)
        self.round_over = False
        self.finished_players = {}  # player_id -> { solved, guesses, finish_time }
        self.player_guesses = {player["player_id"]: [] for player in self.players}

        if full_reset:
            self.round = 1

    def _tile_pattern(self, player_id: str) -> list[list[str]]:
        """Returns only the colour results (no letters) for a player's guesses."""
        return [g["result"] for g in self.player_guesses[player_id]]

    def _state(self, player_id: str) -> dict:
        return {
            "round": self.round,
            "round_over": self.round_over,
            "secret_word": self.secret_word if self.round_over else None,
            "guesses": self.player_guesses[player_id],  # full detail for self
            "guesses_remaining": MAX_GUESSES - len(self.player_guesses[player_id]),
            "finished": player_id in self.finished_players,
            "finished_info": self.finished_players.get(player_id),
            "scores": self.scores,
            "other_players": {
                p["player_id"]: {
                    "tile_pattern": self._tile_pattern(p["player_id"]),
                    "guesses_used": len(self.player_guesses[p["player_id"]]),
                    "finished": p["player_id"] in self.finished_players,
                    "finished_info": self.finished_players.get(p["player_id"]) if self.round_over else None,
                }
                for p in self.players
                if p["player_id"] != player_id
            },
        }