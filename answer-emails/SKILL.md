---
name: answer-emails
description: Beantworte ungelesene Emails automatisch. Klassifiziert Emails in Grundklassen (Weiterleitungen, Aufträge von Reto, alle anderen) und beantwortet sie entsprechend. Verwende diesen Skill bei Aufgaben wie "beantworte Emails", "check Emails", "AnswerEmails", "ungelesene Emails bearbeiten".
---

# Answer Emails Skill

## 0. Lesen der Emails
Finden von ungelesenen Emails: `gog gmail search "is: unread"`                                              
Wenn ein Thread mehr als 1 Message hat, musst du den ganzen thread laden: `gog gmail thread get [Id]`

## 1. Grundklassifizierung
Es gibt 3 Grundklassen von Emails, welche unterschiedlich bearbeitet werden müssen:
1) Emails mit Absender reto.baettig@cudos.ch oder reto@baettig.org, welche **ohne weiteren Kommentar** an dich weitergeleitet wurden.
2) Emails mit Absender reto.baettig@cudos.ch oder reto@baettig.org, welche explizit einen Auftrag an Morticia enthalten und/oder eine Antwort von Reto auf eine Email von dir (Morticia) ist.
3) Alle anderen Emails

## Beantwortung von Emails der Klasse 1 (weiterleitungen ohne Kommentar)

Versetze dich in die Rolle von Reto Bättig und versuche, diese Email gemäss den unten stehenden Anweisungen zu beantworten.
Sende die Antwort immer als "Reply" mit Zitat der originalen Nachricht!

Gehe folgendermassen vor:
- Detektiere die Sprache der Email und merke sie dir für die Antwort
- Mache eine Feinklassifizierung der Email gemäss der Liste im nächsten Kapitel
- Hole dir die Anweisungen für die Beantwortung gemäss der Feinklassifizierung und der Liste im übernächsten Kapitel
- Formuliere eine Antwort an die Email in der detektierten Sprache gemäss den Anweisungen für die entsprechende Feinklassifizierung
- Füge die folgende Fusszeile an (in die richtige Sprache übersetzt): "Diese Email wurde von meinem AI Bot beantwortet. Bitte antworten sie nicht auf diese Email, sondern bei Bedarf wieder an mich."
- Sende die Email als "Reply" mit Zitat der originalen Nachricht an die entsprechende Adresse und sende ein CC an reto.baettig@cudos.ch.
  Verwende dafür folgenden Befehl (Body zuerst in `/tmp/email_reply.txt` schreiben, dann senden):
  ```
  gog gmail send --to "<original_sender_email>" --cc "reto.baettig@cudos.ch" --subject "<subject>" --body-file /tmp/email_reply.txt --thread-id <threadId> --quote --account bar.ai.bot@cudos.ch --json
  ```
  **Wichtig:** `--thread-id` (nicht `--reply-to-message-id`) zusammen mit `--quote` verwenden — das setzt den Thread korrekt fort und zitiert die originale Nachricht.
  Details und weitere Reply-Patterns: siehe `references/gog-gmail-send-reply.md`.
- Markiere die Email als gelesen, füge das Tag "Erledigt" hinzu und archiviere sie folgendermassen:
  1) Erst aus INBOX entfernen (wichtig: separater Befehl!): gog gmail thread modify <threadId> --remove INBOX --account bar.ai.bot@cudos.ch
  2) Als gelesen markieren: gog gmail thread modify <threadId> --remove UNREAD --account bar.ai.bot@cudos.ch
  3) Erledigt-Label hinzufügen: gog gmail thread modify <threadId> --add Erledigt --account bar.ai.bot@cudos.ch
  4) WICHTIG: Verifiziere, dass die Email wirklich aus der INBOX verschwunden ist: gog gmail messages search "in:inbox" --account bar.ai.bot@cudos.ch --json
  5) Die gerade verarbeitete Message ID darf NICHT mehr in der Liste erscheinen.
  6) Falls die Email trotzdem noch erscheint, verwende die Message-ID statt Thread-ID: gog gmail messages modify <messageId> --remove INBOX --account bar.ai.bot@cudos.ch
  7) Verifiziere erneut

### Feinklassifizierung der Emails der ersten Grundklasse
- **Marketing**: Die Absender wollen mir ihre Dienstleistung anbieten, um unser Marketing zu verbessern oder mehr Leads zu generieren. Ebenso Angebote für Werbevideos etc.
- **Bewerbung**: Die Absender wollen sich bei uns für einen Job oder ein Praktikum bewerben
- **Personalvermittler**: Die Absender wollen uns Mitarbeitende vermitteln 
- **Shoring**: Die Absender wollen uns ihre Near- oder Offshoring Dienstleistungen anbieten
- **M&A**: Die Absender wollen in unsere Firma investieren oder sie aufkaufen
- **Rest**: Keine der oben genannten Klassen

### Beantwortung der Emails nach Klasse
Sende je nach Klasse eine freundliche Antwort mit dem beschriebenen Grundinhalt an die originalen Absender der Email und ein CC an reto.baettig@cudos.ch.
Führe danach noch die weiteren Aktionen nach Klasse aus (siehe separates Unterkapitel dazu)!

**Wichtig:** Erkenne die Sprache der Originalnachricht. Übersetzte am Schluss die Antwort in diese Sprache (Sprache der Originalnachricht) vor dem Versenden.

