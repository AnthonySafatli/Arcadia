from flask import Blueprint, jsonify, request
from engine import game_registry, room_manager

api_bp = Blueprint("api", __name__)

@api_bp.route("/games")
def api_list_games():
    return jsonify(game_registry.list_games())

@api_bp.route("/rooms", methods=["POST"])
def api_create_room():
    """
    Create a new room.
    Body: { game_slug, player_id, nickname }
    Returns: room info
    """
    data = request.get_json(force=True)
    game_slug = data.get("game_slug", "").strip()
    player_id = data.get("player_id", "").strip()
    nickname = data.get("nickname", "").strip()

    if not game_slug or not player_id or not nickname:
        return jsonify({"error": "game_slug, player_id, and nickname are required."}), 400
    if not game_registry.get_game_class(game_slug):
        return jsonify({"error": f"Unknown game: {game_slug}"}), 400
    if len(nickname) > 20:
        return jsonify({"error": "Nickname too long (max 20)."}), 400

    room = room_manager.create_room(game_slug, player_id, nickname)
    return jsonify(room_manager.room_to_dict(room)), 201

@api_bp.route("/rooms/<code>")
def api_get_room(code):
    room = room_manager.get_room(code)
    if not room:
        return jsonify({"error": "Room not found."}), 404
    return jsonify(room_manager.room_to_dict(room))
