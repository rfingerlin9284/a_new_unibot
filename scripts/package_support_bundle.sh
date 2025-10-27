#!/usr/bin/env bash
# Package a sanitized support bundle with logs and code/config references.
# Output: support_upload_YYYYMMDD_HHMMSS/{logs.zip, code_config.zip}
# Usage: scripts/package_support_bundle.sh [output_dir]

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

TS="$(date +%Y%m%d_%H%M%S)"
OUT_DIR="${1:-support_upload_${TS}}"
STAGE_DIR="$OUT_DIR/.stage"
LOG_STAGE="$STAGE_DIR/logs"
CODE_STAGE="$STAGE_DIR/code_config"

mkdir -p "$OUT_DIR" "$STAGE_DIR" "$LOG_STAGE" "$CODE_STAGE"

echo "==> Creating support bundle in: $OUT_DIR"

# 1) Collect and trim logs
LOG_PRIMARY="logs/narration.jsonl"
LOG_ALT="narration.jsonl"

if [[ -f "$LOG_PRIMARY" ]]; then
  echo "-> Found $LOG_PRIMARY"
  # Tail to keep size reasonable
  tail -n 20000 "$LOG_PRIMARY" > "$LOG_STAGE/narration_tail.jsonl" || true
elif [[ -f "$LOG_ALT" ]]; then
  echo "-> Found $LOG_ALT"
  tail -n 20000 "$LOG_ALT" > "$LOG_STAGE/narration_tail.jsonl" || true
else
  echo "-> No narration.jsonl found; creating placeholder"
  echo "{}" > "$LOG_STAGE/narration_tail.jsonl"
fi

# Copy logs under logs/ with caps: *.log (last 5000 lines), *.json and *.jsonl (last 20000 lines)
if [[ -d logs ]]; then
  # .log tails
  mapfile -t LOGFILES < <(find logs -maxdepth 1 -type f -name "*.log" 2>/dev/null || true)
  for lf in "${LOGFILES[@]}"; do
    bn="$(basename "$lf")"
    echo "-> Adding $bn (last 5000 lines)"
    tail -n 5000 "$lf" > "$LOG_STAGE/${bn%.log}_tail.log" || true
  done
  # .json tails
  mapfile -t JSONFILES < <(find logs -maxdepth 1 -type f -name "*.json" 2>/dev/null || true)
  for jf in "${JSONFILES[@]}"; do
    bn="$(basename "$jf")"
    echo "-> Adding $bn (last 20000 lines)"
    tail -n 20000 "$jf" > "$LOG_STAGE/${bn%.json}_tail.json" || true
  done
  # .jsonl tails
  mapfile -t JSONLFILES < <(find logs -maxdepth 1 -type f -name "*.jsonl" 2>/dev/null || true)
  for jl in "${JSONLFILES[@]}"; do
    bn="$(basename "$jl")"
    echo "-> Adding $bn (last 20000 lines)"
    tail -n 20000 "$jl" > "$LOG_STAGE/${bn%.jsonl}_tail.jsonl" || true
  done
fi

# 2) Sanitize env files (.env, .env.autonomous) and include minimal configs
sanitize_env() {
  local src="$1" dst="$2"
  # Redact common secrets: TOKEN, SECRET, KEY, PASS, ACCOUNT, ID
  sed -E 's/^([A-Za-z0-9_]*(TOKEN|SECRET|KEY|PASS|ACCOUNT|ID)[A-Za-z0-9_]*)=.*/\1=REDACTED/g' "$src" > "$dst"
}

if [[ -f .env ]]; then
  echo "-> Sanitizing .env"
  sanitize_env .env "$CODE_STAGE/.env.sanitized"
fi
if [[ -f .env.autonomous ]]; then
  echo "-> Sanitizing .env.autonomous"
  sanitize_env .env.autonomous "$CODE_STAGE/.env.autonomous.sanitized"
fi

# Include VS Code config for reproducibility
if [[ -d .vscode ]]; then
  mkdir -p "$CODE_STAGE/.vscode"
  cp -f .vscode/tasks.json "$CODE_STAGE/.vscode/" 2>/dev/null || true
  cp -f .vscode/settings.json "$CODE_STAGE/.vscode/" 2>/dev/null || true
fi

# Include key engine and tooling files (paths exist check)
copy_if_exists() { for f in "$@"; do [[ -e "$f" ]] && install -D "$f" "$CODE_STAGE/$f" 2>/dev/null || true; done; }

copy_if_exists \
  autonomous_decision_engine.py \
  rick_charter.py \
  start_paper_trading_mega.sh \
  app/run_paper.py

# Include selected directories while excluding heavy/temp content
copy_tree_if_exists() {
  local d
  for d in "$@"; do
    if [[ -d "$d" ]]; then
      rsync -a --prune-empty-dirs \
        --exclude "__pycache__/" \
        --exclude ".venv*/" \
        --exclude "node_modules/" \
        --exclude "data/" \
        --exclude "backtesting/" \
        --exclude "snapshots/" \
        --exclude "*.pyc" \
        "$d" "$CODE_STAGE/"
    fi
  done
}

copy_tree_if_exists util hive wolf_packs foundation tools scripts configs config

# 3) Create zip artifacts
pushd "$STAGE_DIR" >/dev/null
  zip -rq9 ../logs.zip logs
  zip -rq9 ../code_config.zip code_config
popd >/dev/null

echo "✅ Support bundle created:"
echo "   $OUT_DIR/logs.zip"
echo "   $OUT_DIR/code_config.zip"
echo "Done."