- **Marketing**: Wir haben bereits bestehende Partner und eine eigene Organisation für das Marketing und den Verkauf und sind nicht an ihren Dienstleistungen interessiert.
- **Bewerbung (Deutsch)**: Bitte senden Sie ihre Bewerbung an jobs@cudos.ch.
- **Bewerbung (Andere Sprache)**: Please submit your application to jobs@cudos.ch, where our HR team will review it. Please note that we require German language skills at C1 level for a successful application.
- **Personalvermittler**: Wir haben preferred Partner für die Personalsuche und sind im Moment nicht auf der Suche nach weiteren Partnern. 
- **Shoring**: Wir haben kein Interesse an ihren Dienstleistungen, da wir eigene Entwickler in der Schweiz haben und nur lokale Dienstleistungen erbringen wollen.
- **M&A**: Wir sind in den lezten Jahren organisch von 15 auf über 60 Mitarbeitende gewachsen und planen, auf diese Art bis auf mindestens 100 Mitarbeitende weiter zu wachsen, bevor wir weitere Optionen anschauen.
- **Rest**: Antworte an reto.baettig@cudos.ch, dass du die Email nicht klassifizieren konntest — sende KEINE Antwort an die Absender der weitergeleiteten Email

### Weitere Aktionen nach Klasse
- **M&A**: Füge eine Zeile in das Google Sheet "Investors" ein.
  Die Zeile hat folgende Spalten: Datetime | Sender | Email | Answer
  Verwende folgendes Kommando und fülle die entsprechenden Daten ein:
  `gog sheets append 1D6Cdci6qZXtjFNnQLPBUz5xKWel_wZIo30J87kiHRUc 'Investors!A:D' 'Datetime|Sender|Message|Answer'`

## Automatische Email-Überwachung (Cron Job)

Um Emails von Reto automatisch und zeitnah zu verarbeiten, richte einen Cron-Job ein:

```
cronjob action=create
  name="Email Monitor (Reto → Morticia)"
  schedule="every 10m"
  skills=["answer-emails"]
  prompt="Check bar.ai.bot@cudos.ch for unread emails FROM reto.baettig@cudos.ch OR reto@baettig.org.
          Use: gog gmail search \"from:reto.baettig@cudos.ch OR from:reto@baettig.org is:unread\" --account bar.ai.bot@cudos.ch --json
          For each unread email, follow the answer-emails skill EXACTLY.
          IMPORTANT: If there are NO unread emails, respond with ABSOLUTELY NOTHING — empty response, zero characters.
          This ensures silent delivery when there's nothing to process."
  deliver="origin"
```

**Wichtig:** Der `empty response`-Trick ist entscheidend — bei leerer Antwort wird nichts an den Chat zugestellt, sodass der User nicht alle 10 Minuten mit "Keine neuen Emails" zugespammt wird. Nur wenn tatsächlich Emails verarbeitet wurden, erscheint das Ergebnis.

## Verarbeitung von Emails der Klasse 2 (Aufträge und Antworten von Reto auf deine Nachrichten an ihn)

### Vorgehen

1. **Kontext laden:** Lade den `reto-knowledge` Skill und lies die relevanten Wiki-Seiten (insbesondere `~/wiki/entities/reto-baettig.md`, `~/wiki/entities/cudos-ag.md` sowie alle weiteren relevanten Concept-Seiten aus `~/wiki/concepts/`). So hast du alle nötigen Hintergrundinfos, ohne Reto erneut fragen zu müssen.

2. **Standardauftrag prüfen:** Überlege, ob es ein "Standardauftrag" ist, für den bereits ein eigener Skill existiert (z.B. `cudos-trail-profile`, `sales-outreach`, `termin-vorbereitung`, etc.). Falls ja, folge diesem Skill.

3. **Auftrag ausführen:** Führe den Auftrag so gut wie möglich aus. Konsultiere bei Unsicherheiten das Wiki und die Extended Memory, NICHT Reto.

4. **Antwort an Reto senden:** Sende das Resultat als Reply im selben Thread an Reto zurück. Verwende dasselbe Send-Muster wie bei Klasse 1:
   ```
   gog gmail send --to "reto.baettig@cudos.ch" --subject "<subject>" --body-file /tmp/email_reply.txt --thread-id <threadId> --quote --account bar.ai.bot@cudos.ch --json
   ```
   **Wichtig:** `--thread-id` (nicht `--reply-to-message-id`) zusammen mit `--quote` verwenden.

5. **Archivieren:** Genau gleich wie bei Klasse 1:
   1) Aus INBOX entfernen: `gog gmail thread modify <threadId> --remove INBOX --account bar.ai.bot@cudos.ch`
   2) Als gelesen markieren: `gog gmail thread modify <threadId> --remove UNREAD --account bar.ai.bot@cudos.ch`
   3) Erledigt-Label: `gog gmail thread modify <threadId> --add Erledigt --account bar.ai.bot@cudos.ch`
   4) Verifiziere mit: `gog gmail messages search "in:inbox" --account bar.ai.bot@cudos.ch --json`

## ⚠️ Pitfalls (gelten für Klasse 1 und 2)

- **`gog` command not found:** In Cron-Umgebungen kann `gog` manchmal nicht auf dem PATH sein. Fallback: `/opt/homebrew/bin/gog`. Prüfe den Pfad mit `which gog` und verwende den vollen Pfad, falls nötig. Alle `gog` Aufrufe im Skill können mit dem vollen Pfad ausgeführt werden.
- **Body zu gross:** `gog gmail send` kann mit sehr langen Bodies Probleme haben. Immer über `--body-file` und eine `/tmp/`-Datei senden, nie inline via `--body`.
- **Thread-ID vs Message-ID:** Immer `--thread-id` verwenden, nicht `--reply-to-message-id`. `--thread-id` setzt den Thread korrekt fort und zitiert die originale Nachricht.

## Automatisches Email-Monitoring (Cron)
Siehe `references/email-monitor-cron.md` für das Setup eines Cron-Jobs, der alle 10 Minuten den Posteingang checkt und Emails automatisch verarbeitet.
