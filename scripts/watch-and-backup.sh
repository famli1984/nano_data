#!/usr/bin/env bash
# Watches nanoclaw group folders for file changes and triggers backup.
# Uses a flag file for debounce so the state is shared between processes.
set -euo pipefail

WATCH_DIR="/home/nano2/nanoclaw/groups"
BACKUP_SCRIPT="/home/nano2/nano_data/scripts/backup.sh"
DEBOUNCE=10  # seconds of quiet before backup fires
FLAG="/tmp/nanoclaw-backup-pending"

rm -f "$FLAG"
echo "[watch-and-backup] Starting. Watching $WATCH_DIR"

# Write current timestamp to flag file on every relevant change
inotifywait -m -r -q \
  --exclude '(\.claude-shared|\.claude-fragments|hooks|\.heartbeat|\.db-shm|\.db-wal|conversations)' \
  -e close_write,create,delete,move \
  "$WATCH_DIR" | while read -r _line; do
    date +%s > "$FLAG"
  done &

# Poll the flag every 2s; once it's DEBOUNCE seconds old, run backup
while true; do
  sleep 2
  [ -f "$FLAG" ] || continue
  trigger=$(cat "$FLAG")
  now=$(date +%s)
  if (( now - trigger >= DEBOUNCE )); then
    rm -f "$FLAG"
    echo "[watch-and-backup] Change detected — running backup"
    bash "$BACKUP_SCRIPT" && echo "[watch-and-backup] Done." || echo "[watch-and-backup] Backup failed."
  fi
done
