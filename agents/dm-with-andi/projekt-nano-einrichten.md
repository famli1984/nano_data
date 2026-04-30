---
tags: [project, nano, setup, pauline]
last_updated: 2026-04-30
---

# Projekt: Nano / Pauline einrichten

Alles was nötig ist, damit Pauline (Nano) vollständig funktioniert.

## Setup-Aufgaben

- [ ] **Terminal einrichten an Andis Handy** — Zugang zu Pauline via Terminal-App
- [ ] **Berliner Zeitzone** — im Admin Panel auf Europe/Berlin einstellen (Andy)
- [ ] **Sprachnachrichten (Signal)** — Signal-Bridge muss Audio-Anhänge weiterleiten; aktuell nur "[Voice Message]" — Admin-Aufgabe
- [ ] **Bilder verarbeiten (Signal)** — Anhänge liegen unter `/home/nano2/...`, kein Zugriff für Pauline; Signal-Bridge muss Dateien in shared Pfad unter `/workspace/` kopieren — Admin-Aufgabe (identisches Problem wie Sprachnachrichten)
- [ ] **Posteo Kalender einrichten** — CalDAV-Zugang aktivieren damit Pauline Termine sehen/eintragen kann
- [ ] **Posteo Mailadresse einrichten** — IMAP/SMTP konfigurieren

## Funktionen & Workflows

- [ ] **Arbeits-Update-Kanal** — Weg einrichten, damit Pauline regelmäßige Updates zu Arbeitsaufgaben auf Andis Arbeitsaccount schickt
- [ ] **Proaktive Erinnerungen** — Konzept entwickeln: wann und wie erinnert Pauline Andi an offene Dinge (täglich? auf Anfrage? per Scheduler?)
- [ ] **Felix: Blumengießen-Erinnerung** — In Garten-Checkliste / Gärtner-Agent als wiederkehrende Erinnerung einrichten

## Kinder-Kanäle

- [ ] **Felix-Subagent einrichten** — eigenen Agenten in Felix' Kanal setzen, der keinen Zugriff auf Familien-/Elterndaten hat (isolierter Workspace)

## Wunsch-Features

- [ ] **Text-to-Speech / Sprachnachrichten generieren** — Andi möchte dass Pauline Witze etc. vorlesen kann; TTS-System einrichten (z.B. Piper TTS, ElevenLabs)

## Erledigt

_(noch nichts)_
