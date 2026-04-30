# Putzfrau / Reinigung

Koordination der Haushaltshilfe und Reinigungsplanung.

## Dateien
- `/workspace/global/Areas/House/putzplan.md` — Putzplan nach Raum

## Regeln
- Putzfrau mindestens 48h vorher kontaktieren
- Bestätigung einholen und in Kalender eintragen
- Sonderwünsche im Voraus kommunizieren

## Subagent starten

Für aktive Koordination (Termine buchen, Sonderwünsche planen):

```
mcp__nanoclaw__create_agent({
  name: "Putzfrau",
  instructions: `Du koordinierst die Haushaltshilfe der Familie Lindenblatt.
Putzplan: /workspace/global/Areas/House/putzplan.md
Termine 48h im Voraus bestätigen. Sonderwünsche vorab kommunizieren.
Melde Bestätigungen an den aufrufenden Agenten.`
})
```
