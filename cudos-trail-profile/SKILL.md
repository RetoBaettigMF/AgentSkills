---
name: cudos-trail-profile
description: Erstelle und versende personalisierte Email-Vorlagen mit passenden CudosTrail-Kandidatenprofilen (PDFs) an Kunden. Verwende diesen Skill bei Aufgaben wie "CudosTrail Profile senden", "Juniors anbieten", "Profile für Kunden", "CT Profile".
---

# CudosTrail Profile versenden

Dieser Skill dient dazu, eine personalisierte Email zu erstellen, um unseren Kunden vom Cudos Trail (Nachwuchsförderungsprogramm für Software Engineers) passende Profile von unseren Juniors anzubieten.

Die Hauptaufgabe ist es, aufgrund eines Emails mit Anweisungen eine passende Email für den Kunden zu entwerfen und dem Absender des Emails mit den Anweisungen zurückzusenden, damit er es forwarden kann an den Kunden.

## Vorgehen

1. Falls die Email Anhänge hat, lade diese herunter und wandle sie in ein lesbares Format (z.B. Markdown) um
2. Falls die Email Links zu mehr Informationen (z.B. Jobprofil) hat, lade diese Informationen herunter
3. Lies die Anweisungen im Email und die Information in den Links und Anhängen genau. Was ist das gesuchte Profil? Welches Know-How müssten die Juniors mitbringen?
4. Hole die Profile vom Google Drive:
   ```bash
   gog drive ls --parent 1zCmCS-ipO9LMCv_B1oyBEzwHrFFE13nR --max 200 | grep ".pdf"
   ```
5. Lies die entsprechenden Profile und mache eine kurze Zusammenfassung (3-4 Zeilen), warum sich der Kandidat gut eignet
6. Formuliere eine Email ähnlich wie das Muster unten
   - **WICHTIG:** Die Email muss so formuliert sein, dass sie unverändert weitergeleitet werden kann. Es muss z.B. "Hoi {Empfänger}" stehen und am Schluss "Herzliche Grüsse, Reto". KEINE Kommentare, die entfernt werden müssten.
7. Hänge die passenden Profile (PDFs) direkt an die Email an — **KEINE Links auf Google Drive**, sondern PDFs als Anhang einbetten
8. Sende die Email **inklusive Attachments** zurück an Reto, damit er sie weiterleiten kann
9. Markiere die Email mit dem Auftrag als erledigt:
   ```bash
   gog gmail thread modify <threadId> --add Erledigt --remove INBOX --remove UNREAD
   ```

## Beispiel-Email

```
Hoi {Empfänger}

Schön, dass ihr euch für unsere Juniors interessiert.

Ich hätte dir folgende Kandidaten zu bieten, welche passen könnten:

Timos Papidas: Verfügbar ab 1.4.
- Fundierte C# Erfahrungen
- Erste Angular Erfahrungen
- IT und DevOps Erfahrungen
- Super typ, selbständig, sehr fit, arbeitet sich überall schnell ein

Florian Leuenberger: Verfügbar ab 1.5.
- Fundierte Embedded und C++ Erfahrungen
- Erfahrungen mit C# und Angular
- Super typ, selbständig, sehr fit, arbeitet sich überall schnell ein

Jonas Degelo: Verfügbar ab 1.5.
- Fundierte Fullstack Erfahrungen (Vor allem React, NodeJS)
- Müsste C# noch auffrischen
- Super typ, selbständig, sehr fit, arbeitet sich überall schnell ein ;-)

Im Cudos Trail Stundensatz ist die Einarbeitung in neue Technologien inbegriffen, d.h. wir würden bei allen - sofern nötig - vorgängig noch eine Grundausbildung in C# und Angular organisieren und ggf. auch während der Einarbeitungszeit noch ein Budget zur Verfügung stellen, das euch nicht verrechnet wird, damit die Juniors sich richtig fundiert einarbeiten können.

Falls du einen oder zwei der Kandidaten gerne mal ganz unverbindlich kennenlernen möchtest, können wir das sehr gerne organisieren.

Noch ganz kurz zusammengefasst die Bedingungen im Cudos Trail:
- Einsatz für 6 oder 12 Monate 
- Stundensatz Fr. 120 (alles inklusive, spesen, mentoring, weiterbildung, grundausbildung etc. wird alles nicht verrechnet. Nur die "produktiven" Stunden bei euch vor Ort werden verrechnet)

Bei Fragen einfach melden.

Ich habe noch Marianne und Rachel, die Co-Leiterinnen des Cudos-Trails in's CC genommen, du kannst dich auch jederzeit bei ihnen melden.

Herzliche Grüsse und einen schönen Abend,

Reto
```
