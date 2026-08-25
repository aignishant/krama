"""The Krama syllabus, as data.

One row per day. Every day carries two lessons: a DSA lesson and a System Design
lesson. build_skeleton.py turns this file into days/ and docs/CURRICULUM_INDEX.md.

Row shape:

    (n, day_slug,
     dsa_title, dsa_line, dsa_ask,
     sd_title,  sd_line,  sd_ask)

    day_slug   folder name after "day-NNN-"; taken from the DSA topic
    *_line     what you can DO after reading it, in one sentence
    *_ask      how an interviewer actually phrases this question
"""

from __future__ import annotations

from dataclasses import dataclass

from syllabus import part1, part2, part3, part4

DSA_PHASES = [
    ("Foundations: how code costs", 1, 8),
    ("Arrays", 9, 18),
    ("Strings", 19, 26),
    ("Two pointers and sliding window", 27, 36),
    ("Prefix sums", 37, 41),
    ("Binary search", 42, 50),
    ("Sorting", 51, 59),
    ("Hashing: maps and sets", 60, 67),
    ("Stacks and queues", 68, 77),
    ("Linked lists", 78, 86),
    ("Recursion and backtracking", 87, 97),
    ("Trees and binary search trees", 98, 112),
    ("Heaps and priority queues", 113, 119),
    ("Tries", 120, 124),
    ("Graphs", 125, 142),
    ("Dynamic programming", 143, 163),
    ("Greedy and intervals", 164, 170),
    ("Bits and maths", 171, 176),
    ("Final mocks and revision", 177, 180),
]

SD_PHASES = [
    ("How computers and the internet work", 1, 14),
    ("APIs: how services talk", 15, 24),
    ("Databases from zero", 25, 42),
    ("Object-oriented design", 43, 54),
    ("SOLID and design principles", 55, 62),
    ("Design patterns", 63, 76),
    ("Low-level design case studies", 77, 96),
    ("Scaling fundamentals", 97, 112),
    ("Distributed systems core", 113, 128),
    ("Building blocks of big systems", 129, 144),
    ("High-level design case studies", 145, 170),
    ("Reliability, security, and the interview itself", 171, 180),
]

RAW = part1.DAYS + part2.DAYS + part3.DAYS + part4.DAYS


@dataclass(frozen=True)
class Lesson:
    """One of the two lessons a day carries."""

    track: str  # "dsa" or "system-design"
    title: str
    line: str  # what you can do after reading it
    ask: str  # how an interviewer phrases it
    phase: str


@dataclass(frozen=True)
class Day:
    n: int
    slug: str
    dsa: Lesson
    sd: Lesson

    @property
    def folder(self) -> str:
        return f"day-{self.n:03d}-{self.slug}"


def _phase_of(phases: list[tuple[str, int, int]], n: int) -> str:
    for name, lo, hi in phases:
        if lo <= n <= hi:
            return name
    raise ValueError(f"day {n} falls outside every phase")


def load() -> list[Day]:
    """Validate the raw rows and return them as Day objects."""
    days: list[Day] = []
    seen: set[int] = set()
    for row in RAW:
        if len(row) != 8:
            raise ValueError(f"row for day {row[0]} has {len(row)} fields, expected 8")
        n, slug, d_title, d_line, d_ask, s_title, s_line, s_ask = row
        if n in seen:
            raise ValueError(f"day {n} appears twice")
        seen.add(n)
        days.append(
            Day(
                n=n,
                slug=slug,
                dsa=Lesson("dsa", d_title, d_line, d_ask, _phase_of(DSA_PHASES, n)),
                sd=Lesson("system-design", s_title, s_line, s_ask, _phase_of(SD_PHASES, n)),
            )
        )
    days.sort(key=lambda d: d.n)
    expected = list(range(1, 181))
    if [d.n for d in days] != expected:
        missing = sorted(set(expected) - seen)
        raise ValueError(f"day numbers are not 1..180; missing {missing}")
    return days


if __name__ == "__main__":
    loaded = load()
    print(f"{len(loaded)} days, {len(loaded) * 2} lessons")
    for name, lo, hi in DSA_PHASES:
        print(f"  DSA  {lo:>3}-{hi:<3} {name}")
    for name, lo, hi in SD_PHASES:
        print(f"  SD   {lo:>3}-{hi:<3} {name}")
