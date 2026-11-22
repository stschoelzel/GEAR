# GEAR

Game Evidence Archive & Repository

[English](README.md)

GEAR ist ein offener Datensatz für Gameplay-Belege. Jede Behauptung über ein Spiel ("in Quest X muss man Y tun") soll sich auf einen Beleg zurückführen lassen: wer hat wann, unter welchen Bedingungen, was gespielt oder gelesen und beobachtet. Beobachtung und Interpretation stehen dabei getrennt.

Der Datensatz besteht aus Markdown-Dateien mit YAML-Frontmatter und lässt sich mit jedem Texteditor bearbeiten; Zettlr eignet sich zum Schreiben, VSCodium für Struktur und Git. Skripte machen daraus Tabellen, eine durchsuchbare Datenbank und Bäume, siehe [Suchen und anzeigen](#suchen-und-anzeigen). Die öffentliche Website entsteht daraus in einem eigenen Repository (madGear).

Maßgeblich ist die [englische Fassung](README.md). Feldnamen und Werte sind englisch; ihre deutschen Bezeichnungen stehen in `vocabularies.yaml`.

Die Beispiele vergleichen Folter in zwei Spielen: die Quest "The Art of Persuasion" in World of Warcraft: Wrath of the Lich King und die Mission "By the Book" in Grand Theft Auto V. Beide sind Entwürfe aus Referenzquellen und müssen noch im Spiel geprüft werden. Monopoly ist mit seiner Literatur angelegt, hat aber noch keine Events.

## Drei Zugänge

```
games/                                      ins Spiel schauen
├── grand_theft_auto_v/
│   ├── game.md
│   └── by_the_book/                        eine Sequenz: die Mission
│       ├── sequence.md
│       └── 0001_ordered_to_torture.md …    ihre Events
├── monopoly/
│   └── game.md
└── world_of_warcraft/
    ├── game.md
    └── the_art_of_persuasion/              eine Sequenz: die Quest
        ├── sequence.md
        └── 0001_accepting_the_quest.md …
tags/                                       nach Begriffen suchen
└── torture.md
literature/                                 Fachliteratur nachschlagen
└── game_evidence_archive_and_repository.bib
```

**Über das Spiel:** den Ordner des Spiels öffnen. Darin liegen die Spieldatei und je Sequenz ein Ordner, also die Stelle im Spiel wie eine Quest oder Mission. Ein Sequenzordner enthält die Sequenzdatei und ihre Events.

**Über Begriffe:** eine Datei in `tags/` öffnen. Sie definiert den Begriff, beschreibt seine Aspekte und führt zu allen Events und aller Literatur dazu, über Spiele hinweg.

**Über Literatur:** `literature/game_evidence_archive_and_repository.bib` enthält die Fachliteratur, mit Zotero-Tags, die sagen, wo und wie ein Werk relevant ist.

## Dateitypen

| Typ | Ort | Was es ist |
|---|---|---|
| game | `games/<spiel>/game.md` | das Spiel, seine Referenzquelle und wie es für GEAR gespielt wurde |
| sequence | `games/<spiel>/<sequenz>/sequence.md` | eine Stelle im Spiel: Quest, Mission, Kapitel, Level oder Szene, mit spielinternen IDs und Kontext |
| event | `games/<spiel>/<sequenz>/<nnnn>_<name>.md` | ein einzelner Moment der Sequenz als Beleg, mit den Bedingungen, unter denen er beobachtet wurde |
| tag | `tags/<name>.md` | ein Begriff: Definition, Aspekte, Diskussion |

Eine Sequenz ist der Rahmen, ihre Events sind die Momente darin. Was die Quest oder Mission ist (IDs, Questgeber, Ort, vorherige und nächste) steht einmal in `sequence.md`; ein Event beschreibt nur seinen Moment. Eine Sequenz kann auch eine Interpretation des Ganzen tragen.

Jedes Event trägt seine Beobachtungsbedingungen in `observed`: Datum, Version, Plattform, Sprache, wer beobachtet hat und, wenn gelesen statt gespielt wurde, die Quelle. Ein Event lässt sich deshalb für sich lesen und zitieren. Die Nummer im Dateinamen ist die Nummer der ID (`0002_…` ist `EVT-WOW-0002`).

Deutungen und Notizen gehören ins Event oder in den Tag. Die Deutung eines Events steht in seiner Interpretation; Deutungen über Events hinweg, Begriffe und offene Fragen stehen im Tag. Offene Fragen werden mit "Open:" markiert. Unfertige private Notizen gehören nicht in GEAR; sie bleiben in `_local/` (wird nicht committet) oder außerhalb des Repos.

## Was wohin gehört

| Schicht | Ort | Frage | Beispiel |
|---|---|---|---|
| Metadaten | Frontmatter | Was ist diese Datei, woher stammt der Beleg? | `id`, `status`, `observed` |
| Kodierung | Frontmatter | Welche festen Kategorien treffen zu? | `layer`, `agency`, `tags`, `content_warnings` |
| Beschreibung (Description) | Text | Was ist das für eine Stelle im Spiel? | in der Sequenz: Erweiterung, Quest und Quest-ID, Questgeber, Ort; im Event: der Moment |
| Beobachtung (Observation) | Text | Was war zu sehen oder zu tun? | "Nach jeder Anwendung flüstert der Gefangene eine Zeile." |
| Interpretation | Text | Was bedeutet das? | Deutung, Fachliteratur, Links zu Aspekten eines Tags |

**Metadaten** beschreiben den Beleg, nicht das Spiel. Wohin eine Datei gehört, ergibt sich aus dem Ordner und steht nicht noch einmal da.

**Kodierung** nutzt nur kontrollierte Werte. `tags` muss eine Datei in `tags/` nennen; alle anderen Werte stehen in `vocabularies.yaml`. Freie Tags gibt es nicht, weil sie auseinanderlaufen (`torture`, `folter`, `torture_scene`).

**Beschreibung** kennzeichnet die Stelle im Spiel: Teil oder Erweiterung, Quest oder Mission, spielinterne IDs, Namen. Sie folgt der Referenzquelle des Spiels und steht in der Sequenz; die Beschreibung im Event nennt nur den Moment darin.

**Beobachtung** hält fest, was wahrnehmbar ist, mit Timecode (gespielt) oder Fundstelle (gelesen). Keine Wertung, keine Absicht unterstellen. Kurze Zitate sind erlaubt. Die Regeln stehen im [Leitfaden für Beobachtungen](schema/observation_style.de.md).

**Interpretation** ist die Deutung dieses einen Events. Deutungen über mehrere Events gehören in einen Tag.

## Kodierung

### Ebene: fest, bedingt, kontingent

Fällt diese Beobachtung in jedem Durchgang gleich aus?

| Wert | Bedeutung | Beispiel |
|---|---|---|
| `fixed` (fest) | im Spiel angelegt, in dieser Version für alle gleich | Questtext, Gegenstandstext, eine geskriptete Abfolge |
| `conditional` (bedingt) | angelegt, erscheint aber nur nach bestimmten Entscheidungen oder Zuständen | die Zeilen des Gefangenen, wenn der Needler nach dem Geständnis weiter benutzt wird |
| `contingent` (kontingent) | entsteht in diesem Durchgang | welche Foltermethode in "By the Book" gewählt wird |

Die Unterscheidung läuft quer zu Erzählung und Regeln: Eine Regel kann fest sein, eine Cutscene kann von früheren Entscheidungen abhängen. Fest heißt nicht zeitlos; Patches, Phasing und Lokalisierung ändern Inhalte, deshalb zählt immer die Version. Feste Inhalte lassen sich durch Lesen von Spieldaten oder einer Referenzdatenbank belegen; kontingente brauchen Spielen, eigenes oder das in einem Walkthrough beschriebene. Hintergrund sind Aarseths Textonen und Scriptonen (1997) und Juuls Progression und Emergenz (2005); GEAR übernimmt keines der beiden Begriffspaare.

### Beteiligung (agency)

Wie ist die Spieler:in an dem beteiligt, was das Event zeigt? `reference` (nur erwähnt), `watching` (gezeigt, ohne Handlung), `optional` (kann es ausführen), `forced` (muss es ausführen, um weiterzukommen).

Bei `optional` und `forced` kommen zwei Felder dazu:

```yaml
agency: forced
act: perform            # trigger: die Spieler:in entscheidet nur, das Spiel führt aus
                        # perform: die Spieler:in führt es spielend selbst aus
consequence:
  if_done: progress     # was folgt, wenn sie handelt
  if_not_done: blocks   # was folgt, wenn sie nicht handelt
```

Folgen: `none` (keine), `progress` (Fortschritt), `reward` (Belohnung), `penalty` (Nachteil), `branch` (verändert spätere Inhalte), `blocks` (kein Weiterkommen), `fail` (Scheitern), `unknown` (noch unbekannt). Was genau geschieht, steht in der Beobachtung.

### Inhaltshinweise

| Zustand | Bedeutung |
|---|---|
| Feld fehlt | nicht geprüft |
| `content_warnings: []` | geprüft, nichts gefunden |
| `content_warnings: [torture]` | geprüft, Werte aus `vocabularies.yaml` |

Die Werte sind gruppiert (Gewalt, Angst, belastende Themen, Sexualität, Sprache, Suchtmittel, Glücksspiel, Diskriminierung); siehe `vocabularies.yaml`.

## Tags

Tags werden sparsam vergeben. Ein Tag benennt ein breites Thema, etwa `torture`; feinere Unterscheidungen sind Abschnitte unter Aspects in der Datei des Tags, etwa ausgelagerte Folter, weiße Folter oder Folter über die Information hinaus. Ein Event trägt den Tag und verlinkt in seiner Interpretation auf den Aspekt (`tags/torture.md#white-torture`).

Eine Tag-Datei ist Registereintrag und Zettel zugleich: Definition, Aspekte, Diskussion. Sie ist das Codebuch von GEAR (DiGAP Item 27). `related` verbindet eng verwandte Tags; `mappings` verweist auf Begriffe anderer Vokabulare (VGMS, Game Ontology Project, Gameplay Design Patterns, Wikidata), ohne sie zu kopieren.

## Literatur

GEAR sammelt Fachliteratur mit konkretem Bezug zu einem Spiel, einer Sequenz, einem Event oder einem Befund in GEAR. Allgemeine Texte der Game Studies ohne solchen Bezug werden nicht gesammelt; Texte, auf die sich diese Dokumentation stützt, stehen unter [References](README.md#references).

Die Literatur wird in Zotero gepflegt, in einer eigenen Sammlung. Better BibTeX exportiert diese Sammlung automatisch nach `literature/game_evidence_archive_and_repository.bib`; GEAR liest diese Datei nur. In den Export-Einstellungen von Better BibTeX die Felder `file` (lokale Pfade) und `abstract` (Verlagstexte, nicht unter CC BY) weglassen.

Ein Werk wird über Zotero-Tags der Form `gear:<ziel>:<rolle>` mit GEAR verbunden:

| Zotero-Tag | Bedeutung |
|---|---|
| `gear:torture:analysis` | analysiert das Thema des Tags `torture` |
| `gear:grand_theft_auto_v:coverage` | berichtet über das Spiel in `games/grand_theft_auto_v/` |
| `gear:SEQ-WOW-001:analysis` | analysiert diese Sequenz, die Quest als Ganzes |
| `gear:EVT-GTA5-0004:analysis` | analysiert dieses eine Event |
| `gear:monopoly:source` | eine Primärquelle zum Spiel, hier seine Patente |

Jeder Tag braucht ein Ziel: einen Tag, einen Spielordner, eine Sequenz-ID oder eine Event-ID. Rollen: `analysis` (Analyse), `coverage` (Berichterstattung), `collection` (Sammelband oder Themenheft zum Titel), `method` (Methode), `theory` (Theorie), `context` (Kontext), `source` (Primärquelle wie ein Patent, eine Spielregel oder eine Aussage der Entwickler:innen). Ein Werk mit Tags für ein Spiel und einen Tag erscheint dort, wo beide sich treffen. Andere Zotero-Tags werden ignoriert; Zusammenfassungen und Notizen bleiben in Zotero. In allen Texten wird Literatur mit Pandoc-Citekeys wie `[@willsAintAmericanDream2021]` zitiert.

## Verknüpfungen

Jede Verknüpfung, die man wiederfinden muss, steht einmal, in der spezielleren Datei, mit kontrollierten Werten:

| Verknüpfung | Wo |
|---|---|
| Sequenz gehört zu einem Spiel | Ordner |
| Event gehört zu einer Sequenz und ihrem Spiel | Ordner |
| Event betrifft einen Begriff | `tags` im Event |
| Literatur betrifft ein Spiel, eine Sequenz, einen Begriff oder ein Event, und wie | Zotero-Tag `gear:<ziel>:<rolle>` |
| Text zitiert Literatur | Citekey `[@key]` |

Spiel- und Tag-Seiten führen ihre Events und Literatur nicht von Hand auf; Skripte und Website bauen diese Listen. Links im Text sind zum Lesen da: normale Markdown-Links, keine Wikilinks. Der Validator prüft, dass jeder Link und jeder Citekey aufgeht.

## Ablauf

1. **Recherche.** Klären, was es zum Spiel gibt und wo die Stelle liegt (siehe unten).
2. **Spiel anlegen.** Wenn es neu ist: `games/<spiel>/game.md` mit Referenzquelle und Abgrenzung.
3. **Sequenz anlegen.** `templates/sequence.md` in einen Ordner kopieren, der nach Quest oder Mission benannt ist, und die Beschreibung aus der Referenzquelle füllen.
4. **Events schreiben.** `templates/event.md` in den Sequenzordner kopieren. Beschreibung, Beobachtung, Interpretation, getrennt. `layer`, `agency` und `tags` setzen.
5. **Tags ergänzen.** Ein neues Thema bekommt eine Datei in `tags/`, ein neuer Aspekt einen Abschnitt im Tag.
6. **Literatur ergänzen** in Zotero, mit `gear:`-Tags.
7. **Prüfen und committen.** `python scripts/validate.py`, dann Status setzen.

### Recherchequellen

Sie helfen, Spiele, Stellen und Zusammenhänge zu finden. Was dort steht, wird geprüft, bevor es in ein Event kommt.

| Quelle | Nutzen |
|---|---|
| [Game Walkthrough Corpus (GWTC)](https://www.informatik.uni-leipzig.de/~jtiepmar/forschung/gwtc/) | über 12.000 Walkthroughs zu über 6.000 Spielen auf Englisch und Deutsch (Tiepmar & Burghardt 2021); prüfen, ob es Walkthroughs gibt, und über Wortlisten und N-Gramme eine Stelle eingrenzen |
| [MobyGames](https://www.mobygames.com) | Veröffentlichungen, Plattformen, Versionen, Credits |
| [IGDB](https://www.igdb.com) | Spieldaten mit stabilen IDs, auch per Skript nutzbar |
| [VNDB](https://vndb.org) | Visual Novels: Veröffentlichungen, Routen, Figuren |
| [Does the Dog Die?](https://www.doesthedogdie.com) | gesammelte Inhaltshinweise aus der Community; Hinweis, welche Stellen für `content_warnings` zu prüfen sind |
| [TV Tropes](https://tvtropes.org) | wiederkehrende Motive über Spiele hinweg; ein Fingerzeig, nie als Beleg zitiert |

Ein Walkthrough kann als Beleg dienen; `observed.source` nennt ihn, wo vorhanden mit GWTC-Dokument-ID und URL des Originals. Er ist eine Beobachtung aus zweiter Hand: Wer ihn verfasst hat, hat unter meist unbekannten Bedingungen gespielt, und das Event sagt das. Walkthroughs sind urheberrechtlich geschützt, zitiert werden nur kurze Stellen.

### Referenzquellen

Angaben über ein Spiel und seine Inhalte (Titel, IDs, Namen, Orte, Questreihen) kommen aus den etablierten Quellen des Spiels. Offizielle Quellen der Entwickler:innen oder Publisher gehen vor; gibt es keine, nimmt man die Datenbank, auf die sich die Community bezieht. Die Referenzquelle steht in `game.md`: [Wowhead](https://www.wowhead.com) für World of Warcraft, das [GTA Wiki](https://gta.fandom.com) für Grand Theft Auto V, [BoardGameGeek](https://boardgamegeek.com) und die Regeln des Verlags für Monopoly.

## Suchen und anzeigen

```
pip install -r requirements.txt
python scripts/validate.py
python scripts/export.py
python scripts/tree.py
datasette build/gear.db -m datasette.yaml
```

- `validate.py` prüft Felder, IDs, Dateinamen, Tags, Links, Citekeys und die `gear:`-Tags der Literatur.
- `export.py` schreibt `build/` (wird nicht committet): CSV-Dateien für Tabellenkalkulationen, `gear.json` für die Website und `gear.db`, eine SQLite-Datenbank mit Volltextsuche.
- `tree.py` gibt GEAR als Baum aus: Spiel, Sequenz, Events, mit der Literatur auf jeder Ebene. `--by tag` dreht ihn um, `--game` und `--tag` grenzen ein, `--md` schreibt die Bäume zusätzlich als Markdown mit Links.
- [Datasette](https://datasette.io) zeigt `gear.db` im Browser unter `http://localhost:8001`, mit Facetten, Volltextsuche und gespeicherten Abfragen (Events je Tag, Tags je Spiel, Literatur zu Tag, Spiel oder Event, Inhaltshinweise nach Gruppen).

Quelle bleiben die Dateien; alles in `build/` lässt sich jederzeit neu bauen. Nach jedem Push auf `main` wird der Export außerdem unter `https://stschoelzel.github.io/GEAR/` veröffentlicht (`gear.json`, die CSV-Dateien und `gear.db`); die Website gear.madsomeness.de liest `gear.json` von dort.

## Methode: DiGAP

GEAR folgt dem Digital Game Analysis Protocol (DiGAP) von Daneels, Denoo, Vandewalle, Dupont und Malliet, erschienen 2022 in *Game Studies*. Die Spielanalyse gehört zu den häufigsten Methoden der Game Studies, es gibt aber wenig Einigkeit darüber, wie man sie durchführt und darüber berichtet. Forschende spielen selbst, treffen Entscheidungen, spielen manches und anderes nicht, und all das prägt, was sie finden. DiGAP antwortet darauf mit einer Checkliste aus 31 Punkten in sieben Abschnitten, die eine Analyse offenlegen sollte:

1. Begründung und Ziele
2. Hintergrund, Spielweise und Vorerfahrung der Forschenden
3. Auswahl der Spiele und ihre Begründung
4. Abgrenzung: Datum, Version, Plattform, Schwierigkeit, Modi, Spieltiefe, was als abgeschlossen gilt, Entscheidungen im Spiel, Einteilung in Einheiten, genutzte Paratexte
5. Analyseansatz und theoretischer Rahmen
6. erhobene Daten und ihre Kodierung
7. Berichterstattung und offene Bereitstellung

Nicht jeder Punkt passt zu jeder Analyse. DiGAP schreibt keine Theorie und keine Deutungsmethode vor; es verlangt, dass Entscheidungen sichtbar werden.

In GEAR deckt die Spieldatei die Spielauswahl (Item 9), die Forschenden (Items 5 bis 7) und die Art des Spielens ab (Items 15 bis 21), die Spieltiefe kodiert nach Aarseth (2003). Sequenzen sind die Einheiten, in die das Spiel geteilt wurde (Item 20). Jedes Event hält Datum, Version und Plattform fest (Items 12 bis 14). Events sind die erhobenen Daten (Items 25 und 26), Tags das Codebuch (Item 27), und das offene Repo erfüllt Item 31. Fragestellung und Rahmen (Abschnitte 1 und 5) gehören in die Veröffentlichung, die GEAR nutzt, nicht in den Datensatz.

## Sprachen

GEAR ist englisch. Deutsch ist zweite Sprache und Ausweichsprache: Ein Eintrag darf deutsch geschrieben sein, wenn es keine englische Fassung gibt. Weitere Sprachen lassen sich in `vocabularies.yaml` ergänzen.

- Eine Datei ohne Sprachkürzel ist das Original. Sie trägt alle Metadaten und nennt ihre Sprache in `lang` (ohne Angabe `en`).
- Übersetzungen liegen daneben als `<name>.<sprache>.md`. Sie enthalten nur `lang`, `status` und bei Bedarf `title`.
- Zitate aus dem Spiel bleiben in der Sprache des Clients, der gespielt oder gelesen wurde.

## Status

Alles, was hier committet ist, ist öffentlich. `status` sagt, wie belastbar ein Eintrag ist: `draft` (Entwurf, noch nicht geprüft), `reviewed` (Beobachtung am Material kontrolliert), `citable` (geprüft und für Zitate freigegeben).

## Dateien

| Datei | Inhalt |
|---|---|
| `vocabularies.yaml` | kontrollierte Werte mit Bezeichnungen je Sprache |
| `schema/` | Felder, IDs und Regeln, Leitfaden für Beobachtungen, was für später vorbereitet ist |
| `templates/` | leere Dateien zum Kopieren |
| `media/manifest.csv` | Aufnahmen und Stills, nur relativer Pfad und Hash; Mediendateien liegen nicht im Repo |
| `scripts/` | `validate.py`, `export.py`, `tree.py` |
| `.github/workflows/validate.yml` | prüft jeden Push und Pull Request mit `validate.py`; nach einem Push auf `main` veröffentlicht er `build/` auf GitHub Pages |
| `datasette.yaml` | Facetten und gespeicherte Abfragen für Datasette |
| `requirements.txt` | Python-Pakete |

## Lizenz

Daten und Texte stehen unter [CC BY 4.0](LICENSE), der Code in `scripts/` unter [MIT](LICENSE-code).

Nicht unter CC BY stehen Inhalte Dritter: Spieltexte, Dialogzitate, Walkthroughs, Screenshots und Aufnahmen. Die Rechte daran liegen bei den jeweiligen Rechteinhabern. GEAR enthält davon nur kurze Zitate im Rahmen des Zitatrechts; Medien stehen nur als Eintrag im Manifest.

## Zitieren

Siehe [CITATION.cff](CITATION.cff). Zitiert wird immer ein Stand des Datensatzes, mit Commit-Hash oder Release.

## Literatur

Siehe [README.md](README.md#references) und [literature/game_evidence_archive_and_repository.bib](literature/game_evidence_archive_and_repository.bib).
