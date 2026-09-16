"""Progress, computed from disk. Never a stored number.

A day is complete when every one of its required lessons is written: the DSA lesson,
the system design lesson, and the three language lessons with their practice sheet.
The C++ contest lesson is optional and never holds a day back.

python scripts/status.py
python scripts/status.py --next     # print only the first unfinished day number
"""

from __future__ import annotations

import sys
from pathlib import Path

from build_skeleton import lang_lesson_name, practice_name
from curriculum import DSA_PHASES, LANG_LABEL_FOR, LANG_PHASES, LANG_TRACKS, SD_PHASES, load

ROOT = Path(__file__).resolve().parent.parent
DAYS_DIR = ROOT / "days"

GREEN, DIM, BOLD, OFF = "\033[32m", "\033[2m", "\033[1m", "\033[0m"


def written(path: Path) -> bool:
    return path.exists() and "status: empty" not in path.read_text(encoding="utf-8")[:400]


def lesson_paths(folder: Path) -> tuple[Path | None, Path | None]:
    dsa = next(iter(sorted(folder.glob("01-dsa-*.md"))), None)
    sd = next(iter(sorted(folder.glob("02-system-design-*.md"))), None)
    return dsa, sd


def bar(done: int, total: int, width: int = 28) -> str:
    filled = 0 if total == 0 else round(width * done / total)
    return f"[{'#' * filled}{'.' * (width - filled)}]"


def main() -> None:
    days = load()
    dsa_done: set[int] = set()
    sd_done: set[int] = set()
    cpp_done: set[int] = set()
    lang_done: dict[str, set[int]] = {t: set() for t in LANG_TRACKS}
    lang_practice_done: set[int] = set()
    cpp_days = [d for d in days if d.cpp]

    for day in days:
        folder = DAYS_DIR / day.folder
        if not folder.is_dir():
            continue
        dsa, sd = lesson_paths(folder)
        if dsa and written(dsa):
            dsa_done.add(day.n)
        if sd and written(sd):
            sd_done.add(day.n)
        if day.cpp:
            cpp = next(iter(sorted(folder.glob("04-cpp-*.md"))), None)
            if cpp and written(cpp):
                cpp_done.add(day.n)
        for lesson in day.langs.lessons:
            if written(folder / lang_lesson_name(lesson)):
                lang_done[lesson.track].add(day.n)
        if written(folder / practice_name(day)):
            lang_practice_done.add(day.n)

    total = len(days)
    langs_all = set.intersection(*lang_done.values()) & lang_practice_done
    complete = dsa_done & sd_done & langs_all
    nxt = next((d for d in days if d.n not in complete), None)

    if "--next" in sys.argv:
        print(nxt.n if nxt else "done")
        return

    print(f"\n{BOLD}Krama{OFF} — 180 days, DSA, system design, and three languages\n")
    print(f"  DSA            {bar(len(dsa_done), total)} {len(dsa_done):>3}/{total}")
    print(f"  System design  {bar(len(sd_done), total)} {len(sd_done):>3}/{total}")
    for track in LANG_TRACKS:
        got = lang_done[track]
        print(f"  {LANG_LABEL_FOR[track]:<14} {bar(len(got), total)} {len(got):>3}/{total}")
    print(
        f"  Lang practice  {bar(len(lang_practice_done), total)} "
        f"{len(lang_practice_done):>3}/{total}"
    )
    print(f"  Days complete  {bar(len(complete), total)} {len(complete):>3}/{total}")
    print(
        f"  C++ contests   {bar(len(cpp_done), len(cpp_days))} "
        f"{len(cpp_done):>3}/{len(cpp_days)}  {DIM}(optional){OFF}\n"
    )

    def phase_table(title: str, phases: list[tuple[str, int, int]], done: set[int]) -> None:
        print(f"  {BOLD}{title}{OFF}")
        for name, lo, hi in phases:
            span = hi - lo + 1
            got = len([n for n in range(lo, hi + 1) if n in done])
            mark = (
                f"{GREEN}done{OFF}" if got == span else (f"{got}/{span}" if got else f"{DIM}-{OFF}")
            )
            print(f"    {lo:>3}-{hi:<3}  {name:<50} {mark}")
        print()

    phase_table("DSA", DSA_PHASES, dsa_done)
    phase_table("System design", SD_PHASES, sd_done)
    phase_table("Languages", LANG_PHASES, langs_all)

    if nxt:
        missing = []
        if nxt.n not in dsa_done:
            missing.append("DSA")
        if nxt.n not in sd_done:
            missing.append("system design")
        for track in LANG_TRACKS:
            if nxt.n not in lang_done[track]:
                missing.append(LANG_LABEL_FOR[track])
        if nxt.n not in lang_practice_done:
            missing.append("languages practice")
        print(f"  Next: {BOLD}day {nxt.n:03d}{OFF} — {nxt.dsa.title}")
        print(f"        {DIM}+ {nxt.sd.title}{OFF}")
        print(f"        {DIM}+ languages: {nxt.langs.theme}{OFF}")
        print(f"        still to write: {', '.join(missing)}")
        print(f"        write it with:  /day-krama {nxt.n}\n")
    else:
        print(f"  {GREEN}All 180 days written.{OFF}\n")


if __name__ == "__main__":
    main()
