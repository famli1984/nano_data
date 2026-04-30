# nano_data

Personalization and data backup for the NanoClaw family assistant system.

## Contents

### `family/`
The full family assistant system (PARA structure):
- `Agents/` — EA and support agent definitions (Quatschkopf, Fabio, Pauline, …)
- `Areas/` — Ongoing areas: family calendar, todos, finances, house, school, garden, vehicles
- `Projects/` — Active projects with deadlines
- `Resources/` — Reference material, checklists, templates
- `Archives/` — Completed projects

### `agents/`
Per-agent personalization for the DM channels:
- `dm-with-andi/` — Nano's persona and project notes for Andi
- `dm-with-suse/` — Quatschkopf's persona for Suse
- `dm-with-felix/` — Fabio's persona for Felix

## Sync

Run `scripts/backup.sh` from the nanoclaw server to push the latest data here.
