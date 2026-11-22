#!/usr/bin/env python3
"""Rebuild the aggregated data files from data/days/*.json.

Run from the repo root:  python3 scripts/build.py

Each day file is the single source of truth. This script regenerates:
  data/index.json     list of days (newest first) with headline info
  data/entities.json  merged companies / people / organisations
  data/glossary.json  merged glossary terms
  data/mindmap.json   industry -> concept -> entity tree with audience tags

It also checks every day file against the schema and fails loudly if a
required field is missing or an em-dash slipped in.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAYS = ROOT / "data" / "days"
RESEARCH = ROOT / "data" / "research"
OUT = ROOT / "data"

AUDIENCES = {"lay", "builder", "decision"}
ACTIONS = {"Watch", "Try", "Pitch"}
RESEARCH_REQUIRED = ["date", "covers", "one_line", "papers"]
PAPER_REQUIRED = ["title", "venue", "kind", "summary", "why", "audience", "link"]
REQUIRED = ["date", "sources", "one_line", "top_stories", "saudi_lens",
            "idea", "watchlist", "verify", "entities", "terms", "concepts"]


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def check(day, path):
    errors = []
    for key in REQUIRED:
        if key not in day:
            errors.append(f"missing '{key}'")
    raw = path.read_text(encoding="utf-8")
    if "—" in raw:
        errors.append("contains an em-dash (U+2014); use a colon, comma or full stop")
    q = day.get("question")
    if q is not None and not str(q).strip().endswith("?"):
        errors.append("question must end with a question mark")
    for s in day.get("top_stories", []):
        if s.get("action") not in ACTIONS:
            errors.append(f"story '{s.get('title')}' has action {s.get('action')!r}")
        bad = set(s.get("audience", [])) - AUDIENCES
        if bad:
            errors.append(f"story '{s.get('title')}' has unknown audience {bad}")
    for c in day.get("concepts", []):
        bad = set(c.get("audience", [])) - AUDIENCES
        if bad:
            errors.append(f"concept '{c.get('concept')}' has unknown audience {bad}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", day.get("date", "")):
        errors.append("date must be YYYY-MM-DD")
    elif path.stem != day["date"]:
        errors.append(f"file name {path.name} does not match date {day['date']}")
    return errors


def check_covers(day, errors):
    c = day.get("covers")
    if c is None:
        return
    if not isinstance(c, dict) or not all(re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(c.get(k, ""))) for k in ("from", "to")):
        errors.append("covers must be {\"from\": \"YYYY-MM-DD\", \"to\": \"YYYY-MM-DD\"}")
    elif c["from"] > c["to"]:
        errors.append("covers.from is after covers.to")


def check_research(r, path):
    errors = [f"missing '{k}'" for k in RESEARCH_REQUIRED if k not in r]
    if "\u2014" in path.read_text(encoding="utf-8"):
        errors.append("contains an em-dash (U+2014)")
    if path.stem != r.get("date"):
        errors.append(f"file name {path.name} does not match date {r.get('date')}")
    check_covers(r, errors)
    for p in r.get("papers", []):
        for k in PAPER_REQUIRED:
            if not p.get(k) and k != "link":
                errors.append(f"paper '{p.get('title', '?')}' missing '{k}'")
        bad = set(p.get("audience", [])) - AUDIENCES
        if bad:
            errors.append(f"paper '{p.get('title')}' has unknown audience {bad}")
    return errors


def main():
    days, problems = [], {}
    for path in sorted(DAYS.glob("*.json")):
        try:
            day = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems[path.name] = [f"invalid JSON: {exc}"]
            continue
        errs = check(day, path)
        check_covers(day, errs)
        if errs:
            problems[path.name] = errs
        days.append(day)

    research = []
    for path in sorted(RESEARCH.glob("*.json")) if RESEARCH.exists() else []:
        try:
            r = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            problems["research/" + path.name] = [f"invalid JSON: {exc}"]
            continue
        errs = check_research(r, path)
        if errs:
            problems["research/" + path.name] = errs
        research.append(r)

    if problems:
        for name, errs in problems.items():
            for e in errs:
                print(f"ERROR {name}: {e}", file=sys.stderr)
        sys.exit(1)

    days.sort(key=lambda d: d["date"], reverse=True)

    missing = [d["date"] for d in days if not d.get("question") or not d.get("reflection")]
    if missing:
        print(f"NOTE: {len(missing)} day(s) have no question/reflection yet: {', '.join(sorted(missing))}")

    index = [{
        "date": d["date"],
        "question": d.get("question", ""),
        "one_line": d["one_line"],
        "titles": [s["title"] for s in d["top_stories"]],
        "newsletters": sorted({s["newsletter"] for s in d["sources"]}),
    } for d in days]

    entities, glossary = {}, {}
    tree = {}
    for d in sorted(days, key=lambda x: x["date"]):
        for e in d["entities"]:
            key = slug(e["name"])
            cur = entities.setdefault(key, {
                "id": key, "name": e["name"], "type": e.get("type", "company"),
                "sector": e.get("sector", ""), "url": e.get("url", ""),
                "note": e.get("note", ""), "days": [],
            })
            # later mentions refresh the description, keep the first URL found
            cur["note"] = e.get("note") or cur["note"]
            cur["sector"] = e.get("sector") or cur["sector"]
            cur["url"] = cur["url"] or e.get("url", "")
            if d["date"] not in cur["days"]:
                cur["days"].append(d["date"])
        for t in d["terms"]:
            key = slug(t["term"])
            cur = glossary.setdefault(key, {
                "id": key, "term": t["term"], "definition": t["definition"],
                "audience": t.get("audience", "lay"), "days": [],
            })
            if d["date"] not in cur["days"]:
                cur["days"].append(d["date"])
        for c in d["concepts"]:
            ind = tree.setdefault(c["industry"], {})
            con = ind.setdefault(c["concept"], {
                "audience": set(), "entities": set(), "days": set(),
                "summary": c.get("summary", ""),
            })
            con["audience"].update(c.get("audience", []))
            con["entities"].update(c.get("entities", []))
            con["days"].add(d["date"])
            con["summary"] = c.get("summary") or con["summary"]

    mindmap = {"name": "AI landscape", "children": []}
    for ind in sorted(tree):
        node = {"name": ind, "kind": "industry", "children": []}
        for con in sorted(tree[ind]):
            info = tree[ind][con]
            node["children"].append({
                "name": con, "kind": "concept",
                "summary": info["summary"],
                "audience": sorted(info["audience"]),
                "days": sorted(info["days"], reverse=True),
                "children": [{"name": n, "kind": "entity"} for n in sorted(info["entities"])],
            })
        mindmap["children"].append(node)

    def dump(name, obj):
        (OUT / name).write_text(json.dumps(obj, ensure_ascii=False, indent=1), encoding="utf-8")

    research.sort(key=lambda r: r["date"], reverse=True)
    dump("research_index.json", [{
        "date": r["date"], "covers": r["covers"], "one_line": r["one_line"],
        "titles": [p["title"] for p in r["papers"]],
    } for r in research])

    dump("index.json", index)
    dump("entities.json", sorted(entities.values(), key=lambda e: e["name"].lower()))
    dump("glossary.json", sorted(glossary.values(), key=lambda g: g["term"].lower()))
    dump("mindmap.json", mindmap)
    print(f"OK: {len(days)} briefings, {len(research)} research radars, {len(entities)} entities, {len(glossary)} terms, "
          f"{sum(len(v) for v in tree.values())} concepts")


if __name__ == "__main__":
    main()
