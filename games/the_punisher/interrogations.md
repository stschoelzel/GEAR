---
id: EVD-PUN-0001
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
    source: "[Wikipedia, The Punisher (2005 video game)](https://en.wikipedia.org/wiki/The_Punisher_%282005_video_game%29), accessed 2026-11-23; [The Escapist, The Punisher game 2005](https://www.escapistmagazine.com/the-punisher-game-2005-volition-ultra-violent-gore-torture-adaptation/), accessed 2026-11-23"
    locator: "Wikipedia, section Gameplay"
    layer: fixed
    agency: optional
    act: perform
    consequence: {if_done: reward, if_not_done: none}
  2:
    source: "[Wikipedia, The Punisher (2005 video game)](https://en.wikipedia.org/wiki/The_Punisher_%282005_video_game%29), accessed 2026-11-23; [OGDB, The Punisher](https://ogdb.eu/index.php?section=article&articleid=591), accessed 2026-11-23"
    locator: "Wikipedia, section on the rating"
    layer: fixed
    agency: optional
    act: perform
    consequence: {if_done: penalty, if_not_done: none}
---

# Interrogations

Game: [The Punisher](game.md).

## 0. Interrogations

### Description

| | |
|---|---|
| Kind | recurring mechanic through the campaign |
| Forms | simple interrogations of grabbed enemies; interrogations at hot spots in the levels |

## 1. Interrogating an enemy

### Description

Interrogation of a grabbed enemy.

### Observation

The player as Frank Castle grabs an enemy and can interrogate him. At interrogation hot spots in the levels, the Punisher interrogates enemies with death threats and torture, using the surroundings. An intimidation meter shows the enemy's health and his breaking point. If the player holds the intimidation level at the breaking point for a few seconds, the enemy gives information.

### Interpretation

Torture is part of the core loop and is controlled through a meter: too little pressure gives nothing, too much kills.

## 2. Killing after the confession

### Description

After the enemy has confessed.

### Observation

In the released versions, interrogation scenes are shown in black and white. Killing a victim after the confession gives the player a penalty. According to Wikipedia, both were added to avoid an Adults Only rating.

### Interpretation

The penalty separates torture for information from killing for its own sake; it was added for the rating, not as part of the design.
