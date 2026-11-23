#!/usr/bin/env python3
"""Checks GEAR files against schema 0.8. Run from the repository root: python scripts/validate.py"""
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
NUMBERED = re.compile(r"^##\s+(\d+)\.\s+(.+?)\s*$", re.M)
SUBSECTIONS = {"description", "observation", "interpretation"}
LINK = re.compile(r"\]\(([^)\s]+)\)")
TRANSLATION_FIELDS = {"lang", "status", "title"}
CODED = ["status", "engagement", "unit"]
EVENT_CODED = ["layer", "agency", "act"]
EVENT_FIELDS = {"observed", "source", "timecode", "locator", "layer", "agency", "act", "consequence", "media", "coded_by"}


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
    if len(p) == 3:
        return "evidence", None if NAME.fullmatch(split_lang(rel)[0]) else "evidence file name must be a-z, 0-9, _"
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


def numbered(path):
    """[(n, title)] of the numbered sections, in file order."""
    body = path.read_text(encoding="utf-8").split("---", 2)[-1]
    body = re.sub(r"<!--.*?-->|```.*?```", "", body, flags=re.S)
    return [(int(n), title) for n, title in NUMBERED.findall(body)]


def check_evidence(path, rel, fm, err, ids, branches):
    secs = numbered(path)
    nums = [n for n, _ in secs]
    if not [n for n in nums if n > 0]:
        err(rel, "evidence needs at least one numbered event section (## 1. Title)")
    if len(set(nums)) != len(nums):
        err(rel, "section numbers must be unique")
    expected = ([0] if 0 in nums else []) + list(range(1, len([n for n in nums if n > 0]) + 1))
    if nums != expected:
        err(rel, f"sections must be numbered in order, 0 (optional) then 1, 2, 3 …, are {nums}")
    if 0 in nums and not fm.get("unit"):
        err(rel, "section 0 (sequence) needs unit")
    if "unit" in fm and 0 not in nums:
        err(rel, "unit only with section 0")
    first = fm.get("first_appeared")
    if first is not None:
        if not isinstance(first, dict) or set(first) - {"branch", "version", "note"} or not first.get("version"):
            err(rel, "first_appeared takes version (required), branch and note")
        elif branches and first.get("branch") not in branches:
            err(rel, f"first_appeared.branch {first.get('branch')!r} not in game.md")
        elif not branches and "branch" in first:
            err(rel, "first_appeared.branch only for games with branches in game.md")
    if "variant_of" in fm and not re.fullmatch(r"EVD-[A-Z0-9]+-\d{4}", str(fm["variant_of"])):
        err(rel, f"variant_of {fm['variant_of']!r} must be an evidence ID")
    obs0 = fm.get("observed") if isinstance(fm.get("observed"), dict) else {}
    meta = fm.get("events") or {}
    if not isinstance(meta, dict):
        err(rel, "events must map section numbers to their fields")
        meta = {}
    for n in meta:
        if n not in nums or n == 0:
            err(rel, f"events.{n} has no section ## {n}.")
    for n in [n for n in nums if n > 0]:
        em = meta.get(n)
        where = f"events.{n}"
        if not isinstance(em, dict):
            err(rel, f"{where} missing")
            continue
        for f in set(em) - EVENT_FIELDS:
            err(rel, f"{where}.{f} is no event field")
        obs = {**obs0, **(em.get("observed") or {})}
        for f in ("date", "version", "platform", "language", "by") + (("branch",) if branches else ()):
            if obs.get(f) in (None, ""):
                err(rel, f"observed.{f} missing for event {n}")
        if branches and obs.get("branch") and obs["branch"] not in branches:
            err(rel, f"event {n}: observed.branch {obs['branch']!r} not in game.md")
        if not branches and obs.get("branch"):
            err(rel, f"event {n}: observed.branch only for games with branches in game.md")
        if not em.get("layer"):
            err(rel, f"{where}.layer missing")
        for f in EVENT_CODED:
            if f in em and em[f] not in VOC[f]:
                err(rel, f"{where}.{f} {em[f]!r} not in vocabularies.yaml")
        if ("act" in em or "consequence" in em) and em.get("agency") not in ("optional", "forced"):
            err(rel, f"{where}: act and consequence only with agency optional or forced")
        cons = em.get("consequence")
        if cons is not None:
            if not isinstance(cons, dict) or set(cons) - {"if_done", "if_not_done"}:
                err(rel, f"{where}.consequence takes if_done and if_not_done")
            else:
                for k, v in cons.items():
                    if v not in VOC["consequence"]:
                        err(rel, f"{where}.consequence.{k} {v!r} not in vocabularies.yaml")
        if not (em.get("timecode") or em.get("locator")):
            err(rel, f"{where} needs timecode (played) or locator (read)")
        ids[f"{fm.get('id')}.{n}"] = rel
    for tag in fm.get("tags") or []:
        if tag not in TAGS:
            err(rel, f"tag {tag!r} has no file in tags/")


