#!/usr/bin/env bash
set -euo pipefail

SRC="/home/nano2/nanoclaw/groups"
DST="/home/nano2/nano_data"

# family system (full PARA)
rsync -a --delete \
  --exclude='.claude-shared.md' \
  --exclude='.claude-fragments/' \
  --exclude='hooks/' \
  "$SRC/family/" "$DST/family/"

# per-agent DM channels
for agent in dm-with-andi dm-with-suse dm-with-felix; do
  mkdir -p "$DST/agents/$agent"
  rsync -a --delete \
    --include='CLAUDE.local.md' \
    --include='*.md' \
    --exclude='CLAUDE.md' \
    --exclude='container.json' \
    --exclude='.claude-shared.md' \
    --exclude='.claude-fragments/' \
    --exclude='hooks/' \
    --exclude='*' \
    "$SRC/$agent/" "$DST/agents/$agent/"
done

cd "$DST"
git add -A
if git diff --cached --quiet; then
  echo "Nothing changed."
else
  git commit -m "backup: $(date -u '+%Y-%m-%d %H:%M') UTC"
  git push origin main
  echo "Pushed."
fi
