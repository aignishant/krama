"""Doubling benchmark. The ratio column is the proof; the wall clock is noise.

Run:  uv run python days/day-00-setup/lab/bench.py

Two columns, side by side, on the same inputs. `quadratic` is reference.py --
the version that re-reads the whole prefix at every step. `yours` is
implement.py. While implement.py is still a stub its columns read `stub`, so you
can run this before writing a line and see the slow shape on its own first.

What to look for, in this order.

1. The two `ratio` columns. A ratio is this row's time divided by the previous
   row's, and doubling n is what makes it meaningful. Theta(n) predicts 2.00 --
   twice the input, twice the work. Theta(n^2) predicts 4.00, because
   n(n+1)/2 roughly quadruples when n doubles. That is the whole of Day 0.
2. The absolute seconds, second. At the smallest n the quadratic version is not
   embarrassing; it might even win. Asymptotics are a claim about what happens
   as n grows, not a claim about n = 1000, and the table shows you both.
3. The second table, which the quadratic version cannot be run on at all
   without you waiting for minutes. That is the practical meaning of the ratio.
4. One row in that second table, usually around n = 400000, reading nearer 3
   than 2 -- and reading it again on the next run, which is how you know it is
   not noise. Your procedure did not become quadratic between two rows. The
   list stopped fitting in a cache. Nothing in the ratio column can tell those
   two apart, and Day 1 is where that gets a name.

Nothing floats: the seed is fixed, so this table is the same table tomorrow.
"""

import gc
import random
import time
from collections.abc import Callable

from implement import running_max as yours
from reference import running_max as quadratic

BATCH_SECONDS = 0.05  # long enough that the clock's own resolution stops mattering
PASSES = 3  # interleaved sweeps of the ladder, best time kept per cell


def batch(fn: Callable[[list[int]], list[int]], xs: list[int], loops: int) -> float | None:
    """Seconds for `loops` back-to-back calls, or None if fn is still a stub."""
    gc.collect()
    gc.disable()  # the cyclic collector is not part of what you wrote
    try:
        start = time.perf_counter()
        for _ in range(loops):
            fn(xs)
        return time.perf_counter() - start
    except NotImplementedError:
        return None
    finally:
        gc.enable()


def timed(fn: Callable[[list[int]], list[int]], xs: list[int]) -> float | None:
    """Seconds for one call, or None if fn is still a stub.

    One measurement, taken carefully. `ladder` is what takes several and keeps
    the best, because taking them all here would take them all at the same
    moment, and a moment is the thing being defended against.

    The care is in the batching. A single pass over a thousand elements finishes
    in tens of microseconds, close enough to the clock's own resolution that you
    would be reading the clock rather than the code. So a probe run decides how
    many calls fit in BATCH_SECONDS, that many run inside one timed region, and
    the total is divided by the count. The quadratic version is never quick
    enough to need this. Yours always is, which is the point.
    """
    probe = batch(fn, xs, 1)
    if probe is None:
        return None
    if probe > BATCH_SECONDS / 4:
        return probe
    loops = int(BATCH_SECONDS / probe) + 1
    elapsed = batch(fn, xs, loops)
    assert elapsed is not None  # a stub would have been caught by the probe
    return elapsed / loops


def column(seconds: float | None, previous: float | None) -> str:
    """One (seconds, ratio) pair, formatted, tolerating a stub or a first row."""
    if seconds is None:
        return f"{'stub':>12} {'-':>8}"
    ratio = f"{seconds / previous:8.2f}" if previous else f"{'-':>8}"
    return f"{seconds:>12.6f} {ratio}"


def ladder(sizes: list[int], fns: dict[str, Callable[[list[int]], list[int]]]) -> dict:
    """Time every function at every size, in PASSES interleaved sweeps.

    The sweeps are why this is not a nested loop with the timings taken where
    they fall. A machine gets busier and hotter while a benchmark runs, so
    measuring the whole ladder bottom to top once puts the largest n in the
    worst conditions -- and a ratio column is exactly the thing that turns
    "later" into "steeper". Sweeping the ladder several times and keeping the
    best time seen for each cell gives the slow patch nowhere to hide.
    """
    inputs = {n: [random.randint(-(10**6), 10**6) for _ in range(n)] for n in sizes}
    best: dict = {name: dict.fromkeys(sizes) for name in fns}
    for _ in range(PASSES):
        for n in sizes:
            for name, fn in fns.items():
                seen = timed(fn, inputs[n])
                if seen is None:
                    continue
                current = best[name][n]
                best[name][n] = seen if current is None else min(current, seen)
    return best


def main() -> None:
    random.seed(20260823)
    small = [1_000, 2_000, 4_000, 8_000]
    large = [100_000, 200_000, 400_000, 800_000]
    measured = ladder(small, {"quadratic": quadratic, "yours": yours})

    print("both versions, same inputs -- read the two ratio columns")
    print(f"{'n':>8} {'quadratic':>12} {'ratio':>8} {'yours':>12} {'ratio':>8}")
    previous: dict[str, float | None] = {"quadratic": None, "yours": None}
    for n in small:
        cells = ""
        for name in ("quadratic", "yours"):
            seconds = measured[name][n]
            cells += " " + column(seconds, previous[name])
            previous[name] = seconds or previous[name]
        print(f"{n:>8}{cells}")

    if previous["yours"] is None:
        print()
        print("implement.py is still a stub, so the second table is skipped. The")
        print("quadratic column above is the whole story so far: it is climbing")
        print("towards 4. Write the single pass, run this again, and put the two")
        print("ratio columns next to each other.")
        return

    # The second ladder ends at 800000, which a quadratic procedure would take
    # something like two hours to finish. So the bench reads its own ratio column
    # and refuses, which is more useful than a hang and is the same reasoning the
    # comparison-count test uses: the shape at n = 8000 already tells you.
    slowest, previous_size = small[-1], small[-2]
    yours_ratio = measured["yours"][slowest] / measured["yours"][previous_size]
    if yours_ratio > 3:
        print()
        print(f"your ratio across the last doubling is {yours_ratio:.2f}, not 2 -- so this")
        print(f"is the quadratic version, and the second table is skipped: at n = {large[-1]:,}")
        print("it would run for hours. That is not a punishment, it is the measurement.")
        print("Now write the single pass and run this again.")
        return

    print()
    print("one size ladder up, where the quadratic version cannot follow")
    print(f"{'n':>10} {'yours':>12} {'ratio':>8}")
    measured = ladder(large, {"yours": yours})
    last: float | None = None
    for n in large:
        seconds = measured["yours"][n]
        print(f"{n:>10} {column(seconds, last)}")
        last = seconds or last


if __name__ == "__main__":
    main()
