#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv"

mkdir -p \
  "$PROJECT_ROOT/data/raw" \
  "$PROJECT_ROOT/data/processed" \
  "$PROJECT_ROOT/figures" \
  "$PROJECT_ROOT/derivations" \
  "$PROJECT_ROOT/manuscript" \
  "$PROJECT_ROOT/logs"

if [[ ! -d "$VENV_PATH" ]]; then
  python -m venv --system-site-packages "$VENV_PATH"
fi

source "$VENV_PATH/bin/activate"

python "$PROJECT_ROOT/code/env_check.py" || true

cat <<EOF
Project runtime bootstrap complete.

Project root:
  $PROJECT_ROOT

Virtual environment:
  $VENV_PATH

Environment report:
  $PROJECT_ROOT/logs/env_check.json

Current rule:
  Refill raw and processed benchmark data before figure rendering.
EOF
