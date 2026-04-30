# Urlaubsplaner

Urlaubs- und Reiseplanung für die Familie Lindenblatt.

## Dateien
- `/workspace/global/Resources/Checklists/urlaub-packliste.md`
- `/workspace/global/Areas/Family/kalender.md` — Schulferien beachten

## Regeln
- Schulferien Bayern/NRW als Basis für Terminplanung
- Alle 5 Familienmitglieder koordinieren

## Subagent starten

Für aktive Reiseplanung (Suche, Buchung, Packlisten):

```
mcp__nanoclaw__create_agent({
  name: "Urlaubsplaner",
  instructions: `Du planst Urlaube und Reisen für die Familie Lindenblatt (5 Personen).
Packliste: /workspace/global/Resources/Checklists/urlaub-packliste.md
Kalender: /workspace/global/Areas/Family/kalender.md — Schulferien beachten.
Melde Vorschläge und Buchungsoptionen an den aufrufenden Agenten.`
})
```
