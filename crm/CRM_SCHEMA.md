# CRM Schema Reference

Dieses Dokument beschreibt alle Tabellen, Felder und gültigen Auswahlwerte des berliCRM.  
Verwende es als Nachschlagewerk beim Formulieren von Queries.

---

## Tabellen-Übersicht

| Modul | ID-Präfix | Beschreibung |
|---|---|---|
| `Accounts` | `3x…` | Firmen / Organisationen |
| `Contacts` | `4x…` | Personen / Ansprechpartner |
| `Potentials` | `5x…` | Verkaufschancen / Projekte |
| `ModComments` | `29x…` | Kommentare (zu Accounts, Contacts, Potentials) |

---

## Tabelle: Accounts (Firmen)

### Standardfelder

| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | ID | CRM-ID, Format `3x<N>` |
| `account_no` | Text | Interne Nummer (z.B. `ACC5085`) |
| `accountname` | Text | **Firmenname** – primäres Suchfeld |
| `accounttype` | Auswahl | Firmentyp → siehe Auswahlwerte |
| `industry` | Auswahl | Branche → siehe Auswahlwerte |
| `phone` | Text | Haupttelefon |
| `fax` | Text | Fax |
| `otherphone` | Text | Weitere Telefonnummer |
| `email1` | Text | Haupt-E-Mail |
| `email2` | Text | Zweite E-Mail |
| `website` | Text | Website (ohne `https://`) |
| `employees` | Zahl | Mitarbeiterzahl (offizielle Angabe) |
| `tickersymbol` | Text | Börsenkürzel |
| `bill_street` | Text | Strasse |
| `bill_city` | Text | Stadt |
| `bill_code` | Text | PLZ |
| `bill_country` | Text | Land (z.B. `Schweiz`, `Deutschland`) |
| `bill_pobox` | Text | Postfach |
| `buyerreference` | Text | Käufer-Referenz |
| `description` | Text | Freie Beschreibung |
| `account_id` | ID | Übergeordnete Firma (Muttergesellschaft) |
| `assigned_user_id` | ID | Zuständiger Benutzer → Benutzer-Tabelle |
| `createdtime` | Datum | Erstellungsdatum (`YYYY-MM-DD HH:MM:SS`) |
| `modifiedtime` | Datum | Letzte Änderung |
| `modifiedby` | ID | Zuletzt geändert von |

### Custom Fields (cf_) – Accounts

| Feld | Name | Typ | Auswahlwerte / Hinweise |
|---|---|---|---|
| `cf_615` | SW-Engineering Potential | Auswahl | `0 - abklären`, `1 - High Potential`, `2 - Regelmässig Nachfassen`, `3 - Wenig Potential`, `4 - Kein Potential`, `D - Kein Potential` |
| `cf_632` | AI Potential | Auswahl | `0 - abklären`, `1 - High Potential`, `2 - Regelmässig Nachfassen`, `3 - Wenig Potential`, `4 - Kein Potential` |
| `cf_940` | Prüfsystem Potential | Auswahl | `0 - abklären`, `1 - High Potential`, `2 - Regelmässig Nachfassen`, `3 - Wenig Potential`, `4 - Kein Potential` |
| `cf_952` | IIoT/Trail Potential | Auswahl | `0 - abklären`, `3 - potentieller Kunde`, `4 - Kein Interesse / kein Potential`, `D - Drittmittelgeber`, `W - Werbeträger / Partner` |
| `cf_981` | Weiteres Potential | Auswahl | `1 - High Potential`, `2 - Regelmässig Nachfassen`, `4 - Kein Potential` |
| `cf_654` | Kundeninteresse / Status | Auswahl | `0 - abklären`, `1 - Kunde`, `2 - ex Kunde`, `3 - Potentieller Kunde`, `4 - Kein Interesse`, `5 - Keine SW/Kein Potential`, `6 - Falscher Zeitpunkt / Falsche Person`, `E - Keine SW / Kein Potential` |
| `cf_973` | Kundentyp | Auswahl | `produzierende Kunden`, `nicht-produzierende Kunden` |
| `cf_644` | Mitarbeiterzahl (intern geschätzt) | Zahl | Eigene Schätzung (unabhängig von `employees`) |
| `cf_655` | Besuchsroute / Tour-Code | Zahl | Interner Gebiets-/Routencode |
| `cf_669` | Entscheider / Geschäftsführer | Text | Namen komma-separiert (aus Handelsregister) |
| `cf_670` | Inhaber / VR-Mitglieder | Text | Namen komma-separiert |
| `cf_671` | Firmenbeschreibung / Zweck | Text | Gesellschaftszweck (Handelsregister) |
| `cf_983` | Interner Score | Zahl | Numerischer Wert (z.B. 72, 100) |

