#!/usr/bin/env bash
# Watches nanoclaw group folders for file changes and triggers backup.
# Debounces: waits 10s of quiet after the last change before running.
set -euo pipefail

WATCH_DIR="/home/nano2/nanoclaw/groups"
BACKUP_SCRIPT="/home/nano2/nano_data/scripts/backup.sh"
DEBOUNCE=10  # seconds to wait after last change

echo "[watch-and-backup] Starting. Watching $WATCH_DIR"

pending=false
last_change=0

inotifywait -m -r -q \
  --exclude '(\.claude-shared|\.claude-fragments|hooks|\.heartbeat|\.db-shm|\.db-wal|conversations)' \
  -e close_write,create,delete,move \
  "$WATCH_DIR" |
while read -r _dir _event _file; do
  last_change=$(date +%s)
  if ! $pending; then
    pending=true
    (
      while true; do
        sleep 1
        now=$(date +%s)
        elapsed=$(( now - last_change ))
        if (( elapsed >= DEBOUNCE )); then
          echo "[watch-and-backup] Change detected — running backup"
          bash "$BACKUP_SCRIPT" && echo "[watch-and-backup] Done." || echo "[watch-and-backup] Backup failed."
          pending=false
          exit 0
        fi
      done
    ) &
  fi
done
