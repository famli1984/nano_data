# 🏠 Family Assistant – Familie Lindenblatt

Ein umfassendes KI-gestütztes Assistenten-System für die Familie Lindenblatt, aufgebaut mit PARA-Wissensmanagement und Obsidian-Kompatibilität.

---

## 🚀 Quick Start

1. Öffne diesen Ordner in [Obsidian](https://obsidian.md) als Vault
2. Lies [`CLAUDE.md`](CLAUDE.md) für eine Übersicht des Gesamtsystems
3. Navigiere zu deinem Agenten-Ordner unter `Agents/Executive/<Name>/`
4. Befülle die kritischen Daten (Arbeitszeiten, Kontakte, Abholplan)

---

## 📁 Struktur

```
Family-assistant/
├── CLAUDE.md                    # System-Übersicht & globale Regeln
├── Projects/                    # Aktive Projekte mit Deadline
├── Areas/                       # Dauerhaft laufende Verantwortungsbereiche
│   ├── Family/                  # Kalender, Todos, Abholplan, Einkauf
│   ├── House/                   # Haus-Wartung & Reinigung
│   ├── Garden/                  # Gartenpflege
│   ├── Vehicles/                # Fahrzeuge & Fahrräder
│   ├── Health/                  # Sport & Gesundheit
│   ├── Finances/                # Familienfinanzen
│   └── School/                  # Schulischer Bereich
├── Resources/                   # Referenzmaterial & Vorlagen
│   ├── Templates/               # Projekt- & Berichtsvorlagen
│   ├── Knowledge/               # Familienwissen
│   └── Checklists/              # Urlaub, Schuljahr, etc.
├── Archives/                    # Abgeschlossenes Material
├── Agents/
│   ├── Executive/               # Primär-Agenten (je Familienmitglied)
│   │   ├── Suse/                # Suses Executive Assistant
│   │   ├── Andy/                # Andys Executive Assistant
│   │   ├── Felix/               # Felix' Assistent (13, Gymnasium)
│   │   ├── Marie/               # Maries Assistentin (9, Grundschule)
│   │   └── Rosa/                # Rosas Assistentin (6, KiGa/Schule)
│   └── Support/                 # Spezialisierte Support-Agenten
│       ├── Putzfrau/            # Reinigungskoordination
│       ├── Babysitter/          # Betreuungsplanung
│       ├── Hausmeister/         # Haus in Schuss halten
│       ├── Gaertner/            # Gartenpflege
│       ├── Urlaubsplaner/       # Reiseplanung
│       ├── Mechaniker/          # Fahrzeuge & Fahrräder
│       ├── Familienberater/     # Familien- & Beziehungstipps
│       ├── PersonalAssistant/   # Sport & Gesundheit Eltern
│       └── ManagementConsultant/# System-Optimierung
└── .obsidian/                   # Obsidian-Konfiguration
```

---

## 👨‍👩‍👧‍👦 Die Familie

| Person | Rolle | Alter | Assistent |
|--------|-------|-------|-----------|
| **Suse** | Mutter / Executive | - | `Agents/Executive/Suse/` |
| **Andy** | Vater / Executive | - | `Agents/Executive/Andy/` |
| **Felix** | Sohn | 13 | `Agents/Executive/Felix/` |
| **Marie** | Tochter | 9 | `Agents/Executive/Marie/` |
| **Rosa** | Tochter | 6 | `Agents/Executive/Rosa/` |

---

## 🔑 Wichtigste Dateien

| Datei | Zweck |
|-------|-------|
| [`CLAUDE.md`](CLAUDE.md) | Globale Regeln & System-Übersicht |
| [`Areas/Family/kalender.md`](Areas/Family/kalender.md) | Familien-Kalender |
| [`Areas/Family/abholplan.md`](Areas/Family/abholplan.md) | Abholplan (täglich prüfen!) |
| [`Areas/Family/shared-todos.md`](Areas/Family/shared-todos.md) | Geteilte Todos |
| [`Agents/Support/ManagementConsultant/system-report.md`](Agents/Support/ManagementConsultant/system-report.md) | System-Status & Empfehlungen |

---

## ✅ Sofort zu erledigen

1. **Arbeitszeiten eintragen** → [`Areas/Family/kalender.md`](Areas/Family/kalender.md)
2. **Abholplan erstellen** → [`Areas/Family/abholplan.md`](Areas/Family/abholplan.md)
3. **Kontakte erfassen** → [`Areas/Family/kontakte.md`](Areas/Family/kontakte.md)
4. **Familienprofil ausfüllen** → [`Resources/Knowledge/family-profile.md`](Resources/Knowledge/family-profile.md)

---

*Powered by PARA + Obsidian + AI Agents*
