#!/usr/bin/env bash

set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PYTHON_BIN="python3.14"

cleanup() {
  echo ""
  echo "Stopping Flask server..."
  kill "$FLASK_PID" 2>/dev/null || true
}

trap cleanup EXIT

echo "==> Checking for Python 3.14"
if ! command -v $PYTHON_BIN >/dev/null 2>&1; then
  echo "Error: Python 3.14 is not installed or not in PATH"
  exit 1
fi

echo "==> Creating virtual environment"
$PYTHON_BIN -m venv "$VENV_DIR"

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "==> Upgrading pip"
pip install --upgrade pip

if [ -f "$ROOT_DIR/requirements.txt" ]; then
  echo "==> Installing server requirements"
  pip install -r "$ROOT_DIR/server/requirements.txt"
else
  echo "Error: requirements.txt not found at server/requirements.txt"
  exit 1
fi

if [ -f "$ROOT_DIR/client/package.json" ]; then
  echo "==> Installing frontend dependencies"
  cd "$ROOT_DIR/client"
  npm install
  npm run build

  cd "$ROOT_DIR"
else
  echo "Error: package.json not found in client/"
  exit 1
fi

echo "==> Starting Flask server"
cd "$ROOT_DIR/server"
"$VENV_DIR/bin/python" app.py &
FLASK_PID=$!

wait "$FLASK_PID"