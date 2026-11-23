# GEAR

Game Evidence Archive & Repository

[Deutsch](README.de.md)

GEAR is an open dataset of gameplay evidence. Every claim about a game ("in quest X you have to do Y") should be traceable to a piece of evidence: who played or read what, when, under which conditions, and what they observed. Observation and interpretation are kept apart.

The dataset is plain Markdown with YAML frontmatter. Any text editor can read and edit it; Zettlr suits writing, VSCodium suits structure and Git. Scripts turn it into tables, a searchable database and trees, see [Search and browse](#search-and-browse). The public website is built from it in a separate repository (madGear).

The examples compare torture in two games: the quest "The Art of Persuasion" in World of Warcraft: Wrath of the Lich King and the mission "By the Book" in Grand Theft Auto V. Each is one evidence entry. Both are drafts compiled from reference sources and still have to be checked in play.

## Principles

GEAR rests on five principles. DiGAP is the framework they build on, and Zotero is the tool for literature.

1. **Raw and processed kept apart** (OAIS). A source is kept as it was found. An observation is a processed record of it and is written as such. A passage quoted from a walkthrough is raw material and carries its locator.
2. **Every description has its origin** (OLAC). Each event names its `source`: the reference or walkthrough, with URL and access date where one exists, or `own play` for played material.
3. **Locators are precise** (Media Fragments). A locator points to the exact place: a timecode for played video, a Media Fragments `#t=` fragment for web video, the named passage or section for text.
4. **Descriptions are neutral and unambiguous** (ASD-STE100, with EARS and Gherkin sentence patterns). One term has one meaning. Observations follow the [observation style guide](schema/observation_style.md). Evaluation and reading go into Interpretation only.
5. **Rules, dynamics and effects kept apart** (MDA). Rules and dynamics are observed; effects are interpreted. See [What goes where](#what-goes-where-in-a-file).

DiGAP is described under [Method](#method-digap). Literature is kept in Zotero; see [Literature](#literature).

## Three ways in

```
games/                                      look into a game
├── grand_theft_auto_v/
│   ├── game.md
│   └── by_the_book.md                      evidence: the mission, with its events
└── world_of_warcraft/
    ├── game.md
    ├── the_art_of_persuasion.md            evidence: the quest, with its events
    └── the_art_of_persuasion.de.md         German translation of parts of it
tags/                                       look up a term
└── torture.md
literature/                                 look up research
└── game_evidence_archive_and_repository.bib
```

**By game:** open the game's folder. It holds the game file and one file per evidence entry.

**By term:** open a file in `tags/`. It defines the term, describes its aspects and leads to all evidence and literature carrying it, across games.

**By literature:** `literature/game_evidence_archive_and_repository.bib` holds the research literature, with Zotero tags saying where and how each work is relevant.

## File types

| Type | Place | What it is |
|---|---|---|
| game | `games/<game>/game.md` | the game, its reference source, and how it was played for GEAR |
| evidence | `games/<game>/<name>.md` | one piece of evidence, such as a quest or mission: the sequence and its events in numbered sections |
| tag | `tags/<name>.md` | a term: definition, aspects, discussion |

An evidence entry is one file. Its sections are numbered:

```
## 0. The Art of Persuasion        the sequence: the place in the game, if there is one
### Description                    part, quest and quest ID, quest giver, location, previous and next
### Interpretation                 optional: reading of the whole

## 1. Accepting the quest          an event: one moment in the sequence
### Description
### Observation
### Interpretation

## 2. Using the Neural Needler
…
```

Section 0 is the sequence in the sense of DiGAP (item 20, the unit the game was divided into). It is written only where it applies, such as a quest, mission, chapter or level, and then needs `unit` in the frontmatter. Events start at 1 and are numbered without gaps, in the order of play. An event describes only its moment; what the quest or mission is stands once in section 0.

The frontmatter holds what applies to the whole entry (`observed`, `tags`) and, under `events`, the coding of each event by its number:

```yaml
observed:                      # conditions of observation, for every event
  date: 2026-11-22
  version: "Wrath of the Lich King Classic"
  platform: web
  language: enUS
  by: Stephan Schölzel
events:
  1:
    source: "wowclassicdb.com/wotlk/quest/11648"   # required; played: "own play"
    locator: "quest offer text"                     # played: timecode; read: the exact place
    layer: fixed
    agency: optional
  3:
    observed: {version: "patch 3.0.2"}              # an event can override single fields
    …
```

### Versions and branches

Some games exist in several branches that run side by side, such as retail and the Classic branches of World of Warcraft. Such a game lists its branches under `branches` in `game.md` and explains them in a section Versions. `observed.branch` then says in which branch something was observed; an event can override that.

`first_appeared` records where a sequence appeared first: branch (if the game has branches), version or patch and a note such as the expansion and year. What matters is that it was there, not whether it is still there. A sequence that also exists in later branches stays one entry as long as its content is the same. Where the content differs, the branch gets an entry of its own, linked with `variant_of: <evidence ID>`. Games without branches need none of this; there `version` is enough.

An event is cited as `EVD-WOW-0001.2`, the ID of the entry and the number of the section. The entry's file name is free (`a-z`, `0-9`, `_`), usually the name of the quest or mission.

Interpretations and notes belong in the evidence or the tag. A reading of one event goes into its Interpretation, a reading of the whole sequence into section 0; readings across entries, concepts and open questions go into the tag. Open questions are marked "Open:". Unfinished private notes do not belong in GEAR; keep them in `_local/` (not committed) or outside the repository.

## What goes where in a file

| Layer | Place | Question | Example |
|---|---|---|---|
| Metadata | frontmatter | What is this file, where does the evidence come from? | `id`, `status`, `observed`, `source`, `locator` |
| Coding | frontmatter | Which fixed categories apply? | `layer`, `agency`, `tags` |
| Description | text | What is this place in the game? | in section 0: expansion, quest and quest ID, quest giver, location; in an event: the moment |
| Observation | text | What could be seen or done? | "After each use the prisoner whispers a line." |
| Interpretation | text | What does it mean? | reading, research literature, links to aspects of tags |

**Metadata** describe the evidence, not the game. Where a file belongs follows from its folder and is not repeated.

**Source and locator** come from the raw material and stay apart from the processed text (OAIS). `source` is required for every event: for read material the reference, with URL and access date where one exists; for played material `own play`. A `locator` names the exact place: a timecode (`HH:MM:SS`) for played video, a Media Fragments `#t=` fragment for web video, the section or passage name for text.

**Coding** uses only controlled values. `tags` must name a file in `tags/`; all other codes come from `vocabularies.yaml`. Free tags are not allowed, because they drift (`torture`, `folter`, `torture_scene`).

**Description** identifies the place in the game: part or expansion, quest or mission, in-game IDs, names. It follows the game's reference source and stands in section 0; an event's Description names only the moment within it.

**Observation** records what is perceivable, with a timecode (played) or a locator (read). No judgement, no assumed intentions. Short quotes are allowed. The [observation style guide](schema/observation_style.md) gives the rules.

**Interpretation** is the reading of this one event, or in section 0 of the whole sequence. Readings across entries belong in a tag.

**Rules, dynamics and effects** (MDA) map onto these layers. The rules the game sets and what happens in play are observed; they go into Description and Observation, coded with `layer` and `agency`. What this does to the player or reader is a reading and goes into Interpretation. The `consequence` field is observed: what the game does next.

## Coding

### Layer: fixed, conditional, contingent

Would this observation turn out the same in every playthrough?

| Value | Meaning | Example |
|---|---|---|
| `fixed` | laid down in the game, the same for everyone in this version | quest text, item text, a scripted sequence |
| `conditional` | laid down, but only appears after certain choices or states | the prisoner's lines when the needler is used after the confession |
| `contingent` | arises in this playthrough | which torture method is chosen in "By the Book" |

The distinction runs across narrative and ludic content: a rule can be fixed, a cutscene can depend on earlier choices. Fixed is not timeless; patches, phasing and localisation change content, so the version always matters. Fixed content can be evidenced by reading game data or a reference database; contingent content needs play, one's own or that described in a walkthrough. Background: Aarseth's textons and scriptons (1997) and Juul's progression and emergence (2005); GEAR adopts neither pair of terms.

### Agency

How is the player involved in what the event shows? Coded per event under `events`. `reference` (only mentioned), `watching` (shown, no action), `optional` (can carry it out), `forced` (must carry it out to go on).

For `optional` and `forced` two more fields apply:

```yaml
agency: forced
act: perform            # trigger: the player only decides, the game carries it out
                        # perform: the player carries it out through play
consequence:
  if_done: progress     # what follows if the player acts
  if_not_done: blocks   # what follows if the player does not
```

Consequences: `none`, `progress`, `reward`, `penalty`, `branch` (changes later content), `blocks` (cannot go on), `fail`, `unknown`. What exactly happens is described in the Observation.


## Tags

Tags are used sparingly. A tag names a broad topic, such as `torture`; finer distinctions are sections under Aspects in the tag's file, such as outsourced torture, white torture or torture past the information. An evidence entry carries the tag; an event links to the aspect in its interpretation (`tags/torture.md#white-torture`).

A tag file is both an index entry and a note in the sense of a Zettelkasten: definition, aspects, discussion. It is GEAR's codebook (DiGAP item 27). `related` connects closely related tags; `mappings` points to concepts in other vocabularies (VGMS, Game Ontology Project, Gameplay Design Patterns, Wikidata), without copying them.

## Literature

GEAR collects research literature with a concrete reference to a game, an evidence entry, an event or a tag in GEAR. General game studies texts without such a reference are not collected; texts this documentation relies on are listed under [References](#references).

The literature is kept in Zotero, in a collection of its own. Better BibTeX exports this collection automatically to `literature/game_evidence_archive_and_repository.bib`; GEAR only reads this file. In the export settings of Better BibTeX, leave out the fields `file` (local paths) and `abstract` (publishers' text, not covered by CC BY).

A work is connected to GEAR with Zotero tags of the form `gear:<target>:<role>`:

| Zotero tag | Meaning |
|---|---|
| `gear:torture:analysis` | analyses the topic of the tag `torture` |
| `gear:grand_theft_auto_v:coverage` | reports on the game in `games/grand_theft_auto_v/` |
| `gear:EVD-WOW-0001:analysis` | analyses this evidence entry, the quest as a whole |
| `gear:EVD-GTA5-0001.4:analysis` | analyses this one event |

Every tag needs a target: a tag, a game folder, an evidence ID or an event ID. Roles: `analysis`, `coverage`, `collection` (an edited volume or special issue on the title), `method`, `theory`, `context`, `source` (a primary source such as a patent, a rulebook or a statement by the developer). A work with tags for both a game and a tag shows up where the two meet. Other Zotero tags are ignored; summaries and notes stay in Zotero. In any text, literature is cited with Pandoc citekeys such as `[@willsAintAmericanDream2021]`.

## Relations

Every relation that must be found again is stated once, in the more specific file, with controlled values:

| Relation | Where |
|---|---|
| evidence belongs to a game | folder |
| event belongs to an evidence entry | numbered section in its file |
| evidence concerns a term | `tags` in the evidence |
| literature concerns a game, evidence, event or term, and how | Zotero tag `gear:<target>:<role>` |
| text cites literature | citekey `[@key]` |

Game and tag pages do not list their evidence or literature by hand; scripts and the website build those lists. Links in the text are for reading: ordinary Markdown links, no wikilinks. The validator checks that every link and every citekey resolves.

## Workflow

1. **Research.** Find out what exists about the game and where the passage is (see below).
2. **Set up the game.** If it is new: `games/<game>/game.md` with reference source and boundaries.
3. **Set up the evidence.** Copy `templates/evidence.md` into the game's folder, named after the quest or mission. Fill in section 0 from the reference source, or delete it if there is no sequence.
4. **Write events.** One numbered section per moment: description, observation, interpretation, kept apart. Code each under `events` with `layer` and `agency`, and name a `source` and a precise `locator`; set `tags` for the entry.
5. **Extend tags.** A new topic gets a file in `tags/`; a new aspect a section in the tag.
6. **Add literature** in Zotero, with `gear:` tags.
7. **Check and commit.** `python scripts/validate.py`, then set the status.

### Research sources

These help to find games, passages and context. What they say is checked before it enters GEAR.

| Source | Use |
|---|---|
| [Game Walkthrough Corpus (GWTC)](https://www.informatik.uni-leipzig.de/~jtiepmar/forschung/gwtc/) | more than 12,000 walkthroughs for more than 6,000 games in English and German (Tiepmar & Burghardt 2021); find out whether walkthroughs exist and narrow down a passage via word lists and n-grams |
| [MobyGames](https://www.mobygames.com) | releases, platforms, versions, credits |
| [IGDB](https://www.igdb.com) | game metadata with stable IDs, also usable by script |
| [VNDB](https://vndb.org) | visual novels: releases, routes, characters |
| [Does the Dog Die?](https://www.doesthedogdie.com) | crowd-sourced content notes; a hint where a topic occurs in a game |
| [TV Tropes](https://tvtropes.org) | recurring motifs across games; a lead, never cited as evidence |

A walkthrough can serve as evidence; the event's `source` names it, with the GWTC document ID and the URL of the original where available. It is second-hand observation: its author played under conditions that are usually unknown, and the event says so. Walkthroughs are protected by copyright, so only short passages are quoted.

### Reference sources

Information about a game and its content (titles, IDs, names, places, quest chains) comes from the established sources for that game. Official sources by developers or publishers come first; where there are none, use the database the game's community relies on. The reference source is named in `game.md`: [Wowhead](https://www.wowhead.com) for World of Warcraft, the [GTA Wiki](https://gta.fandom.com) for Grand Theft Auto V.

## Search and browse

```
pip install -r requirements.txt
python scripts/validate.py
python scripts/export.py
python scripts/tree.py
datasette build/gear.db -m datasette.yaml
```

- `validate.py` checks fields, IDs, file names, tags, links, citekeys and the `gear:` tags in the literature.
- `export.py` writes `build/` (not committed): CSV files for spreadsheets, `gear.json` for the website and `gear.db`, an SQLite database with full-text search.
- `tree.py` prints GEAR as a tree: game, evidence, events, with the literature at each level. `--by tag` turns it round, `--game` and `--tag` narrow it down, `--md` also writes the trees as Markdown with links.
- [Datasette](https://datasette.io) shows `gear.db` in the browser at `http://localhost:8001`, with facets, full-text search and saved queries (evidence by tag, tags by game, literature for a tag, game, evidence or event).

The files remain the source; everything in `build/` can be rebuilt at any time. After every push to `main`, the export is also published at `https://stschoelzel.github.io/GEAR/` (`gear.json`, the CSV files and `gear.db`); the website gear.madsomeness.de reads `gear.json` from there.

## Method: DiGAP

GEAR follows the Digital Game Analysis Protocol (DiGAP) by Daneels, Denoo, Vandewalle, Dupont and Malliet, published in *Game Studies* in 2022. Game analysis is one of the most common methods in game studies, but there is little agreement on how to carry it out and report it. Researchers play themselves, make choices, play some parts and skip others, and all of this shapes what they find. DiGAP responds with a checklist of 31 items in seven sections that an analysis should disclose:

1. rationale and objectives
2. the researcher's background, play style and prior experience
3. which games were selected and why
4. boundaries: date, version, platform, difficulty, modes, depth of engagement, what counts as completed, in-game choices, how the game was divided into units, which paratexts were used
5. the analytical approach and framework
6. what data were collected and how they were coded
7. reporting and open availability

Not every item applies to every analysis. DiGAP does not prescribe a theory or a method of interpretation; it asks that choices be made visible.

In GEAR, the game file covers game selection (item 9), the researcher (items 5 to 7) and how the game was played (items 15 to 21), with depth of play coded after Aarseth (2003). Section 0 of an evidence entry is the unit the game was divided into (item 20). Each entry records date, version and platform (items 12 to 14), which an event can override. Evidence entries and their events are the collected data (items 25 and 26), tags the codebook (item 27), and the open repository fulfils item 31. Research question and framework (sections 1 and 5) belong to the publication that uses GEAR, not to the dataset.

## Languages

GEAR is written in English. German is the second language and the fallback: an entry may be written in German if there is no English version. More languages can be added in `vocabularies.yaml`.

- A file without a language suffix is the original. It carries all metadata and states its language in `lang` (default `en`).
- Translations sit next to it as `<name>.<lang>.md`. They contain only `lang`, `status` and optionally `title`.
- Quotes from the game stay in the language of the client that was played or read.

## Status

Everything committed here is public. `status` says how reliable an entry is: `draft` (not yet checked), `reviewed` (observation checked against the material), `citable` (reviewed and released for citation).

## Files

| File | Content |
|---|---|
| `vocabularies.yaml` | controlled values with labels per language |
| `schema/` | fields, IDs and rules, observation style guide, what is prepared for later |
| `templates/` | empty files to copy |
| `media/manifest.csv` | recordings and stills, relative path and hash only; media files are not in the repository |
| `scripts/` | `validate.py`, `export.py`, `tree.py` |
| `.github/workflows/validate.yml` | runs `validate.py` on every push and pull request; after a push to `main` it publishes `build/` on GitHub Pages |
| `datasette.yaml` | facets and saved queries for Datasette |
| `requirements.txt` | Python packages |

## Licence

Data and texts are licensed under [CC BY 4.0](LICENSE), the code in `scripts/` under [MIT](LICENSE-code).

Third-party content is not covered by CC BY: game texts, dialogue quotes, walkthroughs, screenshots and recordings. The rights remain with their holders. GEAR contains only short quotes under quotation right; media appear only as entries in the manifest.

## Citation

See [CITATION.cff](CITATION.cff). Always cite a specific state of the dataset, with commit hash or release.

## References

Aarseth, E. J. (1997). *Cybertext: Perspectives on Ergodic Literature*. Johns Hopkins University Press.

Aarseth, E. (2003). Playing Research: Methodological Approaches to Game Analysis. *Proceedings of the 5th Digital Arts and Culture Conference*, Melbourne.

Burghardt, M. & Tiepmar, J. (2021). The Game Walkthrough Corpus (GWTC). A Resource for the Analysis of Textual Game Descriptions. *Journal of Open Humanities Data*, 7. https://doi.org/10.5334/johd.34

Daneels, R., Denoo, M., Vandewalle, A., Dupont, B. & Malliet, S. (2022). The Digital Game Analysis Protocol (DiGAP): Introducing a Guide for Reflexive and Transparent Game Analyses. *Game Studies*, 22(2). https://gamestudies.org/2202/articles/gap_daneels_denoo_vandewalle_dupont_malliet

Juul, J. (2005). *Half-Real: Video Games between Real Rules and Fictional Worlds*. MIT Press.

Remael, A., Reviers, N. & Vercauteren, G. (Eds.) (2015). *Pictures Painted in Words: ADLAB Audio Description Guidelines*. Trieste.

Tiepmar, J. & Burghardt, M. (2021). *Game Walkthrough Corpus (GWTC)* (Version 1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.4562336
