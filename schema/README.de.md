# Schema 0.7

[English](README.md)

Maßgeblich ist die [englische Fassung](README.md). Hier das Wichtigste auf Deutsch.

## Pfade

```
games/<spiel>/game.md
games/<spiel>/<sequenz>/sequence.md                  die Stelle im Spiel: Quest, Mission, Kapitel …
games/<spiel>/<sequenz>/<nnnn>_<name>.md             Events darin; <nnnn> ist die Nummer der ID
tags/<name>.md
literature/game_evidence_archive_and_repository.bib                            Export aus Zotero
```

Namen sind englisch und klein: `a-z`, `0-9`, `_`. Übersetzungen liegen neben dem Original als `<name>.<sprache>.md`.

## Felder

Alle Originale brauchen `type`, `schema_version` (als String, `"0.7"`), `status` und `title`. Überall optional: `lang` (ohne Angabe `en`).

| Typ | Pflicht | optional |
|---|---|---|
| game | `id` | `wikidata` (Q-ID), `engagement` |
| sequence | `id` (`SEQ-<CODE>-<nnn>`), `unit` | |
| event | `id`, `layer`, `observed` mit `date`, `version`, `platform`, `language`, `by`; `timecode` oder `locator` | in `observed`: `server`, `season`, `difficulty`, `mode`, `source`; `agency`, `act`, `consequence`, `tags`, `content_warnings`, `media`, `coded_by` |
| tag | | `related`, `mappings` |

Übersetzungen: `lang` und `status`, bei Bedarf `title`, sonst nichts.

Tags werden über ihren Dateinamen angesprochen; der darf sich deshalb nicht ändern.

Literatur kommt aus Zotero (`literature/game_evidence_archive_and_repository.bib`, Export mit Better BibTeX). Verbindungen sind Zotero-Tags im Feld `keywords`: `gear:<ziel>:<rolle>`, immer mit Ziel. Ziel ist ein Tag, ein Spielordner, eine Sequenz-ID oder eine Event-ID.

## Abschnitte

Die Überschriften sind auch in deutschen Originalen englisch (Description, Observation, Interpretation, Boundaries, Definition, Aspects, Discussion). In Übersetzungen dürfen sie übersetzt werden.

## Kodierte Werte

| Feld | Werte |
|---|---|
| `layer` | `fixed` (fest), `conditional` (bedingt: angelegt, aber nur nach bestimmten Entscheidungen oder Zuständen), `contingent` (kontingent) |
| `agency` | `reference` (Erwähnung), `watching` (zuschauen), `optional`, `forced` (erzwungen) |
| `unit` (Sequenz) | `quest`, `mission`, `chapter`, `level`, `cutscene`, `scene`, `menu`, `other` |
| `engagement` (Spiel) | Spieltiefe nach Aarseth (2003): `superficial_play` bis `expert_play` |
| `act` | nur bei agency `optional` oder `forced`: `trigger` (löst aus), `perform` (führt aus) |
| `consequence` | nur bei agency `optional` oder `forced`: `if_done` und `if_not_done` |
| `content_warnings` | gruppierte Werte, siehe `vocabularies.yaml` |

Für den Abschnitt Observation gilt der [Leitfaden für Beobachtungen](observation_style.de.md).

## Abbildungen auf fremde Vokabulare

Ein Tag kann über `mappings` auf Begriffe anderer Vokabulare verweisen (Wikidata, VGMS, GOP, Gameplay Design Patterns, Does the Dog Die?), mit SKOS-Entsprechungsarten. Übernommen wird nichts, nur verwiesen; so bleiben auch die Lizenzen getrennt.

## Für später vorbereitet

Mehr Sprachen, SKOS-Export, mehrere Kodierende, archivische Beschreibung nach RiC-CM und weitere externe IDs sind noch nicht nötig, aber so angelegt, dass bestehende Dateien sich dafür nicht ändern müssen. Einzelheiten in der [englischen Fassung](README.md#prepared-for-later).

## content_warnings

| Zustand | Bedeutung |
|---|---|
| Feld fehlt | nicht geprüft |
| `content_warnings: []` | geprüft, nichts gefunden |
| `content_warnings: [torture]` | geprüft, Werte aus `vocabularies.yaml` |
