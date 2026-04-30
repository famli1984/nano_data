# Garten – Familie Lindenblatt

Garten der Familie Lindenblatt. Saisonale Pflege, Planung und Koordination.

## Verantwortung
- Freigabe für Ausgaben >200€: Andy
- Kinder können für altersgerechte Aufgaben eingeplant werden:
  - Felix (13): Mähen, Laub harken
  - Marie (9): Gießen, Pflanzen
  - Rosa (6): Aussäen, kleine Pflege

## Saisonale Aufgaben

Siehe `checkliste.md` für die vollständige Saisonliste.

**Frühling (März–Mai):** Rasen düngen, Beete bepflanzen, Hecke schneiden, Geräte herrichten  
**Sommer (Juni–Aug):** Mähen 1–2x/Woche, Bewässerung, Schädlingsbekämpfung  
**Herbst (Sep–Nov):** Laub harken, Wintervorbereitung, Bäume schneiden  
**Winter (Dez–Feb):** Schneeräumen, Streumittel, Geräte einlagern

## Subagent: Gärtner

Für eigenständige Gartenplanung (z.B. längere Projekte, Wochenpläne, regelmäßige Koordination) kannst du einen spezialisierten Gärtner-Agenten starten:

```
mcp__nanoclaw__create_agent({
  name: "Gaertner",
  instructions: `Du bist der Gärtner-Agent der Familie Lindenblatt.
Du planst und koordinierst alle Gartenarbeiten selbstständig.
Auftraggeber: Andy (via Nano) oder direkt.
Ressourcen: /workspace/global/Areas/Garden/
Eskaliere Ausgaben >200€ an Andy.
Melde dich wenn ein Plan steht oder Entscheidungen nötig sind.`
})
```

Wann einen Gärtner-Agenten starten:
- Saisonaler Jahresplan soll erstellt werden
- Externe Gartenhelfer koordiniert werden müssen
- Regelmäßige wöchentliche Gartenaufgaben getrackt werden sollen

Für einfache Fragen ("Was steht diese Woche im Garten an?") reicht ein Blick in `checkliste.md` — kein Subagent nötig.
