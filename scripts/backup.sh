#!/usr/bin/env bash
# Sync personalization data from nanoclaw into nano_data and push to GitHub.
# Run from anywhere; paths are relative to the nanoclaw install.

set -euo pipefail

NANOCLAW_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
NANO_DATA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$NANOCLAW_DIR/nanoclaw/groups"

echo "Syncing from $SRC → $NANO_DATA_DIR"

# family system (full PARA)
rsync -a --delete \
  --exclude='.claude-shared.md' \
  --exclude='.claude-fragments/' \
  --exclude='hooks/' \
  "$SRC/family/" "$NANO_DATA_DIR/family/"

# per-agent DM channels (persona + data files only)
for agent in dm-with-andi dm-with-suse dm-with-felix; do
  mkdir -p "$NANO_DATA_DIR/agents/$agent"
  rsync -a --delete \
    --include='CLAUDE.local.md' \
    --include='*.md' \
    --exclude='CLAUDE.md' \
    --exclude='container.json' \
    --exclude='.claude-shared.md' \
    --exclude='.claude-fragments/' \
    --exclude='hooks/' \
    --exclude='*' \
    "$SRC/$agent/" "$NANO_DATA_DIR/agents/$agent/"
done

cd "$NANO_DATA_DIR"
git add -A
if git diff --cached --quiet; then
  echo "Nothing changed — no commit needed."
else
  git commit -m "backup: $(date -u '+%Y-%m-%d %H:%M') UTC"
  git push origin main
  echo "Pushed."
fi
