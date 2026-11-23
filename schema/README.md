# Schema 0.8

[Deutsch](README.de.md)

Layers, relations and the reasons behind them are explained in the [README](../README.md). This file lists paths, fields and rules.

## Paths

```
games/<game>/game.md
games/<game>/<name>.md                              evidence: sequence (section 0) and events (1, 2, 3 …)
tags/<name>.md
literature/game_evidence_archive_and_repository.bib exported from Zotero
```

Names are lowercase English: `a-z`, `0-9`, `_`. Translations sit next to the original as `<name>.<lang>.md`.

## IDs

| Type | Pattern | Example |
|---|---|---|
| game | `GAME-<CODE>` | `GAME-WOW` |
| evidence | `EVD-<CODE>-<nnnn>` | `EVD-WOW-0001` |
| event | `<evidence ID>.<n>` | `EVD-WOW-0001.2` |

`<CODE>` is the game's code from `game.md`. IDs are stable and used for citation; an event's number therefore does not change once published. Tags are identified by their file name, which therefore must not change.

## Fields

All originals need `type`, `schema_version` (a string, `"0.8"`), `status` and `title`. Optional everywhere: `lang` (default `en`).

| Type | Required | Optional |
|---|---|---|
| game | `id` | `wikidata` (Q-ID), `engagement`, `branches` (key: short description) |
| evidence | `id`, `observed` with `date`, `version`, `platform`, `language`, `by`; `events` | `unit` (required with section 0), `tags`, `first_appeared` with `version`, optionally `branch` (only if the game has `branches`) and `note`, `variant_of` (evidence ID); in `observed`: `branch` (required if the game has `branches`), in `observed`: `server`, `season`, `difficulty`, `mode` |
| tag | | `related`, `mappings` |

`events` maps each event's number to its fields:

| Field | |
|---|---|
| `layer` | required |
| `timecode` or `locator` | one of them required |
| `agency`, `act`, `consequence` | coding, see below |
| `source` | if read, not played: database, walkthrough, video |
| `observed` | overrides single fields of the entry's `observed` for this event |
| `media`, `coded_by` | optional |

Translations: `lang` and `status`, optionally `title`, nothing else.

## Sections in the text

| Type | Sections |
|---|---|
| game | Description, Versions (if the game has branches), Reference source, Boundaries (how the game was played: parts, choices, background) |
| evidence | `## 0. <title>` (optional, the sequence): `### Description` (in-game IDs, place, characters, previous and next), optionally `### Interpretation` of the whole. `## 1. <title>`, `## 2. <title>` … (events): `### Description` (only the moment), `### Observation` (see [observation style guide](observation_style.md)), `### Interpretation` (open questions marked "Open:") |
| tag | Definition, Aspects (one `###` per aspect), Discussion |

A translation of an evidence entry contains the numbered sections it translates, with the same numbers; it need not contain all of them.

## Coded values

All in `vocabularies.yaml`, with labels per language.

| Field | Values |
|---|---|
| `layer` | `fixed`, `conditional` (laid down, but only after certain choices or states), `contingent` |
| `agency` | `reference`, `watching`, `optional`, `forced` |
| `unit` (section 0) | `quest`, `mission`, `chapter`, `level`, `cutscene`, `scene`, `menu`, `other` |
| `engagement` (game) | Aarseth's (2003) strata: `superficial_play`, `light_play`, `partial_completion`, `total_completion`, `repeated_play`, `expert_play` |
| `act` | only with agency `optional` or `forced`: `trigger`, `perform` |
| `consequence` | only with agency `optional` or `forced`: `if_done` and `if_not_done`, each one of `none`, `progress`, `reward`, `penalty`, `branch`, `blocks`, `fail`, `unknown` |

## Rules checked by the validator

1. Every file is in a known place and named by the rules above.
2. Required fields present, including `observed` for every event; `schema_version` is a string.
3. IDs match their pattern and the game's code, and are unique.
4. Evidence sections are numbered 0 (optional), then 1, 2, 3 … without gaps; section 0 and `unit` go together; every event has an entry under `events` and every entry under `events` a section.
5. With `branches` in `game.md`: every event has an `observed.branch`, and it and `first_appeared.branch` come from `branches`; `variant_of` names an existing entry.
6. Coded values match `vocabularies.yaml`; `act` and `consequence` only with agency `optional` or `forced`.
7. `tags` and `related` name files in `tags/`.
8. Zotero tags `gear:<target>:<role>` in `game_evidence_archive_and_repository.bib` point to an existing tag, game folder, evidence ID or event ID, and the role comes from `vocabularies.yaml`.
9. Every relative Markdown link and every citekey `[@key]` resolves.
10. Translations have an original, no further metadata and only sections the original has.

## Literature

`literature/game_evidence_archive_and_repository.bib` is exported by Better BibTeX from Zotero. Relations are Zotero tags in `keywords`: `gear:<target>:<role>`. Every tag needs a target. The target is a tag name, a game folder name, an evidence ID (`EVD-WOW-0001`) or an event ID (`EVD-WOW-0001.2`) and must be unambiguous.

## Mappings to external vocabularies

A tag can point to concepts in other vocabularies. Nothing is copied; GEAR only references them, which also keeps licences apart (VGMS is CC BY-NC-SA).

```yaml
mappings:
  - {scheme: gop, concept: "Entity Manipulation", match: related, url: "..."}
```

Schemes: `wikidata`, `vgms`, `gop`, `gdp` (Gameplay Design Patterns), `ddd`. Match types follow SKOS: `exact`, `close`, `broader`, `narrower`, `related`. Add a mapping only where a concept really fits.

## Media

`media/manifest.csv` lists recordings and stills with relative path and SHA-256. The media root is set locally in `.gear.local`, which is not committed.

## Prepared for later

These are not needed yet, but the schema is laid out so that they can be added without changing existing files.

| Topic | How it is prepared |
|---|---|
| more languages | translations as `<name>.<lang>.md`; labels per language in `vocabularies.yaml`; a new language is one entry under `lang` |
| SKOS export | every coded value has a stable key and labels per language; mappings use SKOS match types. A script can write SKOS/RDF from `vocabularies.yaml` and `tags/`. Keys are never renamed or deleted; a value that is no longer used gets `deprecated: true`. The base URI is fixed at the first release. |
| several coders | `coded_by` under `events` names who coded an event (default: `observed.by`). For a second coding, alternative codes would be kept side by side rather than averaged, so that disagreement stays visible. Agreement can then be computed by script. |
| archival description | a mapping of game, evidence, event and tag to ICA Records in Contexts (RiC-CM) is still open and has to be made against the ICA specification. |
| external identifiers | `wikidata` on games; mappings on tags. Further IDs (IGDB, MobyGames) can be added the same way. |

## Known limits

Evidence IDs are counted per game. If several people work in parallel, numbers can collide; an observer code in the ID would then be needed (`EVD-WOW-SS-0001`). Inserting an event between two others renumbers the later ones and changes their IDs; once an entry is `citable`, new events are added at the end.
