#!/usr/bin/env bash
set -euo pipefail

REPO="/home/nano2/nano_data"
LIVE="/home/nano2/nanoclaw/groups/familypara"
LOG="$REPO/sync.log"

cd "$REPO"

BEFORE=$(git rev-parse HEAD)

# Pull from GitHub; if there's a conflict, log and bail
if ! git pull --no-rebase origin main >> "$LOG" 2>&1; then
  echo "$(date -u '+%Y-%m-%d %H:%M') UTC [pull_and_sync] ERROR: git pull failed (conflict needs manual resolution)" >> "$LOG"
  exit 1
fi

AFTER=$(git rev-parse HEAD)

if [ "$BEFORE" = "$AFTER" ]; then
  echo "$(date -u '+%Y-%m-%d %H:%M') UTC [pull_and_sync] No remote changes." >> "$LOG"
  exit 0
fi

# Only rsync if familypara actually changed in this pull
if git diff --name-only "$BEFORE" "$AFTER" | grep -q '^familypara/'; then
  echo "$(date -u '+%Y-%m-%d %H:%M') UTC [pull_and_sync] familypara changed — syncing to live..." >> "$LOG"
  rsync -a \
    --exclude='container.json' \
    --exclude='.claude-shared.md' \
    --exclude='.claude-fragments/' \
    --exclude='hooks/' \
    "$REPO/familypara/" "$LIVE/"
  echo "$(date -u '+%Y-%m-%d %H:%M') UTC [pull_and_sync] Done." >> "$LOG"
else
  echo "$(date -u '+%Y-%m-%d %H:%M') UTC [pull_and_sync] Pulled (no familypara changes)." >> "$LOG"
fi
