#!/usr/bin/env python3
"""Shows GEAR as a tree, without a browser.

  python scripts/tree.py                     game -> sequence -> event, all games
  python scripts/tree.py --game world_of_warcraft
  python scripts/tree.py --by tag            tag -> game -> sequence -> event, all tags
  python scripts/tree.py --by tag --tag torture
  python scripts/tree.py --md                also write build/tree_by_game.md and build/tree_by_tag.md

The Markdown files contain links to the files and can be read in Zettlr, VSCodium or on GitHub.
"""
import argparse
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from export import OUT, collect  # noqa: E402


def literature_index(tables):
    """{(target_type, target): [work]}, and {citekey: set of targets} for intersections."""
    works = {w["citekey"]: w for w in tables["literature"]}
    by_target, targets_of = defaultdict(list), defaultdict(set)
    for link in tables["literature_links"]:
        w = works.get(link["citekey"])
        if not w:
            continue
        key = (link["target_type"], link["target"])
        by_target[key].append((w, link["role"]))
        targets_of[link["citekey"]].add(key)
    return works, by_target, targets_of


def cite(work, role):
    who = (work.get("author") or work.get("editor") or "").split(" and ")[0].split(",")[0]
    return f"{who} {work.get('year', '')}: {work.get('title', '')} ({role})"


def build(tables, by):
    """Return a nested list of (label, path or None, children)."""
    games = {g["game"]: g for g in tables["games"]}
    tags = {t["tag"]: t for t in tables["tags"]}
    works, lit, targets_of = literature_index(tables)

    def lit_nodes(*keys, both=None):
        out = []
        for key in keys:
            for w, role in lit.get(key, []):
                out.append(("Literature: " + cite(w, role), None, []))
        if both:  # works connected to both a game and a tag
            a, b = both
            for ck, tg in targets_of.items():
                if a in tg and b in tg:
                    out.append(("Literature (both): " + cite(works[ck], "/".join(sorted({r for (w, r) in lit[a] if w['citekey'] == ck}))), None, []))
        return out

    def event_node(e):
        meta = ", ".join(x for x in (e["layer"], e["agency"]) + tuple(e["tags"]) if x)
        kids = lit_nodes(("event", e["id"]))
        return (f"{e['id']}  {e['title']}  · {meta}", e["path"], kids)

    sequences = {q["id"]: q for q in tables["sequences"]}

    def seq_nodes(evs, gname, tag=None):
        per = defaultdict(list)
        for e in evs:
            per[e["sequence"]].append(e)
        out = []
        for sid, es in sorted(per.items()):
            q = sequences[sid]
            kids = lit_nodes(("sequence", sid)) + [event_node(e) for e in sorted(es, key=lambda e: e["id"])]
            out.append((f"{q['title']}  ({q['unit']}, {len(es)})", q["path"], kids))
        return out

    tree = []
    if by == "game":
        for gname, g in sorted(games.items()):
            evs = [e for e in tables["events"] if e["game"] == gname]
            kids = lit_nodes(("game", gname)) + seq_nodes(evs, gname)
            tree.append((f"{g['title']}  ({len(evs)} events)", g["path"], kids))
    else:
        for t, tag in sorted(tags.items()):
            evs = [e for e in tables["events"] if t in e["tags"]]
            kids = lit_nodes(("tag", t))
            per_game = defaultdict(list)
            for e in evs:
                per_game[e["game"]].append(e)
            for gname, es in sorted(per_game.items()):
                gkids = lit_nodes(both=(("game", gname), ("tag", t))) + seq_nodes(es, gname, t)
                kids.append((f"{games[gname]['title']}  ({len(es)})", games[gname]["path"], gkids))
            tree.append((f"{tag['title']}  ({len(evs)} events)", tag["path"], kids))
    return tree


def as_text(tree, prefix=""):
    lines = []
    for i, (label, _, kids) in enumerate(tree):
        last = i == len(tree) - 1
        lines.append(prefix + ("└─ " if last else "├─ ") + label)
        lines += as_text(kids, prefix + ("   " if last else "│  "))
    return lines


def as_md(tree, depth=0):
    lines = []
    for label, path, kids in tree:
        text = f"[{label}](../{path})" if path else label
        lines.append("  " * depth + "- " + text)
        lines += as_md(kids, depth + 1)
    return lines


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--by", choices=["game", "tag"], default="game")
    ap.add_argument("--game", help="only this game folder")
    ap.add_argument("--tag", help="only this tag")
    ap.add_argument("--md", action="store_true", help="also write Markdown files to build/")
    args = ap.parse_args()

    tables = collect()
    tree = build(tables, args.by)
    if args.game:
        name = next((g["title"] for g in tables["games"] if g["game"] == args.game), None)
        tree = [n for n in tree if name and n[0].startswith(name)]
    if args.tag:
        name = next((t["title"] for t in tables["tags"] if t["tag"] == args.tag), None)
        tree = [n for n in tree if name and n[0].startswith(name)]
    print("\n".join(as_text(tree)))

    if args.md:
        OUT.mkdir(exist_ok=True)
        for by, heading in (("game", "GEAR by game"), ("tag", "GEAR by tag")):
            md = [f"# {heading}", ""] + as_md(build(tables, by))
            (OUT / f"tree_by_{by}.md").write_text("\n".join(md) + "\n", encoding="utf-8")
        print(f"\nwritten: build/tree_by_game.md, build/tree_by_tag.md")


if __name__ == "__main__":
    main()
