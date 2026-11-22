#!/usr/bin/env python3
"""Checks GEAR files against schema 0.7. Run from the repository root: python scripts/validate.py"""
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
VOC = yaml.safe_load((ROOT / "vocabularies.yaml").read_text(encoding="utf-8"))
LANGS = set(VOC["lang"])
TAGS = {p.stem for p in (ROOT / "tags").glob("*.md") if "." not in p.stem}
GAMES = {p.name for p in (ROOT / "games").iterdir() if p.is_dir()}
BIB = ROOT / "literature" / "game_evidence_archive_and_repository.bib"


def read_bib(path):
    """Return {citekey: [keywords]} from a BibTeX/BibLaTeX file."""
    entries = {}
    if not path.exists():
        return entries
    text = path.read_text(encoding="utf-8")
    for m in re.finditer(r"^@\w+\s*\{\s*([^,\s]+)\s*,(.*?)(?=^@|\Z)", text, flags=re.S | re.M):
        kw = re.search(r"\bkeywords\s*=\s*[{\"](.*?)[}\"]\s*,?\s*$", m.group(2), flags=re.S | re.M)
        entries[m.group(1)] = [k.strip() for k in re.split(r"[,;]", kw.group(1))] if kw else []
    return entries


BIBLIO = read_bib(BIB)
CITEKEYS = set(BIBLIO)
CITATION = re.compile(r"\[([^\]]*@[^\]]*)\]")

NAME = re.compile(r"[a-z0-9_]+")
EVENT_FILE = re.compile(r"(\d{4})_[a-z0-9_]+")
LINK = re.compile(r"\]\(([^)\s]+)\)")
TRANSLATION_FIELDS = {"lang", "status", "title"}
CODED = ["status", "layer", "agency", "engagement", "unit"]


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    try:
        return yaml.safe_load(text.split("---", 2)[1]) or {}
    except yaml.YAMLError as e:
        return {"_error": str(e)}


def split_lang(path):
    """'01_x.de.md' -> ('01_x', 'de'); '01_x.md' -> ('01_x', None)."""
    stem = path.name[:-3]
    return tuple(stem.rsplit(".", 1)) if "." in stem else (stem, None)


def place(rel):
    """Type a file must have, and the naming rule it breaks (or None), from its path."""
    p = rel.parts
    if p[0] == "tags" and len(p) == 2:
        return "tag", None if NAME.fullmatch(split_lang(rel)[0]) else "tag file name must be a-z, 0-9, _"
    if p[0] != "games":
        return None, "file is not in a known place"
    if not NAME.fullmatch(p[1]):
        return None, "game folder name must be a-z, 0-9, _"
    if len(p) == 3 and p[2] == "game.md":
        return "game", None
    if len(p) == 4:
        if not NAME.fullmatch(p[2]):
            return None, "sequence folder name must be a-z, 0-9, _"
        if p[3] == "sequence.md" or split_lang(rel)[0] == "sequence":
            return "sequence", None
        if not EVENT_FILE.fullmatch(split_lang(rel)[0]):
            return "event", "event file name must be <nnnn>_<name>.md"
        return "event", None
    return None, "file is not in a known place"


def check_links(path, rel, err):
    """Every relative Markdown link must point to an existing file."""
    text = re.sub(r"<!--.*?-->|```.*?```", "", path.read_text(encoding="utf-8"), flags=re.S)
    for target in LINK.findall(text):
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            continue
        t = target.split("#", 1)[0]
        if t and not (path.parent / t).resolve().exists():
            err(rel, f"broken link {target}")
    for group in CITATION.findall(text):
        for key in re.findall(r"@([\w:-]+)", group):
            if key not in CITEKEYS:
                err(rel, f"citekey @{key} not in literature/game_evidence_archive_and_repository.bib")


