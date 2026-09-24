# Zefix API — Feldreferenz

Extrahiert aus der OpenAPI-Spec (`GET /ZefixPublicREST/v3/api-docs`, Version
2.8.2.0). Die Spec selbst ist ohne Authentifizierung abrufbar, alle
Daten-Endpoints verlangen HTTP Basic Auth.

Basis-URL: `https://www.zefix.admin.ch/ZefixPublicREST`

## Endpoints

| Methode | Pfad | Antwort |
|---------|------|---------|
| POST | `/api/v1/company/search` | `array[CompanySearchResult]` |
| GET | `/api/v1/company/uid/{id}` | `array[CompanyFull]` |
| GET | `/api/v1/company/chid/{id}` | `array[CompanyFull]` |
| GET | `/api/v1/company/ehraid/{id}` | `array[CompanyFull]` |
| GET | `/api/v1/sogc/{id}` | `SogcPublication` |
| GET | `/api/v1/sogc/bydate/{date}` | `array[{companyShort, sogcPublication}]` |
| GET | `/api/v1/legalForm` | `array[LegalForm]` |
| GET | `/api/v1/community` | Gemeindeliste |
| GET | `/api/v1/registryOfCommerce` | Registerämter |
| GET | `/api/v1/registryOfCommerce/byBfsCommunityId/{id}` | Registeramt einer Gemeinde |

Die `company/*`-Endpoints liefern ein **Array** mit typischerweise einem
Element — nicht das Objekt direkt.

`/sogc/bydate` weicht in der Struktur ab: die Publikation steckt in
`sogcPublication`, die Firma in `companyShort`.

## CompanySearchQuery (POST-Body der Suche)

| Feld | Typ | Bemerkung |
|------|-----|-----------|
| `name` | string | Firmenname |
| `activeOnly` | boolean | gelöschte Firmen ausblenden |
| `canton` | string | nicht kombinierbar mit `registryOfCommerceId`/`legalSeatId` |
| `legalFormId` | integer | siehe `/api/v1/legalForm` |
| `legalFormUid` | string | Alternative zu `legalFormId` |
| `legalSeatId` | integer | Gemeinde-ID |
| `registryOfCommerceId` | integer | Registeramt |

## CompanyFull

### Flache Felder

| Feld | Typ |
|------|-----|
| `name` | string |
| `uid` | string (`CHE100618212`, unformatiert) |
| `chid` | string |
| `ehraid` | integer |
| `status` | string (`ACTIVE`, …) |
| `legalSeat` / `legalSeatId` | string / integer |
| `canton` | string |
| `registryOfCommerceId` | integer |
| `capitalNominal` / `capitalCurrency` | string / string |
| `purpose` | string (Zweckartikel im Volltext) |
| `sogcDate` | string (Datum der letzten Publikation) |
| `deletionDate` | string (nur bei gelöschten Firmen) |
| `cantonalExcerptWeb` | string (URL kantonaler Registerauszug) |
| `translation` | array[string] |

### Verschachtelte Objekte

- **`address`** → `street`, `houseNumber`, `swissZipCode`, `city`, `addon`,
  `careOf`, `poBox`, `organisation`
- **`legalForm`** → `id`, `uid`, `name` (DFIEString), `shortName` (DFIEString)
- **`zefixDetailWeb`** → DFIEString mit Zefix-Deeplink je Sprache
- **`oldNames`** → array aus `{name, sequenceNr, translation}`
- **`sogcPub`** → array[SogcPublication]

**`DFIEString`** ist durchgängig `{de, fr, it, en}`.

### Verflechtungen — alle array[CompanyShort]

`auditCompanies` · `branchOffices` · `headOffices` · `furtherHeadOffices` ·
`hasTakenOver` · `wasTakenOverBy`

**`CompanyShort`**: `name`, `uid`, `chid`, `ehraid`, `legalForm`,
`legalSeat`, `legalSeatId`, `registryOfCommerceId`, `sogcDate`, `status`,
`deletionDate`

## SogcPublication

| Feld | Typ |
|------|-----|
| `message` | string, enthält `<FT TYPE="F\|S\|A\|N">`-Markup und HTML-Entities |
| `mutationTypes` | array aus `{id, key}`, z.B. `aenderungorgane`, `adressaenderung` |
| `sogcId` | integer |
| `sogcDate` | string |
| `registryOfCommerceCanton` | string |
| `registryOfCommerceId` | integer |
| `registryOfCommerceJournalId` | integer |
| `registryOfCommerceJournalDate` | string |

Das `FT`-Markup kennzeichnet Firma (`F`), Sitz (`S`), UID (`A`) und neuen
Namen (`N`). Entities wie `&quot;` und `&amp;` sind zusätzlich enthalten und
müssen separat dekodiert werden.

## Beobachtetes Verhalten

Verifiziert am Datensatz Cudos AG (CHE-100.618.212, 11'529 Bytes, 10
SHAB-Publikationen von 2017-02-03 bis 2024-10-15):

- **Leere Felder werden weggelassen**, nicht auf `null` gesetzt. Im
  Cudos-Response fehlen `branchOffices`, `headOffices` und `deletionDate`
  vollständig.
- **Verflechtungen sind lückenhaft.** Die existierende „Cudos AG,
  Zweigniederlassung Chur" (CHE-155.852.094) steht nicht in
  `branchOffices` der Hauptgesellschaft; der ZN-Datensatz liefert
  `headOffices: null`. Die Beziehung lässt sich nur über die Namenssuche
  rekonstruieren.
- **Keine strukturierten Personendaten.** Organe und Zeichnungsberechtigte
  existieren ausschliesslich als Fliesstext in `sogcPub[].message`.
- `/sogc/bydate` liefert grosse Mengen — der 2024-10-15 hat 1129 Einträge.
