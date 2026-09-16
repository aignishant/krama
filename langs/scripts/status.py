"""Progress, computed from disk. Never a stored number.

python scripts/status.py
python scripts/status.py --next     # print only the first unwritten day number
"""

from __future__ import annotations

import sys
from pathlib import Path

from build_skeleton import lesson_name
from curriculum import LABEL_FOR, PHASES, TRACKS, load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"

GREEN, DIM, BOLD, OFF = "\033[32m", "\033[2m", "\033[1m", "\033[0m"


def written(path: Path) -> bool:
    return path.exists() and "status: empty" not in path.read_text(encoding="utf-8")[:400]


def bar(done: int, total: int, width: int = 28) -> str:
    filled = 0 if total == 0 else round(width * done / total)
    return f"[{'#' * filled}{'.' * (width - filled)}]"


def main() -> None:
    days = load()
    done: dict[str, set[int]] = {t: set() for t in TRACKS}
    practice_done: set[int] = set()

    for day in days:
        folder = DAYS_DIR / day.folder
        if not folder.is_dir():
            continue
        for lesson in day.lessons:
            if written(folder / lesson_name(lesson)):
                done[lesson.track].add(day.n)
        if written(folder / "04-practice.md"):
            practice_done.add(day.n)

    complete = set.intersection(*done.values()) & practice_done
    nxt = next((d for d in days if d.n not in complete), None)

    if "--next" in sys.argv:
        print(nxt.n if nxt else "done")
        return

    total = len(days)
    print(f"\n{BOLD}Krama Languages{OFF} — 180 days, three languages\n")
    for t in TRACKS:
        print(f"  {LABEL_FOR[t]:<14} {bar(len(done[t]), total)} {len(done[t]):>3}/{total}")
    print(f"  {'Practice':<14} {bar(len(practice_done), total)} {len(practice_done):>3}/{total}")
    print(f"  {'Days complete':<14} {bar(len(complete), total)} {len(complete):>3}/{total}\n")

    print(f"  {BOLD}Phases{OFF}")
    for name, lo, hi in PHASES:
        span = hi - lo + 1
        got = len([n for n in range(lo, hi + 1) if n in complete])
        mark = f"{GREEN}done{OFF}" if got == span else (f"{got}/{span}" if got else f"{DIM}-{OFF}")
        print(f"    {lo:>3}-{hi:<3}  {name:<44} {mark}")
    print()
    if nxt:
        print(f"  next: day {nxt.n:03d} — {nxt.theme}\n")
    else:
        print("  all 180 days written\n")


if __name__ == "__main__":
    main()
