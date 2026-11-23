---
id: GAME-WOW
type: game
schema_version: "0.8"
status: draft
title: World of Warcraft
branches:
  original: "the game as released and patched until Cataclysm, patches 1.x to 3.3.5; no longer officially playable"
  retail: "the current game, continuously patched"
  classic_era: "Classic, re-release of patch 1.12 content"
  season_of_discovery: "seasonal Classic realms with new content on the basis of Classic, from 2023"
  wrath_classic: "Wrath of the Lich King Classic, patch 3.4.x"
  cata_classic: "Cataclysm Classic"
  mists_classic: "Mists of Pandaria Classic"
  forever: "World of Warcraft: Forever, from 4 November 2026; reworked original world with new content, in its own continuity apart from retail"
---

# World of Warcraft

## Description

Online role-playing game by Blizzard Entertainment, released in 2004 and updated continuously since.

## Versions

World of Warcraft exists in several branches that run side by side as separate clients with their own data: the current game (retail) and the Classic branches, which re-release older states on a newer engine. Within each branch, content changes with patches. The branch and the patch in which something was observed are recorded in `observed` of every evidence entry; `first_appeared` says where a sequence appeared first.

Content of older expansions stays in retail, but is reached differently: through Chromie Time, with level scaling and changed phasing.

A sequence that exists in several branches is one evidence entry as long as its content is the same. Where the content differs, a branch gets an entry of its own, linked with `variant_of`.

## Reference source

[Wowhead](https://www.wowhead.com). Blizzard offers no official database of quests and NPCs; Wowhead is the one the community relies on, with separate pages per branch. IDs in descriptions are taken from there.

## Boundaries

<!-- DiGAP items 5 to 7 and 15 to 21: how this game was played for GEAR -->

Not yet played for GEAR. The evidence so far is compiled from reference sources; each event names its source.