def main():
    errors, ids, codes = [], {}, {}
    err = lambda rel, msg: errors.append(f"{rel}: {msg}")
    n_entries = n_trans = 0

    for game_md in sorted((ROOT / "games").glob("*/game.md")):
        fm = frontmatter(game_md) or {}
        m = re.fullmatch(r"GAME-([A-Z0-9]+)", str(fm.get("id", "")))
        codes[game_md.parent.name] = m.group(1) if m else None

    files = sorted((ROOT / "games").rglob("*.md")) + sorted((ROOT / "tags").glob("*.md"))
    files += sorted((ROOT / "literature").glob("*.md")) if (ROOT / "literature").exists() else []  # not allowed, reported
    for path in files:
        rel = path.relative_to(ROOT)
        check_links(path, rel, err)
        t, problem = place(rel)
        if problem:
            err(rel, problem)
        if t is None:
            continue
        fm = frontmatter(path)
        if fm is None or "_error" in fm:
            err(rel, "no valid frontmatter")
            continue
        base, lang = split_lang(path)

        if lang is not None:  # translation
            n_trans += 1
            if lang not in LANGS or fm.get("lang") != lang:
                err(rel, "language suffix and lang must match a language in vocabularies.yaml")
            if set(fm) - TRANSLATION_FIELDS:
                err(rel, f"translations carry no further metadata: {sorted(set(fm) - TRANSLATION_FIELDS)}")
            if fm.get("status") not in VOC["status"]:
                err(rel, f"status {fm.get('status')!r} not in vocabularies.yaml")
            if not (path.parent / f"{base}.md").exists():
                err(rel, f"original {base}.md missing")
            continue

        n_entries += 1
        if fm.get("type") != t:
            err(rel, f"type must be {t!r} here, is {fm.get('type')!r}")
            continue
        required = ["schema_version", "status", "title"] + ([] if t == "tag" else ["id"])
        required += {"event": ["layer", "observed"], "sequence": ["unit"]}.get(t, [])
        for f in required:
            if fm.get(f) in (None, ""):
                err(rel, f"required field {f} missing")
        if str(fm.get("title", "")).startswith("Template:"):
            err(rel, "title still says Template, replace it")
        if not isinstance(fm.get("schema_version"), str):
            err(rel, "schema_version must be a string")
        if "lang" in fm and fm["lang"] not in LANGS:
            err(rel, f"lang {fm['lang']!r} not in vocabularies.yaml")
        for field in CODED:
            if field in fm and fm[field] not in VOC[field]:
                err(rel, f"{field} {fm[field]!r} not in vocabularies.yaml")

        if t != "tag":
            code = codes.get(rel.parts[1])
            pattern = {"game": "GAME-{c}", "sequence": r"SEQ-{c}-\d{{3}}", "event": r"EVT-{c}-\d{{4}}"}[t]
            fid = str(fm.get("id", ""))
            if code and not re.fullmatch(pattern.format(c=code), fid):
                err(rel, f"id {fid!r} does not match {pattern.format(c=code)}")
            if fid in ids:
                err(rel, f"id {fid} also used in {ids[fid]}")
            ids[fid] = rel

        if t == "tag":
            for tag in fm.get("related") or []:
                if tag not in TAGS or tag == base:
                    err(rel, f"related tag {tag!r} has no file in tags/")
            for m in fm.get("mappings") or []:
                if not isinstance(m, dict) or not m.get("concept"):
                    err(rel, "each mapping needs scheme, concept and match")
                    continue
                if m.get("scheme") not in VOC["mapping_scheme"]:
                    err(rel, f"mapping scheme {m.get('scheme')!r} not in vocabularies.yaml")
                if m.get("match") not in VOC["mapping_match"]:
                    err(rel, f"mapping match {m.get('match')!r} not in vocabularies.yaml")
        if t == "game" and fm.get("wikidata") not in (None, "", "TODO"):
            if not re.fullmatch(r"Q\d+", str(fm["wikidata"])):
                err(rel, f"wikidata {fm['wikidata']!r} must be a Q-ID such as Q12345")
        if t == "event" and not (path.parent / "sequence.md").exists():
            err(rel, "event folder has no sequence.md")
        if t == "event":
            obs = fm.get("observed") if isinstance(fm.get("observed"), dict) else {}
            for f in ("date", "version", "platform", "language", "by"):
                if obs.get(f) in (None, ""):
                    err(rel, f"observed.{f} missing")
            num = EVENT_FILE.fullmatch(base)
            if num and not fid.endswith("-" + num.group(1)):
                err(rel, f"file number {num.group(1)} does not match id {fid}")
            has_act = "act" in fm or "consequence" in fm
            if has_act and fm.get("agency") not in ("optional", "forced"):
                err(rel, "act and consequence only with agency optional or forced")
            if "act" in fm and fm["act"] not in VOC["act"]:
                err(rel, f"act {fm['act']!r} not in vocabularies.yaml")
            cons = fm.get("consequence")
            if cons is not None:
                if not isinstance(cons, dict) or set(cons) - {"if_done", "if_not_done"}:
                    err(rel, "consequence takes if_done and if_not_done")
                else:
                    for k, v in cons.items():
                        if v not in VOC["consequence"]:
                            err(rel, f"consequence.{k} {v!r} not in vocabularies.yaml")
            if not (fm.get("timecode") or fm.get("locator")):
                err(rel, "event needs timecode (played) or locator (read)")
            for tag in fm.get("tags") or []:
                if tag not in TAGS:
                    err(rel, f"tag {tag!r} has no file in tags/")
            for w in fm.get("content_warnings") or []:
                if w not in VOC["content_warnings"]:
                    err(rel, f"content_warning {w!r} not in vocabularies.yaml")

    bibrel = BIB.relative_to(ROOT) if BIB.exists() else "literature/game_evidence_archive_and_repository.bib"
    n_links = 0
    for key, keywords in BIBLIO.items():
        for kw in keywords:
            if not kw.startswith("gear:"):
                continue  # other Zotero tags are ignored
            n_links += 1
            parts = kw.split(":")[1:]
            if len(parts) == 2:
                target, role = parts
            else:
                errors.append(f"{bibrel}: {key}: {kw!r} must be gear:<target>:<role>; GEAR collects only literature on a game, sequence, event or tag")
                continue
            if role not in VOC["literature_role"]:
                errors.append(f"{bibrel}: {key}: role {role!r} in {kw!r} not in vocabularies.yaml")
            if target is not None:
                kinds = [k for k, ok in (("tag", target in TAGS), ("game", target in GAMES),
                                         ("sequence", target.startswith("SEQ-") and target in ids),
                                         ("event", target.startswith("EVT-") and target in ids)) if ok]
                if not kinds:
                    errors.append(f"{bibrel}: {key}: {target!r} in {kw!r} is no tag, game folder, sequence ID or event ID")
                elif len(kinds) > 1:
                    errors.append(f"{bibrel}: {key}: {target!r} is ambiguous ({', '.join(kinds)})")

    for code_dir, code in codes.items():
        if code is None:
            errors.append(f"games/{code_dir}/game.md: missing or invalid id")

    for e in errors:
        print(e)
    print(f"{n_entries} entries, {n_trans} translations and {n_links} literature links checked, {len(errors)} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
