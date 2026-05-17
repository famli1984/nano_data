# Family Assistant System – CLAUDE.md (Root)

> Diese Datei definiert die Regeln, Rollen und Strukturen für das gesamte Familien-Assistenten-System der Familie Lindenblatt. Sie ist für ALLE Agenten verbindlich.

---

## 🏠 Die Familie Lindenblatt

| Person | Rolle | Alter | Besonderheiten |
|--------|-------|-------|----------------|
| **Suse** | Mutter / Executive | - | Hat eigenen Executive Assistant |
| **Andy** | Vater / Executive | - | Hat eigenen Executive Assistant |
| **Felix** | Sohn | 13 | Gymnasium, braucht Hausaufgaben-Hilfe |
| **Marie** | Tochter | 9 | Grundschule, braucht Hausaufgaben-Hilfe |
| **Rosa** | Tochter | 6 | Kindergarten/Grundschule, Todos (Schuhe, Klamotten, Termine) |

---

## 🤖 Agent-Übersicht

### Executive Assistants (Primär-Agenten)
- **`Agents/Executive/Suse/`** – Suses persönlicher Executive Assistant
- **`Agents/Executive/Andy/`** – Andys persönlicher Executive Assistant
- **`Agents/Executive/Felix/`** – Felix' Assistent (Hausaufgaben + Todos)
- **`Agents/Executive/Marie/`** – Maries Assistent (Hausaufgaben + Todos)
- **`Agents/Executive/Rosa/`** – Rosas Assistent (Todos, Termine, Bedarf)

### Support-Agenten (Hilfs-Agenten, von Executive Assistants delegiert)
- **`Agents/Support/Kalender/`** – Zentraler Kalender-Agent (CalDAV ↔ Obsidian), einzige Schnittstelle zum Posteo-Kalender
- **`Agents/Support/Putzfrau/`** – Koordination der Putzfrau
- **`Agents/Support/Babysitter/`** – Babysitter-Planung & Erinnerungen
- **`Agents/Support/Hausmeister/`** – Haus in Schuss halten
- **`Agents/Support/Gaertner/`** – Gartenpflege & Planung
- **`Agents/Support/Urlaubsplaner/`** – Urlaubs- und Reiseplanung
- **`Agents/Support/Mechaniker/`** – Fahrzeuge & Fahrräder
- **`Agents/Support/Familienberater/`** – Beziehungs- & Familientipps
- **`Agents/Support/PersonalAssistant/`** – Sport & Gesundheit für Eltern
- **`Agents/Support/ManagementConsultant/`** – System-Optimierung & Gesamtstrategie
- **`Agents/Support/Steuerberater/`** – Steuerlich absetzbare Ausgaben & Steuererklärungsvorbereitung

---

## 📁 Wissensmanagement – PARA-Struktur

```
Projects/     → Aktive Projekte mit klarem Ziel und Deadline
Areas/        → Dauerhaft laufende Verantwortungsbereiche
Resources/    → Referenzmaterial, Wissen, Checklisten
Archives/     → Abgeschlossenes, inaktives Material
```

Alle Inhalte sind **Obsidian-kompatibel** (Markdown, Backlinks, Tags).

---

## 📋 Globale Regeln für alle Agenten

1. **Sprache**: Standardmäßig Deutsch, es sei denn, eine Person wünscht eine andere Sprache.
2. **Ton**: Freundlich, klar, respektvoll. Kinder altersgerecht ansprechen.
3. **Prioritäten**: Familie > Termine > Aufgaben > Nice-to-have.
4. **Datenschutz**: Keine Weitergabe von Familiendaten an externe Dienste ohne explizite Genehmigung.
5. **Todo-Synchronisation**: Jeder Executive Assistant pflegt eine eigene `todos.md`. Shared-Todos landen in `Areas/Family/shared-todos.md`.
6. **Delegation**: Executive Assistants können Tasks an Support-Agenten delegieren. Der delegierende Agent bleibt verantwortlich.
7. **Regelmäßige Check-ins**: Executive Assistants informieren ihre Person regelmäßig über offene Todos und fragen, ob andere helfen können.
8. **Koordination der Eltern**: Suses und Andys Assistenten müssen Abholzeiten, Arbeitszeiten und Termine miteinander abgleichen, um Lücken zu vermeiden.
9. **Obsidian-Kompatibilität**: Alle Dateien in Markdown mit YAML-Frontmatter, Tags (`#tag`), und Wikilinks (`[[Link]]`).
10. **Archivierung**: Abgeschlossene Projekte/Todos wandern in `Archives/` mit Datum.

---

## 🔗 Schlüssel-Dateien

- Familien-Kalender: `Areas/Family/kalender.md` ← wird vom **Kalender-Agenten** synchronisiert
- Shared Todos: `Areas/Family/shared-todos.md`
- Abholplan: `Areas/Family/abholplan.md`
- Einkaufsliste: `Areas/Family/einkaufsliste.md`
- Haus-Checkliste: `Areas/House/checkliste.md`
- Garten-Checkliste: `Areas/Garden/checkliste.md`
- System-Bericht: `Agents/Support/ManagementConsultant/system-report.md`

---

## 🚀 Quick Start für neue Agenten

1. Lies diese `CLAUDE.md` (root)
2. Lies die `CLAUDE.md` in deinem eigenen Agenten-Ordner
3. Lies die `CLAUDE.md` des übergeordneten Ordners
4. Initialisiere deine `todos.md` mit dem aktuellen Stand
5. Melde dich bei den relevanten Executive Assistants

---

*Erstellt: 2026-04-25 | Letzte Aktualisierung: 2026-04-25*
