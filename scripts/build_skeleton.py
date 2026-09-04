"""Create every day folder and every empty lesson file from scripts/curriculum.py.

Safe to re-run: a file that already has content (status is not "empty") is never
touched. Only placeholders are regenerated.

    python scripts/build_skeleton.py
    python scripts/build_skeleton.py --force   # rewrite placeholders too
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from curriculum import DSA_PHASES, SD_PHASES, Day, Lesson, load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"
DOCS_DIR = ROOT / "docs"

# The nine sections every lesson carries. DSA and system design share the frame
# so you only ever learn one reading rhythm; sections 5, 6 and 7 differ.
DSA_SECTIONS = [
    (
        "What this is, and why they ask it",
        "The idea in three sentences, and the reason it appears in interviews.",
    ),
    ("The story", "A scene from ordinary life where this idea already exists. No code, no jargon."),
    (
        "The idea in plain English",
        "The story translated into the technical idea, one step at a time.",
    ),
    (
        "The picture",
        "The diagram. Arrays with indices above and values below; trees and graphs in Mermaid.",
    ),
    (
        "The code, built step by step",
        "Small pieces, each explained, then the complete working solution.",
    ),
    ("What it costs", "Time and space, counted by hand from the loops. No hand-waving."),
    (
        "The traps",
        "The wrong versions that look right, the input that kills each, and the real error text.",
    ),
    (
        "In the interview",
        "How it is asked, what to say out loud, the follow-ups, and a model answer.",
    ),
    ("Recall card", "Five lines. If you remember nothing else from today, remember these."),
]

SD_SECTIONS = [
    (
        "What this is, and why they ask it",
        "The idea in three sentences, and the reason it appears in interviews.",
    ),
    ("The story", "A scene from ordinary life where this idea already exists. No code, no jargon."),
    (
        "The idea in plain English",
        "The story translated into the technical idea, one step at a time.",
    ),
    (
        "The picture",
        "The architecture diagram, in Mermaid. Every box labelled, every arrow directed.",
    ),
    ("How it actually works", "The mechanics, and the real products that do it this way."),
    (
        "The numbers",
        "The arithmetic: users, QPS, bytes per record, storage per year. Show the multiplication.",
    ),
    (
        "The trade-offs",
        "What you give up by choosing this, and when you would choose something else.",
    ),
    (
        "In the interview",
        "How it is asked, what to say out loud, the follow-ups, and a model answer.",
    ),
    ("Recall card", "Five lines. If you remember nothing else from today, remember these."),
]


# The C++ lesson carries the same nine headings as a DSA lesson, because it is a
# coding lesson — only the notes under them change.
CPP_SECTIONS = [
    (
        "What this is, and why they ask it",
        "The idea in three sentences, and the reason it appears in interviews.",
    ),
    ("The story", "A scene from ordinary life where this idea already exists. No code, no jargon."),
    (
        "The idea in plain English",
        "The story translated into the C++ idea, one step at a time. Every term defined.",
    ),
    (
        "The picture",
        "The diagram. Memory laid out in ASCII boxes; what a copy does and what a reference does.",
    ),
    (
        "The code, built step by step",
        "Fragments of ten lines or fewer, each explained, then the complete compilable program.",
    ),
    (
        "What it costs",
        "Time, space, and the arithmetic: bytes per element, operations per second, the copy.",
    ),
    (
        "The traps",
        "The near-miss that compiles and misbehaves, and the compiler's real error text, pasted.",
    ),
    (
        "In the interview",
        "How it is asked, what to say out loud, the follow-ups, and a model answer.",
    ),
    ("Recall card", "Five lines. If you remember nothing else from today, remember these."),
]

SECTIONS_FOR = {"dsa": DSA_SECTIONS, "system-design": SD_SECTIONS, "cpp": CPP_SECTIONS}
LABEL_FOR = {"dsa": "DSA", "system-design": "System Design", "cpp": "C++"}


def slugify(text: str) -> str:
    text = text.lower().replace("'", "")
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


TRAILING_STOP = {
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "in",
    "to",
    "for",
    "is",
    "it",
    "at",
    "on",
    "its",
    "with",
}


def short_slug(title: str, words: int = 5) -> str:
    """The first few words of the title, minus any dangling connector.

    Splits on whitespace, not on hyphens, so "off-by-one" stays one word.
    """
    head = " ".join(title.split()[:words])
    parts = [w for w in slugify(head).split("-") if w]
    while parts and parts[-1] in TRAILING_STOP:
        parts.pop()
    return "-".join(parts) or slugify(title)[:30]


def is_placeholder(path: Path) -> bool:
    if not path.exists():
        return True
    return "status: empty" in path.read_text(encoding="utf-8")[:400]


def write(path: Path, body: str, force: bool) -> bool:
    """Write body unless the file already holds real content. Returns True if written."""
    if path.exists() and not is_placeholder(path):
        return False
    if path.exists() and not force and is_placeholder(path):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8", newline="\n")
    return True


def lesson_file(day: Day, lesson: Lesson) -> str:
    label = LABEL_FOR[lesson.track]
    sections = SECTIONS_FOR[lesson.track]
    lines = [
        "---",
        f"day: {day.n}",
        f"track: {lesson.track}",
        f'title: "{lesson.title}"',
        f'phase: "{lesson.phase}"',
        "status: empty",
        "---",
        "",
        f"# Day {day.n:03d} · {label} — {lesson.title}",
        "",
        f"**After today you can:** {lesson.line}",
        "",
        f"**The interviewer asks it as:** *{lesson.ask}*",
        "",
        "---",
        "",
        "> Not written yet. The nine headings below are the shape every Krama lesson takes;",
        "> the italic line under each says what belongs there.",
        "> See [how a day works](../../docs/00_HOW_A_DAY_WORKS.md).",
        "",
    ]
    for i, (heading, note) in enumerate(sections, start=1):
        lines += [f"## {i}. {heading}", "", f"*{note}*", ""]
    return "\n".join(lines)


def practice_file(day: Day) -> str:
    return "\n".join(
        [
            "---",
            f"day: {day.n}",
            "track: practice",
            f'title: "Practice — {day.dsa.title}"',
            "status: empty",
            "---",
            "",
            f"# Day {day.n:03d} · Practice",
            "",
            f"**DSA topic:** {day.dsa.title}  ",
            f"**System design topic:** {day.sd.title}",
            "",
            "---",
            "",
            "## Code these, in this order",
            "",
            "*Named problems only, easiest first. Each one carries a single line saying what it is",
            "really testing. Solutions live in the lesson file, not here.*",
            "",
            "| # | Problem | Source | What it is really testing |",
            "|---|---|---|---|",
            "| 1 | | | |",
            "| 2 | | | |",
            "| 3 | | | |",
            "| 4 | | | |",
            "",
            "## Say these out loud",
            "",
            "*Three questions from today. Answer each in two minutes, standing up, no notes.*",
            "",
            f"1. {day.dsa.ask}",
            f"2. {day.sd.ask}",
            "3. ",
            "",
            "## Before you move on",
            "",
            "- [ ] I can write today's DSA code from memory, no reference.",
            "- [ ] I can draw today's system design diagram in whatever tool I like.",
            "- [ ] I answered all three questions above out loud.",
            "",
        ]
    )


def cpp_name(day: Day) -> str:
    """The C++ lesson's filename. Three words is enough after the 04-cpp- prefix."""
    return f"04-cpp-{short_slug(day.cpp.title, 3)}.md"


