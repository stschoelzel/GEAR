---
id: EVD-WOW-0001
type: evidence
schema_version: "0.8"
status: draft
title: The Art of Persuasion
unit: quest
first_appeared:
  branch: original
  version: "3.0.2"
  note: "Wrath of the Lich King, 2008"
observed:
  date: 2026-11-22
  branch: wrath_classic
  version: "3.4.x"
  platform: web
  language: enUS
  by: Stephan Schölzel
tags: [torture]
events:
  1:
    source: "[wowclassicdb.com, quest 11648](https://wowclassicdb.com/wotlk/quest/11648); Warcraft Wiki"
    locator: "quest offer text"
    layer: fixed
    agency: optional
    act: trigger
    consequence: {if_done: progress, if_not_done: unknown}
  2:
    observed: {branch: retail, version: unknown}
    source: "Warcraft Wiki, The Art of Persuasion and Imprisoned Beryl Sorcerer"
    locator: "Notes, objective 'Prisoner Interrogated'"
    layer: fixed
    agency: forced
    act: perform
    consequence: {if_done: progress, if_not_done: blocks}
  3:
    observed: {branch: original, version: "3.0.2"}
    source: "Warcraft Wiki, Prototype Neural Needler"
    locator: "item tooltip, Prototype Neural Needler"
    layer: fixed
    agency: reference
  4:
    observed: {branch: retail, version: unknown}
    source: "Warcraft Wiki (Wowpedia), The Art of Persuasion, Notes"
    locator: "Notes, continued use after the objective"
    layer: conditional
    agency: optional
    act: perform
    consequence: {if_done: none, if_not_done: none}
---

# The Art of Persuasion

Game: [World of Warcraft](game.md).

## 0. The Art of Persuasion

### Description

| | |
|---|---|
| Part | Wrath of the Lich King (2008) |
| Quest | [The Art of Persuasion, ID 11648](https://www.wowhead.com/quest=11648) |
| Location | Borean Tundra, Amber Ledge |
| Quest giver | Librarian Normantis (also receives the quest) |
| Previous | The Borean Inquisition |
| Next | Sharing Intelligence |
| Reward | reputation with the Kirin Tor |

The Kirin Tor want to know where the blue dragonflight holds Lady Evanor. The player is to use the item Neural Needler on an imprisoned sorcerer until he reveals it.

The events so far rely on sources for different branches, each named with the event. Whether quest text, item text and the prisoner's lines are the same in all of them is not yet checked.

## 1. Accepting the quest

### Description

Quest text shown by Librarian Normantis when offering the quest.

### Observation

In the quest text, Normantis says the Kirin Tor code of conduct "frowns upon our taking certain 'extreme' measures". The player, as an outsider, is not bound by these restrictions and may take any steps necessary. The objective is to use the Neural Needler on the Imprisoned Beryl Sorcerer until he reveals where Lady Evanor is held.

### Interpretation

The institution keeps its rules and has the act carried out by someone they do not apply to. See [outsourced torture](../../tags/torture.md#outsourced-torture).

Open: Is there a way around the quest, and does the chain continue without it?

## 2. Using the Neural Needler

### Description

Objective "Prisoner Interrogated". Target is the Imprisoned Beryl Sorcerer on the second floor of the tower on Amber Ledge.

### Observation

After each use of the Neural Needler the prisoner whispers a line: first defiance, then a plea to be released. After the third line he reveals where Lady Evanor is held, and the objective "Prisoner Interrogated" is complete. The player still holds the needler.

### Interpretation

The torture is a fixed sequence of three uses; the prisoner's resistance is scripted, not a matter of skill or chance.

## 3. Item text of the Neural Needler

### Description

Item tooltip of the Prototype Neural Needler, added in patch 3.0.2, a replacement for the quest item Neural Needler (section 2), handed out by Initiate Mehrtens if the original is destroyed. Conjured item with two charges.

### Observation

The tooltip reads: "Inflicts incredible pain to target, but does no permanent damage."

### Interpretation

The game names the device's purpose plainly and adds that it leaves no permanent damage. See [white torture](../../tags/torture.md#white-torture).

## 4. Continuing after the confession

### Description

After the objective is complete (section 2) the needler stays in the inventory and can still be used on the prisoner.

### Observation

If the player uses the needler again, the prisoner answers with further lines, among them: "Your continued abuse is senseless!"

### Interpretation

The game provides lines for torture that no longer serves the quest. It anticipates that players will go on, and comments on it from the victim's side. See [torture past the information](../../tags/torture.md#torture-past-the-information).
