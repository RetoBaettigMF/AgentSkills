---
name: zefix
description: Offizielle Handelsregisterdaten Schweizer Firmen über die Zefix Public REST API des Bundes. Verwende diesen Skill bei Anfragen nach UID/CHE-Nummer, Handelsregistereintrag, Firmensitz, Rechtsform, Aktienkapital, Firmenzweck, Revisionsstelle, früheren Firmennamen, Zweigniederlassungen, Löschungen oder SHAB-Publikationen (Schweizerisches Handelsamtsblatt). Nutze diesen Skill statt moneyhouse, wenn amtlich verbindliche Registerdaten gefragt sind.
---

# Zefix Skill

Zugriff auf das Zentrale Firmenindex (Zefix) des Eidgenössischen Amts für das
Handelsregister via offizieller REST-API. Die Daten sind amtlich und stehen
unter Open-Government-Data-Lizenz (Quellenangabe erforderlich).

**Abgrenzung zu `moneyhouse`:** Zefix liefert den amtlichen Registerinhalt,
aber **keine** Mitarbeiterzahlen, Umsätze oder Branchencodes. Umgekehrt
enthält Zefix die SHAB-Publikationshistorie, die moneyhouse nicht hat. Für
Personendaten siehe „Grenzen" unten.

## Voraussetzungen

Zugangsdaten in `scripts/.env` (Vorlage: `.env.example`):

```
ZEFIX_USER=user@example.com
ZEFIX_PASS=yourpassword
```

Zugang kostenlos unter https://www.zefix.admin.ch → Webservices/API. Die
Freischaltung erfolgt **manuell und dauert einige Werktage** — bis dahin
antwortet die API auf jeden Aufruf mit `401`.

## Verwendung

```bash
scripts/zefix <kommando> [Optionen]
```

### Firmen suchen

```bash
scripts/zefix search "Cudos AG"
scripts/zefix search "Muster" --canton ZH --active-only
scripts/zefix search "Muster" --legal-form-id 4          # nur GmbH
```

| Option | Beschreibung |
|--------|--------------|
| `--active-only` | Nur aktive Firmen (gelöschte ausblenden) |
| `--canton ZH` | Auf einen Kanton einschränken |
| `--legal-form-id N` | Rechtsform-ID (siehe `legalforms`) |
| `--legal-seat-id N` | Gemeinde-ID des Sitzes |

`--canton` ist laut API nicht mit `--legal-seat-id` kombinierbar.

### Volldatensatz abrufen

```bash
scripts/zefix company CHE-100.618.212          # UID, formatiert oder nicht
scripts/zefix company CH02039263170            # CHID
scripts/zefix company 192809                   # EHRAID
scripts/zefix company CHE-100.618.212 --publications 5 --related
```

Der ID-Typ wird automatisch erkannt; Punkte und Bindestriche sind egal.

| Option | Beschreibung |
|--------|--------------|
| `--publications N` | N SHAB-Meldungen im Volltext (Standard: 0, nur Anzahl) |
| `--related` | Zweigniederlassungen/Hauptsitz über Namenssuche ergänzen |

### SHAB-Publikationen

```bash
scripts/zefix sogc 2024-10-15                  # alle Meldungen eines Tages
scripts/zefix sogc 2024-10-15 --limit 50       # Standard: 20
scripts/zefix sogc 1006153927                  # einzelne Meldung per SOGC-ID
```

### Rechtsformen

```bash
scripts/zefix legalforms       # IDs für --legal-form-id
```

### Globale Optionen

| Option | Beschreibung |
|--------|--------------|
| `--json` | Rohes API-JSON statt formatierter Ausgabe |
| `--lang de\|fr\|it\|en` | Sprache mehrsprachiger Felder (Standard: `de`) |

Beide funktionieren vor und nach dem Subkommando.

## Beispielausgabe

```
========================================================================
Cudos AG
========================================================================
  UID            CHE-100.618.212
  CHID           CH02039263170
  EHRAID         192809
  Status         ACTIVE
  Rechtsform     Aktiengesellschaft
  Sitz           Weiningen (ZH)
  Kanton         ZH
  Adresse        Querstrasse 17, 8951 Fahrweid
  Kapital        CHF 400000
  Letzte SHAB    2024-10-15

  Frühere Firmennamen
    - Thau-Computer AG
    - M&F Engineering AG

  Revisionsstelle
    - "REVISION" Aktiengesellschaft (CHE-107.903.292, Erlenbach (ZH))
```

## Grenzen der API

Drei Eigenheiten, die bei der Weiterverarbeitung regelmässig Probleme machen:

1. **Keine strukturierten Personendaten.** Organe, Verwaltungsräte und
   Zeichnungsberechtigte gibt es ausschliesslich als Fliesstext in
   `sogcPub[].message`. Wer sie strukturiert braucht, muss den Text parsen
   oder auf `moneyhouse` bzw. den kantonalen Auszug ausweichen.

2. **Leere Felder fehlen ganz**, statt `null` zu sein. Beim Parsen von
   `--json` also immer `.get()` verwenden, nie Indexzugriff.

3. **Die Verflechtungsfelder sind unzuverlässig.** `branchOffices`,
   `headOffices` etc. bleiben oft leer, obwohl die Beziehung besteht — bei
   Cudos AG fehlt die Zweigniederlassung Chur in `branchOffices`, und
   umgekehrt ist `headOffices` der ZN leer. Deshalb `--related`, das den
   Bezug über die Namenssuche rekonstruiert.

Eine vollständige Feldreferenz aller Endpoints steht in `reference.md`.

## Fehlerbehandlung

| Meldung | Ursache |
|---------|---------|
| `Fehler 401` | Account nicht freigeschaltet, falscher technischer Benutzername oder Tippfehler im Passwort |
| `Keine Firma gefunden` | ID existiert nicht (API antwortet mit 404) |
| `Unbekanntes ID-Format` | Weder UID (`CHE…`), CHID (`CH…`) noch numerische EHRAID |

## Quellenangabe

Open Government Data, Nutzung nur mit Quellenangabe:
„Quelle: Zefix / Eidgenössisches Amt für das Handelsregister (EHRA)".
