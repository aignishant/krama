"""Doubling benchmark. The ratio column is the proof; the wall clock is noise.

Run:  uv run python days/day-02-proving-a-loop-correct/lab/bench.py

What to look for, in this order.

1. The `ratio` column, this row's time divided by the previous row's. The
   derivation in section 7 says the body runs a // b times, so doubling a with b
   fixed doubles the work: the column settles near 2.00. If it sits near 1.00,
   you did not write a loop.
2. The `iters` column against `a / b`. They must be equal, exactly. The variant
   starts at a, falls by b each pass, and stops below b -- there is no room in
   that sentence for an off-by-one.
3. The second table, which holds a // b *fixed* at 64 and grows a and b
   together. The iteration count does not move and neither does the time. That
   is the whole point of the phrase "linear in a / b" rather than "linear in a",
   and it is the table that tells you which quantity is really n here (CPX-02).

Nothing floats: the sizes are fixed, so this table is the same table tomorrow.
"""

import time

from implement import divide

REPEATS = 3


def best_of(a: int, b: int) -> tuple[float, int]:
    """Smallest of REPEATS runs -- the minimum is the least noisy statistic here."""
    best = None
    iterations = 0
    for _ in range(REPEATS):
        start = time.perf_counter()
        _, _, iterations = divide(a, b)
        elapsed = time.perf_counter() - start
        best = elapsed if best is None else min(best, elapsed)
    assert best is not None
    return best, iterations


def growing_a() -> None:
    print("b fixed at 7, a doubling")
    print(f"{'a':>12} {'seconds':>12} {'ratio':>8} {'iters':>12}")
    previous = None
    a = 100_000
    for _ in range(6):
        elapsed, iterations = best_of(a, 7)
        ratio = f"{elapsed / previous:8.2f}" if previous else "       -"
        print(f"{a:>12} {elapsed:>12.6f} {ratio} {iterations:>12,}")
        previous, a = elapsed, a * 2


def fixed_quotient() -> None:
    print()
    print("a // b held at 64, both growing")
    print(f"{'a':>12} {'b':>12} {'seconds':>12} {'iters':>8}")
    b = 1
    for _ in range(6):
        a = 64 * b
        elapsed, iterations = best_of(a, b)
        print(f"{a:>12} {b:>12} {elapsed:>12.6f} {iterations:>8,}")
        b *= 100


def main() -> None:
    growing_a()
    fixed_quotient()


if __name__ == "__main__":
    main()