### Auswahlwerte: `accounttype`

`Kunde` · `Freelancer` · `Lieferant` · `Mitbewerber` · `andere`

### Auswahlwerte: `industry`

`Anlagenbau` · `Beratung/Consulting` · `Bildung/Schule` · `Defense` · `Dienstleister` · `Einzelhandel` · `Elektronik` · `Energie` · `Engineering` · `Fertigung` · `Finanzen/Banken` · `Industrie` · `Keine Zielbranche` · `Kommunikation` · `Maschinenbau` · `Medizin` · `Nahrungsmittel` · `Regierung` · `Sicherheitstechnik` · `Software` · `Technologie` · `Transport/Logistik` · `Versicherung` · `andere`

---

## Tabelle: Contacts (Kontakte / Personen)

### Standardfelder

| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | ID | CRM-ID, Format `4x<N>` |
| `contact_no` | Text | Interne Nummer (z.B. `CON8`) |
| `firstname` | Text | Vorname |
| `lastname` | Text | **Nachname** – primäres Suchfeld |
| `salutationtype` | Auswahl | Anrede → siehe Auswahlwerte |
| `title` | Text | Berufsbezeichnung / Jobtitel |
| `email` | Text | **Haupt-E-Mail** – primäres Suchfeld |
| `secondaryemail` | Text | Zweite E-Mail |
| `phone` | Text | Telefon Geschäft |
| `mobile` | Text | Mobiltelefon |
| `homephone` | Text | Privat-Telefon |
| `otherphone` | Text | Weitere Telefonnummer |
| `mailingstreet` | Text | Strasse |
| `mailingcity` | Text | Stadt |
| `mailingzip` | Text | PLZ |
| `mailingcountry` | Text | Land |
| `mailingpobox` | Text | Postfach |
| `account_id` | ID | Zugehörige Firma |
| `account_id_nameValue` | Text | Name der zugehörigen Firma (automatisch) |
| `description` | Text | Notizen / Freitext |
| `assigned_user_id` | ID | Zuständiger Benutzer |
| `createdtime` | Datum | Erstellungsdatum |
| `modifiedtime` | Datum | Letzte Änderung |

### Custom Fields (cf_) – Contacts

| Feld | Name | Typ | Auswahlwerte / Hinweise |
|---|---|---|---|
| `cf_544` | Briefanrede | Text | Vollständige Briefanrede (z.B. `Sehr geehrter Herr Müller,`) |
| `cf_545` | Funktion (Kurzbezeichnung) | Text | Kurztitel intern |
| `cf_546` | Abteilung / Funktion | Text | Freitext, sehr variabel (z.B. `Abt. SW-Entwicklung`, `Engineering/Entwicklung`) |
| `cf_555` | Sprache | Auswahl | `Deutsch`, `Englisch`, `Französisch` |
| `cf_573` | Akademischer Titel | Text | z.B. `Dr.`, `Dipl. El. Ing. FH` |
| `cf_575` | Event-Anmeldungen | Multi-Select (historisch) | Seminar-/Webinar-Anmeldungen, getrennt durch ` \|##\| ` |
| `cf_576` | Kontakttyp | Multi-Select | `Engineering Interessent`, `Engineering Beeinflusser`, `Engineering Mitbewerber`, `CT Beeinflusser`, `ehem. Mitarbeiter:in` – getrennt durch ` \|##\| ` |
| `cf_583` | Flag A | Boolean | `1` = gesetzt |
| `cf_585` | Status-Notiz | Text | z.B. `Pensioniert`, `selbstständig` |
| `cf_604` | Gruppen-Code | Text | Interner Kurzcode (z.B. `BAR`, `POST`, `RAM`) |
| `cf_605` | Newsletter-Abo | Auswahl | `Ja`, `Nein` |
| `cf_630` | Marketing-Notizen | Text | Freitext, Anmeldungen/Abmeldungen |
| `cf_638` | Flag B | Boolean | `1` = gesetzt |

### Auswahlwerte: `salutationtype`

`Sehr geehrte Frau` · `Sehr geehrter Herr`

---

## Tabelle: Potentials (Verkaufschancen)

### Standardfelder

| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | ID | CRM-ID, Format `5x<N>` |
| `potential_no` | Text | Interne Nummer (z.B. `POT2`) |
| `potentialname` | Text | **Bezeichnung** – primäres Suchfeld, Format oft `Kunde: Projektname` |
| `amount` | Dezimal | Auftragswert geschätzt (CHF) |
| `probability` | Zahl | Wahrscheinlichkeit (0–100 %) |
| `sales_stage` | Auswahl | Status → siehe Auswahlwerte. **Aktive Potentials haben leeren `sales_stage`!** |
| `closingdate` | Datum | Geplantes Abschlussdatum (`YYYY-MM-DD`) |
| `related_to` | ID | Verknüpfte Firma (Account) |
| `related_to_nameValue` | Text | Name der Firma (automatisch) |
| `contact_id` | ID | Verknüpfter Ansprechpartner |
| `campaignid` | ID | Kampagne |
| `assigned_user_id` | ID | Zuständiger Benutzer |
| `createdtime` | Datum | Erstellungsdatum |
| `modifiedtime` | Datum | Letzte Änderung |
| `modifiedby` | ID | Zuletzt geändert von |

### Custom Fields (cf_) – Potentials

| Feld | Name | Typ | Auswahlwerte / Hinweise |
|---|---|---|---|
| `cf_547` | Ausgangslage / Situation | Text | Kontext und Hintergrund des Projekts |
| `cf_548` | Herausforderungen / Risiken | Text | Bekannte Probleme und Risiken |
| `cf_549` | Lösungsansatz / Vorgehen | Text | Geplante Lösung oder Methodik |
| `cf_550` | Zeitdruck / Motivation | Text | Dringlichkeit und treibende Faktoren |
| `cf_551` | Budget / Kostenvorgabe | Text | Budget-Angabe des Kunden |
| `cf_552` | Finanzielle Situation | Text | Einschätzung Zahlungsfähigkeit |
| `cf_553` | Entscheider | Text | Wer entscheidet über den Auftrag |
| `cf_554` | Bedürfnis / Warum | Text | Kernbedürfnis des Kunden |
| `cf_587` | Kategorie | Auswahl | `Software Engineering`, `AI (Künstliche Intelligenz)`, `Prüfsystem`, `IIoT`, `Cudos Trail` |
| `cf_598` | Flag | Boolean | `1` = gesetzt |
| `cf_659` | Aufwand geschätzt (CHF) | Dezimal | Eigene Aufwandschätzung (vs. `amount` = Kundenwert) |
| `cf_956` | Lead-Quelle / Akquisitionskanal | Multi-Select | z.B. `Kundenpflege`, `Newsletter / E-Mail-Marketing`, `Pflege des persönlichen Netzwerks`, `Messe / Events / Vorträge extern`, `Seminar / Events intern`, `Pers. Empfehlung`, `Partnerschaft / Verband`, `Ausschreibung / Simap`, `Linkedin`, `Google/Online-Suche` – mehrere Werte durch ` \|##\| ` getrennt |
| `cf_958` | Datum letzter Kontakt | Datum | `YYYY-MM-DD` |
| `cf_960` | Datum nächster Kontakt | Datum | `YYYY-MM-DD` (Follow-up Termin) |
| `cf_962` | Datum erste Kontaktaufnahme | Datum | `YYYY-MM-DD` |
| `cf_979` | Weitere Kostenschätzung | Dezimal | Zusätzlicher Betrag (CHF) |

### Auswahlwerte: `sales_stage`

| Wert | Bedeutung |
|---|---|
| *(leer)* | **Aktives Potential** (in Bearbeitung) |
| `Closed Won` | Auftrag gewonnen |
| `Closed Lost` | Ausschreibung verloren |
| `gestorben` | Projekt eingestellt / abgebrochen |
| `inaktiv` | Momentan nicht aktiv, aber nicht abgeschlossen |

---

## Tabelle: ModComments (Kommentare)

| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | ID | CRM-ID, Format `29x<N>` |
| `commentcontent` | Text | **Kommentar-Text** – primäres Suchfeld |
| `related_to` | ID | Zugehöriges Objekt (Account, Contact oder Potential) |
| `related_to_nameValue` | Text | Name des zugehörigen Objekts (automatisch) |
| `parent_comments` | ID | Übergeordneter Kommentar (bei Threads) |
| `creator` | ID | Ersteller (Benutzer-ID) |
| `userid` | ID | Benutzer-ID (alternativ zu `creator`) |
| `assigned_user_id` | ID | Zuständiger Benutzer |
| `customer` | Text | Kunden-Referenz |
| `reasontoedit` | Text | Begründung bei nachträglicher Änderung |
| `createdtime` | Datum | Erstellungsdatum (`YYYY-MM-DD HH:MM:SS`) |
| `modifiedtime` | Datum | Letzte Änderung |

---

## Bekannte Benutzer

| `assigned_user_id` | Name |
|---|---|
| `19x7` | Reto Bättig |
| `19x9` | (System-User / ältere Einträge) |
| `19x17312` | Rachel Blaser |

---

## Fuzzy-Suche nach Firmennamen

