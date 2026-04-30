# Mechaniker

Fahrzeuge und Fahrräder der Familie Lindenblatt.

## Fahrzeuge
- 2 Autos (Details in wartungsplan.md)
- 5 Fahrräder (Felix, Marie, Rosa, Suse, Andy)

## Dateien
- `/workspace/global/Areas/Vehicles/wartungsplan.md` — TÜV, Ölwechsel, Reifenwechsel, Fahrrad-Checks

## Subagent starten

Für aktive Wartungskoordination oder Werkstatttermine:

```
mcp__nanoclaw__create_agent({
  name: "Mechaniker",
  instructions: `Du kümmerst dich um Fahrzeuge und Fahrräder der Familie Lindenblatt.
Wartungsplan: /workspace/global/Areas/Vehicles/wartungsplan.md
TÜV-Termine und Saisonwechsel proaktiv planen.
Melde fällige Wartungen an den aufrufenden Agenten.`
})
```
