#!/usr/bin/env bash
set -euo pipefail

SRC="/home/nano2/nanoclaw/groups"
DST="/home/nano2/nano_data"

# familypara — full live PARA, exclude only generated/runtime files
rsync -a --delete \
  --exclude='.claude-shared.md' \
  --exclude='.claude-fragments/' \
  --exclude='hooks/' \
  --exclude='container.json' \
  "$SRC/familypara/" "$DST/familypara/"

# all agent groups — only markdown content, never credentials
# container.json is excluded (contains passwords), CLAUDE.md is generated at spawn
for group in \
  dm-with-andi \
  dm-with-suse \
  dm-with-felix \
  dm-with-nano2 \
  cli-with-andi \
  cli-with-nano2 \
  hausmeister \
  tony-andi; do
  [ -d "$SRC/$group" ] || continue
  mkdir -p "$DST/agents/$group"
  rsync -a --delete \
    --exclude='CLAUDE.md' \
    --exclude='container.json' \
    --exclude='.claude-shared.md' \
    --exclude='.claude-fragments/' \
    --exclude='hooks/' \
    --include='CLAUDE.local.md' \
    --include='*/' \
    --include='*.md' \
    --exclude='*' \
    "$SRC/$group/" "$DST/agents/$group/"
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
