"""Day 1 — property-based tests against the oracle, plus a real comparison count.

The whole suite skips while `implement.py` is still a stub, so that a freshly
cloned repo is green. It stops skipping the moment you write your first line,
and from then on it is allowed to go red -- which is the point of it.

Note what `Counted` is for. Your function *reports* a comparison count, and a
test that only checks the reported number is checking your arithmetic rather
than your procedure: `return sorted(xs)[-1], len(xs) - 1` would sail through it.
So the elements themselves keep the tally. Every ordering test between two
elements ticks a counter your function cannot see, and the assertion is on that.
"""

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st
from implement import max_and_comparisons as implement
from reference import max_and_comparisons as reference


class Counted:
    """An integer that records every ordering comparison it takes part in.

    Equality does not tick: the contract counts ordering tests (`<`, `>`, `<=`,
    `>=`) between two elements. Comparison against anything that is not an
    element -- a sentinel like -inf, a length, an index -- does not tick either,
    which is exactly the rule the docstring in implement.py states.
    """

    __slots__ = ("log", "value")

    def __init__(self, value: int, log: list[int]) -> None:
        self.value = value
        self.log = log

    def _against(self, other: Any) -> int:
        if isinstance(other, Counted):
            self.log[0] += 1
            return other.value
        return other

    def __lt__(self, other: Any) -> bool:
        return self.value < self._against(other)

    def __gt__(self, other: Any) -> bool:
        return self.value > self._against(other)

    def __le__(self, other: Any) -> bool:
        return self.value <= self._against(other)

    def __ge__(self, other: Any) -> bool:
        return self.value >= self._against(other)

    def __eq__(self, other: Any) -> bool:
        return self.value == (other.value if isinstance(other, Counted) else other)

    def __repr__(self) -> str:
        return f"Counted({self.value})"


def _is_still_a_stub() -> bool:
    try:
        implement([1])
    except NotImplementedError:
        return True
    except Exception:  # noqa: BLE001 -- any other failure is a real failure, not a stub
        return False
    return False


pytestmark = pytest.mark.skipif(
    _is_still_a_stub(),
    reason="implement.py is still a stub -- write it, and this suite wakes up",
)


@given(st.lists(st.integers(), min_size=1))
def test_matches_reference(xs: list[int]) -> None:
    assert implement(xs) == reference(xs)


@given(st.lists(st.integers(min_value=-3, max_value=3), min_size=1))
def test_matches_reference_on_duplicate_heavy_input(xs: list[int]) -> None:
    """A tiny value range means ties everywhere -- where `>` versus `>=` shows up."""
    assert implement(xs) == reference(xs)


@pytest.mark.parametrize(
    "xs",
    [
        [0],  # single element: zero comparisons
        [7, 7],  # the tie from 1.1's check-yourself
        [1, 1, 1, 1, 1],  # all equal
        [1, 2, 3, 4, 5],  # already sorted, maximum last
        [5, 4, 3, 2, 1],  # reverse sorted, maximum first
        [-1, -2, -3],  # all negative
        [-5, 0, 5],  # straddling zero
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],  # duplicates, maximum in the middle
        [2**70, 2**70 - 1],  # wider than a machine word (2.2 and 2.3)
        [0] * 1000,  # the largest of the small cases
    ],
)
def test_edge_battery(xs: list[int]) -> None:
    assert implement(xs) == reference(xs)


@pytest.mark.parametrize(
    "values",
    [
        [42],
        [3, 1, 4, 1, 5],
        list(range(64)),  # maximum last
        list(range(64))[::-1],  # maximum first
        [7] * 64,  # every comparison a tie
        # The unsorted cases are the ones doing the work here, and it is worth
        # knowing why: on input that is already sorted, reverse-sorted, or all
        # equal, `sorted()` also performs exactly n - 1 comparisons, because
        # Timsort finds one run and stops. Tidy inputs cannot tell a single pass
        # apart from a sort. These two can.
        [(i * 37 + 11) % 101 for i in range(64)],
        [(i * 7919 + 13) % 4093 for i in range(512)],
    ],
)
def test_performs_exactly_n_minus_one_real_comparisons(values: list[int]) -> None:
    """Not the number you report -- the number you actually perform."""
    log = [0]
    wrapped = [Counted(v, log) for v in values]

    largest, reported = implement(wrapped)

    assert log[0] == len(values) - 1, (
        f"performed {log[0]} comparisons on {len(values)} elements; the contract "
        f"is exactly {len(values) - 1}. Sorting costs about n log n and checking "
        f"every pair costs n squared -- both give the right answer and fail here."
    )
    assert reported == len(values) - 1, "the count you report disagrees with the count you made"
    assert largest == reference(values)[0]


def test_comparison_count_does_not_depend_on_the_data() -> None:
    """The claim from section 7 of part 2.1: this procedure is oblivious."""
    counts = {implement(xs)[1] for xs in ([1, 2, 3, 4], [4, 3, 2, 1], [2, 2, 2, 2])}
    assert counts == {3}


def test_empty_list_raises() -> None:
    with pytest.raises(ValueError, match="empty sequence"):
        implement([])


def test_large_input_still_costs_exactly_n_minus_one() -> None:
    """One size up, to catch anything that is linear only for small n.

    If this test seems to hang rather than fail, your procedure is quadratic and
    the comparison-count test above has already said so in one line. Read that
    failure, not this one.
    """
    xs = list(range(20_000))
    assert implement(xs) == (19_999, 19_999)
