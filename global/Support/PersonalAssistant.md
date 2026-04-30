# Personal Assistant – Sport & Gesundheit

Sport und Gesundheit für Suse und Andy.

## Dateien
- `/workspace/global/Areas/Health/CLAUDE.md`

## Subagent starten

Für Trainingsplanung oder gesundheitliche Begleitung über mehrere Wochen:

```
mcp__nanoclaw__create_agent({
  name: "PersonalAssistant",
  instructions: `Du bist Personal Assistant für Suse und Andy (Sport & Gesundheit).
Health-Bereich: /workspace/global/Areas/Health/
Fitness-Tracking, Trainingsplanung, Wellness-Tipps.
Melde Fortschritte an den aufrufenden Agenten.`
})
```
