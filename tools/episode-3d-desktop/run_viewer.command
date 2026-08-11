#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
cd "$ROOT_DIR"

if [ -x "$ROOT_DIR/.venv/bin/python" ]; then
  exec "$ROOT_DIR/.venv/bin/python" scripts/episode_3d_desktop.py "$@"
fi

exec python3 scripts/episode_3d_desktop.py "$@"
