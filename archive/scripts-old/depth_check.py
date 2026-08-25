"""Enforce the Part 11 depth contract.

A day passes when every part carries the ten sections, in order, with the required
substance in the sections where quality usually dies (2, 6, 7, 8, 9, 10), and when the
parts between them cover exactly the concept IDs the index assigns to the day.

Usage:
    python scripts/depth_check.py 37
    python scripts/depth_check.py --all
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAYS = ROOT / "days"
INDEX = ROOT / "docs" / "CURRICULUM_INDEX.md"

SECTIONS = [
    "The one-line answer",
    "The story",
    "The idea in plain language",
    "Where this actually shows up",
    "The mechanism",
    "Line by line",
    "The cost, derived",
    "When it breaks",
    "In production",
    "Check yourself",
]

DERIVATIONS = ("summation", "recurrence", "accounting", "potential", "expectation")
STORY_MIN, STORY_MAX = 180, 700
ID_RE = re.compile(r"\b([A-Z]{3})-(\d{2})\b")
TIME_ESTIMATE_RE = re.compile(
    r"\b\d+\s*(?:-\s*\d+\s*)?(?:min(?:ute)?s?|hours?|hrs?)\b", re.IGNORECASE
)

# Folders carry their subject in their name, so `ls days/` is a table of contents:
#   days/day-01-what-computation-costs/parts/02-model-of-computation/2.1-the-ram-model.md
SLUG = r"[a-z0-9]+(?:-[a-z0-9]+)*"
DAY_DIR_RE = re.compile(rf"^day-(\d{{2}})-{SLUG}$")
SECTION_DIR_RE = re.compile(rf"^(\d{{2}})-{SLUG}$")
PART_FILE_RE = re.compile(rf"^(\d+)\.(\d+)-{SLUG}\.md$")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def day_dir(n: int) -> Path | None:
    """The folder for day n, found by its number. None when the day is not on disk yet."""
    hits = sorted(d for d in DAYS.glob(f"day-{n:02d}-*") if d.is_dir())
    if len(hits) > 1:
        names = ", ".join(d.name for d in hits)
        raise SystemExit(f"day {n} has {len(hits)} folders ({names}) — one day, one folder")
    return hits[0] if hits else None


def index_ids(n: int) -> set[str]:
    """Concept IDs the index assigns to day n."""
    if not INDEX.exists():
        return set()
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3 or not cells[0].isdigit() or int(cells[0]) != n:
            continue
        return {m.group(0) for m in ID_RE.finditer(cells[2])}
    return set()


def parse_front_matter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    out: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            out[k.strip()] = v.strip()
    return out


def split_sections(text: str) -> list[tuple[str, str]]:
    parts = re.split(r"^##\s+\d+\.\s*", text, flags=re.MULTILINE)[1:]
    out = []
    for chunk in parts:
        head, _, body = chunk.partition("\n")
        out.append((head.strip(), body))
    return out


def check_naming(d: Path, rep: Report) -> None:
    """Folder and file names must say what they hold. `ls days/` is the table of contents."""
    where = str(d.relative_to(ROOT))
    if not DAY_DIR_RE.match(d.name):
        rep.err(where, "day folder must be day-NN-<kebab-slug>, e.g. day-01-what-computation-costs")

    parts = d / "parts"
    if not parts.is_dir():
        return

    for stray in sorted(parts.glob("*.md")):
        rep.err(str(stray.relative_to(ROOT)), "parts/ holds section folders, not loose documents")

    for sec in sorted(p for p in parts.iterdir() if p.is_dir()):
        sec_where = str(sec.relative_to(ROOT))
        m = SECTION_DIR_RE.match(sec.name)
        if not m:
            rep.err(
                sec_where,
                "section folder must be NN-<kebab-slug>, e.g. 02-model-of-computation",
            )
            continue
        for f in sorted(sec.glob("*.md")):
            fm = PART_FILE_RE.match(f.name)
            if not fm:
                rep.err(
                    str(f.relative_to(ROOT)),
                    "part file must be named <section>.<subtopic>-<kebab-slug>.md",
                )
            elif int(fm.group(1)) != int(m.group(1)):
                rep.err(
                    str(f.relative_to(ROOT)),
                    f"part {fm.group(1)}.{fm.group(2)} sits in section folder {sec.name}",
                )


def check_part(path: Path, allowed: set[str], rep: Report) -> str | None:
    text = path.read_text(encoding="utf-8")
    where = str(path.relative_to(ROOT))

    fm = parse_front_matter(text)
    for key in ("id", "day", "section", "subtopic", "title"):
        if key not in fm:
            rep.err(where, f"front matter missing '{key}'")
    folder = SECTION_DIR_RE.match(path.parent.name)
    if folder and fm.get("section", "").isdigit() and int(fm["section"]) != int(folder.group(1)):
        rep.err(where, f"front matter says section {fm['section']}, folder says {path.parent.name}")
    concept = fm.get("id")
    if concept and allowed and concept not in allowed:
        rep.err(where, f"id {concept} is not assigned to this day by the index ({sorted(allowed)})")

    found = split_sections(text)
    titles = [t for t, _ in found]
    if titles != SECTIONS:
        for i, want in enumerate(SECTIONS):
            got = titles[i] if i < len(titles) else "<missing>"
            if got != want:
                rep.err(where, f"section {i + 1} must be '{want}', found '{got}'")
                break
        return concept

    body = dict(found)

    words = len(body["The story"].split())
    if not STORY_MIN <= words <= STORY_MAX:
        rep.err(where, f"§2 story is {words} words; contract wants {STORY_MIN}-{STORY_MAX}")
    if "```" in body["The story"]:
        rep.err(where, "§2 story contains code; the story has no code in it")

    if "```" not in body["Line by line"]:
        rep.err(where, "§6 has no code fragment")
    if "near-miss" not in body["Line by line"].lower():
        rep.err(where, "§6 has no near-miss")

    cost = body["The cost, derived"].lower()
    if not any(d in cost for d in DERIVATIONS):
        rep.err(where, f"§7 names no derivation technique (one of {DERIVATIONS})")

    if "```" not in body["When it breaks"]:
        rep.err(where, "§8 has no pasted error text or wrong output")

    prod = body["In production"]
    if not re.search(r"^>\s", prod, flags=re.MULTILINE):
        rep.err(where, "§9 has no reviewer quote (blockquote)")
    if len(re.findall(r"^\d\.\s", prod, flags=re.MULTILINE)) < 3:
        rep.err(where, "§9 has fewer than three interviewer follow-ups")

    check = body["Check yourself"]
    if "<details>" not in check:
        rep.err(where, "§10 has no <details> answers")
    if not any(m.group(0) != concept for m in ID_RE.finditer(check)):
        rep.warn(where, "§10 cites no earlier concept ID (retention, plan Part 12)")
    if "break it" not in check.lower():
        rep.warn(where, "§10 has no 'break it' question")

    if TIME_ESTIMATE_RE.search(text):
        hit = TIME_ESTIMATE_RE.search(text)
        rep.err(where, f"time estimate found ({hit.group(0)!r}); a day is a unit of subject")

    return concept


def check_day(n: int, rep: Report) -> None:
    d = day_dir(n)
    if d is None:
        rep.err(f"days/day-{n:02d}-*", f"no day folder; expected days/day-{n:02d}-<slug>/")
        return
    where = str(d.relative_to(ROOT))
    check_naming(d, rep)
    if not (d / "LESSON.md").exists():
        rep.err(where, "no LESSON.md hub")
    if not (d / "CHECKLIST.md").exists():
        rep.err(where, "no CHECKLIST.md")

    parts = sorted((d / "parts").rglob("*.md")) if (d / "parts").exists() else []
    assigned = index_ids(n)

    if not parts:
        # Day 0 and gate days are the two documented exemptions.
        if n != 0 and assigned:
            rep.err(where, f"no parts/, but the index assigns IDs {sorted(assigned)}")
        return

    covered = {c for p in parts if (c := check_part(p, assigned, rep))}
    missing = assigned - covered
    if missing:
        rep.err(where, f"index IDs not covered by any part: {sorted(missing)}")


def written_days() -> list[int]:
    """Day numbers on disk, read off the folder names: day-NN-<slug>."""
    out = []
    for d in sorted(DAYS.glob("day-*")):
        m = DAY_DIR_RE.match(d.name)
        if m and (d / "LESSON.md").exists():
            out.append(int(m.group(1)))
    return sorted(out)


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2
    targets = written_days() if args[0] == "--all" else [int(args[0])]

    rep = Report()
    for n in targets:
        check_day(n, rep)

    for w in rep.warnings:
        print(f"warn  {w}")
    for e in rep.errors:
        print(f"FAIL  {e}")

    if rep.errors:
        print(f"\n{len(rep.errors)} depth-contract violation(s) across {len(targets)} day(s).")
        return 1
    print(f"depth contract satisfied for {len(targets)} day(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
