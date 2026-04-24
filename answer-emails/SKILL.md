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
- Füge die folgende Fusszeile an: "Diese Email wurde von meinem AI Bot beantwortet. Bitte antworten sie nicht auf diese Email, sondern bei Bedarf wieder an mich."
- Sende die Email als "Reply" mit Zitat der originalen Nachricht an die entsprechende Adresse und sende ein CC an reto.baettig@cudos.ch
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

- **Marketing**: Wir haben bereits bestehende Partner und eine eigene Organisation für das Marketing und den Verkauf und sind nicht an ihren Dienstleistungen interessiert.
- **Bewerbung**: Bitte senden Sie ihre Bewerbung an jobs@cudos.ch
- **Personalvermittler**: Wir haben preferred Partner für die Personalsuche und sind im Moment nicht auf der Suche nach weiteren Partnern. 
- **Shoring**: Wir haben kein Interesse an ihren Dienstleistungen, da wir eigene Entwickler in der Schweiz haben und nur lokale Dienstleistungen erbringen wollen.
- **M&A**: Wir sind in den lezten Jahren organisch von 15 auf über 60 Mitarbeitende gewachsen und planen, auf diese Art bis auf mindestens 100 Mitarbeitende weiter zu wachsen, bevor wir weitere Optionen anschauen.
- **Rest**: Antworte an reto.baettig@cudos.ch, dass du die Email nicht klassifizieren konntest — sende KEINE Antwort an die Absender der weitergeleiteten Email

### Weitere Aktionen nach Klasse
- **M&A**: Füge eine Zeile in das Google Sheet "Investors" ein.
  Die Zeile hat folgende Spalten: Datetime | Sender | Email | Answer
  Verwende folgendes Kommando und fülle die entsprechenden Daten ein:
  `gog sheets append 1D6Cdci6qZXtjFNnQLPBUz5xKWel_wZIo30J87kiHRUc 'Investors!A:D' 'Datetime|Sender|Message|Answer'`

## Verarbeitung von Emails der Klasse 2 (Aufträge und Antworten von Reto auf deine Nachrichten an ihn)
Überlege zuerst, ob der Auftrag ein "Standardauftrag" ist, für welchen bereits ein Tool in /home/reto/.openclaw/workspace/TOOLS.md existiert.
Insbesondere sind für folgende Aufträge detaillierte Prompts in /home/reto/.openclaw/workspace/prompts vorhanden, die du ausführen kannst:
- Generate Weekly Report → /home/reto/.openclaw/workspace/prompts/WeeklyReportPrompt.md
- Send Cudos Trail (CT) Profiles → /home/reto/.openclaw/workspace/prompts/CudosTrailProfile.md
- Check Invoices → Check TOOLS.md for instructions

Versuche den Auftrag so gut wie möglich auszuführen und melde den Fortschritt per Email an reto.baettig@cudos.ch und an den aktiven Telegram Kanal von Reto.
