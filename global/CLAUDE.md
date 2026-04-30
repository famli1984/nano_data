# Shared Family Resources

This folder (`/workspace/global`) is mounted read-only in every agent container and contains shared reference information for the Lindenblatt family.

## Contents

### Areas
Each area CLAUDE.md contains relevant data files and — where applicable — a `## Subagent` section explaining when and how to spawn a specialized agent.

- `Areas/Family/` — Kalender, Abholplan, Einkaufsliste, Kontakte (→ Kalender, Babysitter, Urlaubsplaner, Familienberater)
- `Areas/Finances/` — Ausgaben, Steuern (→ Steuerberater)
- `Areas/Garden/` — Gartenpflege, Checkliste (→ Gärtner, spawn-Anleitung inline)
- `Areas/Health/` — Sport & Gesundheit (→ PersonalAssistant)
- `Areas/House/` — Haus-Wartung, Putzplan (→ Hausmeister, Putzfrau)
- `Areas/School/` — Hausaufgaben, Termine, Noten (→ Knaufi)
- `Areas/Vehicles/` — Fahrzeuge & Fahrräder, Wartungsplan (→ Mechaniker)

### Support-Agenten
Each file describes the role and contains the `create_agent` call to start the agent on demand:

- `Support/Babysitter.md`
- `Support/Familienberater.md`
- `Support/Hausmeister.md`
- `Support/Kalender.md`
- `Support/Knaufi.md`
- `Support/ManagementConsultant.md`
- `Support/Mechaniker.md`
- `Support/PersonalAssistant.md`
- `Support/Putzfrau.md`
- `Support/Steuerberater.md`
- `Support/Urlaubsplaner.md`
