# Schema 0.8

[English](README.md)

Maßgeblich ist die [englische Fassung](README.md). Hier das Wichtigste auf Deutsch.

## Pfade

```
games/<spiel>/game.md
games/<spiel>/<name>.md                              Befund: Sequenz (Abschnitt 0) und Events (1, 2, 3 …)
tags/<name>.md
literature/game_evidence_archive_and_repository.bib  Export aus Zotero
```

Namen sind englisch und klein: `a-z`, `0-9`, `_`. Übersetzungen liegen neben dem Original als `<name>.<sprache>.md`.

## IDs

| Typ | Muster | Beispiel |
|---|---|---|
| game | `GAME-<CODE>` | `GAME-WOW` |
| evidence (Befund) | `EVD-<CODE>-<nnnn>` | `EVD-WOW-0001` |
| event | `<Befund-ID>.<n>` | `EVD-WOW-0001.2` |

## Felder

Alle Originale brauchen `type`, `schema_version` (als String, `"0.8"`), `status` und `title`. Überall optional: `lang` (ohne Angabe `en`).

| Typ | Pflicht | optional |
|---|---|---|
| game | `id` | `wikidata` (Q-ID), `engagement`, `branches` (Schlüssel: kurze Beschreibung), `machine_generated` (siehe README) |
| evidence | `id`, `observed` mit `date`, `version`, `platform`, `language`, `by`; `events` | `unit` (Pflicht mit Abschnitt 0), `tags`, `first_appeared` mit `version`, optional `branch` (nur wenn das Spiel `branches` hat) und `note`, `variant_of` (Befund-ID), `machine_generated` (siehe README); in `observed`: `branch` (Pflicht, wenn das Spiel `branches` hat), `server`, `season`, `difficulty`, `mode` |
| tag | | `related`, `mappings` |

`events` ordnet jeder Event-Nummer ihre Felder zu: `layer` (Pflicht), `timecode` oder `locator` (eins davon Pflicht; `timecode` als `HH:MM:SS` bei Gespieltem, `locator` nennt bei Gelesenem die genaue Stelle), `source` (Pflicht; gelesen: Referenz als Markdown-Link mit Abrufdatum, `[Titel](URL), accessed JJJJ-MM-TT`, mehrere durch `;` getrennt, ohne URL nur die Referenz; gespielt: `own play`), `agency`, `act`, `consequence`, `observed` (überschreibt einzelne Angaben des Befunds), `media`, `coded_by`.

Übersetzungen: `lang` und `status`, bei Bedarf `title`, sonst nichts. Eine Übersetzung enthält die nummerierten Abschnitte, die sie übersetzt, mit denselben Nummern.

Tags werden über ihren Dateinamen angesprochen; der darf sich deshalb nicht ändern.

Literatur kommt aus Zotero (`literature/game_evidence_archive_and_repository.bib`, Export mit Better BibTeX). Verbindungen sind Zotero-Tags im Feld `keywords`: `gear:<ziel>:<rolle>`, immer mit Ziel. Ziel ist ein Tag, ein Spielordner, eine Befund-ID oder eine Event-ID.

## Abschnitte

Ein Befund gliedert sich in `## 0. <Titel>` (optional, die Sequenz) und `## 1. <Titel>`, `## 2. <Titel>` … (die Events), jeweils mit `### Description`, `### Observation`, `### Interpretation`; Abschnitt 0 hat nur Description und Interpretation.

Die Überschriften sind auch in deutschen Originalen englisch (Description, Observation, Interpretation, Boundaries, Definition, Aspects, Discussion). In Übersetzungen dürfen sie übersetzt werden.

## Kodierte Werte

| Feld | Werte |
|---|---|
| `layer` | `fixed` (fest), `conditional` (bedingt: angelegt, aber nur nach bestimmten Entscheidungen oder Zuständen), `contingent` (kontingent) |
| `agency` | `reference` (Erwähnung), `watching` (zuschauen), `optional`, `forced` (erzwungen) |
| `unit` (Abschnitt 0) | `quest`, `mission`, `chapter`, `level`, `cutscene`, `scene`, `menu`, `other` |
| `engagement` (Spiel) | Spieltiefe nach Aarseth (2003): `superficial_play` bis `expert_play` |
| `act` | nur bei agency `optional` oder `forced`: `trigger` (löst aus), `perform` (führt aus) |
| `consequence` | nur bei agency `optional` oder `forced`: `if_done` und `if_not_done` |

Für den Abschnitt Observation gilt der [Leitfaden für Beobachtungen](observation_style.de.md).

## Abbildungen auf fremde Vokabulare

Ein Tag kann über `mappings` auf Begriffe anderer Vokabulare verweisen (Wikidata, VGMS, GOP, Gameplay Design Patterns, Does the Dog Die?), mit SKOS-Entsprechungsarten. Übernommen wird nichts, nur verwiesen; so bleiben auch die Lizenzen getrennt.

## Für später vorbereitet

Mehr Sprachen, SKOS-Export, mehrere Kodierende, archivische Beschreibung nach RiC-CM und weitere externe IDs sind noch nicht nötig, aber so angelegt, dass bestehende Dateien sich dafür nicht ändern müssen. Einzelheiten in der [englischen Fassung](README.md#prepared-for-later).

