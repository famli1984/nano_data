# Kapitel 1: KI-Lösungen im Überblick

> Welche Tools gibt es, was kosten sie – und was musst du beim Datenschutz beachten?

---

## Warum KI jetzt auch für Lehrer relevant ist

Künstliche Intelligenz ist kein Zukunftsthema mehr – sie ist im Schulalltag angekommen. KI kann dir helfen, Unterrichtsmaterialien schneller zu erstellen, Texte zu überarbeiten, Erklärungen zu differenzieren oder Ideen zu entwickeln. Das spart Zeit, die du für das Wesentliche nutzen kannst: deine Schülerinnen und Schüler.

Dieses Kapitel gibt dir einen ehrlichen Überblick über die wichtigsten Tools, was sie können, was sie kosten – und worauf du beim Thema Datenschutz achten musst.

---

## Die wichtigsten Tools auf einen Blick

| Tool | Beschreibung | Kosten | Datenschutz | Empfehlung |
|------|-------------|--------|-------------|------------|
| **Claude Code** | KI-Assistent mit Dateizugriff, stark beim Schreiben und Strukturieren | $20/Monat (Pro) | Server in USA, SCCs vorhanden | ⭐ Sehr gut für Lehrer |
| **Perplexity** | KI mit Echtzeit-Internetsuche, ideal für Recherche | Kostenlos / $20/Monat (Pro) | Server in USA | ⭐ Gut für Recherche |
| **GitHub Copilot** | KI-Assistent in VS Code, läuft lokal, viele Modelle wählbar | Kostenlos (limitiert) / $10–39/Monat | Server in USA / lokal möglich | Gut für Technik-affine |
| **Google Gemini Advanced** | Googles KI, direkt im Browser und in Google Workspace integriert | $19,99/Monat (inkl. 2 TB Drive) | EU-Datenverarbeitung möglich | Gut wenn du Google Workspace nutzt |
| **Lokale Modelle** (Ollama, LM Studio) | KI läuft direkt auf deinem Computer, keine Daten nach außen | Kostenlos | ✅ DSGVO-sicher | Für Datenschutz-Bewusste |

---

## Die Tools im Detail

### Claude Code / Claude.ai

Claude ist der KI-Assistent von Anthropic. Er ist besonders stark beim Schreiben, Strukturieren und beim Umgang mit langen Texten – ideal für Unterrichtsvorbereitung.

**Was kann Claude für Lehrer?**
- Unterrichtsmaterialien, Arbeitsblätter und Klausuren erstellen
- Texte zusammenfassen oder vereinfachen (z. B. für unterschiedliche Niveaus)
- Feedback zu Texten geben
- Auf eigene Dateien und Ordner zugreifen und daraus Inhalte erzeugen (über Claude Code)
- Eigene Abläufe als sogenannte „Skills" speichern und wiederholen

**Kosten:**
- Claude.ai Pro: **$20/Monat** – beinhaltet Claude Code und Zugriff auf alle aktuellen Modelle
- Kostenloser Einstieg möglich, aber mit deutlich eingeschränktem Kontingent

**Datenschutz:** Anthropic verarbeitet Daten auf Servern in den USA. Es gibt Standard-Vertragsklauseln (SCCs) gemäß DSGVO. Für eigene Unterrichtsvorbereitung grundsätzlich nutzbar – **keine Schülerdaten eingeben** (siehe Datenschutz-Abschnitt unten).

---

### Perplexity

Perplexity ist eine KI-Suchmaschine: Sie beantwortet Fragen und sucht dabei direkt im Internet – mit Quellenangaben. Das macht sie besonders nützlich für aktuelle Recherchen.

**Was kann Perplexity für Lehrer?**
- Aktuelle Informationen zu Themen finden und zusammenfassen
- Quellenbasierte Antworten – du siehst immer, woher die Information kommt
- Schnelle Hintergrundinformationen zu Unterrichtsthemen
- Bilder und Videos in die Suche einbeziehen

**Kosten:**
- **Kostenlos**: Grundfunktionen mit begrenzten Pro-Suchen täglich
- **Pro: $20/Monat** – unbegrenzte KI-gestützte Suchen, bessere Modelle
- **Education-Rabatt**: Für Lehrkräfte an Hochschulen gibt es vergünstigte Tarife (~$10/Monat)

**Datenschutz:** Server in den USA. Kein Speichern von Schülerdaten.

---

### GitHub Copilot

GitHub Copilot ist ursprünglich für Programmiererinnen und Programmierer entwickelt worden – aber er läuft direkt auf deinem Desktop (in VS Code) und kann dort auf **alle deine lokalen Dateien** zugreifen. Das macht ihn auch für Nicht-Programmierer interessant.

**Was kann GitHub Copilot für Lehrer?**
- Auf lokale Ordner und Dokumente zugreifen (auf deinem Computer)
- Aus Unterrichtsmaterial zusammenfassen, umformulieren, Klausuren erstellen
- Verschiedene KI-Modelle wählbar (auch Claude, Gemini, GPT-4 über Copilot)
- Läuft in VS Code – einem kostenlosen Editor

