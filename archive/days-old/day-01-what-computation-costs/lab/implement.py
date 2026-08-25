"""Day 1 — your implementation. You type every line."""


def max_and_comparisons(xs: list[int]) -> tuple[int, int]:
    """Return the largest element of xs, and the number of comparisons it took.

    A *comparison* means one evaluation of an ordering test between two elements
    of xs -- `a < b`, `a > b`, `a <= b`, `a >= b`. Comparing an element with
    something that is not an element of xs (a loop index, a length, a sentinel
    such as -inf) is not a comparison and must not be counted.

    Pre:   xs is non-empty. On an empty list, raise
           ValueError("max_and_comparisons() arg is an empty sequence").
    Post:  result[0] == the largest value in xs.
           result[1] == len(xs) - 1, exactly -- for every input of that length,
           whatever the values are. Section 7 of part 2.1 says what the
           property that forces this is called; the hub asks you to say why.
    Time:  Theta(n), one pass. Do not sort, and do not compare every pair.
    Space: Theta(1) auxiliary, not counting xs itself.

    Forbidden today: `max`, `min`, `sorted`, `list.sort`, `heapq`, `numpy`,
    and `functools.reduce`. Every one of them is a way of naming the result
    instead of producing it -- which is the distinction part 1.2 is about.
    """
    raise NotImplementedError
