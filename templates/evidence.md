---
id: EVD-XXX-0001
type: evidence
schema_version: "0.8"
status: draft
title: "Template: Evidence"   # replace with the real title, usually the quest or mission
unit:              # only with section 0: quest | mission | chapter | level | cutscene | scene | menu | other
# first_appeared:  # where the sequence appeared first
#   branch:        # only if game.md lists branches
#   version:       # patch or version
#   note:          # e.g. expansion, year
# variant_of:      # evidence ID, if this entry is the variant of another in a different branch
observed:          # applies to every event; an event can override single fields under its own observed
  date:
  version:
  platform:
  language:
  by:
  # branch:        # only if game.md lists branches
  # server:        # online games: realm, region
  # season:        # online games: season, event
tags: []
events:
  1:
    # source:      # if read, not played: database, walkthrough, video
    timecode: "00:00:00"   # or locator: "..." for read material
    layer:         # fixed | conditional | contingent
    agency:        # reference | watching | optional | forced
    # only with optional or forced:
    # act:         # trigger | perform
    # consequence: {if_done: , if_not_done: }   # none | progress | reward | penalty | branch | blocks | fail | unknown
---

# Template: Evidence

Game: [Title](game.md).

## 0. Title of the sequence

<!-- only if the evidence is a place in the game such as a quest or mission (DiGAP item 20); otherwise delete section 0 and unit -->

### Description

<!-- part or expansion, in-game ID, location, characters, previous and next, reward -->

### Interpretation

<!-- optional: reading across the events -->

## 1. Title of the event

### Description

<!-- the moment within the sequence: step, objective, scene -->

### Observation

<!-- see schema/observation_style.md -->

### Interpretation

<!-- reading of this event; open questions marked "Open:" -->
