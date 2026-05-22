from dataclasses import dataclass

@dataclass
class Player:
    player_id: str                  
    nickname: str
    socket_id: str | None = None    
    connected: bool = False
    disconnected_at: float | None = None