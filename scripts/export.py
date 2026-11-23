#!/usr/bin/env python3
"""Exports GEAR into tables for searching and browsing.

Run from the repository root:  python scripts/export.py
Writes build/ (not committed):
  games.csv, evidence.csv, events.csv, tags.csv, translations.csv,
  literature.csv, literature_links.csv, labels.csv, gear.json, gear.db
gear.db is SQLite with full-text search; open it with  datasette build/gear.db -m datasette.yaml
"""
import csv
import json
import re
import sqlite3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build"
VOC = yaml.safe_load((ROOT / "vocabularies.yaml").read_text(encoding="utf-8"))
CODED = ["layer", "agency", "engagement", "status", "lang"]
# section names in German translations
DE_SECTIONS = {"beschreibung": "description", "beobachtung": "observation", "deutung": "interpretation",
               "aspekte": "aspects", "diskussion": "discussion", "abgrenzung": "boundaries",
               "referenzquelle": "reference_source"}
NUMBERED = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$")


def read(path):
    """Return (frontmatter, {section: text}, title from first heading)."""
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    if text.startswith("---"):
        _, raw, body = text.split("---", 2)
        fm = yaml.safe_load(raw) or {}
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    sections, current = {}, "_intro"
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            current = re.sub(r"\W+", "_", m.group(1).strip().lower()).strip("_")
            continue
        if line.startswith("# "):
            continue
        sections.setdefault(current, []).append(line)
    return fm, {k: "\n".join(v).strip() for k, v in sections.items()}


def key(heading):
    k = re.sub(r"\W+", "_", heading.strip().lower()).strip("_")
    return DE_SECTIONS.get(k, k)


def read_numbered(path):
    """Evidence file: (frontmatter, {n: {"title", "description", ...}}).

    Numbered sections are "## <n>. <title>", their parts "### Description" and so on.
    """
    text = path.read_text(encoding="utf-8")
    fm, body = {}, text
    if text.startswith("---"):
        _, raw, body = text.split("---", 2)
        fm = yaml.safe_load(raw) or {}
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    parts, n, part = {}, None, None
    for line in body.splitlines():
        m = NUMBERED.match(line)
        if m:
            n, part = int(m.group(1)), "_text"
            parts[n] = {"title": m.group(2), "_text": []}
            continue
        if n is None:
            continue
        m = re.match(r"^###\s+(.+?)\s*$", line)
        if m:
            part = key(m.group(1))
            parts[n][part] = []
            continue
        parts[n][part].append(line)
    return fm, {n: {k: (v if k == "title" else "\n".join(v).strip()) for k, v in s.items()} for n, s in parts.items()}


def anchor(n, title):
    """GitHub's anchor for the heading "## <n>. <title>"."""
    return re.sub(r"[^\w\- ]", "", f"{n}. {title}".lower()).replace(" ", "-")


def split_lang(path):
    stem = path.name[:-3]
    return tuple(stem.rsplit(".", 1)) if "." in stem else (stem, None)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


LATEX = {r"\textendash": "-", r"\textemdash": "-", r"\textregistered": "\u00ae", r"\&": "&", r"\%": "%",
         r"\ss": "\u00df", "``": "\u201c", "''": "\u201d", "--": "-"}
ACCENTS = {'"': "\u0308", "'": "\u0301", "`": "\u0300", "^": "\u0302", "~": "\u0303", "c": "\u0327", "v": "\u030c"}


def latex_to_text(s):
    """Turn the LaTeX that Better BibTeX writes into plain Unicode."""
    import unicodedata
    s = re.sub(r"\\(emph|textit|textbf)\{([^{}]*)\}", r"\2", s)
    s = re.sub(r"\{?\\([\"'`^~cv])\s*\{?([A-Za-z])\}?\}?",
               lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENTS[m.group(1)]), s)
    for k, v in LATEX.items():
        s = s.replace(k, v)
    s = re.sub(r"\$\\leftrightarrow\$", "\u2194", s)
    return re.sub(r"\s+", " ", re.sub(r"[{}]", "", s)).strip()


def read_bib(path):
    entries = []
    if not path.exists():
        return entries
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"^@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)(?=^@|\Z)", text, flags=re.S | re.M):
        fields = {"entrytype": m.group(1).lower(), "citekey": m.group(2)}
        for f in re.finditer(r"^\s*(\w+)\s*=\s*(?:\{(.*)\}|\"(.*)\"|([^,\s]+))\s*,?\s*$", m.group(3), flags=re.M):
            value = next(v for v in f.groups()[1:] if v is not None)
            fields[f.group(1).lower()] = latex_to_text(value)
        entries.append(fields)
    return entries


