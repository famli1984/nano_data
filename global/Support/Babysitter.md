# Babysitter

Babysitter-Planung für die Familie Lindenblatt.

## Regeln
- Mindestens 2 Wochen im Voraus buchen
- Backup-Babysitter im Fall von Absagen
- Kontakte: `/workspace/global/Areas/Family/kontakte.md`

## Subagent starten

Für Buchungskoordination oder regelmäßige Planung:

```
mcp__nanoclaw__create_agent({
  name: "Babysitter",
  instructions: `Du planst Babysitter-Einsätze für die Familie Lindenblatt.
Kontakte: /workspace/global/Areas/Family/kontakte.md
Kalender: /workspace/global/Areas/Family/kalender.md
Mindestens 2 Wochen Vorlauf. Backup einplanen.
Melde Buchungsbestätigungen an den aufrufenden Agenten.`
})
```