def hub_file(day: Day, prev: Day | None, nxt: Day | None) -> str:
    dsa_name = f"01-dsa-{short_slug(day.dsa.title)}.md"
    sd_name = f"02-system-design-{short_slug(day.sd.title)}.md"
    nav = []
    if prev:
        nav.append(f"[← Day {prev.n:03d}](../{prev.folder}/README.md)")
    nav.append("[All days](../README.md)")
    if nxt:
        nav.append(f"[Day {nxt.n:03d} →](../{nxt.folder}/README.md)")

    tracks = [
        "| Track | Today |",
        "|---|---|",
        f"| **DSA** | {day.dsa.title} |",
        f"| **System design** | {day.sd.title} |",
    ]
    tonight = [
        f"- **DSA** — {day.dsa.line}",
        f"- **System design** — {day.sd.line}",
    ]
    questions = [f"- *{day.dsa.ask}*", f"- *{day.sd.ask}*"]
    order = [
        f"1. [{dsa_name}]({dsa_name}) — the DSA lesson",
        f"2. [{sd_name}]({sd_name}) — the system design lesson",
    ]
    sits = [
        f"- DSA phase: **{day.dsa.phase}**",
        f"- System design phase: **{day.sd.phase}**",
    ]

    if day.cpp:
        name = cpp_name(day)
        tracks.append(f"| **C++** | {day.cpp.title} |")
        tonight.append(f"- **C++** — {day.cpp.line}")
        questions.append(f"- *{day.cpp.ask}*")
        order.append(f"3. [{name}]({name}) — the C++ lesson")
        order.append("4. [03-practice.md](03-practice.md) — code it, then say it out loud")
        sits.append(f"- C++ phase: **{day.cpp.phase}**")
    else:
        order.append("3. [03-practice.md](03-practice.md) — code it, then say it out loud")

    heading = "## The questions today answers" if day.cpp else "## The two questions today answers"

    return "\n".join(
        [
            f"# Day {day.n:03d} — {day.dsa.title}",
            "",
            *tracks,
            "",
            "## What you can do by tonight",
            "",
            *tonight,
            "",
            heading,
            "",
            *questions,
            "",
            "## Read in this order",
            "",
            *order,
            "",
            "## Where this sits",
            "",
            *sits,
            "",
            "---",
            "",
            " · ".join(nav),
            "",
        ]
    )


