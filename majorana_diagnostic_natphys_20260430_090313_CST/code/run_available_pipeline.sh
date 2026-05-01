#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")"/.. && pwd)"
LOG_FILE="$PROJECT_ROOT/logs/pipeline_run_$(TZ=Asia/Shanghai date '+%Y%m%d_%H%M%S_CST').log"

{
  echo "Pipeline start: $(TZ=Asia/Shanghai date '+%F %T %Z')"
  echo "Project root: $PROJECT_ROOT"

  "$PROJECT_ROOT/code/bootstrap_runtime.sh"

  source "$PROJECT_ROOT/.venv/bin/activate"
  python "$PROJECT_ROOT/code/build_benchmark_inventory.py"
  python "$PROJECT_ROOT/code/build_three_terminal_batch1_stubs.py"

  echo "Generated files:"
  find "$PROJECT_ROOT/data" -maxdepth 3 -type f | sort
  echo "Pipeline end: $(TZ=Asia/Shanghai date '+%F %T %Z')"
} | tee "$LOG_FILE"
