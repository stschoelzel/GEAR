# Schema 0.7

[Deutsch](README.de.md)

Layers, relations and the reasons behind them are explained in the [README](../README.md). This file lists paths, fields and rules.

## Paths

```
games/<game>/game.md
games/<game>/<sequence>/sequence.md                 the place in the game: quest, mission, chapter …
games/<game>/<sequence>/<nnnn>_<name>.md            events in it; <nnnn> is the number of the ID
tags/<name>.md
literature/game_evidence_archive_and_repository.bib                           exported from Zotero
```

Names are lowercase English: `a-z`, `0-9`, `_`. Translations sit next to the original as `<name>.<lang>.md`.

## IDs

| Type | Pattern | Example |
|---|---|---|
| game | `GAME-<CODE>` | `GAME-WOW` |
| sequence | `SEQ-<CODE>-<nnn>` | `SEQ-WOW-001` |
| event | `EVT-<CODE>-<nnnn>` | `EVT-WOW-0001` |

`<CODE>` is the game's code from `game.md`. IDs are stable and used for citation. Tags are identified by their file name, which therefore must not change.

## Fields

All originals need `type`, `schema_version` (a string, `"0.7"`), `status` and `title`. Optional everywhere: `lang` (default `en`).

| Type | Required | Optional |
|---|---|---|
| game | `id` | `wikidata` (Q-ID), `engagement` |
| sequence | `id`, `unit` | |
| event | `id`, `layer`, `observed` with `date`, `version`, `platform`, `language`, `by`; `timecode` or `locator` | in `observed`: `server`, `season`, `difficulty`, `mode`, `source`; `agency`, `act`, `consequence`, `tags`, `content_warnings`, `media`, `coded_by` |
| tag | | `related`, `mappings` |

Translations: `lang` and `status`, optionally `title`, nothing else.

## Sections in the text

| Type | Sections |
|---|---|
| game | Description, Reference source, Boundaries (how the game was played: parts, choices, background) |
| sequence | Description (in-game IDs, place, characters, previous and next), optionally Interpretation of the whole |
| event | Description (only the moment within the sequence), Observation (see [observation style guide](observation_style.md)), Interpretation (open questions marked "Open:") |
| tag | Definition, Aspects (one `###` per aspect), Discussion |

## Coded values

All in `vocabularies.yaml`, with labels per language.

| Field | Values |
|---|---|
| `layer` | `fixed`, `conditional` (laid down, but only after certain choices or states), `contingent` |
| `agency` | `reference`, `watching`, `optional`, `forced` |
| `unit` (sequence) | `quest`, `mission`, `chapter`, `level`, `cutscene`, `scene`, `menu`, `other` |
| `engagement` (game) | Aarseth's (2003) strata: `superficial_play`, `light_play`, `partial_completion`, `total_completion`, `repeated_play`, `expert_play` |
| `act` | only with agency `optional` or `forced`: `trigger`, `perform` |
| `consequence` | only with agency `optional` or `forced`: `if_done` and `if_not_done`, each one of `none`, `progress`, `reward`, `penalty`, `branch`, `blocks`, `fail`, `unknown` |
| `content_warnings` | grouped values, see `vocabularies.yaml` |

## content_warnings

| State | Meaning |
|---|---|
| field missing | not checked |
| `content_warnings: []` | checked, nothing found |
| `content_warnings: [torture]` | checked, values from `vocabularies.yaml` |

## Rules checked by the validator

1. Every file is in a known place and named by the rules above; every event folder has a `sequence.md`; the number in an event's file name matches its ID.
2. Required fields present, including `observed`; `schema_version` is a string.
3. IDs match their pattern and the game's code, and are unique.
4. Coded values match `vocabularies.yaml`.
5. `tags` and `related` name files in `tags/`.
6. Zotero tags `gear:<target>:<role>` in `game_evidence_archive_and_repository.bib` point to an existing tag, game folder, sequence ID or event ID, and the role comes from `vocabularies.yaml`.
7. Every relative Markdown link and every citekey `[@key]` resolves.
8. Translations have an original and no further metadata.

## Literature

`literature/game_evidence_archive_and_repository.bib` is exported by Better BibTeX from Zotero. Relations are Zotero tags in `keywords`: `gear:<target>:<role>`. Every tag needs a target. The target is a tag name, a game folder name, a sequence ID or an event ID and must be unambiguous.

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
| several coders | `coded_by` names who coded an event (default: `observed.by`). For a second coding, alternative codes would be kept side by side rather than averaged, so that disagreement stays visible. Agreement can then be computed by script. |
| archival description | a mapping of game, event and tag to ICA Records in Contexts (RiC-CM) is still open and has to be made against the ICA specification. |
| external identifiers | `wikidata` on games; mappings on tags. Further IDs (IGDB, MobyGames) can be added the same way. |

## Known limits

Sequence and event IDs are counted per game. If several people work in parallel, numbers can collide; an observer code in the ID would then be needed (`EVT-WOW-SS-0001`).
