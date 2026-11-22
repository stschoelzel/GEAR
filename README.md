# GEAR

Game Evidence Archive & Repository

[Deutsch](README.de.md)

GEAR is an open dataset of gameplay evidence. Every claim about a game ("in quest X you have to do Y") should be traceable to a piece of evidence: who played or read what, when, under which conditions, and what they observed. Observation and interpretation are kept apart.

The dataset is plain Markdown with YAML frontmatter. Any text editor can read and edit it; Zettlr suits writing, VSCodium suits structure and Git. Scripts turn it into tables, a searchable database and trees, see [Search and browse](#search-and-browse). The public website is built from it in a separate repository (madGear).

The examples compare torture in two games: the quest "The Art of Persuasion" in World of Warcraft: Wrath of the Lich King and the mission "By the Book" in Grand Theft Auto V. Both are drafts compiled from reference sources and still have to be checked in play. Monopoly is set up with its literature but has no events yet.

## Three ways in

```
games/                                      look into a game
├── grand_theft_auto_v/
│   ├── game.md
│   └── by_the_book/                        a sequence: the mission
│       ├── sequence.md
│       ├── 0001_ordered_to_torture.md      its events
│       └── …
├── monopoly/
│   └── game.md
└── world_of_warcraft/
    ├── game.md
    └── the_art_of_persuasion/              a sequence: the quest
        ├── sequence.md
        ├── 0001_accepting_the_quest.md
        └── …
tags/                                       look up a term
└── torture.md
literature/                                 look up research
└── game_evidence_archive_and_repository.bib
```

**By game:** open the game's folder. It holds the game file and one folder per sequence, the place in the game such as a quest or mission. A sequence folder holds the sequence file and its events.

**By term:** open a file in `tags/`. It defines the term, describes its aspects and leads to all events and literature carrying it, across games.

**By literature:** `literature/game_evidence_archive_and_repository.bib` holds the research literature, with Zotero tags saying where and how each work is relevant.

## File types

| Type | Place | What it is |
|---|---|---|
| game | `games/<game>/game.md` | the game, its reference source, and how it was played for GEAR |
| sequence | `games/<game>/<sequence>/sequence.md` | a place in the game: quest, mission, chapter, level or scene, with its in-game IDs and context |
| event | `games/<game>/<sequence>/<nnnn>_<name>.md` | a single moment in the sequence as evidence, with the conditions under which it was observed |
| tag | `tags/<name>.md` | a term: definition, aspects, discussion |

A sequence is the frame, its events are the moments in it. What the quest or mission is (IDs, quest giver, location, previous and next) is described once in `sequence.md`; an event describes only its moment. A sequence can also carry an Interpretation of the whole.

Every event carries its conditions of observation in `observed`: date, version, platform, language, who observed it and, if it was read rather than played, the source. An event can therefore be read and cited on its own. The number in its file name is the number of its ID (`0002_…` is `EVT-WOW-0002`).

Interpretations and notes belong in the event or the tag. A reading of one event goes into its Interpretation; readings across events, concepts and open questions go into the tag. Open questions are marked "Open:". Unfinished private notes do not belong in GEAR; keep them in `_local/` (not committed) or outside the repository.

## What goes where in a file

| Layer | Place | Question | Example |
|---|---|---|---|
| Metadata | frontmatter | What is this file, where does the evidence come from? | `id`, `status`, `observed` |
| Coding | frontmatter | Which fixed categories apply? | `layer`, `agency`, `tags`, `content_warnings` |
| Description | text | What is this place in the game? | in the sequence: expansion, quest and quest ID, quest giver, location; in the event: the moment |
| Observation | text | What could be seen or done? | "After each use the prisoner whispers a line." |
| Interpretation | text | What does it mean? | reading, research literature, links to aspects of tags |

**Metadata** describe the evidence, not the game. Where a file belongs follows from its folder and is not repeated.

**Coding** uses only controlled values. `tags` must name a file in `tags/`; all other codes come from `vocabularies.yaml`. Free tags are not allowed, because they drift (`torture`, `folter`, `torture_scene`).

**Description** identifies the place in the game: part or expansion, quest or mission, in-game IDs, names. It follows the game's reference source and stands in the sequence; the event's Description names only the moment within it.

**Observation** records what is perceivable, with a timecode (played) or a locator (read). No judgement, no assumed intentions. Short quotes are allowed. The [observation style guide](schema/observation_style.md) gives the rules.

**Interpretation** is the reading of this one event. Readings across events belong in a tag.

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

How is the player involved in what the event shows? `reference` (only mentioned), `watching` (shown, no action), `optional` (can carry it out), `forced` (must carry it out to go on).

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

### Content warnings

| State | Meaning |
|---|---|
| field missing | not checked |
| `content_warnings: []` | checked, nothing found |
| `content_warnings: [torture]` | checked, values from `vocabularies.yaml` |

The values are grouped (violence, fear, burdensome themes, sexuality, language, substances, gambling, discrimination); see `vocabularies.yaml`.

## Tags

Tags are used sparingly. A tag names a broad topic, such as `torture`; finer distinctions are sections under Aspects in the tag's file, such as outsourced torture, white torture or torture past the information. An event carries the tag and links to the aspect in its interpretation (`tags/torture.md#white-torture`).

A tag file is both an index entry and a note in the sense of a Zettelkasten: definition, aspects, discussion. It is GEAR's codebook (DiGAP item 27). `related` connects closely related tags; `mappings` points to concepts in other vocabularies (VGMS, Game Ontology Project, Gameplay Design Patterns, Wikidata), without copying them.

## Literature

GEAR collects research literature with a concrete reference to a game, a sequence, an event or a finding in GEAR. General game studies texts without such a reference are not collected; texts this documentation relies on are listed under [References](#references).

The literature is kept in Zotero, in a collection of its own. Better BibTeX exports this collection automatically to `literature/game_evidence_archive_and_repository.bib`; GEAR only reads this file. In the export settings of Better BibTeX, leave out the fields `file` (local paths) and `abstract` (publishers' text, not covered by CC BY).

A work is connected to GEAR with Zotero tags of the form `gear:<target>:<role>`:

| Zotero tag | Meaning |
|---|---|
| `gear:torture:analysis` | analyses the topic of the tag `torture` |
| `gear:grand_theft_auto_v:coverage` | reports on the game in `games/grand_theft_auto_v/` |
| `gear:SEQ-WOW-001:analysis` | analyses this sequence, the quest as a whole |
| `gear:EVT-GTA5-0004:analysis` | analyses this one event |
| `gear:monopoly:source` | a primary source on the game, here its patents |

Every tag needs a target: a tag, a game folder, a sequence ID or an event ID. Roles: `analysis`, `coverage`, `collection` (an edited volume or special issue on the title), `method`, `theory`, `context`, `source` (a primary source such as a patent, a rulebook or a statement by the developer). A work with tags for both a game and a tag shows up where the two meet. Other Zotero tags are ignored; summaries and notes stay in Zotero. In any text, literature is cited with Pandoc citekeys such as `[@willsAintAmericanDream2021]`.

## Relations

Every relation that must be found again is stated once, in the more specific file, with controlled values:

| Relation | Where |
|---|---|
| sequence belongs to a game | folder |
| event belongs to a sequence and its game | folder |
| event concerns a term | `tags` in the event |
| literature concerns a game, sequence, term or event, and how | Zotero tag `gear:<target>:<role>` |
| text cites literature | citekey `[@key]` |

Game and tag pages do not list their events or literature by hand; scripts and the website build those lists. Links in the text are for reading: ordinary Markdown links, no wikilinks. The validator checks that every link and every citekey resolves.

## Workflow

1. **Research.** Find out what exists about the game and where the passage is (see below).
2. **Set up the game.** If it is new: `games/<game>/game.md` with reference source and boundaries.
3. **Set up the sequence.** Copy `templates/sequence.md` into a folder named after the quest or mission and fill in its Description from the reference source.
4. **Write events.** Copy `templates/event.md` into the sequence folder. Description, observation, interpretation, kept apart. Set `layer`, `agency`, `tags`.
5. **Extend tags.** A new topic gets a file in `tags/`; a new aspect a section in the tag.
6. **Add literature** in Zotero, with `gear:` tags.
7. **Check and commit.** `python scripts/validate.py`, then set the status.

### Research sources

These help to find games, passages and context. What they say is checked before it enters an event.

| Source | Use |
|---|---|
| [Game Walkthrough Corpus (GWTC)](https://www.informatik.uni-leipzig.de/~jtiepmar/forschung/gwtc/) | more than 12,000 walkthroughs for more than 6,000 games in English and German (Tiepmar & Burghardt 2021); find out whether walkthroughs exist and narrow down a passage via word lists and n-grams |
| [MobyGames](https://www.mobygames.com) | releases, platforms, versions, credits |
| [IGDB](https://www.igdb.com) | game metadata with stable IDs, also usable by script |
| [VNDB](https://vndb.org) | visual novels: releases, routes, characters |
| [Does the Dog Die?](https://www.doesthedogdie.com) | crowd-sourced content notes; a hint which passages to check for `content_warnings` |
| [TV Tropes](https://tvtropes.org) | recurring motifs across games; a lead, never cited as evidence |

A walkthrough can serve as evidence; `observed.source` names it, with the GWTC document ID and the URL of the original where available. It is second-hand observation: its author played under conditions that are usually unknown, and the event says so. Walkthroughs are protected by copyright, so only short passages are quoted.

### Reference sources

Information about a game and its content (titles, IDs, names, places, quest chains) comes from the established sources for that game. Official sources by developers or publishers come first; where there are none, use the database the game's community relies on. The reference source is named in `game.md`: [Wowhead](https://www.wowhead.com) for World of Warcraft, the [GTA Wiki](https://gta.fandom.com) for Grand Theft Auto V, [BoardGameGeek](https://boardgamegeek.com) and the publisher's rules for Monopoly.

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
- `tree.py` prints GEAR as a tree: game, sequence, events, with the literature at each level. `--by tag` turns it round, `--game` and `--tag` narrow it down, `--md` also writes the trees as Markdown with links.
- [Datasette](https://datasette.io) shows `gear.db` in the browser at `http://localhost:8001`, with facets, full-text search and saved queries (events by tag, tags by game, literature for a tag, game or event, content warnings by group).

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

In GEAR, the game file covers game selection (item 9), the researcher (items 5 to 7) and how the game was played (items 15 to 21), with depth of play coded after Aarseth (2003). Sequences are the units the game was divided into (item 20). Each event records date, version and platform (items 12 to 14). Events are the collected data (items 25 and 26), tags the codebook (item 27), and the open repository fulfils item 31. Research question and framework (sections 1 and 5) belong to the publication that uses GEAR, not to the dataset.

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
