# Nanoclaw — Installation & Setup on This Server

Reconstructed from session logs. Covers how Nanoclaw was installed, how channels and agents are wired, how data isolation works, and how to collaborate with humans via Signal.

---

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

`/etc/apt/apt.conf.d/50unattended-upgrades` configured to:
- Pull security + updates pockets
- Include ESM (active once Ubuntu Pro is attached)
- Auto-remove unused kernels
- Auto-reboot at 03:00 only when no users are logged in

---

## Prerequisites

Nanoclaw's `nanoclaw.sh` installs these automatically if missing:

| Tool | Version on this server |
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

OneCLI manages all API keys. Secrets are never stored in env vars or passed to containers directly — they are injected at request time through the OneCLI proxy.

- Host proxy: `http://172.17.0.1:10254` (Docker bridge address, reachable from inside containers)
- Web UI: `http://127.0.0.1:10254`

```bash
# List all agent groups and their OneCLI identities
onecli agents list

# New agent groups are auto-created in "selective" secret mode (no secrets assigned).
# Symptom: container starts but gets 401 from APIs even though credentials are in the vault.
# Fix: flip to "all" so any vault secret whose host pattern matches gets injected:
onecli agents set-secret-mode --id <agent-id> --mode all
```

**Common issue**: `/tmp/onecli-proxy-ca.pem` can be owned by the wrong user after restarts, causing every container spawn to fail silently.
```bash
sudo rm -f /tmp/onecli-proxy-ca.pem
# Next container spawn recreates it automatically.
```

---

## How Channels and Agents Work Together

Nanoclaw separates **channels** (where messages arrive) from **agents** (who processes them). When you connect a channel, you decide which agent group handles it — and how isolated it is.

### The Entity Model

```
Channel message arrives
    → identified as a messaging_group (a specific chat/group on one platform)
    → routed to an agent_group (a workspace with its own CLAUDE.md, memory, container)
    → resolved to a session (conversation thread)
    → written to session's inbound.db
    → agent container wakes, reads message, calls Claude, writes response
    → host delivers response back through the channel
```

Each agent group has its own folder under `groups/` with:
- `CLAUDE.md` — personality, instructions, context
- `container.json` — MCP tools, mounts, capabilities
- `skills/` — installed Claude Code skills
- Its own container and session databases

### Adding a New Channel to an Existing Agent

1. Install the channel adapter skill (e.g. `/add-signal-group`, `/add-discord`, `/add-telegram`)
2. Run `/manage-channels` to wire the new messaging group to an agent group and choose an isolation level

---

## Data Isolation — What Agents Share and What They Don't

This is the most important architectural decision when adding a new channel. There are three isolation levels.

### Level 1: Shared Session

All wired channels feed into a single conversation thread. Every message from every wired channel appears in the same context.

**What's shared**: workspace, memory, CLAUDE.md, and the full conversation history.

**Use when**: one channel feeds context into another (e.g. a GitHub webhook + a Slack chat channel — the agent sees PR comments and Slack messages in one thread).

### Level 2: Same Agent, Separate Sessions (most common for personal use)

Multiple channels share the same agent identity (same workspace, memory, personality) but each has its own independent conversation thread.

**What's shared**: workspace, memory, CLAUDE.md, all tools. If the agent learns something in one session, it can remember it across sessions.

**What's separate**: the conversation thread. Messages from one channel don't appear in another channel's context window.

**Use when**: it's the same person across multiple channels and you want a unified agent identity. The agent "knows" you across all channels but conversations don't bleed into each other.

### Level 3: Separate Agent Groups (what we use for family members)

Each channel gets its own independent agent with its own workspace, memory, and personality.

**What's shared**: nothing. Different CLAUDE.md, different memory, different conversation history, different container. The agents don't know about each other.

**Use when**: different people are involved, or information in one channel must never reach another. This is the right choice whenever there's a privacy or confidentiality boundary.

### How to Decide

> Are you okay with any piece of information from one channel being available in the other?

- **No** → Separate agent groups (level 3)
- **Yes, and the conversations should happen in one shared thread** → Shared session (level 1)
- **Yes, but the conversations should be independent** → Same agent, separate sessions (level 2)

### Our Setup

