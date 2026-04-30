# Kalender

Familien-Kalender. Einzige Schnittstelle zum Posteo CalDAV-Konto.

## Dateien
- `/workspace/global/Areas/Family/kalender.md` — Master (600 Tage)
- `/workspace/global/Areas/Family/kalender-familie.md` — Familien-Events
- `/workspace/global/Areas/Family/kalender-andi.md` / `kalender-suse.md` / `kalender-felix.md` / `kalender-kinder.md`

## Subagent starten (CalDAV-Sync)

Für aktive Kalender-Synchronisation mit Posteo (Import/Export CalDAV):

```
mcp__nanoclaw__create_agent({
  name: "Kalender",
  instructions: `Du bist der Kalender-Agent der Familie Lindenblatt.
Du bist die einzige Schnittstelle zum Posteo CalDAV-Konto.
Lies und schreibe /workspace/global/Areas/Family/kalender*.md.
Kein anderer Agent darf direkt auf CalDAV zugreifen.
Melde Änderungen an den aufrufenden Agenten.`
})
```

Für einfache Kalenderabfragen reicht ein Blick in die kalender*.md Dateien — kein Subagent nötig.
