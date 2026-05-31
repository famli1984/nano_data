# Setting Up a Family Assistant System with Nanoclaw

A step-by-step tutorial documenting how to fork [nanoclaw](https://github.com/nanoclaw/nanoclaw), set up per-person DM agents, a shared PARA knowledge base, CalDAV/email integrations, a Discord adapter, and an automated backup system. Includes every mistake made along the way.

---

## What You're Building

One Claude-powered assistant per family member, each with their own persona, memory, and workspace — all sharing a common family knowledge base (PARA structure) and a global read-only knowledge layer. Everything runs locally in Docker containers on your own server.

Final architecture:

```
nanoclaw/
└── groups/
    ├── global/                  ← read-only shared knowledge, auto-mounted in every container
    │   ├── CLAUDE.md            ← index of all areas and support docs
    │   ├── Areas/               ← domain knowledge (Garden, House, Health, etc.)
    │   └── Support/             ← cross-domain support agent docs
    ├── dm-with-[person-a]/      ← Person A's private agent (Signal/Discord)
    ├── dm-with-[person-b]/      ← Person B's private agent
    ├── dm-with-[child]/         ← Child's agent
    ├── [specialist-agent]/      ← Persistent specialist (e.g. hausmeister)
    └── familypara/              ← Shared PARA data (mounted into relevant agents)

nano_data/                       ← Separate git repo: automated markdown backup
```

---

## Prerequisites

- A Linux server (tested on Ubuntu 22.04)
- Docker + Docker Compose
- `pnpm`, `bun`, `node`
- A messaging platform (Signal, Telegram, or Discord) + credentials
- Anthropic API key
- (optional) Posteo or other CalDAV/IMAP provider

---

## Step 1 — Fork Nanoclaw

Do not clone nanoclaw directly. Fork it on GitHub so you can push your customizations.

```bash
git clone https://github.com/YOUR_USERNAME/nanoclaw.git
cd nanoclaw
pnpm install
```

Your fork is the "product" — upstream nanoclaw is the engine. Keep your changes layered on top so you can pull upstream improvements later.

---

## Step 2 — Understand the Key Concepts

Before touching anything, internalize these:

### groups/
Each subdirectory under `groups/` is an **agent group** — one Claude instance in one Docker container. The folder is the agent's workspace, mounted at `/workspace/agent/` inside the container.

### groups/global/ — the shared knowledge layer
`groups/global/` is automatically mounted **read-only at `/workspace/global/`** in every agent container. You do not need to configure this per agent. Anything you put there is available to all agents. This is where cross-cutting knowledge (house info, garden info, support agent instructions) lives.

### CLAUDE.md vs CLAUDE.local.md
- `CLAUDE.md` — **generated at spawn time** by nanoclaw's compose system. It assembles core modules (tools, scheduling, self-mod). **Never edit this file.** Your edits will be overwritten on the next spawn.
- `CLAUDE.local.md` — **your file.** Agent persona, instructions, workspace map, delegation rules. This is what you write.

### container.json
Controls what runs inside the container:
- `mcpServers` — MCP tool servers (e.g., CalDAV, email)
- `packages.apt` — apt packages to install (e.g., `ffmpeg`, `python3-pip`)
- `additionalMounts` — extra host paths mounted at `/workspace/extra/<name>/`
- `assistantName` — the name the agent calls itself
- `skills` — `"all"` gives the agent all nanoclaw skills

### Container lifecycle
Containers **spawn when a message arrives** and can stay running. You do not need to restart a container after editing `CLAUDE.local.md` or `container.json` — the new config takes effect on the next inbound message (the container is re-created from the updated config at that point).

### .gitignore
By default, nanoclaw ignores `groups/*`. Groups are per-install state — they contain credentials, generated files, conversation logs. Only commit what you intentionally want tracked.

---

## Step 3 — Run Initial Setup

```bash
./nanoclaw.sh setup
```

The interactive setup wizard configures your Anthropic API key, creates the main/global agent, and registers your messaging platform channels. After setup, you have a running `main` agent.

### Known setup bugs (and fixes)

These bugs existed in the version we used. They may already be patched upstream — check before applying:

#### Bug: Signal auth step hangs forever

**Symptom:** Setup gets stuck at the `signal-auth` step with no output.

**Root cause:** `setup/signal-auth.ts` calls `signal-cli` via `spawnSync` with no timeout. If the signal-cli daemon is already running and holding the config lock, `spawnSync` hangs indefinitely. Multiple stuck processes accumulate.

**Fix in `setup/signal-auth.ts`:**
```typescript
// Add timeout to prevent hang
spawnSync('signal-cli', ['listAccounts', '--output=json'], {
  timeout: 5000,  // ← add this
  encoding: 'utf8',
})
```

Also add: if `SIGNAL_ACCOUNT` is already set in `.env`, skip the link step entirely.

#### Bug: Successfully linked Signal account not detected

**Symptom:** Signal-cli link completes (QR scanned, device appears in Signal app), but setup says "no accounts found" and asks you to link again.

**Two root causes, both in `listAccounts()` in `setup/signal-auth.ts`:**

1. A newly linked secondary device has `registered: false` in signal-cli's JSON output. The code filtered these out with `.filter((a) => a.registered !== false)` — which discards the successful link.

2. The JSON output from signal-cli uses `a.number` for the phone number, but the code read `a.account` — so even after removing the filter, the account appeared empty.

**Fix:**
```typescript
// WRONG — filters out newly linked devices
const accounts = parsed.filter((a) => a.registered !== false);

// CORRECT — keep all accounts
const accounts = parsed;

// WRONG — signal-cli JSON uses 'number', not 'account'
return accounts.map((a) => a.account);

// CORRECT
return accounts.map((a) => a.number);
```

#### Bug: Stale partial-link directory blocks re-linking

**Symptom:** After a failed link attempt, signal-cli refuses to link again.

**Fix:** Remove the stale data directory:
```bash
rm -rf ~/.local/share/signal-cli/data/+YOUR_NUMBER_PARTIAL
```

#### Bug: Container authentication fails (EACCES on CA cert)

**Symptom:** Agent containers spawn but all Anthropic API calls return 401. Logs show `EACCES: permission denied` on `/tmp/onecli-proxy-ca.pem`.

**Root cause:** A previous setup run as a different user left `/tmp/onecli-proxy-ca.pem` with the wrong ownership. New containers can't write the CA cert and can't authenticate.

**Fix:**
```bash
sudo rm -f /tmp/onecli-proxy-ca.pem
# then re-run setup or restart nanoclaw
```

#### Bug: Signal isMention not set for DM messages

**Symptom:** Messages from new phone numbers are silently dropped — no response, no error.

**Root cause:** `src/channels/signal.ts` wasn't setting `isMention: true` for direct message payloads. Nanoclaw's routing ignores messages where `isMention` is false (it treats them as ambient group messages the agent wasn't addressed to).

**Fix in `src/channels/signal.ts`:** Set `isMention: true` for all Signal DM messages (non-group messages addressed directly to the bot number).

---

## Step 4 — Add a Discord Adapter (if needed)

Nanoclaw ships Signal and Telegram adapters. If you want Discord, add the adapter:

### 4a — Install the package

```bash
pnpm add @chat-adapter/discord
```

### 4b — Create `src/channels/discord.ts`

```typescript
import { createDiscordAdapter } from '@chat-adapter/discord';
import { readEnvFile } from '../env.js';
import { createChatSdkBridge, type ReplyContext } from './chat-sdk-bridge.js';
import { registerChannelAdapter } from './channel-registry.js';

function extractReplyContext(raw: Record<string, any>): ReplyContext | null {
  if (!raw.referenced_message) return null;
  const reply = raw.referenced_message;
  return {
    text: reply.content || '',
    sender: reply.author?.global_name || reply.author?.username || 'Unknown',
  };
}

registerChannelAdapter('discord', {
  factory: () => {
    const env = readEnvFile(['DISCORD_BOT_TOKEN', 'DISCORD_PUBLIC_KEY', 'DISCORD_APPLICATION_ID']);
    if (!env.DISCORD_BOT_TOKEN) return null;
    const discordAdapter = createDiscordAdapter({
      botToken: env.DISCORD_BOT_TOKEN,
      publicKey: env.DISCORD_PUBLIC_KEY,
      applicationId: env.DISCORD_APPLICATION_ID,
    });
    return createChatSdkBridge({
      adapter: discordAdapter,
      concurrency: 'concurrent',
      botToken: env.DISCORD_BOT_TOKEN,
      extractReplyContext,
      supportsThreads: true,
    });
  },
});
```

### 4c — Register in `src/channels/index.ts`

```typescript
import './discord.js';
```

### 4d — Add credentials to your env file

```
DISCORD_BOT_TOKEN=your-bot-token
DISCORD_PUBLIC_KEY=your-public-key
DISCORD_APPLICATION_ID=your-app-id
```

The adapter self-registers and falls back gracefully if the token is absent.

---

## Step 5 — Create Per-Person Agent Groups

Each family member gets their own nanoclaw group (one container, one persona). Create the group via the nanoclaw setup UI, then customize the files it generates.

### Folder structure for one person

```
groups/dm-with-[person]/
├── CLAUDE.local.md     ← your persona definition
├── CLAUDE.md           ← auto-generated at spawn, never edit
└── container.json      ← MCP servers, mounts, packages
```

### Template: CLAUDE.local.md for an adult

```markdown
# [AssistantName]

You are [AssistantName], [Person]'s personal assistant. Keep replies concise.

## Channel roles

Always reply in the channel the message came from — never switch channels unprompted.

- **[channel-id-1]** ([platform] group "[group name]") → reply with `to: "[channel-id-1]"`, NOT `to: "[person]"`
- **[platform] ([phone-number])** → [Person]'s private DM; call yourself [AssistantName] here

## User: [Person]
- Communicates in [language]
- [Any relevant notes]

## Workspace

- Personal todos → `/workspace/agent/todos.md`
- Shared family data → `/workspace/extra/familypara/`

## Global knowledge

Shared domain knowledge and support agent instructions are at `/workspace/global/`.
```

### Template: container.json with CalDAV + email

```json
{
  "mcpServers": {
    "caldav": {
      "command": "bun",
      "args": ["/workspace/agent/caldav-mcp.js"],
      "env": {
        "CALDAV_USERNAME": "your-caldav-username",
        "CALDAV_PASSWORD": "your-caldav-password"
      }
    },
    "email": {
      "command": "email-mcp",
      "args": [],
      "env": {
        "MCP_EMAIL_ADDRESS": "your-email@provider.com",
        "MCP_EMAIL_PASSWORD": "your-password",
        "MCP_EMAIL_IMAP_HOST": "imap-host",
        "MCP_EMAIL_SMTP_HOST": "smtp-host",
        "MCP_EMAIL_SMTP_PORT": "587",
        "MCP_EMAIL_SMTP_TLS": "false",
        "MCP_EMAIL_SMTP_STARTTLS": "true"
      }
    }
  },
  "packages": {
    "apt": ["ffmpeg", "python3-pip"],
    "npm": []
  },
  "additionalMounts": [
    {
      "hostPath": "/absolute/path/to/nanoclaw/groups/familypara",
      "containerPath": "familypara",
      "readonly": false
    }
  ],
  "skills": "all",
  "groupName": "[AssistantName]",
  "assistantName": "[AssistantName]",
  "agentGroupId": "ag-GENERATED-BY-SETUP"
}
```

**Important:** `agentGroupId` is assigned by nanoclaw when you create the group. Let the setup UI generate it.

**Important:** Always use **absolute paths** in `additionalMounts.hostPath`. Tilde (`~`) expansion does not work in JSON configs.

---

## Step 6 — Set Up CalDAV Integration

If you want the agent to read and write calendar events and tasks, you need a CalDAV MCP server.

### 6a — Write a CalDAV MCP server (caldav-mcp.js)

Create a Bun script that exposes CalDAV operations as MCP tools. Place it in the agent's group folder at `groups/dm-with-[person]/caldav-mcp.js`.

The script should expose at minimum:
- `list_events` — fetch upcoming events
- `create_event` — create a VEVENT
- `list_tasks` — fetch open VTODOs
- `create_task` — create a VTODO

Wire it into `container.json`:
```json
"mcpServers": {
  "caldav": {
    "command": "bun",
    "args": ["/workspace/agent/caldav-mcp.js"],
    "env": {
      "CALDAV_USERNAME": "your-username",
      "CALDAV_PASSWORD": "your-password"
    }
  }
}
```

Then allowlist `mcp__caldav__*` in `container/agent-runner/src/providers/claude.ts` so the agent is permitted to call these tools.

### 6b — Posteo-specific CalDAV notes

If your provider is Posteo (or a compatible groupware):

- **Port:** `8443` (not the standard CalDAV port 5232)
- **Host:** `posteo.de` (not `caldav.posteo.de` — that hostname doesn't resolve)
- **URL path:** uses the bare username without `@posteo.de`

  Correct: `https://posteo.de:8443/caldav/v2/[username]/calendar/`

  Wrong: `https://posteo.de:8443/caldav/v2/[username]@posteo.de/calendar/`

- **IMAP host:** `posteo.de` (not `imap.posteo.de`)
- After a failed authentication attempt, Posteo may temporarily block you for a few minutes before accepting the correct password — wait and retry.

### 6c — Calendar sync script

To keep markdown calendar files up to date from CalDAV (so agents can read the calendar without making live API calls on every message), write a sync script that:

1. Fetches all VEVENTs and VTODOs from CalDAV
2. Writes per-person `.md` files into `groups/familypara/01_Calendars/`

**Critical:** Write the sync script using **Python standard library only**. The `caldav` pip package (and other pip packages) are not available on the host without a pip install step. Use `urllib.request` for HTTP, and parse the iCalendar format manually or with the stdlib `re` module.

**Common bug:** `REPO_ROOT` derivation breaks when the script is run from different working directories. Derive the path from `__file__`, not from `os.getcwd()`:

```python
import os
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

**Never write to `01_Calendars/` manually.** That folder is overwritten by the sync script. Agents must be instructed not to write there either.

### 6d — Automate with cron

```bash
# Every 30 minutes
*/30 * * * * /absolute/path/to/nanoclaw/scripts/sync_calendar.py >> /absolute/path/to/nanoclaw/logs/sync_calendar.log 2>&1
```

---

## Step 7 — Create the Global Knowledge Layer

Instead of repeating domain knowledge (house, garden, vehicles, health, etc.) in every agent, put it in `groups/global/` once. Every container mounts it read-only at `/workspace/global/` automatically.

### Structure

```
groups/global/
├── CLAUDE.md              ← index: lists all areas and support docs
├── Areas/
│   ├── Garden/
│   │   ├── CLAUDE.md      ← Garden knowledge + Gärtner subagent instructions
│   │   └── checkliste.md
│   ├── House/CLAUDE.md    ← House knowledge + Hausmeister/Putzfrau subagent instructions
│   ├── Vehicles/CLAUDE.md
│   ├── Health/CLAUDE.md
│   ├── Finances/CLAUDE.md
│   ├── School/CLAUDE.md
│   └── Family/CLAUDE.md
└── Support/
    ├── Kalender.md
    ├── Babysitter.md
    ├── Urlaubsplaner.md
    ├── ManagementConsultant.md
    └── ... (one file per cross-domain support role)
```

### Document format for global/ files

Each global knowledge file is written in **third person** (reference doc style), not as an agent identity. It includes:

1. Domain knowledge (what you know, checklists, contacts, tools)
2. A `## Subagent` section with `create_agent` spawn instructions and when-to-use criteria

Example pattern for `global/Areas/Garden/CLAUDE.md`:

```markdown
# Garden

## Overview
[Domain knowledge about the garden: layout, plants, tools, seasonal tasks...]

## Checklist
@./checkliste.md

## Subagent

**Gärtner** — spawn when the user needs active garden planning, seasonal advice, or task coordination.

When to spawn: seasonal prep, problem diagnosis, planting plans, maintenance scheduling.

\`\`\`
mcp__nanoclaw__create_agent({
  name: "Gärtner",
  instructions: "You are the Gärtner (garden manager) for [Family]. [Full persona instructions here...]"
})
\`\`\`
```

The primary agent reads the global doc inline for simple questions. For complex tasks, it spawns the subagent using the embedded instructions.

---

## Step 8 — Create the Shared Family PARA Knowledge Base

For live family data (calendars, shopping lists, todos, finances), mount one shared directory into all agents that need read-write access.

### Create groups/familypara/

```
groups/familypara/
├── CLAUDE.local.md
├── container.json
├── 00_Todos/
├── 01_Calendars/          ← auto-synced by CalDAV script — agents must never write here
├── 02_Projects/
├── 03_Areas/
│   ├── Family/            ← pickup schedules, contacts, shopping
│   ├── Finances/          ← tax tracking (steuerausgaben-YYYY.md, one file per year)
│   ├── Food/              ← meal planning, shopping list
│   ├── Garden/
│   ├── Health/
│   ├── House/             ← cleaning plan, maintenance checklist
│   ├── School/
│   ├── Urlaube/           ← vacation planning + pack lists
│   └── Vehicles/          ← maintenance log
├── 04_Resources/
│   ├── Checklists/
│   ├── Knowledge/         ← family-profile.md (who is who, ages, preferences)
│   └── Templates/
└── 05_Archives/
```

### Mount into each relevant agent's container.json

```json
"additionalMounts": [
  {
    "hostPath": "/absolute/path/to/nanoclaw/groups/familypara",
    "containerPath": "familypara",
    "readonly": false
  }
]
```

Inside the container, this appears at `/workspace/extra/familypara/`.

### Reference rules for agents

Include this in `CLAUDE.local.md` for any agent that uses familypara:

```markdown
## Shared family data (PARA)

Path: `/workspace/extra/familypara/`

- `01_Calendars/` — **read only, never write here** — auto-synced every 30 min
- `03_Areas/Finances/` — tax tracking
- `03_Areas/Urlaube/` — vacation planning + pack lists

**Where to create new files:**
1. Affects the whole family → `/workspace/extra/familypara/03_Areas/<domain>/`
2. Affects only this person → `/workspace/agent/`
3. Tax tracking → always `03_Areas/Finances/steuerausgaben-YYYY.md`
```

---

## Step 9 — Specialist Agents

For focused persistent tasks (home maintenance, etc.), create a specialist group that receives delegated tasks from a person's primary agent.

```
groups/[specialist]/
├── CLAUDE.local.md     ← specialist persona
├── container.json      ← minimal; usually no MCP servers
└── [domain]-tasks.md   ← task list the agent maintains
```

**CLAUDE.local.md pattern:**

```markdown
# [SpecialistName]

You handle [domain] tasks delegated by [PersonAgent].

## Your tasks
- Maintain `/workspace/agent/[domain]-tasks.md`
- Report results concisely back to the delegating agent

## Style
- Short and structured. [Language]. No lengthy explanations.
```

**Wiring delegation in the primary agent's CLAUDE.local.md:**

```markdown
## Companion agents

- **[specialist-group-name]** → [domain]: use `mcp__nanoclaw__send_message`
```

---

## Step 10 — Spawn-on-Demand Subagents

For session-scoped tasks (tutoring, one-off deep dives), use `mcp__nanoclaw__create_agent` instead of a persistent group.

### Pattern

1. Write the subagent's full instruction set as a standalone markdown file in the primary agent's workspace (e.g., `groups/dm-with-[child]/tutor.md`)
2. In the primary agent's `CLAUDE.local.md`:

```markdown
## [TutorName] — homework coach

Full profile: `/workspace/agent/tutor.md`

**When to spawn:** User asks for homework help, explanation of a school topic, or test prep.

\`\`\`
mcp__nanoclaw__create_agent({
  name: "[TutorName]",
  instructions: "<read /workspace/agent/tutor.md and paste full content here>"
})
\`\`\`

Read the file first, insert its content as `instructions`. [TutorName] reports back to you after the session.
```

### Teaching style pattern (from Knaufi, the homework coach)

For a children's learning agent, the instruction file should specify:
- **Socratic first** — ask questions rather than give answers; guide to the solution
- **Step by step** — never skip; confirm understanding before moving on
- **Multiple explanation routes** — if one approach fails, try analogy, drawing, real-world example
- **Errors as curiosity** — "Why do you think that?" not "That's wrong"
- **No spoilers policy** — never give the finished answer, only the next clue

---

## Step 11 — Automated Backup to a Separate Repo

Create a separate `nano_data` git repo for backing up agent content **without credentials**.

### Backup script pattern

```bash
#!/usr/bin/env bash
set -euo pipefail

SRC="/absolute/path/to/nanoclaw/groups"
DST="/absolute/path/to/nano_data"

# Shared PARA — full sync, excluding generated/runtime files
rsync -a --delete \
  --exclude='.claude-shared.md' \
  --exclude='.claude-fragments/' \
  --exclude='hooks/' \
  --exclude='container.json' \
  "$SRC/familypara/" "$DST/familypara/"

# Agent groups — only markdown content, never credentials
for group in dm-with-[person-a] dm-with-[person-b] dm-with-[child] [specialist]; do
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
git pull --no-rebase origin main
git add -A
if git diff --cached --quiet; then
  echo "Nothing changed."
else
  git commit -m "backup: $(date -u '+%Y-%m-%d %H:%M') UTC"
  git push origin main
fi
```

### Key exclusion rules

| File | Exclude? | Why |
|------|----------|-----|
| `container.json` | **Always** | Contains API keys, CalDAV passwords, email passwords |
| `CLAUDE.md` | Yes | Generated at spawn, not your content |
| `.claude-fragments/` | Yes | Generated module fragments |
| `CLAUDE.local.md` | **Include** | This is the persona you wrote |
| `*.md` in agent workspace | Include | Knowledge and todos |

### GitHub auth from a server

`gh auth login` requires an interactive TTY — it cannot be driven from Claude Code's Bash tool or a non-interactive shell. Options:
- Run `gh auth login` directly in your terminal
- Or embed a Personal Access Token (PAT) in the git remote URL: `https://TOKEN@github.com/user/repo.git` — but rotate this token periodically, as it's stored in `.git/config`

### Automate with cron

```bash
# Every 30 minutes
*/30 * * * * /absolute/path/to/nano_data/scripts/backup.sh >> /absolute/path/to/nano_data/backup.log 2>&1
```

---

## Mistakes We Made (Don't Repeat These)

### Mistake 1 — Committing generated per-install files

Early on, `groups/global/CLAUDE.md` and `groups/main/CLAUDE.md` were committed to the fork. These are generated at spawn time and belong to per-install state.

**Fix:** Remove them from git and update `.gitignore`:
```bash
git rm groups/global/CLAUDE.md groups/main/CLAUDE.md
```

### Mistake 2 — Building a full multi-agent tree inside one group

The first design put every family role (Executives per person, plus Gärtner, Hausmeister, Kalender, etc.) as separate subdirectories inside one `groups/family/` container — a 60+ file tree with `Agents/Executive/` and `Agents/Support/` nested inside.

The problem: nanoclaw's model is one group = one primary agent persona. One container can't naturally be multiple agents at once. The tree was impossible to wire to the right messaging channels.

**Fix:** Split into individual `dm-with-[person]` groups (one container per person). Domain knowledge moved to `groups/global/` as third-person reference docs. Support roles became either specialist groups or spawn-on-demand subagents.

The original Agents/ content wasn't wasted — role descriptions migrated into `CLAUDE.local.md` files and subagent instruction files.

### Mistake 3 — Editing CLAUDE.md directly

`CLAUDE.md` looks editable. It's not — nanoclaw regenerates it from module fragments at every spawn. Any content written there disappears.

**Rule:** Always edit `CLAUDE.local.md`. That's what nanoclaw appends to the generated base.

### Mistake 4 — Using relative or tilde paths in container.json

```json
// WRONG — tilde not expanded in JSON
{ "hostPath": "~/nanoclaw/groups/familypara" }

// CORRECT
{ "hostPath": "/home/username/nanoclaw/groups/familypara" }
```

### Mistake 5 — Duplicate agent on the same Signal channel

"Nano" and the personal assistant agent were both wired to the same Signal "Note to Self" group — a leftover from a naming migration. Both agents received and responded to the same messages.

**Fix:** Identify the duplicate in the nanoclaw DB (check `agent_groups` and `channel_wirings`), stop its container, and delete its DB entries. Keep only the intended agent.

### Mistake 6 — Persona names chosen mid-flight

One child agent's assistant was named "Marienkäfer" in the first commit, then renamed to "Clarie" two commits later. The conversation history already had the old name.

**Lesson:** Settle on names before the agent goes live. Names appear in every user-facing message.

### Mistake 7 — Missing channel routing rules → wrong-channel replies

When an agent receives messages from multiple channels (Signal group + Signal DM + Discord), without explicit routing it can reply to the wrong channel.

**Fix in CLAUDE.local.md:**
```markdown
## Channel roles

Always reply in the channel the message came from — never switch channels unprompted.

- **[group-channel-id]** (Signal group "[Group Name]") → reply with `to: "[group-channel-id]"`
- **Signal ([number])** → private DM, call myself [AssistantName] here
```

### Mistake 8 — Forgetting to exclude container.json from backup

`container.json` contains CalDAV passwords, email passwords, and MCP server credentials. The backup rsync must always exclude it. This is your last line of defense against credential leaks to GitHub.

### Mistake 9 — No pip on host; using pip-dependent Python scripts

Initial CalDAV and calendar scripts used the `caldav` pip library. It wasn't installed on the host, and installing pip packages as root for one-off scripts is fragile.

**Fix:** Rewrite all Python helper scripts to use only the standard library (`urllib.request`, `re`, `datetime`). No pip dependencies.

### Mistake 10 — Python sync script breaks depending on working directory

```python
# WRONG — breaks when run from cron (different cwd)
REPO_ROOT = os.path.abspath('.')

# CORRECT — always resolves relative to the script file
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

### Mistake 11 — Signal rate-limits first messages to new numbers

After sending a welcome message to a new Signal number (one that's never received a message from your bot), Signal may block outbound messages to that number for ~24 hours. This is a Signal anti-spam measure.

**Lesson:** Don't expect welcome messages to work for new contacts. Test with a number that has existing history with your Signal account first.

### Mistake 12 — Posteo CalDAV: wrong host and wrong URL path

```
// WRONG — hostname doesn't resolve
https://caldav.posteo.de:5232/caldav/v2/user@posteo.de/calendar/

// CORRECT
https://posteo.de:8443/caldav/v2/user/calendar/
```

After failed auth attempts, Posteo may temporarily block your IP for a few minutes. Wait and retry before diagnosing further.

---

## Architecture Evolution: From Multi-Agent to Single-Agent + Global

We went through two architectures. Understanding both helps if you're deciding which to use.

### Architecture 1 (first attempt): Multi-agent tree

```
groups/family/
└── Agents/
    ├── Executive/
    │   ├── [Person-A]/CLAUDE.md    ← persona + first-person identity
    │   ├── [Person-B]/CLAUDE.md
    │   └── [Child]/CLAUDE.md
    └── Support/
        ├── Hausmeister/CLAUDE.md
        ├── Gärtner/CLAUDE.md
        ├── Kalender/CLAUDE.md
        └── ...
```

**Why it doesn't work well:** One nanoclaw group = one Claude instance. You can't route different Signal/Discord channels to different subfolders within the same container. The Executives and Support agents all end up being the same agent (the one the container is).

### Architecture 2 (final): One group per person + global knowledge

```
groups/
├── global/                   ← knowledge layer, auto-mounted everywhere
│   ├── Areas/<domain>/       ← domain facts + subagent spawn instructions
│   └── Support/<role>.md     ← cross-domain role facts + spawn instructions
├── dm-with-[person-a]/       ← one container, one persona, one or more channels
├── dm-with-[person-b]/
└── dm-with-[child]/
```

**Why it works:** Each group maps cleanly to one set of channels. The agent reads global/ for domain knowledge and spawns subagents on demand for heavy tasks. Specialist groups can receive delegated tasks via `send_message`.

**Migration path:** Take the content from each `Agents/Support/<role>/CLAUDE.md` (first-person identity), rewrite it as a third-person reference doc + `## Subagent` spawn block, and put it in `global/Support/<role>.md` or `global/Areas/<domain>/CLAUDE.md`.

---

## Key File Reference

| File | Location | Purpose | Edit? |
|------|----------|---------|-------|
| `CLAUDE.local.md` | `groups/[name]/` | Agent persona + instructions | Yes |
| `CLAUDE.md` | `groups/[name]/` | Auto-assembled at spawn | Never |
| `container.json` | `groups/[name]/` | MCP servers, mounts, packages | Yes |
| `caldav-mcp.js` | `groups/[primary]/` | CalDAV MCP tool server | Yes |
| `sync_calendar.py` | `scripts/` or `groups/[primary]/` | CalDAV → markdown sync | Yes |
| `backup.sh` | `nano_data/scripts/` | Credential-safe rsync + git | Yes |
| `src/channels/discord.ts` | nanoclaw src | Discord adapter | Only if adding Discord |
| `src/channels/index.ts` | nanoclaw src | Channel adapter registry | Add one import line |

---

## What Gets Committed to the Fork vs. Left Untracked

### Committed to the fork repo

```
src/channels/discord.ts          ← Discord adapter implementation
src/channels/index.ts            ← +1 import line
package.json                     ← @chat-adapter/discord dependency
pnpm-lock.yaml                   ← updated lockfile
.gitignore                       ← groups/* exclusion with exceptions
setup/signal-auth.ts             ← Signal setup bug fixes
src/channels/signal.ts           ← isMention fix
```

### Untracked (per-install state, never commit)

```
groups/dm-with-*/                ← agent workspaces (contain credentials)
groups/familypara/               ← live family data (synced to nano_data instead)
groups/global/                   ← knowledge docs (synced to nano_data)
groups/*/container.json          ← always contains credentials
data/                            ← nanoclaw SQLite database
logs/                            ← container and sync logs
```

### In nano_data backup repo (markdown only, no credentials)

```
familypara/                      ← PARA knowledge base (all .md)
agents/dm-with-*/                ← CLAUDE.local.md + workspace .md files
agents/[specialist]/             ← CLAUDE.local.md + workspace .md files
scripts/backup.sh                ← the backup script itself
```
