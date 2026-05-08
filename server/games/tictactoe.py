import random

from engine.base_game import BaseGame
from engine.game_registry import register

@register("tictactoe")
class TicTacToe(BaseGame):
    NAME = "Tic Tac Toe"
    MIN_PLAYERS = 2
    MAX_PLAYERS = 2

    def __init__(self, room_code, players, host_id):
        super().__init__(room_code, players, host_id)
        self._set_initial_state()
        self.scores = {
            self.players[0]["player_id"]: 0,
            self.players[1]["player_id"]: 0,
        }

    def on_start(self) -> dict:
        return self._state()

    def on_action(self, player_id: str, action: dict) -> dict:
        """
        Action format:
            {"type": "cell", "cell": int}  
                — place a mark (0-8)
            {"type": "reset"}              
                — reset board (host only, game must be over)
        """
        action_type = action.get("type")
        if action_type == "reset":
            return self._handle_reset(player_id)
        elif action_type == "cell":
            return self._handle_cell(player_id, action)
        else:
            raise ValueError(f"Unknown action type: {action_type!r}")

    def _handle_cell(self, player_id: str, action: dict) -> dict:
        if self.winner:
            raise ValueError("Game is already over.")
        if player_id != self.current_turn:
            raise ValueError("Not your turn.")
        cell = action.get("cell")
        if cell is None or not (0 <= cell <= 8):
            raise ValueError("Invalid cell.")
        if self.board[cell] is not None:
            raise ValueError("Cell already taken.")

        self.board[cell] = player_id
        self.winner = self._check_winner()

        if self.winner and self.winner != "draw":
            self.scores[self.winner] += 1

        if not self.winner:
            other = [p for p in self.player_ids if p != player_id]
            self.current_turn = other[0] if other else player_id

        return self._state()

    def _handle_reset(self, player_id: str) -> dict:
        if player_id != self.host_id:
            raise ValueError("Only the host can reset the game.")
        if not self.winner:
            raise ValueError("Game is not over yet.")
        self._set_initial_state()
        return self._state()

    def is_over(self) -> str | None:
        return self.winner

    def get_state(self, player_id):
        return self._state()

    def _check_winner(self) -> str | None:
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in wins:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        if all(c is not None for c in self.board):
            return "draw"
        return None

    def _set_initial_state(self):
        self.board = [None] * 9
        self.current_turn = random.choice(self.players)["player_id"]
        self.winner = None
        self.marks = {
            self.players[0]["player_id"]: "X",
            self.players[1]["player_id"]: "O",
        }

    def _state(self) -> dict:
        return {
            "board": self.board,
            "current_turn": self.current_turn,
            "marks": self.marks,
            "winner": self.winner,
            "scores": self.scores,
        }