Das CRM speichert oft längere oder leicht abweichende Firmennamen (z.B. `Walo Bertschinger Central AG` statt `Walo Bertschinger AG`). Strategie:

### 1. Wichtigstes Schlüsselwort verwenden

```sql
-- Suche nach dem markantesten Namensteil
select id, accountname from Accounts where accountname like '%Bertschinger%' limit 0, 10;
```

### 2. Mehrere Keywords kombinieren (AND)

```sql
-- Beide Kernwörter müssen enthalten sein
select id, accountname from Accounts
where accountname like '%Walo%' and accountname like '%Bertschinger%'
limit 0, 10;
```

### 3. Firmentyp-Suffix weglassen

Suffixe wie `AG`, `GmbH`, `SA`, `Ltd.`, `GmbH & Co. KG` beim Suchen weglassen – sie variieren oft:

```sql
-- Statt 'Siemens AG' → nur nach 'Siemens' suchen
select id, accountname from Accounts where accountname like '%Siemens%' limit 0, 10;
```

### 4. Bei mehreren Treffern: ID verwenden

Wenn die Suche mehrere Firmen liefert, dem Benutzer die Liste zeigen und die genaue ID erfragen. Dann mit ID weiterarbeiten:

```sql
select * from Potentials where related_to = '3x5104' limit 0, 20;
```

### 5. Teilstring aus Mitte des Namens

```sql
-- Sucht "Meyer" in allen Varianten: Meyer AG, Hans Meyer GmbH, ...
select id, accountname from Accounts where accountname like '%Meyer%' limit 0, 20;
```

---

## Typische Queries

### Aktive Verkaufschancen (offene Projekte)

```sql
select potentialname, amount, probability, closingdate, related_to_nameValue
from Potentials
where sales_stage = ''
order by closingdate
limit 0, 50;
```

### Aktive Potentials nach Kategorie

```sql
select potentialname, amount, closingdate, related_to_nameValue
from Potentials
where sales_stage = '' and cf_587 = 'Software Engineering'
order by closingdate
limit 0, 50;
```

### High-Potential Firmen für SW-Engineering

```sql
select accountname, industry, phone, email1, cf_615, cf_632
from Accounts
where cf_615 = '1 - High Potential'
limit 0, 50;
```

### Neueste Kommentare zu einem Account

```sql
select commentcontent, createdtime
from ModComments
where related_to = '3x12345'
order by createdtime
limit 0, 30;
```

### Kontakte einer Firma

```sql
select firstname, lastname, title, email, phone, cf_546
from Contacts
where account_id = '3x12345'
limit 0, 20;
```

### Kürzlich geänderte Potentials

```sql
select potentialname, modifiedtime, sales_stage, amount, related_to_nameValue
from Potentials
where modifiedtime > '2026-01-01'
order by modifiedtime
limit 0, 50;
```

### Kontakte mit Newsletter-Abo

```sql
select firstname, lastname, email, account_id_nameValue
from Contacts
where cf_605 = 'Ja'
limit 0, 100;
```

### Potentials nach Follow-up Datum (heute fällig)

```sql
select potentialname, cf_960, related_to_nameValue, cf_587
from Potentials
where sales_stage = '' and cf_960 <= '2026-04-25'
order by cf_960
limit 0, 30;
```

### Firmen in einer Branche mit gutem Potential

```sql
select accountname, phone, email1, cf_615, cf_654
from Accounts
where industry = 'Maschinenbau'
  and cf_654 in ('1 - Kunde', '3 - Potentieller Kunde')
limit 0, 50;
```

### Gewonnene Aufträge in einem Zeitraum

```sql
select potentialname, amount, closingdate, related_to_nameValue
from Potentials
where sales_stage = 'Closed Won'
  and closingdate >= '2025-01-01'
  and closingdate <= '2025-12-31'
order by closingdate
limit 0, 100;
```

---

## Multi-Select Felder

Einige Felder enthalten mehrere Werte, getrennt durch ` |##| ` (mit Leerzeichen). Beim Suchen deshalb immer `like` statt `=` verwenden:

```sql
-- Korrekt (findet auch Mehrfach-Einträge):
where cf_956 like '%Kundenpflege%'

-- Falsch (findet nur wenn Kundenpflege der einzige Wert ist):
where cf_956 = 'Kundenpflege'
```

Betrifft: `cf_956` (Potentials), `cf_575`, `cf_576` (Contacts).

---

## Paginierung

Maximal 100 Datensätze pro Query. Für mehr Daten Offset erhöhen:

```sql
-- Seite 1
select ... limit 0, 100;
-- Seite 2
select ... limit 100, 100;
-- Seite 3
select ... limit 200, 100;
```