def days_readme(days: list[Day]) -> str:
    lines = [
        "# The 180 days",
        "",
        "Every day is one folder. Every folder holds one DSA lesson, one system design",
        "lesson, and one practice sheet. Start at day 001 and do not skip.",
        "",
        "Ten of the days carry a fourth lesson: the C++ track, for readers who want to solve",
        "in C++ as well. They are marked in the last column. A day with a blank there is four",
        "files, as always.",
        "",
        "| Day | DSA | System design | C++ |",
        "|---:|---|---|---|",
    ]
    for d in days:
        cpp = d.cpp.title if d.cpp else ""
        lines.append(
            f"| [{d.n:03d}]({d.folder}/README.md) | {d.dsa.title} | {d.sd.title} | {cpp} |"
        )
    lines.append("")
    return "\n".join(lines)


def curriculum_index(days: list[Day]) -> str:
    by_n = {d.n: d for d in days}
    lines = [
        "# Krama — the curriculum index",
        "",
        "180 days. Each day teaches one DSA topic and one system design topic, side by side.",
        "This file is generated from `scripts/curriculum.py` — edit that, then run",
        "`python scripts/build_skeleton.py`.",
        "",
        "- **Days 1-96** build the foundations and the low-level design half.",
        "- **Days 97-180** build distributed systems and the high-level design half.",
        "",
        "---",
        "",
        "## The DSA track, by phase",
        "",
        "| Days | Phase |",
        "|---|---|",
    ]
    for name, lo, hi in DSA_PHASES:
        lines.append(f"| {lo}-{hi} | {name} |")
    lines += ["", "## The system design track, by phase", "", "| Days | Phase |", "|---|---|"]
    for name, lo, hi in SD_PHASES:
        lines.append(f"| {lo}-{hi} | {name} |")

    cpp_days = [d for d in days if d.cpp]
    lines += [
        "",
        "## The C++ track",
        "",
        "Optional, and ten days long. Each one sits on the day the course first needs that",
        "piece of C++. Five land in the first six days, which is enough to start solving in",
        "C++; five more are placed at the head of the phase that needs them. Every other day",
        "is four files, unchanged.",
        "",
        "| Day | C++ lesson |",
        "|---:|---|",
    ]
    for d in cpp_days:
        lines.append(f"| [{d.n:03d}](../days/{d.folder}/README.md) | {d.cpp.title} |")

    lines += ["", "---", "", "## Every day"]

    # Group the day table by DSA phase so the index reads as a syllabus.
    for name, lo, hi in DSA_PHASES:
        lines += [
            "",
            f"### Days {lo}-{hi} — {name}",
            "",
            "| Day | DSA lesson | System design lesson |",
            "|---:|---|---|",
        ]
        for n in range(lo, hi + 1):
            d = by_n[n]
            lines.append(
                f"| [{n:03d}](../days/{d.folder}/README.md) | {d.dsa.title} | {d.sd.title} |"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="rewrite existing placeholders")
    args = ap.parse_args()

    days = load()
    written = skipped = generated = 0

    for i, day in enumerate(days):
        folder = DAYS_DIR / day.folder
        prev = days[i - 1] if i > 0 else None
        nxt = days[i + 1] if i + 1 < len(days) else None

        # The hub is derived entirely from the syllabus, so it is always regenerated —
        # like days/README.md and the index. Only the lessons hold hand-written prose.
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(hub_file(day, prev, nxt), encoding="utf-8", newline="\n")
        generated += 1

        targets = [
            (folder / f"01-dsa-{short_slug(day.dsa.title)}.md", lesson_file(day, day.dsa)),
            (folder / f"02-system-design-{short_slug(day.sd.title)}.md", lesson_file(day, day.sd)),
            (folder / "03-practice.md", practice_file(day)),
        ]
        if day.cpp:
            targets.append((folder / cpp_name(day), lesson_file(day, day.cpp)))
        for path, body in targets:
            if write(path, body, args.force):
                written += 1
            else:
                skipped += 1

    DAYS_DIR.mkdir(parents=True, exist_ok=True)
    (DAYS_DIR / "README.md").write_text(days_readme(days), encoding="utf-8", newline="\n")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "CURRICULUM_INDEX.md").write_text(
        curriculum_index(days), encoding="utf-8", newline="\n"
    )

    print(f"{len(days)} days · {generated} hubs · {written} written · {skipped} left alone")
    print("index: docs/CURRICULUM_INDEX.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
