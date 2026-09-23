"""Day 1 — the oracle. Brute force. Correct by inspection. Slow is fine.

Two jobs, and they are deliberately separate.

The *value* is found the most obvious way there is: an element is the maximum
when no other element is greater than it, so try every element and check it
against all the others. That is Theta(n^2) and there is nowhere in it for a bug
to hide, which is the only property an oracle needs.

The *count* is not counted here -- it is asserted. A correct single-pass
procedure performs exactly len(xs) - 1 element-to-element comparisons: it must
look at every element other than its starting candidate, and one comparison is
enough for each. So the oracle states len(xs) - 1 as part of the contract.

That assertion alone cannot catch a solution that sorts and then *reports*
len(xs) - 1, because the count is self-reported. Checking the count that was
actually performed is a separate job, done in test_implement.py by handing your
function elements that keep their own tally. Getting the right answer the wrong
way is still a failure, and that is the test which says so.
"""


def max_and_comparisons(xs: list[int]) -> tuple[int, int]:
    """Return (largest element of xs, len(xs) - 1). Raises on an empty list."""
    if not xs:
        raise ValueError("max_and_comparisons() arg is an empty sequence")

    for candidate in xs:
        beaten_by_nothing = True
        for other in xs:
            if other > candidate:
                beaten_by_nothing = False
                break
        if beaten_by_nothing:
            return candidate, len(xs) - 1

    raise AssertionError("unreachable: a non-empty list always has a maximum")
