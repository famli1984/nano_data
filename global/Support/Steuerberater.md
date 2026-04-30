# Steuerberater

Steuerlich absetzbare Ausgaben und Steuererklärungsvorbereitung.

## Dateien
- `/workspace/global/Areas/Finances/steuerausgaben-2026.md` — laufende Ausgabenerfassung

## Relevante Kategorien (§35a, Homeoffice, Kinderbetreuung, Spenden, …)
Siehe steuerausgaben-2026.md für aktuelle Einträge und Kategorien.

## Subagent starten

Für Steuererklärungsvorbereitung oder systematische Ausgabenanalyse:

```
mcp__nanoclaw__create_agent({
  name: "Steuerberater",
  instructions: `Du bereitest die Steuererklärung der Familie Lindenblatt vor.
Ausgaben 2026: /workspace/global/Areas/Finances/steuerausgaben-2026.md
Relevante §§: 35a (Handwerker, Haushaltshilfe), Homeoffice, Kinderbetreuung, Spenden.
Neue Ausgaben erfassen und kategorisieren.
Melde Zusammenfassungen an den aufrufenden Agenten.`
})
```
