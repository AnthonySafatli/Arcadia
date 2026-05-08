from flask import request
from flask_socketio import emit, join_room as sio_join_room, leave_room as sio_leave_room

from engine import room_manager

def register_socket_events(socketio_instance):

    @socketio_instance.on("connect")
    def on_connect():
        # Client connects but doesn't join a room yet
        pass

    @socketio_instance.on("disconnect")
    def on_disconnect():
        result = room_manager.player_disconnect(request.sid)
        if not result:
            return
        room, player = result
        
        emit(
            "player_disconnected",
            {
                "player_id": player.player_id,
                "nickname": player.nickname,
                "room": room_manager.room_to_dict(room),
            },
            to=room.code,
        )

    @socketio_instance.on("join_room")
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
            emit("game_state", {"state": room.game.get_state(player_id)})

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

    @socketio_instance.on("start_game")
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
        socketio_instance.emit(
            "game_start",
            {"state": state, "room": room_manager.room_to_dict(room)},
            to=room_code,
        )

    @socketio_instance.on("change_nickname")
    def on_change_nickname(data):
        room_code = (data.get("room_code") or "").strip().upper()
        player_id = (data.get("player_id") or "").strip()
        nickname = (data.get("nickname") or "").strip()

        try:
            player = room_manager.change_nickname(room_code, player_id, nickname)
        except ValueError as e:
            emit("error", {"message": str(e)})
            return

        emit("player_renamed", {
            "player_id": player.player_id,
            "nickname": player.nickname,
        }, to=room_code)

    @socketio_instance.on("action")
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
        
        # Broadcast new state to everyone in the room
        socketio_instance.emit("game_state", {"state": new_state}, to=room_code)

        if winner:
            socketio_instance.emit(
                "game_over",
                {
                    "winner": winner,
                    "room": room_manager.room_to_dict(room),
                },
                to=room_code,
            )
