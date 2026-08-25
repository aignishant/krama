"""Day 3 — the oracle. Brute force. Correct by inspection. Slow is fine.

The definition says: n0 works when the inequality holds at every index from n0
to the end. So the oracle transcribes the definition literally -- try every
candidate n0 in increasing order, and for each one check the entire suffix. The
first candidate that survives is the smallest, and that is the answer.

That is Theta(n^2) and it is the correct shape for an oracle: there is nowhere
in it for a bug to hide, because it is the specification with a `for` in front
of it. Your implementation must not look like this. If it does, bench.py will
say so in the ratio column, which is the only review this file offers.
"""


def dominates_from(f: list[int], g: list[int], c: int) -> int | None:
    """Smallest n0 with f[i] <= c*g[i] for all i >= n0, or None if there is none."""
    if len(f) != len(g):
        raise ValueError("dominates_from() requires tables of equal length")

    n = len(f)
    for n0 in range(n + 1):
        holds = True
        for i in range(n0, n):
            if f[i] > c * g[i]:
                holds = False
                break
        if holds:
            return None if n0 == n and n > 0 else n0
    return None
