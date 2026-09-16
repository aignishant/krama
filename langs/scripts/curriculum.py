"""The Krama Languages syllabus, as data.

One row per day. Every day carries three lessons, one per language, on the same theme:
Python, Go, and C++. build_skeleton.py turns this file into days/ and
docs/CURRICULUM_INDEX.md.

Row shape:

    (n, day_slug, theme,
     py_title, go_title, cpp_title,
     outcome, ask)

    day_slug    folder name after "day-NNN-"
    theme       the one idea all three lessons teach today
    *_title     what that language's lesson is about
    outcome     what you can DO after the day, in one sentence
    ask         how an interviewer actually phrases the question
"""

from __future__ import annotations

from dataclasses import dataclass

from syllabus import part1, part2, part3

TRACKS = ("python", "go", "cpp")

LABEL_FOR = {"python": "Python", "go": "Go", "cpp": "C++"}

PHASES = [
    ("Foundations: every language, every basic", 1, 15),
    ("Advanced features", 16, 45),
    ("Networking, HTTP, and data", 46, 60),
    ("Protocol Buffers and gRPC", 61, 75),
    ("Performance and systems programming", 76, 90),
    ("Messaging, resilience, and deployment", 91, 105),
    ("Idiomatic depth and design", 106, 135),
    ("Six five-day builds", 136, 165),
    ("Interview prep and the capstone", 166, 180),
]

# Days that end a block with something you can run and show. Mini projects are one day;
# builds and the capstone span several days and are named by their first day.
PROJECTS: dict[int, str] = {
    15: "Mini project 1: a to-do CLI",
    30: "Mini project 2: a text analyser",
    45: "Mini project 3: a concurrent downloader",
    60: "Mini project 4: a URL shortener API",
    75: "Mini project 5: an inventory service over gRPC",
    90: "Mini project 6: a log analytics pipeline",
    105: "Mini project 7: orders, events, and notifications",
    120: "Mini project 8: a rate-limiter library",
    135: "Mini project 9: a key-value store with a wire protocol",
    136: "Build A: a distributed cache (days 136-140)",
    141: "Build B: a job queue (days 141-145)",
    146: "Build C: a storage engine (days 146-150)",
    151: "Build D: a chat system (days 151-155)",
    156: "Build E: an observability toolkit (days 156-160)",
    161: "Build F: a tiny language (days 161-165)",
    171: "Capstone: an order platform (days 171-178)",
}

RAW = part1.DAYS + part2.DAYS + part3.DAYS


@dataclass(frozen=True)
class Lesson:
    """One of the three lessons a day carries."""

    track: str  # "python", "go", or "cpp"
    title: str


@dataclass(frozen=True)
class Day:
    n: int
    slug: str
    theme: str
    outcome: str
    ask: str
    lessons: tuple[Lesson, Lesson, Lesson]  # python, go, cpp — always in this order

    @property
    def folder(self) -> str:
        return f"day-{self.n:03d}-{self.slug}"

    @property
    def phase(self) -> str:
        for name, lo, hi in PHASES:
            if lo <= self.n <= hi:
                return name
        raise ValueError(f"day {self.n} is in no phase")

    @property
    def project(self) -> str | None:
        return PROJECTS.get(self.n)


def load() -> list[Day]:
    """Validate the raw rows and return them as Day objects."""
    days: list[Day] = []
    seen: set[int] = set()
    for row in RAW:
        if len(row) != 8:
            raise ValueError(f"row for day {row[0]} has {len(row)} fields, expected 8")
        n, slug, theme, py, go, cpp, outcome, ask = row
        if n in seen:
            raise ValueError(f"day {n} appears twice")
        seen.add(n)
        days.append(
            Day(
                n=n,
                slug=slug,
                theme=theme,
                outcome=outcome,
                ask=ask,
                lessons=(Lesson("python", py), Lesson("go", go), Lesson("cpp", cpp)),
            )
        )
    days.sort(key=lambda d: d.n)
    expected = list(range(1, 181))
    got = [d.n for d in days]
    if got != expected:
        missing = sorted(set(expected) - set(got))
        extra = sorted(set(got) - set(expected))
        raise ValueError(f"days must be exactly 1..180; missing={missing} extra={extra}")
    return days


if __name__ == "__main__":
    for d in load():
        print(f"{d.n:03d}  {d.theme}")