def main():
    errors, ids, codes, branches = [], {}, {}, {}
    err = lambda rel, msg: errors.append(f"{rel}: {msg}")
    n_entries = n_trans = 0

    for game_md in sorted((ROOT / "games").glob("*/game.md")):
        fm = frontmatter(game_md) or {}
        m = re.fullmatch(r"GAME-([A-Z0-9]+)", str(fm.get("id", "")))
        codes[game_md.parent.name] = m.group(1) if m else None
        branches[game_md.parent.name] = fm.get("branches") or {}

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
            elif t == "evidence":
                have = {n for n, _ in numbered(path.parent / f"{base}.md")}
                for n, _ in numbered(path):
                    if n not in have:
                        err(rel, f"section {n} is not in the original")
            continue

        n_entries += 1
        if fm.get("type") != t:
            err(rel, f"type must be {t!r} here, is {fm.get('type')!r}")
            continue
        required = ["schema_version", "status", "title"] + ([] if t == "tag" else ["id"])
        required += {"evidence": ["observed", "events"]}.get(t, [])
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
            pattern = {"game": "GAME-{c}", "evidence": r"EVD-{c}-\d{{4}}"}[t]
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
        if t == "game" and "branches" in fm and not (isinstance(fm["branches"], dict) and all(NAME.fullmatch(str(k)) for k in fm["branches"])):
            err(rel, "branches maps keys (a-z, 0-9, _) to a short description")
        if t == "game" and fm.get("wikidata") not in (None, "", "TODO"):
            if not re.fullmatch(r"Q\d+", str(fm["wikidata"])):
                err(rel, f"wikidata {fm['wikidata']!r} must be a Q-ID such as Q12345")
        if t == "evidence":
            check_evidence(path, rel, fm, err, ids, branches.get(rel.parts[1], {}))

    for path in files:
        fm = frontmatter(path) or {}
        if fm.get("type") == "evidence" and fm.get("variant_of") and fm["variant_of"] not in ids:
            errors.append(f"{path.relative_to(ROOT)}: variant_of {fm['variant_of']} not found")

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
                errors.append(f"{bibrel}: {key}: {kw!r} must be gear:<target>:<role>; GEAR collects only literature on a game, evidence entry, event or tag")
                continue
            if role not in VOC["literature_role"]:
                errors.append(f"{bibrel}: {key}: role {role!r} in {kw!r} not in vocabularies.yaml")
            if target is not None:
                kinds = [k for k, ok in (("tag", target in TAGS), ("game", target in GAMES),
                                         ("evidence", target.startswith("EVD-") and "." not in target and target in ids),
                                         ("event", target.startswith("EVD-") and "." in target and target in ids)) if ok]
                if not kinds:
                    errors.append(f"{bibrel}: {key}: {target!r} in {kw!r} is no tag, game folder, evidence ID or event ID (EVD-….n)")
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
