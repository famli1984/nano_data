# Kapitel 2: Die wichtigsten KI-Begriffe einfach erklärt

> Du musst keine Informatikerin oder Informatiker sein – aber ein paar Grundbegriffe helfen dir, KI-Tools besser zu verstehen und gezielter einzusetzen.

---

## LLM – Large Language Model

Ein **Large Language Model** (kurz: LLM) ist das Herzstück moderner KI-Assistenten wie Claude, ChatGPT oder Gemini.

Stell dir ein LLM wie einen extrem belesenen Gesprächspartner vor: Er hat riesige Mengen an Texten gelesen – Bücher, Artikel, Webseiten – und gelernt, wie Sprache funktioniert. Er kann daraus Antworten, Texte und Ideen erzeugen, die sinnvoll und flüssig klingen.

**Wichtig zu verstehen:**
- Ein LLM erfindet keine Fakten – aber es kann plausibel klingende falsche Aussagen machen (das nennt man „Halluzinieren"). Prüfe wichtige Fakten immer nach.
- Ein LLM hat keine echte Meinung oder Gefühle – es erkennt sprachliche Muster und antwortet entsprechend.
- Aktualität: Die meisten LLMs haben ein Wissensdatum (z. B. „Trainingsdaten bis Oktober 2024"). Für sehr aktuelle Informationen brauchst du ein Tool mit Internetsuche (wie Perplexity).

---

## Prompt

Ein **Prompt** ist deine Eingabe an die KI – also das, was du in das Chatfenster tippst.

Die Qualität deines Prompts beeinflusst die Qualität der Antwort erheblich. Ein guter Prompt:
- Erklärt den **Kontext** (z. B. „Ich bin Lehrerin für Biologie in der 9. Klasse")
- Beschreibt die gewünschte **Aufgabe** klar
- Gibt bei Bedarf ein **Format** vor (z. B. „Erstelle eine Tabelle" oder „Schreib in einfacher Sprache")
- Nennt die **Zielgruppe** (z. B. „für Schüler mit Lernschwäche")

**Beispiel – schlechter Prompt:**
> „Klausur erstellen"

**Beispiel – guter Prompt:**
> „Erstelle eine Klausur zum Thema Fotosynthese für die 9. Klasse Gymnasium. Die Klausur soll 45 Minuten dauern und aus drei Teilen bestehen: Multiple Choice (10 Fragen), Lückentext (5 Sätze) und einer Freitextaufgabe. Schwierigkeitsgrad: mittelschwer."

---

## Kontext / Context Window

Das **Context Window** ist der „Arbeitsspeicher" der KI – die Menge an Text, die sie auf einmal lesen und verarbeiten kann.

Moderne LLMs haben sehr große Context Windows (oft 100.000 Wörter oder mehr). Das bedeutet:
- Du kannst lange Dokumente komplett einfügen
- Die KI erinnert sich an alles, was im aktuellen Gespräch steht
- Aber: Wenn du ein neues Gespräch startest, ist der Kontext weg – die KI kennt keine Informationen aus früheren Chats (außer du hast ein Memory eingerichtet, dazu mehr in Kapitel 8)

**Praktisch für Lehrer:** Du kannst ein ganzes Schulbuchkapitel, eine Lehrplaneinheit oder deine eigenen Unterrichtsmaterialien in die KI einfügen – sie arbeitet dann damit.

---

## Token

Ein **Token** ist die kleinste Einheit, in die die KI Text zerlegt – ungefähr 3–4 Zeichen oder etwa ¾ eines durchschnittlichen Worts.

Warum ist das relevant?
- Viele KI-Dienste rechnen die Kosten in Tokens ab (Eingabe + Ausgabe)
- Sehr lange Eingaben (z. B. ein ganzes Buch) verbrauchen viele Tokens
- Bei kostenpflichtigen Tarifen gibt es oft ein monatliches Token-Kontingent

**Als Lehrer musst du Tokens nicht zählen** – aber es erklärt, warum manchmal Nutzungslimits entstehen.

---

## Agent

Ein **Agent** ist eine KI, die nicht nur antwortet, sondern auch selbstständig handelt: Sie kann Aufgaben planen, Werkzeuge benutzen, Dateien öffnen, im Internet suchen und mehrere Schritte nacheinander ausführen – ohne dass du jeden Schritt vorgeben musst.

**Beispiel ohne Agent:**
> Du: „Wie kann ich diese Unterrichtseinheit verbessern?"
> KI: „Hier sind fünf Vorschläge: …"

**Beispiel mit Agent:**
> Du: „Erstelle aus meinem Ordner ‚Biologie Klasse 9' eine komplette Unterrichtseinheit zu Fotosynthese mit Arbeitsblättern und einer Klausur."
> Agent: öffnet den Ordner → liest die Dateien → erstellt die Unterrichtseinheit → legt neue Dateien an

Der Agent erledigt mehrere Schritte selbstständig. Du gibst das Ziel vor, er kümmert sich um den Weg.

---

## Multi-Agenten-System

Ein **Multi-Agenten-System** besteht aus mehreren KI-Agenten, die zusammenarbeiten – jeder ist auf eine Aufgabe spezialisiert.

**Beispiel:**
- Agent 1 (Recherche): Sucht aktuelle Informationen zum Thema im Internet
- Agent 2 (Autor): Schreibt daraus einen Lehrtext für die 8. Klasse
- Agent 3 (Prüfer): Überprüft den Text auf Fehler und passt ihn an den Lehrplan an

In der Praxis begegnen dir Multi-Agenten-Systeme z. B. wenn du einem KI-Tool sagst: „Bereite eine komplette Unterrichtsstunde vor" – im Hintergrund arbeiten dann mehrere spezialisierte Prozesse zusammen.

Als Lehrer musst du diese Systeme nicht selbst bauen – aber du wirst sie nutzen, ohne es zu merken.

---

## RAG – Retrieval Augmented Generation

**RAG** bedeutet: Die KI antwortet nicht nur aus ihrem trainierten Wissen, sondern sucht sich zusätzlich Informationen aus einer bestimmten Quelle heraus (z. B. deinen eigenen Dokumenten).

**Vereinfacht:** Du gibst der KI einen Ordner mit deinen Unterrichtsmaterialien. Statt aus dem Gedächtnis zu antworten, schaut sie zuerst in deine Dokumente – und gibt dann eine Antwort, die auf deinen eigenen Inhalten basiert.

Das ist genau das, was passiert, wenn du Claude Code Zugriff auf deinen Materialordner gibst (→ Kapitel 4).

---

## MCP – Model Context Protocol

**MCP** ist ein technischer Standard, der es KI-Assistenten ermöglicht, mit externen Tools und Programmen zu kommunizieren – zum Beispiel mit deinem Kalender, deiner E-Mail, einer Datenbank oder dem Internet.

Ohne MCP: Die KI lebt in einer Blase und kennt nur das, was du ihr schreibst.

Mit MCP: Die KI kann Werkzeuge benutzen – Termine abrufen, Dateien lesen, im Web suchen, Formulare ausfüllen.

Als Lehrer wirst du MCP-fähige Tools nutzen (z. B. Internetsuche in Perplexity, Dateizugriff in Claude Code), ohne dich mit dem technischen Hintergrund beschäftigen zu müssen. Es erklärt aber, warum manche KI-Tools so viel mehr können als andere.

---

## Skill (in Claude Code)

Ein **Skill** ist ein gespeicherter Ablauf, den du immer wieder aufrufen kannst.

Stell dir vor, du erstellst einmal einen guten Prompt für „Klausur aus Unterrichtsmaterial generieren". Mit einem Skill kannst du diesen Ablauf abspeichern und mit einem einzigen Befehl jederzeit wiederverwenden – für neue Themen, neue Klassen, neue Materialien.

Mehr dazu in Kapitel 5.

---

## Fine-Tuning (kurz erklärt)

**Fine-Tuning** bedeutet, ein bestehendes KI-Modell mit eigenen Daten weiterzutrainieren, damit es auf ein bestimmtes Fachgebiet oder einen bestimmten Stil spezialisiert ist.

Für den Schulalltag ist Fine-Tuning kaum relevant – es ist technisch aufwändig und teuer. Erwähnenswert ist es, weil du den Begriff in Diskussionen über KI hören wirst. Als Lehrerin oder Lehrer arbeitest du mit fertigen Modellen – und die sind für deine Zwecke mehr als ausreichend.

---

## Auf einen Blick: Die Begriffe

| Begriff | Kurzerklärung |
|---------|--------------|
| **LLM** | Das KI-Modell selbst – hat viele Texte gelesen und kann Sprache erzeugen |
| **Prompt** | Deine Eingabe an die KI |
| **Context Window** | Der „Arbeitsspeicher" der KI für das aktuelle Gespräch |
| **Token** | Kleinste Texteinheit – Grundlage für Kosten und Limits |
| **Agent** | KI, die selbstständig mehrere Schritte ausführt |
| **Multi-Agenten-System** | Mehrere spezialisierte KI-Agenten, die zusammenarbeiten |
| **RAG** | KI antwortet auf Basis deiner eigenen Dokumente |
| **MCP** | Schnittstelle, die KI mit externen Tools verbindet |
| **Skill** | Gespeicherter, wiederverwendbarer Ablauf |
| **Fine-Tuning** | Weitertraining eines Modells auf spezifische Daten |

---

*Weiter mit Kapitel 3: GitHub Copilot einrichten →*
