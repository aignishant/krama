"""Create the day folders and placeholders for Krama Languages from curriculum.py.

Safe to re-run: a file that already has content (status is not "empty") is never
touched. Hubs, days/README.md and docs/CURRICULUM_INDEX.md are generated and always
rewritten.

python scripts/build_skeleton.py
python scripts/build_skeleton.py --force   # also rewrite untouched placeholders
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from curriculum import LABEL_FOR, PHASES, PROJECTS, Day, Lesson, load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"
DOCS_DIR = ROOT / "docs"

FILE_PREFIX = {"python": "01-python", "go": "02-go", "cpp": "03-cpp"}

# The nine sections every language lesson carries, with the note the placeholder shows.
SECTIONS = [
    ("What this is, and why it matters",
     "Three sentences on what the idea is, then why it shows up at work and in interviews."),
    ("The story",
     "200-400 words. A person, a scene almost anyone has lived, and zero technical words."),
    ("The idea in plain English",
     "Map the story onto the idea, one step at a time. Define each term the first time it appears."),
    ("The picture",
     "At least one diagram, captioned with what to notice. ASCII for memory, Mermaid for flows."),
    ("The code, built step by step",
     "Fragments of ten lines or fewer, each followed by prose. Then the complete runnable program."),
    ("How the other two languages do it",
     "A short side-by-side: the same idea in the other two languages, and the one line of difference that matters."),
    ("The traps",
     "The near-miss that looks right, and the real error text pasted from a real run."),
    ("Say it out loud",
     "How it gets asked, a ninety-second script, the three follow-ups, and a model answer."),
    ("Recall card",
     "Five lines, maximum. What survives if you forget everything else."),
]


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def short_slug(title: str, words: int = 4) -> str:
    parts = [p for p in slugify(title).split("-") if p]
    return "-".join(parts[:words]) or "lesson"


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


def lesson_name(lesson: Lesson) -> str:
    return f"{FILE_PREFIX[lesson.track]}-{short_slug(lesson.title)}.md"


def lesson_file(day: Day, lesson: Lesson) -> str:
    label = LABEL_FOR[lesson.track]
    lines = [
        "---",
        f"day: {day.n}",
        f"track: {lesson.track}",
        f'title: "{lesson.title}"',
        f'theme: "{day.theme}"',
        f'phase: "{day.phase}"',
        "status: empty",
        "---",
        "",
        f"# Day {day.n:03d} · {label} — {lesson.title}",
        "",
        f"**Today's theme:** {day.theme}",
        "",
        f"**After today you can:** {day.outcome}",
        "",
        f"**The interviewer asks it as:** *{day.ask}*",
        "",
        "---",
        "",
        "> Not written yet. The nine headings below are the shape every lesson takes;",
        "> the italic line under each says what belongs there.",
        "> See [how a day works](../../docs/00_HOW_A_DAY_WORKS.md).",
        "",
    ]
    for i, (heading, note) in enumerate(SECTIONS, start=1):
        lines += [f"## {i}. {heading}", "", f"*{note}*", ""]
    return "\n".join(lines)


def practice_file(day: Day) -> str:
    py, go, cpp = day.lessons
    return "\n".join(
        [
            "---",
            f"day: {day.n}",
            "track: practice",
            f'title: "Practice — {day.theme}"',
            "status: empty",
            "---",
            "",
            f"# Day {day.n:03d} · Practice",
            "",
            f"**Theme:** {day.theme}",
            "",
            "---",
            "",
            "## Build these, in all three languages",
            "",
            "*Three exercises, easiest first. Each one says what it is really testing. Every",
            "exercise is done three times: once in Python, once in Go, once in C++.*",
            "",
            "| # | Exercise | What it is really testing |",
            "|---|---|---|",
            "| 1 | | |",
            "| 2 | | |",
            "| 3 | | |",
            "",
            "## Compare",
            "",
            "*One sentence per language: what was easiest, what was hardest, and why.*",
            "",
            f"- **Python** — {py.title}",
            f"- **Go** — {go.title}",
            f"- **C++** — {cpp.title}",
            "",
            "## Say these out loud",
            "",
            "*Three questions from today. Answer each in two minutes, standing up, no notes.*",
            "",
            f"1. {day.ask}",
            "2. ",
            "3. ",
            "",
            "## Before you move on",
            "",
            "- [ ] All three programs run and I can explain every line.",
            "- [ ] I can say the one-line difference between the three languages on today's theme.",
            "- [ ] I answered all three questions above out loud.",
            "",
        ]
    )


def hub_file(day: Day, prev: Day | None, nxt: Day | None) -> str:
    py, go, cpp = day.lessons
    lines = [
        f"# Day {day.n:03d} — {day.theme}",
        "",
        "| Track | Today |",
        "|---|---|",
        f"| **Python** | {py.title} |",
        f"| **Go** | {go.title} |",
        f"| **C++** | {cpp.title} |",
        "",
        "## What you can do by tonight",
        "",
        day.outcome,
        "",
        "## The question today answers",
        "",
        f"*{day.ask}*",
        "",
    ]
    if day.project:
        lines += ["## Project", "", f"**{day.project}** — this is a build day. The lessons are the",
                  "walkthrough; the practice sheet is the deliverable.", ""]
    lines += [
        "## Read in this order",
        "",
        f"1. [{lesson_name(py)}]({lesson_name(py)}) — the Python lesson",
        f"2. [{lesson_name(go)}]({lesson_name(go)}) — the Go lesson",
        f"3. [{lesson_name(cpp)}]({lesson_name(cpp)}) — the C++ lesson",
        "4. [04-practice.md](04-practice.md) — build it three times, then say it out loud",
        "",
        "## Where this sits",
        "",
        f"- Phase: **{day.phase}**",
        "",
        "---",
        "",
    ]
    left = f"[← Day {prev.n:03d}](../{prev.folder}/README.md)" if prev else "Start"
    right = f"[Day {nxt.n:03d} →](../{nxt.folder}/README.md)" if nxt else "End"
    lines += [f"{left} · [All days](../README.md) · {right}", ""]
    return "\n".join(lines)


def days_readme(days: list[Day]) -> str:
    lines = [
        "# All 180 days",
        "",
        "Generated from `scripts/curriculum.py`. Do not edit by hand.",
        "",
    ]
    for name, lo, hi in PHASES:
        lines += [f"## {name} (days {lo}-{hi})", ""]
        for d in days[lo - 1 : hi]:
            tag = " · **project**" if d.project else ""
            lines.append(f"- [Day {d.n:03d}]({d.folder}/README.md) — {d.theme}{tag}")
        lines.append("")
    return "\n".join(lines)


def curriculum_index(days: list[Day]) -> str:
    lines = [
        "# Krama Languages — the plan for all 180 days",
        "",
        "Generated from `scripts/curriculum.py`. Do not edit by hand.",
        "",
        "Every day teaches one theme in three languages: Python, Go, and C++. The same",
        "idea, three ways, so the differences are the lesson.",
        "",
        "## Phases",
        "",
        "| Days | Phase |",
        "|---|---|",
    ]
    for name, lo, hi in PHASES:
        lines.append(f"| {lo}-{hi} | {name} |")
    lines += ["", "## Projects", "", "| Starts | Project |", "|---|---|"]
    for n, name in sorted(PROJECTS.items()):
        lines.append(f"| Day {n:03d} | {name} |")
    lines += [""]
    for name, lo, hi in PHASES:
        lines += [
            f"## {name} (days {lo}-{hi})",
            "",
            "| Day | Theme | Python | Go | C++ | You can |",
            "|---|---|---|---|---|---|",
        ]
        for d in days[lo - 1 : hi]:
            py, go, cpp = d.lessons
            lines.append(
                f"| [{d.n:03d}](../days/{d.folder}/README.md) | {d.theme} | {py.title} | "
                f"{go.title} | {cpp.title} | {d.outcome} |"
            )
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    force = "--force" in sys.argv
    days = load()
    written = 0
    for i, day in enumerate(days):
        folder = DAYS_DIR / day.folder
        prev = days[i - 1] if i > 0 else None
        nxt = days[i + 1] if i + 1 < len(days) else None
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(hub_file(day, prev, nxt), encoding="utf-8", newline="\n")
        for lesson in day.lessons:
            written += write(folder / lesson_name(lesson), lesson_file(day, lesson), force)
        written += write(folder / "04-practice.md", practice_file(day), force)
    (DAYS_DIR / "README.md").write_text(days_readme(days), encoding="utf-8", newline="\n")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    (DOCS_DIR / "CURRICULUM_INDEX.md").write_text(
        curriculum_index(days), encoding="utf-8", newline="\n"
    )
    print(f"{len(days)} days · {written} placeholder files written · hubs and index rebuilt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
