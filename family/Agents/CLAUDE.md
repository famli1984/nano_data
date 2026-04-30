# Agents – CLAUDE.md

> Übersicht aller Agenten im Familien-Assistenten-System.

## Architektur

```
Executive Assistants (Primär)
    ↓ delegieren an
Support-Agenten (Sekundär)
    ↓ berichten an
Executive Assistants → Familienmitglieder
```

## Executive Assistants

| Agent | Person | Hauptaufgaben |
|-------|--------|--------------|
| [[Executive/Suse/CLAUDE\|Suse-EA]] | Suse | Todos, Termine, Koordination |
| [[Executive/Andy/CLAUDE\|Andy-EA]] | Andy | Todos, Termine, Koordination |
| [[Executive/Felix/CLAUDE\|Felix-EA]] | Felix | Hausaufgaben, Todos, Schule |
| [[Executive/Marie/CLAUDE\|Marie-EA]] | Marie | Hausaufgaben, Todos, Schule |
| [[Executive/Rosa/CLAUDE\|Rosa-EA]] | Rosa | Todos, Bedarf, Termine |

## Support-Agenten

| Agent | Fokus | Auftraggeber |
|-------|-------|-------------|
| [[Support/Putzfrau/CLAUDE\|Putzfrau]] | Reinigung organisieren | Suse-EA / Andy-EA |
| [[Support/Babysitter/CLAUDE\|Babysitter]] | Betreuung koordinieren | Suse-EA / Andy-EA |
| [[Support/Hausmeister/CLAUDE\|Hausmeister]] | Haus in Schuss | Andy-EA |
| [[Support/Gaertner/CLAUDE\|Gärtner]] | Garten pflegen | Andy-EA |
| [[Support/Urlaubsplaner/CLAUDE\|Urlaubsplaner]] | Urlaube planen | Suse-EA / Andy-EA |
| [[Support/Mechaniker/CLAUDE\|Mechaniker]] | Fahrzeuge & Fahrräder | Andy-EA |
| [[Support/Familienberater/CLAUDE\|Familienberater]] | Beziehungstipps | Alle EAs |
| [[Support/PersonalAssistant/CLAUDE\|PersonalAssistant]] | Sport & Gesundheit Eltern | Suse-EA / Andy-EA |
| [[Support/ManagementConsultant/CLAUDE\|ManagementConsultant]] | System-Optimierung | Suse-EA / Andy-EA |
| [[Support/Steuerberater/CLAUDE\|Steuerberater]] | Steuern & absetzbare Ausgaben | Andy-EA / Suse-EA |
| [[Support/Knaufi/CLAUDE\|Knaufi]] | Hausaufgaben-Coach & Lernbegleitung | Fabio (Felix-EA) |

---
*Tags: `#agents #system`*
