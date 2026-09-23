"""Day 0 — your implementation. You type every line."""


def running_max(xs: list[int]) -> list[int]:
    """Return the list whose i-th element is max(xs[0..i]).

    Pre:   xs may be empty.
    Post:  len(result) == len(xs); result is non-decreasing;
           result[i] == max(xs[:i+1]) for all i.
    Time:  O(n), single pass.
    Space: O(n) for the output, O(1) auxiliary.

    Forbidden today: `itertools.accumulate`, `numpy`, and any call to `max()` on
    a slice inside the loop. That last one is the O(n^2) version -- bench.py
    shows its ratio column climbing towards 4 while a single pass sits near 2,
    and test_forbidden_shapes.py fails on it by reading this file's syntax tree.

    Write the quadratic one first, on purpose. Run bench.py. Read the two ratio
    columns side by side. Then delete it and write this one from an empty file.
    """
    raise NotImplementedError
