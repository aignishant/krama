"""Check written lessons against the format contract in docs/00_HOW_A_DAY_WORKS.md.

Sections and their order, the story's length and freedom from jargon, that the code
section ends in a complete program, that nothing sends the reader to paper, and that
no lesson estimates reading time.

python scripts/check_day.py         # every day that has been written
python scripts/check_day.py 37      # just day 37
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from build_skeleton import SECTIONS, is_placeholder, lesson_name
from curriculum import load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"

# Section 2 is a story. These are the words that mean it stopped being one.
JARGON = [
    "variable", "function", "compile", "pointer", "memory", "thread", "server",
    "string", "array", "slice", "vector", "class", "struct", "interface", "goroutine",
    "channel", "byte", "protobuf", "gRPC", "API", "JSON", "database", "cache",
    "exception", "error code", "null", "loop", "type",
]

PAPER = [
    r"on paper", r"a blank page", r"blank sheet", r"pen and paper",
    r"sheet of paper", r"piece of paper", r"in your notebook", r"on a page",
]

TIME_ESTIMATES = [r"minutes? to read", r"≈\s*\d+\s*min", r"\bquick (read|lesson)\b"]

FENCE = re.compile(r"^```(\w*)", re.M)


def sections_of(text: str) -> list[str]:
    return re.findall(r"^## (\d+\. .+)$", text, flags=re.M)


def section_body(text: str, number: int) -> str:
    m = re.search(rf"^## {number}\. .*?$(.*?)(?=^## \d+\. |\Z)", text, flags=re.M | re.S)
    return m.group(1) if m else ""


def check_lesson(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    expected = [f"{i}. {h}" for i, (h, _) in enumerate(SECTIONS, start=1)]
    got = sections_of(text)
    if got != expected:
        problems.append(f"sections are {got!r}, expected {expected!r}")

    story = section_body(text, 2)
    words = len(re.findall(r"\w+", story))
    if not 200 <= words <= 400:
        problems.append(f"story is {words} words, wanted 200-400")
    if "```" in story:
        problems.append("story contains a code block")
    for term in JARGON:
        if re.search(rf"\b{re.escape(term)}\b", story, flags=re.I):
            problems.append(f"story uses the technical word {term!r}")

    code = section_body(text, 5)
    fences = FENCE.findall(code)
    if not fences:
        problems.append("section 5 has no code")
    else:
        blocks = re.findall(r"```\w*\n(.*?)```", code, flags=re.S)
        if blocks and len(blocks[-1].strip().splitlines()) < 8:
            problems.append("section 5 does not end in a complete program")

    interview = section_body(text, 8)
    for needle in ("follow-up", "model answer"):
        if needle not in interview.lower():
            problems.append(f"section 8 has no {needle}")

    recall = section_body(text, 9)
    bullets = [l for l in recall.splitlines() if l.strip().startswith(("-", "*", "1", "2", "3", "4", "5"))]
    if len(bullets) > 5:
        problems.append(f"recall card has {len(bullets)} lines, maximum 5")

    for pat in PAPER:
        if re.search(pat, text, flags=re.I):
            problems.append(f"sends the reader to paper: {pat!r}")
    for pat in TIME_ESTIMATES:
        if re.search(pat, text, flags=re.I):
            problems.append(f"estimates reading time: {pat!r}")
    return problems


def check_practice(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []
    rows = re.findall(r"^\| \d+ \| (.+?) \| (.+?) \|$", text, flags=re.M)
    if len([r for r in rows if r[0].strip()]) < 3:
        problems.append("fewer than three exercises")
    if "## Say these out loud" not in text:
        problems.append("missing the out-loud section")
    return problems


def main() -> int:
    only = int(sys.argv[1]) if len(sys.argv) > 1 else None
    days = load()
    failures = 0
    checked = 0
    for day in days:
        if only is not None and day.n != only:
            continue
        folder = DAYS_DIR / day.folder
        files = [folder / lesson_name(l) for l in day.lessons] + [folder / "04-practice.md"]
        if all(is_placeholder(f) for f in files):
            continue
        for f in files:
            if is_placeholder(f):
                print(f"day {day.n:03d}  {f.name}: still a placeholder")
                failures += 1
                continue
            checked += 1
            probs = check_practice(f) if f.name == "04-practice.md" else check_lesson(f)
            for p in probs:
                print(f"day {day.n:03d}  {f.name}: {p}")
            failures += len(probs)
    print(f"{checked} files checked · {failures} problems")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
