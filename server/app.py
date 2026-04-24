import os
from flask import Flask, send_from_directory
from flask_socketio import SocketIO

from routes.api import api_bp
from sockets.events import register_socket_events

import games  # noqa — triggers all @register decorators

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

app.register_blueprint(api_bp, url_prefix="/api")
register_socket_events(socketio)

# Catch-all → serve Vue app  (must be last)

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path and os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    
    index = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index):
        return send_from_directory(STATIC_DIR, "index.html")
    
    return "Vue app not built yet. Run: cd client && npm run build", 404


# Entry point

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
