---
id: EVD-RIM-0001
type: evidence
schema_version: "0.8"
status: draft
title: "Treatment of prisoners"
observed:
  date: 2026-11-23
  version: "unknown"
  platform: web
  language: en
  by: Stephan Schölzel
tags: [torture]
events:
  1:
    source: "[RimWorld Wiki, Prisoners](https://rimworldwiki.com/wiki/Prisoners), accessed 2026-11-23; [RimWorld Wiki, Organ harvesting](https://rimworldwiki.com/wiki/Organ_harvesting), accessed 2026-11-23"
    locator: "wiki page Prisoners, sections Summary and Tips (unwanted prisoners)"
    layer: contingent
    agency: optional
    act: trigger
    consequence: {if_done: reward, if_not_done: none}
  2:
    source: "[RimWorld Wiki, Prisoners](https://rimworldwiki.com/wiki/Prisoners), accessed 2026-11-23; [RimWorld Wiki, Torture crown](https://rimworldwiki.com/wiki/Torture_crown), accessed 2026-11-23"
    locator: "wiki page Prisoners, section Tips (changing ideoligion); wiki page Torture crown"
    layer: contingent
    agency: optional
    act: trigger
    consequence: {if_done: unknown, if_not_done: none}
---

# Treatment of prisoners

Game: [RimWorld](game.md).

## 1. Operations on prisoners

### Description

What the player can order for prisoners.

### Observation

The game has no interaction called torture. Prisoners can be given any number of medical operations, among them injecting drugs, installing artificial body parts and organ harvesting. A kidney and a lung can be taken without killing the prisoner; a heart, a liver or the second kidney or lung kills. Unless the colony's ideoligion accepts organ use, the colony gets a mood penalty.

### Interpretation

Harm to prisoners arises from combining rules that are not made for torture; the game prices it in mood.

## 2. Keeping prisoners in pain

### Description

Converting prisoners to the colony's ideoligion (Ideology DLC).

### Observation

The wiki advises keeping prisoners in pain to convert them, and names the torture crown as a way of inflicting pain without risk. The torture crown (Ideology DLC) is a headpiece with spikes pointing inward. Worn, it adds 5 % pain without damage; normal pawns get a mood penalty of -5.

### Interpretation

Here the game has an item made for pain, and the community wiki names its use on prisoners.

Open: Isolation and withholding food are not yet documented.
