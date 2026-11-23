---
id: EVD-SCB-0001
type: evidence
schema_version: "0.8"
status: draft
title: "Interrogations"
unit: other
observed:
  date: 2026-11-23
  version: "unknown"
  platform: web
  language: en
  by: Stephan Schölzel
tags: [torture]
events:
  1:
    source: "[Splinter Cell Wiki, Interrogation](https://splintercell.fandom.com/wiki/Interrogation), accessed 2026-11-23; [GamesIndustry.biz, Ubisoft cuts torture scene](https://www.gamesindustry.biz/ubisoft-cuts-torture-scene-from-splinter-cell-blacklist), accessed 2026-11-23"
    locator: "wiki page Interrogation"
    layer: fixed
    agency: watching
  2:
    source: "[Splinter Cell Wiki, Interrogation](https://splintercell.fandom.com/wiki/Interrogation), accessed 2026-11-23"
    locator: "wiki page Interrogation"
    layer: fixed
    agency: optional
    act: trigger
    consequence: {if_done: unknown, if_not_done: unknown}
  3:
    source: "[Fox News, Splinter Cell cuts controversial torture sequence](https://www.foxnews.com/tech/splinter-cell-video-game-cuts-controversial-torture-sequence), accessed 2026-11-23"
    locator: "article, description of the released game"
    layer: fixed
    agency: watching
---

# Interrogations

Game: [Tom Clancy's Splinter Cell: Blacklist](game.md).

## 0. Interrogations

### Description

| | |
|---|---|
| Kind | recurring interrogations in cutscenes |

A demo shown at E3 before release had an interactive interrogation: Fisher stabs a captive below the collarbone, and the player turns the knife with the thumbstick. After negative reactions, Ubisoft removed interactive torture from the game. Producer Andrew Wilson gave the reactions as the reason ([GamesIndustry.biz](https://www.gamesindustry.biz/ubisoft-cuts-torture-scene-from-splinter-cell-blacklist), [Kotaku](https://kotaku.com/splinter-cell-blacklist-wont-have-interactive-torture-5980350), [Fox News](https://www.foxnews.com/tech/splinter-cell-video-game-cuts-controversial-torture-sequence)).

### Interpretation

A documented case in which interactive torture was replaced by cutscenes before release, following public criticism. Comparable with the predecessor, [Splinter Cell: Conviction](../tom_clancys_splinter_cell_conviction/interrogations.md).

## 1. Interrogation cutscene

### Description

Interrogation in the released game.

### Observation

Fisher interrogates a captive in a cutscene. The player does not act during the interrogation.

### Interpretation

Open: Assign the missions and describe what the cutscenes show.

## 2. Kill or no kill

### Description

End of an interrogation.

### Observation

After the interrogation the player chooses whether Fisher kills the captive or not.

### Interpretation

The player decides only after the torture, about the captive's life.

## 3. A tortured hostage

### Description

A hostage in the hands of the antagonists.

### Observation

Antagonists torture a hostage. Fisher frees the hostage.

### Interpretation

Torture stays in the game, but is done by the antagonists.

Open: Assign the mission.