def collect():
    """Read all files and return the tables as a dict of lists."""
    rel = lambda p: p.relative_to(ROOT).as_posix()
    games, evidence, events, tags, translations, labels = [], [], [], [], [], []
    literature, links = [], []

    for game_md in sorted((ROOT / "games").glob("*/game.md")):
        folder = game_md.parent.name
        fm, sec = read(game_md)
        games.append({"id": fm.get("id"), "game": folder, "title": fm.get("title"),
                      "wikidata": fm.get("wikidata") or "", "status": fm.get("status"),
                      "engagement": fm.get("engagement", ""), "branches": fm.get("branches") or {},
                      "versions": sec.get("versions", ""),
                      "description": sec.get("description", ""), "reference_source": sec.get("reference_source", ""),
                      "boundaries": sec.get("boundaries", ""),
                      "path": rel(game_md)})
        game_title = fm.get("title")

        for ev_md in sorted(game_md.parent.glob("*.md")):
            if ev_md.name == "game.md":
                continue
            base, lang = split_lang(ev_md)
            efm, parts = read_numbered(ev_md)
            if lang:
                translations.append({"of_path": rel(ev_md.parent / f"{base}.md"), "lang": lang,
                                     "title": efm.get("title", ""), "status": efm.get("status"),
                                     "text": "\n\n".join(v for s in parts.values() for v in s.values() if v),
                                     "path": rel(ev_md), "sections": {str(k): v for k, v in parts.items()}})
                continue
            eid, obs0 = efm.get("id"), efm.get("observed") or {}
            seq = parts.get(0, {})
            evidence.append({"id": eid, "game": folder, "game_title": game_title, "name": base,
                             "title": efm.get("title"), "lang": efm.get("lang", "en"), "status": efm.get("status"),
                             "unit": efm.get("unit", ""), "first_appeared": efm.get("first_appeared") or {},
                             "variant_of": efm.get("variant_of", ""), "sequence_title": seq.get("title", ""),
                             "sequence_anchor": anchor(0, seq["title"]) if seq else "",
                             "sequence_description": seq.get("description", ""),
                             "sequence_interpretation": seq.get("interpretation", ""),
                             "tags": as_list(efm.get("tags")),
                             "events": len([n for n in parts if n > 0]), "path": rel(ev_md)})
            meta = efm.get("events") or {}
            for n, sec in sorted(parts.items()):
                if n == 0:
                    continue
                em = meta.get(n) or {}
                obs = {**obs0, **(em.get("observed") or {})}
                cons = em.get("consequence") or {}
                events.append({"id": f"{eid}.{n}", "evidence": eid, "n": n, "game": folder, "game_title": game_title,
                               "evidence_title": efm.get("title"), "title": sec.get("title"), "lang": efm.get("lang", "en"),
                               "observed_date": str(obs.get("date", "")), "branch": obs.get("branch", ""),
                               "version": str(obs.get("version", "")),
                               "platform": obs.get("platform", ""), "language": obs.get("language", ""),
                               "observed_by": obs.get("by", ""), "server": obs.get("server", ""),
                               "season": obs.get("season", ""), "source": em.get("source", ""),
                               "layer": em.get("layer", ""), "agency": em.get("agency", ""), "act": em.get("act", ""),
                               "if_done": cons.get("if_done", ""), "if_not_done": cons.get("if_not_done", ""),
                               "tags": as_list(efm.get("tags")),
                               "timecode": str(em.get("timecode", "")), "locator": em.get("locator", ""),
                               "media": as_list(em.get("media")), "coded_by": em.get("coded_by") or obs.get("by", ""),
                               "status": efm.get("status"),
                               "description": sec.get("description", ""), "observation": sec.get("observation", ""),
                               "interpretation": sec.get("interpretation", ""), "path": rel(ev_md), "anchor": anchor(n, sec.get("title", ""))})

    for tag_md in sorted((ROOT / "tags").glob("*.md")):
        tfm, tsec = read(tag_md)
        base, lang = split_lang(tag_md)
        if lang:
            translations.append({"of_path": rel(tag_md.parent / f"{base}.md"), "lang": lang,
                                 "title": tfm.get("title", ""), "status": tfm.get("status"),
                                 "text": "\n\n".join(v for v in tsec.values() if v), "path": rel(tag_md)})
            continue
        tags.append({"tag": base, "title": tfm.get("title"), "status": tfm.get("status"),
                     "related": as_list(tfm.get("related")), "mappings": as_list(tfm.get("mappings")),
                     "definition": tsec.get("definition", ""), "aspects": tsec.get("aspects", ""),
                     "discussion": tsec.get("discussion", ""), "path": rel(tag_md)})

    tag_names = {t["tag"] for t in tags}
    game_names = {g["game"] for g in games}
    event_ids = {e["id"] for e in events}
    for entry in read_bib(ROOT / "literature" / "game_evidence_archive_and_repository.bib"):
        kws = [k.strip() for k in re.split(r"[,;]", entry.get("keywords", "")) if k.strip()]
        literature.append({k: entry.get(k, "") for k in ("citekey", "entrytype", "author", "editor", "title", "year", "journal", "booktitle", "publisher", "doi", "url", "number", "nationality")})
        for kw in kws:
            if not kw.startswith("gear:"):
                continue
            parts = kw.split(":")[1:]
            if len(parts) != 2:
                continue  # rejected by validate.py
            target, role = parts
            kind = ("tag" if target in tag_names else "game" if target in game_names
                    else "event" if target in event_ids else "evidence")
            links.append({"citekey": entry["citekey"], "target_type": kind, "target": target or "", "role": role})

    for field, values in VOC.items():
        if isinstance(values, dict):
            for key, lab in values.items():
                if isinstance(lab, dict):
                    labels.append({"field": field, "value": key, "en": lab.get("en", ""), "de": lab.get("de", ""),
                                   "group": lab.get("group", "")})

    return {"games": games, "evidence": evidence, "events": events, "tags": tags,
            "translations": translations, "literature": literature, "literature_links": links, "labels": labels}


