#!/usr/bin/env bash
set -euo pipefail
SRC="/home/ing/RICK/RICK_LIVE_CLEAN"
DST="/home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI"
DOCS="$DST/docs"
LOGS="$DST/logs"
mkdir -p "$DOCS" "$LOGS"

# Always source CLEAN first if present
if [[ -d "$SRC" ]]; then
  echo "[audit] CLEAN first: $SRC → $DST"
  rsync -a --ignore-existing "$SRC/"/ "$DST/"/
else
  echo "[audit] CLEAN source not found ($SRC) — skipping sync (pack remains self-contained)"
fi

# Build index
INDEX_JSON="$DOCS/files_index.json"
tmp=$(mktemp)
echo "[" >"$tmp"; first=1
while IFS= read -r -d '' f; do
  sz=$(stat -c '%s' "$f"); mt=$(date -u -d @"$(stat -c '%Y' "$f")" '+%Y-%m-%dT%H:%M:%SZ'); sh=$(sha256sum "$f" | awk '{print $1}')
  row=$(jq -n --arg p "${f#$DST/}" --arg sz "$sz" --arg mt "$mt" --arg sh "$sh" '{path:$p,size:($sz|tonumber),mtime:$mt,sha256:$sh}')
  if [[ $first -eq 1 ]]; then echo "  $row" >>"$tmp"; first=0; else echo " ,$row" >>"$tmp"; fi
done < <(find "$DST" -type f -print0)
echo "]" >>"$tmp"
mv "$tmp" "$INDEX_JSON"
chmod 444 "$INDEX_JSON" || true

echo "[audit] index at $INDEX_JSON"
if command -v jq >/dev/null 2>&1; then
  jq 'length' "$INDEX_JSON" || true
else
  echo "(jq not installed; index length not shown)"
fi
