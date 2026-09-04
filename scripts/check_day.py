"""Check written lessons against the format contract in docs/00_HOW_A_DAY_WORKS.md.

Sections and their order, the story's length and its freedom from jargon, the weight of
the interview section, rule 15 — that nothing sends the reader looking for paper — and
that every link a day makes still points at a folder that exists.

python scripts/check_day.py         # every day that has been written
python scripts/check_day.py 37      # just day 37
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from build_skeleton import CPP_SECTIONS, DSA_SECTIONS, SD_SECTIONS
from curriculum import load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"

# Section 2 is a story. These are the words that mean it stopped being one.
JARGON = [
    "algorithm",
    "complexity",
    "O(n",
    "array",
    "pointer",
    "hash",
    "node",
    "recursion",
    "server",
    "database",
    "cache",
    "latency",
    "API",
    "protocol",
    "query",
    "index",
    "thread",
    "throughput",
    "bandwidth",
    "replica",
    "shard",
]


# Rule 15: the course never sends the reader looking for paper.
PAPER = [
    r"on paper",
    r"a blank page",
    r"blank sheet",
    r"pen and paper",
    r"sheet of paper",
    r"piece of paper",
    r"in your notebook",
    r"on a page",
]


def check_paper(path: Path) -> list[str]:
    """Rule 15. Draw it in any tool, or say it out loud. Never on paper."""
    text = path.read_text(encoding="utf-8")
    if "status: empty" in text[:400]:
        return []
    hits = sorted({m.group(0).lower() for pat in PAPER for m in re.finditer(pat, text, re.I)})
    if not hits:
        return []
    rel = path.relative_to(ROOT).as_posix()
    return [f"{rel}: rule 15 — sends the reader to paper: {', '.join(hits)}"]


# A day links to its neighbours and forward to the day that picks the idea up. Slugs move
# when the syllabus is edited, and a stale link is silent — the reader just lands nowhere.
LINK = re.compile(r"\]\((\.\./[^)#\s]+|[0-9][^)#\s]*\.md)\)")


def check_links(path: Path) -> list[str]:
    """Every relative link in a written file must point at something that exists."""
    text = path.read_text(encoding="utf-8")
    if "status: empty" in text[:400]:
        return []
    rel = path.relative_to(ROOT).as_posix()
    return [
        f"{rel}: broken link to {target}"
        for target in dict.fromkeys(LINK.findall(text))
        if not (path.parent / target).exists()
    ]


def sections_of(text: str) -> list[str]:
    return [m.group(1).strip() for m in re.finditer(r"^## \d+\.\s*(.+)$", text, re.M)]


def body_of(text: str, number: int) -> str:
    """The text under '## <number>. ...' up to the next '## '."""
    m = re.search(rf"^## {number}\.\s*.+$", text, re.M)
    if not m:
        return ""
    rest = text[m.end() :]
    nxt = re.search(r"^## ", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def check_lesson(path: Path, expected: list[tuple[str, str]]) -> list[str]:
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).as_posix()

    if "status: empty" in text[:400]:
        return [f"{rel}: not written yet"]

    found = sections_of(text)
    want = [h for h, _ in expected]
    if found != want:
        missing = [h for h in want if h not in found]
        if missing:
            problems.append(f"{rel}: missing section(s): {'; '.join(missing)}")
        elif len(found) == len(want):
            problems.append(f"{rel}: sections are out of order")
        else:
            problems.append(f"{rel}: expected {len(want)} sections, found {len(found)}")

    story = body_of(text, 2)
    if story:
        words = len(story.split())
        if words < 150:
            problems.append(f"{rel}: §2 story is {words} words, contract says 200-400")
        if "```" in story:
            problems.append(f"{rel}: §2 story contains a code block")
        hits = sorted({j for j in JARGON if re.search(rf"\b{re.escape(j)}", story, re.I)})
        if hits:
            problems.append(f"{rel}: §2 story uses technical words: {', '.join(hits[:6])}")

    interview = body_of(text, 8)
    if interview and len(interview.split()) < 120:
        problems.append(f"{rel}: §8 interview section is too thin")

    recall = body_of(text, 9)
    if recall and not recall.strip():
        problems.append(f"{rel}: §9 recall card is empty")

    return problems


def check_day(n: int) -> tuple[bool, list[str]]:
    days = {d.n: d for d in load()}
    day = days.get(n)
    if day is None:
        return False, [f"day {n} is not in the curriculum"]

    folder = DAYS_DIR / day.folder
    if not folder.is_dir():
        return False, [f"day {n}: no folder at days/{day.folder} — run build_skeleton.py"]

    problems: list[str] = []
    for required in ("README.md", "03-practice.md"):
        if not (folder / required).exists():
            problems.append(f"days/{day.folder}: missing {required}")

    dsa = sorted(folder.glob("01-dsa-*.md"))
    sd = sorted(folder.glob("02-system-design-*.md"))
    if len(dsa) != 1:
        problems.append(f"days/{day.folder}: expected one 01-dsa-*.md, found {len(dsa)}")
    if len(sd) != 1:
        problems.append(f"days/{day.folder}: expected one 02-system-design-*.md, found {len(sd)}")

    stray = [p.name for p in folder.iterdir() if p.is_dir() and p.name == "lab"]
    if stray:
        problems.append(f"days/{day.folder}: lab/ exists — rule 10 forbids it")

    # Rule 1's one exception: a fifth file, but only on the days CPP_DAYS names.
    cpp = sorted(folder.glob("04-cpp-*.md"))
    if day.cpp and len(cpp) != 1:
        problems.append(f"days/{day.folder}: expected one 04-cpp-*.md, found {len(cpp)}")
    if not day.cpp and cpp:
        problems.append(
            f"days/{day.folder}: has {cpp[0].name} but day {n} is not in CPP_DAYS — rule 1"
        )

    if len(dsa) == 1:
        problems += check_lesson(dsa[0], DSA_SECTIONS)
    if len(sd) == 1:
        problems += check_lesson(sd[0], SD_SECTIONS)
    # The C++ lesson is optional, so an unwritten one is not a failure of the day —
    # it is only held to the contract once somebody has written it.
    if day.cpp and len(cpp) == 1 and "status: empty" not in cpp[0].read_text(encoding="utf-8")[:400]:
        problems += check_lesson(cpp[0], CPP_SECTIONS)

    for path in (*dsa, *sd, *cpp, folder / "03-practice.md", folder / "README.md"):
        if path.exists():
            problems += check_paper(path)
            problems += check_links(path)

    written = not any("not written yet" in p for p in problems)
    return written, problems


def main() -> int:
    days = load()
    targets = [int(sys.argv[1])] if len(sys.argv) > 1 else [d.n for d in days]

    failures = 0
    unwritten = 0
    for n in targets:
        written, problems = check_day(n)
        if not written:
            unwritten += 1
            if len(targets) == 1:
                for p in problems:
                    print(f"  · {p}")
            continue
        real = [p for p in problems if "not written yet" not in p]
        if real:
            failures += 1
            print(f"day {n:03d}:")
            for p in real:
                print(f"  · {p}")
        elif len(targets) == 1:
            print(f"day {n:03d}: contract satisfied")

    total = len(targets)
    done = total - unwritten
    print(f"\n{done}/{total} written · {failures} failing the contract")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