def meta():
    """Schema version and the Git state the data come from."""
    import subprocess
    from datetime import datetime, timezone
    def git(*args):
        try:
            r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=5)
            return r.stdout.strip() if r.returncode == 0 else ""
        except (OSError, subprocess.SubprocessError):
            return ""
    commit = git("rev-parse", "--short", "HEAD")
    if commit and git("status", "--porcelain", "--", "games", "tags", "literature", "vocabularies.yaml"):
        commit += "+local"
    return {"schema_version": str(VOC.get("schema_version", "")), "commit": commit or "local",
            "commit_date": git("log", "-1", "--format=%cs"),
            "exported": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}


def main():
    tables = collect()
    events = tables["events"]
    OUT.mkdir(exist_ok=True)

    def flat(row):
        return {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v) for k, v in row.items()}

    for name, rows in tables.items():
        with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
            if rows:
                w = csv.DictWriter(f, fieldnames=list(rows[0]))
                w.writeheader()
                w.writerows(flat(r) for r in rows)
    (OUT / "gear.json").write_text(json.dumps({**tables, "meta": meta()}, ensure_ascii=False, indent=2, default=str),
                                   encoding="utf-8")

    db_path = OUT / "gear.db"
    if db_path.exists():
        db_path.unlink()
    db = sqlite3.connect(db_path)
    empty = {"literature": ["citekey", "entrytype", "author", "editor", "title", "year", "journal", "booktitle",
                            "publisher", "doi", "url", "number", "nationality"],
             "literature_links": ["citekey", "target_type", "target", "role"],
             "translations": ["of_path", "lang", "title", "status", "text", "path", "sections"]}
    for name, rows in tables.items():
        if not rows and name not in empty:
            continue
        cols = list(rows[0]) if rows else empty[name]
        db.execute(f"CREATE TABLE [{name}] ({', '.join(f'[{c}]' for c in cols)})")
        db.executemany(f"INSERT INTO [{name}] VALUES ({', '.join('?' for _ in cols)})", [list(flat(r).values()) for r in rows])
    # helper tables for many-to-many browsing
    evidence = tables["evidence"]
    db.execute("CREATE TABLE evidence_tags (evidence TEXT, tag TEXT)")
    db.executemany("INSERT INTO evidence_tags VALUES (?, ?)", [(e["id"], t) for e in evidence for t in e["tags"]])
    # full-text search, in the layout Datasette recognises
    fts = {"events": ["title", "description", "observation", "interpretation"],
           "evidence": ["title", "sequence_title", "sequence_description", "sequence_interpretation"],
           "tags": ["title", "definition", "aspects", "discussion"],
           "translations": ["title", "text"],
           "literature": ["author", "title"]}
    for table, cols in fts.items():
        if not tables[table] and table not in empty:
            continue
        c = ", ".join(f"[{x}]" for x in cols)
        db.execute(f"CREATE VIRTUAL TABLE [{table}_fts] USING FTS5 ({c}, content=[{table}])")
        db.execute(f"INSERT INTO [{table}_fts] (rowid, {c}) SELECT rowid, {c} FROM [{table}]")
    db.commit()
    db.close()
    print(", ".join(f"{len(r)} {n}" for n, r in tables.items()), f"-> {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