| Channel | Person | Agent group | Isolation |
|---|---|---|---|
| Signal "Note to self" (Andi's number) | Andi | `dm-with-andi` | Level 3 |
| Signal DM from Andi's phone | Andi | `dm-with-andi` | Level 3 |
| Signal DM from Suse's phone | Suse | `dm-with-suse` | Level 3 (fully separate) |
| Signal DM from Felix's phone | Felix | `dm-with-felix` | Level 3 (fully separate) |
| Discord | Andi | `dm-with-andi` | Level 3 |

Each family member has a completely isolated agent. Suse's agent (Quatschkopf) has no access to Andi's conversations or memory, and vice versa.

**Shared read-only context**: The `groups/global/` folder is mounted read-only into every container as `/workspace/global/`. This is where shared family knowledge lives (areas, support agent docs). It's read-only — no agent can write there from inside the container.

---

## Collaborating with Humans in Signal

### How a Human Starts Chatting

Each family member chats via their own Signal DM directly to Nanoclaw's Signal number (`+491639762801`). The agent replies from that number.

- **Andi**: uses "Note to self" (Nanoclaw's own number DMed from Andi's phone) or via Discord
- **Suse**: DMs `+491639762801` from her phone → routed to Quatschkopf
- **Felix**: DMs `+491639762801` from his phone → routed to Fabio

There is no shared group chat — each person has a private, isolated conversation.

### Adding a New Person to Signal

Use the `/add-signal-group` skill in Claude Code. It reads available Signal groups/contacts from the running daemon and lets you wire them to an agent group.

For a new DM channel with a new person:
1. The person sends a message to Nanoclaw's Signal number
2. Claude Code wires the new sender's number to an agent group via the database
3. The agent sends a welcome message back

### What Agents Can and Can't Do in Signal

**Can do:**
- Reply to messages in the conversation thread
- Remember things across conversations (via agent memory/workspace)
- Send proactive messages if scheduled tasks are set up
- Receive images and voice messages (requires the voice/image handling to be enabled in the Signal adapter)

**Can't do:**
- See messages from other family members' private chats
- Write to shared files unless those files are mounted into their container
- Access another agent group's memory or workspace

### Signal Groups (not just DMs)

Signal group chats can also be wired to an agent. Use `/add-signal-group` — it lists available Signal groups and lets you pick one. The agent then participates in the group chat.

---

## Adding Tools to Agents (Email as Example)

Tools are added to agent groups as MCP servers configured in `groups/<group>/container.json`. The general pattern is:

1. Run the relevant skill in Claude Code (e.g. `/add-email-tool`)
2. The skill installs the MCP server binary into the container image (via `container/Dockerfile`)
3. The skill adds the tool allowlist entry to `container/agent-runner/src/providers/claude.ts`
4. The skill writes the tool config (credentials, endpoints) into the target group's `container.json`
5. Rebuild the container: `./container/build.sh`
6. Restart: `systemctl --user restart nanoclaw`

### Email Tool (Posteo) — Our Setup

Email is wired as an MCP tool (`@codefuturist/email-mcp`) in `dm-with-andi`. Tools exposed: read, search, send, draft, move, delete, mark emails and threads.

**Provider**: posteo.de  
**Account**: `famlindenblatt@posteo.de`

Connection settings (in `groups/dm-with-andi/container.json`):
- IMAP: `posteo.de:993` (TLS)
- SMTP: `posteo.de:587` (STARTTLS)
- CalDAV: `https://posteo.de:8443/calendars/famlindenblatt/`

> **Posteo hostname quirk**: Use `posteo.de` directly — `imap.posteo.de` does not resolve.
> CalDAV path uses username without domain: `/calendars/famlindenblatt/` (not `/calendars/famlindenblatt@posteo.de/`).

To add email to another agent group, re-run the `/add-email-tool` skill and select additional groups.

### Other Tools Available via Skills

| Skill | What it adds |
|---|---|
| `/add-email-tool` | IMAP/SMTP email (read, search, send) |
| `/add-gcal-tool` | Google Calendar (list, create, search events) |
| `/add-ollama-tool` | Local models via Ollama |
| `/add-vercel` | Vercel deployment from inside the container |

---

## Agent Groups on This Server

| Group folder | Person | Assistant name | Notes |
|---|---|---|---|
| `groups/dm-with-andi` | Andi (operator) | Pauline | Email + CalDAV wired |
| `groups/dm-with-suse` | Suse | Quatschkopf | Fully isolated |
| `groups/dm-with-felix` | Felix | Fabio / Knaufi | Homework coach |
| `groups/family` | Shared family | — | Family workspace |
| `groups/global/` | All agents (read-only) | — | Shared docs, area knowledge |

---

## Signal Channel Setup Details

Signal is connected via `signal-cli` running as a TCP daemon managed by Nanoclaw.

**Account**: `+491639762801` (Nanoclaw has its own dedicated number)

`.env` entries:
```
SIGNAL_ACCOUNT=+491639762801
SIGNAL_MANAGE_DAEMON=true
ASSISTANT_HAS_OWN_NUMBER=true
```

### Troubleshooting (issues we hit during setup)

**"Signal link failed (link exited 0 but no account registered)"**

`listAccounts()` filtered out `registered: false` accounts, but signal-cli marks newly linked secondary devices as `registered: false`. Fix:
```bash
sed -i 's/\.filter((a) => a\.registered !== false)//' setup/signal-auth.ts
pnpm run setup:auto
```

**"Delete /home/nano2/.local/share/signal-cli/data/938330 before trying again"**

Stale partial-link directory from a failed attempt:
```bash
rm -rf /home/nano2/.local/share/signal-cli/data/938330
```

**`listAccounts` hangs forever / setup stuck in infinite loop**

signal-cli daemon holds the config file lock; `spawnSync` had no timeout. Kill the stuck processes:
```bash
kill $(pgrep -f "signal-cli.*listAccounts") 2>/dev/null || true
```

**Stale `registered: false` account blocking re-link**
```bash
signal-cli -a +491639762801 deleteLocalAccountData
pnpm run setup:auto
```

---

## Discord Channel

Connected via `/add-discord` skill. Application ID: `1497842545592373248`

Wired to `dm-with-andi`.

---

## Service Management

```bash
# Status / restart
systemctl --user status nanoclaw
systemctl --user restart nanoclaw

# Logs
tail -f /home/nano2/nanoclaw/logs/nanoclaw.log
tail -f /home/nano2/nanoclaw/logs/nanoclaw.error.log

# Interactive CLI chat (admin/debug channel)
cd /home/nano2/nanoclaw && pnpm chat
```

---

## Backup

`/home/nano2/nano_data/` is a git repo synced to GitHub (`famli1984/nano_data`).

```bash
/home/nano2/nano_data/scripts/backup.sh
```
