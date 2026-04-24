---
name: daily-sales-input
description: Erstelle einen täglichen Sales-Input mit 1-2 konkreten Firmenkontakten für Cudos AG (Kalt- oder Warmakquisition), inklusive CRM-Check, Moneyhouse-Recherche und Email-Versand. Verwende diesen Skill für "Daily Sales Input", "täglicher Sales Input", "Sales Input erstellen", oder wenn der Cronjob ausgeführt wird.
---

# Daily Sales Input

Dieser Skill wird täglich ausgeführt (Cronjob).

## AUFGABE
Erstelle einen täglichen Sales-Input für Cudos AG.
1. Suche nach aktuellen News/Trigger (verwende google-ai-search oder Web-Suche nach Unternehmen in der Region Zürich, die IT-Projekte, Digitalisierung, Software-Entwicklung oder AI-Integration starten könnten)
2. Prüfe, was wir zu der Firma im CRM schon wissen 
3. Recherchiere gefundene Firmen mit Moneyhouse (~/Development/mb_tools_bar/moneyhouse-scraper/moneyhouse_scraper.py) und Google AI Search
4. Filter: Mindestens 200k CHF/Jahr Potential, max 60min von Zürich erreichbar
5. Wähle 1-2 Firmen aus und erstelle einen konkreten Sales-Input

## Sales-Input Format

Erstelle für jede identifizierte Firma:

```
════════════════════════════════════════════════════════════════
🎯 FIRMA: [Name der Firma]
════════════════════════════════════════════════════════════════

👤 KONTAKT
   Firma:        [Name]
   Adresse:      [Strasse], [PLZ] [Ort]
   Entfernung:   ~[XX] Minuten von Zürich
   Mitarbeitende: [XXX]
   Branche:      [Branche]

   Kontaktpersonen:
   → [Name] ([Position])

💰 POTENTIAL: [XXX-XXXk CHF/Jahr]
   [Beschreibung der möglichen Dienstleistungen]

🎣 AUFHÄNGER / TRIGGER
   [News/Auslöser, warum jetzt kontaktiert werden sollte]

📊 RECHERCHE
   Quellen: [Moneyhouse / News / CRM]

✅ EMPFEHLUNG
   [Konkrete empfohlene Aktion]
```

## OUTPUT
- Schreibe den Sales-Input in memory/sales-logbook.md (neuester Eintrag oben)
- Sende eine Email an reto.baettig@cudos.ch mit:
  * Betreff: "Sales Input [Datum]"  
  * Firma(n) mit Kontaktdaten  
  * Aufhänger/Trigger warum jetzt  
  * Geschätztes Potential  
  * Empfohlene nächste Aktion  
  * Recherche-Quellen
- Falls keine geeignete Firma gefunden wird, schreibe "Kein passender Sales-Input für heute" ins Logbuch und sende keine Email.

## QUALITÄTSKRITERIEN (Stand: 17.03.2026)

### ❌ Ausschlusskriterien
- **Keine kleinen Software-Dienstleister** — diese sehen uns in der Regel als Konkurrenten oder mögliche Kunden, nicht als Partner

### ✅ Pflicht-Checks vor jedem Sales-Input
1. **CRM-Check:** Existiert die Firma bereits im CRM?
2. **CRM-Historie:** Was sind die letzten Kommentare zur Firma?
3. **CRM-Potentiale:** Gibt es offene/geschlossene Potentiale?
4. **Mehr Infos:** Ausführlichere Firmeninfos direkt im Sales-Input liefern

### 🔄 Strategie: Warm/Kalt-Wechsel
- **Abwechselnd vorschlagen:**
  - **Warmakquisition:** Firmen mit bestehendem CRM-Kontakt (Kommentare, Potentiale)
  - **Kaltakquisition:** Neue Firmen ohne CRM-Eintrag oder ohne Aktivität

### 📊 Effiziente Recherche
- **Token-sparender Ansatz:** 20-40 zufällige Firmen aus dem CRM prüfen
- Plus: News-Monitoring für Trigger-Ereignisse

### 📧 Follow-up / Nachfass-Emails (bei Nicht-Antwort)
Sollte nach 1 Woche keine Antwort kommen, kann ein solches "Nummeriertes" Nachfass-Email verwendet werden:

## Google Sheet Tracking

**WICHTIG:** Jeder Sales-Input MUSS im Google Sheet erfasst werden!

- **Sheet ID:** `17kJpnryrYEOdgLdbFux_naG6sTtTUXIiuqe2ywgj9c4`
- **Tab:** `Log`
- **Spalten:** A: Firma | B: Kontaktperson | C: Email | D: Datum (Vorschlag) | E: Nachfass Email (Datum) | F: Antwort Datum | G: Antwort [positiv|negativ]

```bash
gog sheets append 17kJpnryrYEOdgLdbFux_naG6sTtTUXIiuqe2ywgj9c4 'Log!A:G' --values-json '[["Firma","Kontaktperson","Email","2026-03-24","","",""]]'
```

## 5. Bei Feedback von Reto
1. Aktualisiere die entsprechende Zeile im Google Sheet
2. Trage das Feedback in das Memory ein
3. Lerne daraus für zukünftige Vorschläge

## Ausgabe
Sende den Sales Input per Email an: reto.baettig@cudos.ch

```
Grüezi [Name]

Ich will Sie nicht belästigen, eine kurze Antwort aus einer Zahl würde mich freuen:
1) Wir haben keinen Bedarf für Individualsoftware-Dienstleistungen und Digitalisierung, bitte melden Sie sich nicht mehr
2) Wir sind zufrieden mit unseren bestehenden Partnern, bitte melden Sie sich nicht mehr
3) Im Moment haben wir andere Prioritäten, bitte melden Sie sich in 6 Monaten wieder
4) Danke für den Reminder, ich mache einen Termin ab ;-) 25min Meeting mit Reto

Freundliche Grüsse und eine gute Woche,
Reto Bättig
```

## LERNEN
- Lerne täglich dazu — entweder durch selbst entdeckte Verbesserungen oder durch Feedback des Users
- **WICHTIG:** Falls Feedback zum Sales Input kommt, baue das Feedback in dieses Dokument ein (DailySalesInput.md), NICHT in MEMORY.md
- Dieses Dokument ist die zentrale Anlaufstelle für alle Sales-Input-Anweisungen und Qualitätskriterien
