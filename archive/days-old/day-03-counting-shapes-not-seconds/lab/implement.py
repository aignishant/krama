"""Day 3 — your implementation. You type every line."""


def dominates_from(f: list[int], g: list[int], c: int) -> int | None:
    """The smallest index from which f[n] <= c * g[n] holds for the whole tail.

    This is the n0 of a witness pair, computed on data instead of on paper.
    Given two cost tables sampled at n = 0, 1, 2, ... and a candidate
    multiplier c, find the smallest n0 such that

        f[n] <= c * g[n]    for every n in [n0, len(f))

    and return None when no such n0 exists -- which happens exactly when the
    last entry itself violates the inequality, since a violation at the end
    cannot be escaped by starting later.

    Note the shape of the question, because it is the whole exercise. It is not
    "where does the inequality first hold". It is "where does it start holding
    and never stop", which is a claim about a suffix and cannot be answered by
    a scan that stops at the first success. Part 2.1 is what this is for.

    Pre:   len(f) == len(g) == n, with n >= 0; every g[i] >= 0; c >= 0.
           On len(f) != len(g), raise
           ValueError("dominates_from() requires tables of equal length").
    Post:  returns None, or an index n0 in [0, n) such that
           (a) f[i] <= c * g[i] for every i in [n0, n), and
           (b) n0 == 0, or f[n0 - 1] > c * g[n0 - 1] -- it is the *smallest*
               such index, so the entry just before it must be a violation.
           On an empty pair of tables, return 0: every element of an empty
           suffix satisfies the inequality, vacuously (part 1.1 of Day 2).
    Time:  Theta(n). One pass. The oracle checks every suffix separately and is
           Theta(n^2); bench.py shows both, and the ratio columns are the point.
    Space: Theta(1) auxiliary.

    Forbidden today: `reversed`, `enumerate` over a slice, and any construction
    of a reversed or sliced copy of f or g -- `f[::-1]`, `f[i:]`, `list(...)`.
    Each of them copies, which turns a Theta(1)-space single pass into a
    Theta(n)-space one, and the copy inside a loop is how the quadratic version
    gets written by accident. test_forbidden_shapes.py reads your syntax tree.

    You may walk the indices in whichever direction you like. One of the two
    directions makes the invariant a single sentence; the other needs a second
    pass. Work out which before you type, and write the invariant above the
    loop.
    """
    raise NotImplementedError
