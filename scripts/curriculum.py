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

# ---------------------------------------------------------------------------
# The C++ track.
#
# Ten days, and only ten. Each one sits on the day the course first needs that
# piece of C++, so a reader who wants to solve in C++ starts in week one and tops
# up as new structures arrive. Five land in the first six days — enough to write
# real solutions — and five are placed at the head of the phase that needs them.
#
# A day with no entry here carries no C++ lesson, and its folder stays four files.
#
#   n: (title, what you can do after it, how an interviewer phrases it)
# ---------------------------------------------------------------------------

CPP_PHASE = "C++ and competitive programming"

CPP_DAYS: dict[int, tuple[str, str, str]] = {
    1: (
        "Compiling and running your first program",
        "You can install a compiler, turn a text file into a running program, and read a "
        "compiler error instead of panicking at it.",
        "What is the difference between a compiled language and an interpreted one?",
    ),
    2: (
        "Types, numbers, and the overflow that costs contests",
        "You can choose int or long long correctly, and spot the multiplication that will "
        "overflow before you run it.",
        "What is the range of an int, and what happens when you go past it?",
    ),
    3: (
        "Input, output, and the competitive template",
        "You can read any judge's input format fast enough, and say what every line of your "
        "template actually does.",
        "Your algorithm is optimal and it still times out. What do you check?",
    ),
    5: (
        "vector, references, and the array you use for everything",
        "You can use vector for every array problem in the course, and pass one to a function "
        "without copying four megabytes by accident.",
        "What is the difference between passing by value, by reference, and by pointer?",
    ),
    6: (
        "string, map, set, and pair: half of DSA in four containers",
        "You can choose between map and unordered_map with a reason, and count, group and "
        "deduplicate anything.",
        "When would you use std::map instead of std::unordered_map?",
    ),
    42: (
        "sort, lambdas, and lower_bound: the algorithms header",
        "You can sort by any key with a lambda, and binary search a sorted range without "
        "writing the loop yourself.",
        "What is the difference between lower_bound and upper_bound?",
    ),
    68: (
        "stack, queue, deque, and priority_queue",
        "You can reach for the right container adapter instantly, and build a min-heap in C++ "
        "without having to think about it.",
        "How do you make a min-heap with std::priority_queue?",
    ),
    78: (
        "structs, pointers, and building your own nodes",
        "You can define a node, link nodes together, and say what a pointer holds and what "
        "happens when it dangles.",
        "What is the difference between a pointer and a reference?",
    ),
    125: (
        "Graphs and recursion in C++: adjacency lists, depth, and DSU",
        "You can build an adjacency list, run BFS and DFS with the STL, and say why a deep "
        "recursion crashes in C++ where Python only raises.",
        "How do you represent a graph in C++, and what breaks when the recursion goes deep?",
    ),
    143: (
        "DP tables in C++, and the contest traps that are left",
        "You can allocate a DP table of any shape, memoise with a sentinel, and name the five "
        "bugs that still cost you contests.",
        "How would you write a 2D DP table in C++, and what does it cost in memory?",
    ),
}


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
    cpp: Lesson | None = None  # only on the ten days listed in CPP_DAYS

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
        cpp = None
        if n in CPP_DAYS:
            c_title, c_line, c_ask = CPP_DAYS[n]
            cpp = Lesson("cpp", c_title, c_line, c_ask, CPP_PHASE)
        days.append(
            Day(
                n=n,
                slug=slug,
                dsa=Lesson("dsa", d_title, d_line, d_ask, _phase_of(DSA_PHASES, n)),
                sd=Lesson("system-design", s_title, s_line, s_ask, _phase_of(SD_PHASES, n)),
                cpp=cpp,
            )
        )
    days.sort(key=lambda d: d.n)
    expected = list(range(1, 181))
    if [d.n for d in days] != expected:
        missing = sorted(set(expected) - seen)
        raise ValueError(f"day numbers are not 1..180; missing {missing}")
    stray = sorted(set(CPP_DAYS) - seen)
    if stray:
        raise ValueError(f"CPP_DAYS names days that do not exist: {stray}")
    return days


if __name__ == "__main__":
    loaded = load()
    print(f"{len(loaded)} days, {len(loaded) * 2} lessons")
    for name, lo, hi in DSA_PHASES:
        print(f"  DSA  {lo:>3}-{hi:<3} {name}")
    for name, lo, hi in SD_PHASES:
        print(f"  SD   {lo:>3}-{hi:<3} {name}")
