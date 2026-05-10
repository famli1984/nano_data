# Nanoclaw — Installation & Setup on This Server

This documents exactly how Nanoclaw was set up on this server (`nano2` user, Ubuntu Linux), reconstructed from session logs.

## Server Basics

- **OS**: Ubuntu Linux
- **User**: `nano2` (non-root, with `sudo`)
- **Install path**: `/home/nano2/nanoclaw/`
- **Timezone**: `Europe/Berlin`

### Auto-Updates (configured once)

```bash
sudo apt install unattended-upgrades
sudo systemctl enable unattended-upgrades
```

`/etc/apt/apt.conf.d/50unattended-upgrades` was configured to:
- Pull security + updates pockets
- Include ESM (active once Ubuntu Pro is attached)
- Auto-remove unused kernels
- Auto-reboot at 03:00 only when no users are logged in

---

## Prerequisites

Nanoclaw's `nanoclaw.sh` installs these automatically if missing. For reference, the versions running on this server:

| Tool | Version |
|------|---------|
| Node.js | v24 (LTS) |
| pnpm | 10.33.0 |
| Docker Engine | 29.4.1 |
| signal-cli | system install |

---

## Installation

```bash
git clone https://github.com/qwibitai/nanoclaw.git nanoclaw-v2
cd nanoclaw-v2
bash nanoclaw.sh
```

`nanoclaw.sh` handles the full setup flow interactively:
1. Installs Node, pnpm, Docker if missing
2. Registers Anthropic credentials via OneCLI
3. Runs `pnpm install` and builds the container image
4. Walks through channel setup

If a step fails, it automatically invokes Claude Code to diagnose and resume.

---

## OneCLI (Credential Vault)

OneCLI manages all API keys — they are never stored in env vars or passed to containers directly. It runs as a local proxy on `http://172.17.0.1:10254` (Docker bridge address, reachable from inside containers).

```bash
# Check status
onecli agents list

# If a new agent group gets 401 errors, it was auto-created in "selective" secret mode.
# Fix: flip to "all" so vault secrets with matching host patterns are injected:
onecli agents set-secret-mode --id <agent-id> --mode all
```

Web UI: `http://127.0.0.1:10254`

**Common issue**: `/tmp/onecli-proxy-ca.pem` can be owned by the wrong user after restarts.
```bash
sudo rm -f /tmp/onecli-proxy-ca.pem
```
The next container spawn recreates it.

---

## Signal Channel

Signal is connected via `signal-cli` running as a TCP daemon managed by Nanoclaw.

**Account**: `+491639762801` (Nanoclaw has its own number, `ASSISTANT_HAS_OWN_NUMBER=true`)

Relevant `.env` entries:
```
SIGNAL_ACCOUNT=+491639762801
SIGNAL_MANAGE_DAEMON=true
ASSISTANT_HAS_OWN_NUMBER=true
```

### Signal Setup Troubleshooting (what we hit during setup)

**Issue: "Signal link failed (link exited 0 but no account registered)"**

`listAccounts()` filtered out accounts where `registered === false`, but signal-cli marks newly linked secondary devices as `registered: false`. Fix was to remove that filter in `setup/signal-auth.ts`:
```bash
sed -i 's/\.filter((a) => a\.registered !== false)//' setup/signal-auth.ts
pnpm run setup:auto
```

**Issue: "Delete /home/nano2/.local/share/signal-cli/data/938330 before trying again"**

Stale partial-link directory from a failed attempt:
```bash
rm -rf /home/nano2/.local/share/signal-cli/data/938330
```

**Issue: Infinite loop / `listAccounts` hanging**

The signal-cli daemon holds the config file lock; `spawnSync` in `listAccounts()` had no timeout and hung forever. Kill stuck processes:
```bash
kill $(pgrep -f "signal-cli.*listAccounts") 2>/dev/null || true
```
The fix was adding `timeout: 5000` to the `spawnSync` call in `setup/signal-auth.ts`.

**Issue: Stale registered=false account blocking re-link**

Delete the local account data and re-run:
```bash
signal-cli -a +491639762801 deleteLocalAccountData
pnpm run setup:auto
```

### How Users Chat via Signal

- **Andi (operator)**: "Note to self" / self-chat in Signal → agent responds
- **Suse**: separate Signal group wired to `dm-with-suse`
- **Felix**: separate Signal group wired to `dm-with-felix`

To add a new Signal group: use the `/add-signal-group` skill in Claude Code.

---

## Discord Channel

Discord bot is connected. Application ID: `1497842545592373268`

Set up via `/add-discord` skill. Discord was the first channel set up alongside Signal.

---

## Agent Groups

Three personal DM agent groups and one family-wide group:

| Group folder | Person | Assistant name |
|---|---|---|
| `groups/dm-with-andi` | Andi (operator) | Pauline |
| `groups/dm-with-suse` | Suse | Quatschkopf |
| `groups/dm-with-felix` | Felix | Fabio / Knaufi (homework) |
| `groups/family` | Shared family | — |

Global shared docs (mounted read-only into every container) live at:
`groups/global/` → mounted as `/workspace/global/` inside containers.

---

## Email Tool (Posteo)

Email is available as an MCP tool inside the `dm-with-andi` agent.

**Provider**: posteo.de  
**Account**: `famlindenblatt@posteo.de`

Connection settings (all in `groups/dm-with-andi/container.json`):
- IMAP: `posteo.de:993` (TLS)
- SMTP: `posteo.de:587` (STARTTLS)
- CalDAV: `https://posteo.de:8443/calendars/famlindenblatt/`

> **Note**: The hostname is `posteo.de` (not `imap.posteo.de` — that subdomain does not resolve).
> The CalDAV username path strips the `@posteo.de` domain: `/calendars/famlindenblatt/`, not `/calendars/famlindenblatt@posteo.de/`.

---

## Service Management

Nanoclaw runs as a systemd user service:

```bash
# Status
systemctl --user status nanoclaw

# Start / stop / restart
systemctl --user start nanoclaw
systemctl --user stop nanoclaw
systemctl --user restart nanoclaw

# Logs
tail -f /home/nano2/nanoclaw/logs/nanoclaw.log
tail -f /home/nano2/nanoclaw/logs/nanoclaw.error.log
```

To start the interactive CLI chat ("admin channel"):
```bash
cd /home/nano2/nanoclaw
pnpm chat
```

---

## Backup

`/home/nano2/nano_data/` is a git repo synced to GitHub (`famli1984/nano_data`).

Run backup:
```bash
/home/nano2/nano_data/scripts/backup.sh
```
