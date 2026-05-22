from server.engine.base_game import BaseGame

_registry: dict[str, type[BaseGame]] = {}

def register(slug: str):
    """Decorator to register a game class under a slug."""
    def decorator(cls: type[BaseGame]):
        _registry[slug] = cls
        return cls
    return decorator

def get_game_class(slug: str) -> type[BaseGame] | None:
    return _registry.get(slug)

def list_games() -> list[dict]:
    """Return metadata for all registered games (for the lobby)."""
    return [
        {
            "slug": slug,
            "name": cls.NAME,
            "icon_name": cls.ICON_NAME,
            "min_players": cls.MIN_PLAYERS,
            "max_players": cls.MAX_PLAYERS,
            "tags": cls.TAGS
        }
        for slug, cls in _registry.items()
    ]