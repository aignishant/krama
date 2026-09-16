"""Check written lessons against the format contract in docs/00_HOW_A_DAY_WORKS.md.

Sections and their order, the story's length and its freedom from jargon, the weight of
the interview section, rule 15 — that nothing sends the reader looking for paper — and
that every link a day makes still points at a folder that exists. The three language
lessons are held to a little more: section 5 must end in a complete program, section 8
must carry follow-ups and a model answer, and nothing may estimate reading time.

python scripts/check_day.py         # every day that has been written
python scripts/check_day.py 37      # just day 37
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from build_skeleton import (
    CPP_SECTIONS,
    DSA_SECTIONS,
    LANG_SECTIONS,
    SD_SECTIONS,
    UNIFIED_PRACTICE_DAYS,
    lang_lesson_name,
    practice_name,
)
from curriculum import LANG_LABEL_FOR, load

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


# The language lessons' stories are read by someone who has never programmed. These are
# the words that mean the story has started teaching.
LANG_JARGON = [
    "variable",
    "function",
    "compile",
    "pointer",
    "memory",
    "thread",
    "server",
    "string",
    "array",
    "slice",
    "vector",
    "class",
    "struct",
    "interface",
    "goroutine",
    "channel",
    "byte",
    "protobuf",
    "gRPC",
    "API",
    "JSON",
    "database",
    "cache",
    "exception",
    "error code",
    "null",
    "loop",
    "type",
]

# Rule 12: a day is a unit of subject, not of hours.
TIME_ESTIMATES = [r"minutes? to read", r"≈\s*\d+\s*min", r"\bquick (read|lesson)\b"]

FENCE = re.compile(r"^```(\w*)", re.M)

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


def check_lang_lesson(path: Path) -> list[str]:
    """The language lessons' contract: the shared checks, plus the ones that only make
    sense for a lesson whose section 5 is a program and whose section 8 is a script."""
    problems = check_lesson(path, LANG_SECTIONS)
    text = path.read_text(encoding="utf-8")
    if "status: empty" in text[:400]:
        return problems
    rel = path.relative_to(ROOT).as_posix()

    story = body_of(text, 2)
    if story:
        words = len(story.split())
        if words > 400:
            problems.append(f"{rel}: §2 story is {words} words, contract says 200-400")
        hits = sorted({j for j in LANG_JARGON if re.search(rf"\b{re.escape(j)}\b", story, re.I)})
        if hits:
            problems.append(f"{rel}: §2 story uses technical words: {', '.join(hits[:6])}")

    code = body_of(text, 5)
    if code and not FENCE.findall(code):
        problems.append(f"{rel}: §5 has no code")
    else:
        blocks = re.findall(r"```\w*\n(.*?)```", code, flags=re.S)
        if blocks and len(blocks[-1].strip().splitlines()) < 8:
            problems.append(f"{rel}: §5 does not end in a complete program")

    interview = body_of(text, 8).lower()
    for needle in ("follow-up", "model answer"):
        if interview and needle not in interview:
            problems.append(f"{rel}: §8 has no {needle}")

    recall = body_of(text, 9)
    bullets = [
        line
        for line in recall.splitlines()
        if line.strip().startswith(("-", "*", "1", "2", "3", "4", "5"))
    ]
    if len(bullets) > 5:
        problems.append(f"{rel}: §9 recall card has {len(bullets)} lines, maximum 5")

    for pat in TIME_ESTIMATES:
        if re.search(pat, text, flags=re.I):
            problems.append(f"{rel}: estimates reading time: {pat!r}")
    return problems


def check_lang_practice(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if "status: written" not in text[:400]:
        return [f"{path.relative_to(ROOT).as_posix()}: not written yet"]
    rel = path.relative_to(ROOT).as_posix()
    problems: list[str] = []
    rows = re.findall(r"^\| \d+ \| (.+?) \| (.+?) \|$", text, flags=re.M)
    if len([r for r in rows if r[0].strip()]) < 3:
        problems.append(f"{rel}: fewer than three exercises")
    if "## Say these out loud" not in text:
        problems.append(f"{rel}: missing the out-loud section")
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

    # The languages half: three lessons and a practice sheet, on every day.
    lang_paths = [folder / lang_lesson_name(lesson) for lesson in day.langs.lessons]
    for lesson, path in zip(day.langs.lessons, lang_paths, strict=True):
        if not path.exists():
            problems.append(
                f"days/{day.folder}: missing the {LANG_LABEL_FOR[lesson.track]} lesson {path.name}"
            )
    lang_practice = folder / practice_name(day)
    if not lang_practice.exists():
        problems.append(f"days/{day.folder}: missing {lang_practice.name}")
    if day.n in UNIFIED_PRACTICE_DAYS:
        practices = sorted(
            path
            for path in folder.glob("*.md")
            if re.fullmatch(r"\d+-(?:lang-)?practice\.md", path.name)
        )
        if practices != [folder / "03-practice.md"]:
            problems.append(f"days/{day.folder}: expected only 03-practice.md")

    if len(dsa) == 1:
        problems += check_lesson(dsa[0], DSA_SECTIONS)
    if len(sd) == 1:
        problems += check_lesson(sd[0], SD_SECTIONS)
    # The C++ contest lesson is optional, so an unwritten one is not a failure of the
    # day — it is only held to the contract once somebody has written it.
    if (
        day.cpp
        and len(cpp) == 1
        and "status: empty" not in cpp[0].read_text(encoding="utf-8")[:400]
    ):
        problems += check_lesson(cpp[0], CPP_SECTIONS)
    for path in lang_paths:
        if path.exists():
            problems += check_lang_lesson(path)
    if lang_practice.exists():
        problems += check_lang_practice(lang_practice)

    for path in (
        *dsa,
        *sd,
        *cpp,
        *lang_paths,
        lang_practice,
        folder / "03-practice.md",
        folder / "README.md",
    ):
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
            else:
                # A half-written day still gets its written half checked.
                real = [p for p in problems if "not written yet" not in p]
                if real:
                    failures += 1
                    print(f"day {n:03d} (partly written):")
                    for p in real:
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