**Kosten:**
- **Kostenlos**: Sehr limitiert (begrenzte Anfragen pro Monat)
- **Pro: $10/Monat** – für den Einstieg ausreichend
- **Pro+: $39/Monat** – für Power-User
- Hinweis: Ab Juni 2026 wechselt GitHub Copilot auf nutzungsbasierte Abrechnung (AI Credits)

**Vorteil:** Da die Verarbeitung teilweise lokal möglich ist und du keine Daten aktiv hochladen musst, ist die Datenschutz-Situation günstiger als bei Cloud-Diensten.

---

### Google Gemini Advanced

Google Gemini ist Googles KI-Angebot. Besonders praktisch: Es ist direkt in Google Workspace (Docs, Gmail, Drive) integriert.

**Was kann Gemini für Lehrer?**
- Direkt in Google Docs: Texte überarbeiten, zusammenfassen, ausformulieren
- In Gmail: E-Mails vorschlagen lassen
- In Google Drive: Dokumente durchsuchen und zusammenfassen
- Aktuelle Informationen über die Google-Suche einbeziehen

**Kosten:**
- **Google One AI Premium: $19,99/Monat** – inklusive 2 TB Google Drive Speicher
- Für Schulen mit Google Workspace for Education: als Add-on buchbar ($14–30/User/Monat)

**Datenschutz:** Google bietet für Workspace-Nutzer EU-Datenverarbeitung an. Für Schulen mit offizieller Google Workspace-Lizenz oft DSGVO-konformer als private Nutzung.

---

### Lokale Modelle: Ollama & LM Studio

Wer auf maximale Datensicherheit setzt, kann KI-Modelle direkt auf dem eigenen Computer laufen lassen. Die Daten verlassen dabei niemals deinen Rechner.

**Tools:**
- **Ollama**: Einfaches Installieren und Ausführen von KI-Modellen – für die Kommandozeile
- **LM Studio**: Grafische Oberfläche zum Ausprobieren lokaler Modelle – auch für Einsteiger geeignet

**Verfügbare Modelle:** Llama 3 (Meta), Mistral, Phi-4 (Microsoft) u. v. m.

**Kosten:** Kostenlos – du brauchst aber einen halbwegs modernen Computer (mind. 8 GB RAM)

**Für Lehrer geeignet?** Ja, wenn Datenschutz oberste Priorität hat – z. B. beim Umgang mit Schülertexten. Einschränkung: Lokale Modelle sind langsamer und weniger leistungsstark als Cloud-Modelle.

---

## Datenschutz & Sicherheit

Dies ist eines der wichtigsten Themen beim KI-Einsatz in der Schule. Hier die wichtigsten Punkte:

### Deine eigenen Daten

- Alles, was du in eine KI eingibst, wird (zumindest temporär) auf den Servern des Anbieters verarbeitet.
- Bei den meisten kostenpflichtigen Tarifen werden deine Eingaben **nicht** zum Training der KI verwendet – prüfe das aber in den jeweiligen Datenschutzeinstellungen.
- **Empfehlung:** Aktiviere in den Einstellungen die Option, dass deine Daten nicht für Trainings verwendet werden (meist als „Data not used for training" oder ähnlich bezeichnet).

### Schülerdaten – hier ist besondere Vorsicht geboten

> ⚠️ **Grundregel: Gib niemals personenbezogene Daten von Schülerinnen und Schülern in Cloud-KI-Dienste ein.**

Das betrifft:
- Namen in Kombination mit Leistungsdaten
- Zensuren oder Benotungen zu identifizierbaren Personen
- Adressen, Geburtsdaten oder andere persönliche Informationen
- Fotos von Schülern

**Warum?** Cloud-KI-Dienste verarbeiten Daten auf Servern im Ausland (meist USA). Eine Übermittlung personenbezogener Daten dorthin ist nach DSGVO nur unter bestimmten Voraussetzungen zulässig – und für Schulen in der Regel nicht ohne ausdrückliche Genehmigung der Schulverwaltung.

### Was ist erlaubt?

- Unterrichtsmaterialien erstellen, ohne Schülerbezug
- Eigene Texte überarbeiten lassen
- Allgemeine Unterrichtsideen entwickeln
- Anonymisierte Texte (ohne Namen, ohne erkennbare Merkmale) bearbeiten lassen

### Was tun bei Unsicherheit?

1. Frag die Datenschutzbeauftragte/den Datenschutzbeauftragten deiner Schule
2. Nutze lokale Modelle (Ollama, LM Studio) für sensible Aufgaben
3. Verwende ausschließlich anonymisierte oder selbst erstellte Beispieltexte

---

*Weiter mit Kapitel 2: Was ist eigentlich ein LLM? →*
