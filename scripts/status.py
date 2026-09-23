"""Progress, computed from disk. Never a stored number.

python scripts/status.py
"""

from __future__ import annotations

from pathlib import Path

from curriculum import DSA_PHASES, SD_PHASES, load

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

    for day in days:
        folder = DAYS_DIR / day.folder
        if not folder.is_dir():
            continue
        dsa, sd = lesson_paths(folder)
        if dsa and written(dsa):
            dsa_done.add(day.n)
        if sd and written(sd):
            sd_done.add(day.n)

    total = len(days)
    both = dsa_done & sd_done

    print(f"\n{BOLD}Krama{OFF} — 180 days, two tracks\n")
    print(f"  DSA            {bar(len(dsa_done), total)} {len(dsa_done):>3}/{total}")
    print(f"  System design  {bar(len(sd_done), total)} {len(sd_done):>3}/{total}")
    print(f"  Days complete  {bar(len(both), total)} {len(both):>3}/{total}\n")

    def phase_table(title: str, phases: list[tuple[str, int, int]], done: set[int]) -> None:
        print(f"  {BOLD}{title}{OFF}")
        for name, lo, hi in phases:
            span = hi - lo + 1
            got = len([n for n in range(lo, hi + 1) if n in done])
            mark = (
                f"{GREEN}done{OFF}" if got == span else (f"{got}/{span}" if got else f"{DIM}-{OFF}")
            )
            print(f"    {lo:>3}-{hi:<3}  {name:<48} {mark}")
        print()

    phase_table("DSA", DSA_PHASES, dsa_done)
    phase_table("System design", SD_PHASES, sd_done)

    nxt = next((d for d in days if d.n not in both), None)
    if nxt:
        print(f"  Next: {BOLD}day {nxt.n:03d}{OFF} — {nxt.dsa.title}")
        print(f"        {DIM}+ {nxt.sd.title}{OFF}")
        print(f"        write it with:  /day-krama {nxt.n}\n")
    else:
        print(f"  {GREEN}All 180 days written.{OFF}\n")


if __name__ == "__main__":
    main()
