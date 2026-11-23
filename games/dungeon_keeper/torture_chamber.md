---
id: EVD-DK-0001
type: evidence
schema_version: "0.8"
status: draft
title: "Torture Chamber"
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
    source: "[Dungeon Keeper Wiki, Torture Chamber](https://dungeonkeeper.fandom.com/wiki/Torture_Chamber), accessed 2026-11-23"
    locator: "wiki page Torture Chamber"
    layer: fixed
    agency: optional
    act: trigger
    consequence: {if_done: reward, if_not_done: none}
  2:
    source: "[Dungeon Keeper Wiki, Torture Chamber](https://dungeonkeeper.fandom.com/wiki/Torture_Chamber), accessed 2026-11-23"
    locator: "wiki page Torture Chamber"
    layer: fixed
    agency: optional
    act: trigger
    consequence: {if_done: reward, if_not_done: none}
---

# Torture Chamber

Game: [Dungeon Keeper](game.md).

## 0. Torture Chamber

### Description

| | |
|---|---|
| Kind | room type |
| First available | level 6, Snuggledell |
| Cost | 350 gold per tile |
| Attracts | Dark Mistresses |

Once unlocked, the player can build the room in every later level.

## 1. Converting prisoners

### Description

Torture of captured heroes and creatures.

### Observation

The player picks up a captured hero or creature from the Prison and drops it in the Torture Chamber. The prisoner is put on a torture device. Its health goes down over time until it joins the player's side. The player can heal the prisoner or let it eat chickens so that it does not die first.

### Interpretation

Torture is a resource for gaining units. Healing serves to keep the prisoner alive for the torture.

## 2. Torturing own creatures

### Description

Torture of the player's own creatures.

### Observation

The player can put an own creature in the Torture Chamber. All creatures of that type then work 25 % faster for half pay. The tortured creature can become angry or die; a creature that dies there becomes a Ghost.

### Interpretation

Torture also serves to discipline one's own workers.
