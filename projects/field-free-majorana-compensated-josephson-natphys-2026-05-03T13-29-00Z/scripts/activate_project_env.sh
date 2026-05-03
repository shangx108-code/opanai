#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
source "${PROJECT_ROOT}/.venv-system/bin/activate"
export PROJECT_ROOT
export PYTHONPATH="${PROJECT_ROOT}:${PYTHONPATH:-}"

echo "Activated project environment at ${PROJECT_ROOT}"
