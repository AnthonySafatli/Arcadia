import os
from flask import Flask, send_from_directory, jsonify, request
from flask_socketio import SocketIO, join_room as sio_join_room, leave_room as sio_leave_room, emit

import games  # noqa — triggers all @register decorators
from engine import game_registry, room_manager

# App setup

BASE_DIR = os.path.dirname(__file__)
STATIC_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path="/")
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-change-me")

socketio = SocketIO(
    app,
    cors_allowed_origins="*",   # tighten in production
    async_mode="gevent",
)

# REST API  (/api/...)

@app.route("/api/games")
def api_list_games():
    """All available game types."""
    return jsonify(game_registry.list_games())


@app.route("/api/rooms", methods=["POST"])
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


@app.route("/api/rooms/<code>")
def api_get_room(code):
    room = room_manager.get_room(code)
    if not room:
        return jsonify({"error": "Room not found."}), 404
    return jsonify(room_manager.room_to_dict(room))


# Catch-all → serve Vue app  (must be last)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    # Serve real static files (js, css, assets) if they exist
    if path and os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    # Everything else → index.html (Vue router handles it)
    index = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index):
        return send_from_directory(STATIC_DIR, "index.html")
    return "Vue app not built yet. Run: cd client && npm run build", 404


# WebSocket events

@socketio.on("connect")
def on_connect():
    # Client connects but doesn't join a room yet
    pass


@socketio.on("disconnect")
def on_disconnect():
    result = room_manager.player_disconnect(request.sid)
    if not result:
        return
    room, player = result
    # Notify others in the room
    emit(
        "player_disconnected",
        {
            "player_id": player.player_id,
            "nickname": player.nickname,
            "room": room_manager.room_to_dict(room),
        },
        to=room.code,
    )


@socketio.on("join_room")
def on_join_room(data):
    """
    Client sends: { room_code, player_id, nickname }
    player_id is a UUID the client generates and persists in localStorage.
    On reconnect, the same player_id re-identifies the player.
    """
    room_code = (data.get("room_code") or "").strip().upper()
    player_id = (data.get("player_id") or "").strip()
    nickname = (data.get("nickname") or "").strip()

    if not room_code or not player_id or not nickname:
        emit("error", {"message": "room_code, player_id, and nickname are required."})
        return

    try:
        room, player, is_reconnect = room_manager.join_room(room_code, player_id, nickname, request.sid)
    except ValueError as e:
        emit("error", {"message": str(e)})
        return

    sio_join_room(room_code)  # subscribe this socket to the room channel

    # Confirm to the joining client
    emit("joined", {
        "is_reconnect": is_reconnect,
        "player_id": player.player_id,
        "room": room_manager.room_to_dict(room),
    })

    # If reconnecting mid-game, send current game state to them specifically
    if is_reconnect and room.status == "playing" and room.game:
        emit("game_state", room.game.get_state(player_id))

    # Notify everyone else
    emit(
        "player_joined" if not is_reconnect else "player_reconnected",
        {
            "player_id": player.player_id,
            "nickname": player.nickname,
            "room": room_manager.room_to_dict(room),
        },
        to=room_code,
        include_self=False,
    )


@socketio.on("start_game")
def on_start_game(data):
    """Only the host can start the game."""
    room_code = (data.get("room_code") or "").strip().upper()
    player_id = (data.get("player_id") or "").strip()

    room = room_manager.get_room(room_code)
    if not room:
        emit("error", {"message": "Room not found."})
        return
    if room.host_player_id != player_id:
        emit("error", {"message": "Only the host can start the game."})
        return

    try:
        state = room_manager.start_game(room)
    except ValueError as e:
        emit("error", {"message": str(e)})
        return

    # Broadcast game_start to everyone in the room
    socketio.emit(
        "game_start",
        {"state": state, "room": room_manager.room_to_dict(room)},
        to=room_code,
    )


@socketio.on("action")
def on_action(data):
    """
    Client sends: { room_code, player_id, action: { ... game-specific ... } }
    """
    room_code = (data.get("room_code") or "").strip().upper()
    player_id = (data.get("player_id") or "").strip()
    action = data.get("action", {})

    room = room_manager.get_room(room_code)
    if not room:
        emit("error", {"message": "Room not found."})
        return
    if room.status != "playing" or not room.game:
        emit("error", {"message": "Game is not in progress."})
        return
    if player_id not in room.players:
        emit("error", {"message": "You are not in this room."})
        return

    try:
        new_state = room.game.on_action(player_id, action)
    except ValueError as e:
        emit("error", {"message": str(e)})
        return

    winner = room.game.is_over()
    if winner:
        room.status = "finished"

    # Broadcast new state to everyone in the room
    socketio.emit("game_state", {"state": new_state}, to=room_code)

    if winner:
        socketio.emit(
            "game_over",
            {
                "winner": winner,
                "room": room_manager.room_to_dict(room),
            },
            to=room_code,
        )


# Entry point

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)