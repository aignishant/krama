"""Day 0 — property-based tests against the oracle, plus a real comparison count.

The whole suite skips while `implement.py` is still a stub, so that a freshly
cloned repo is green. It stops skipping the moment you write your first line,
and from then on it is allowed to go red -- which is the point of it.

Three kinds of test here, and they check three different things.

*Against the oracle.* Hypothesis invents lists and asserts your answer equals
reference.py's. That catches wrongness.

*Against the specification directly.* The post-condition has three clauses --
length, non-decreasing, prefix maximum -- and each gets its own assertion, so a
failure names which clause you broke rather than just "they differ".

*Against the procedure.* `Counted` elements keep their own tally of every
ordering comparison they take part in, and your function cannot see it. The
quadratic version returns exactly the right answer and fails that test, because
today the answer is not the whole contract: the cost is part of it too.
"""

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st
from implement import running_max as implement
from reference import running_max as reference


class Counted:
    """An integer that records every ordering comparison it takes part in.

    Equality does not tick: the contract counts ordering tests (`<`, `>`, `<=`,
    `>=`) between two elements. Comparison against something that is not an
    element -- a sentinel like -inf, an index, a length -- does not tick either.
    """

    __slots__ = ("log", "value")

    def __init__(self, value: int, log: list[int]) -> None:
        self.value = value
        self.log = log

    def _against(self, other: Any) -> Any:
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


@given(st.lists(st.integers()))
def test_matches_reference(xs: list[int]) -> None:
    assert implement(xs) == reference(xs)


@given(st.lists(st.integers(min_value=-3, max_value=3)))
def test_matches_reference_on_duplicate_heavy_input(xs: list[int]) -> None:
    """A tiny value range means ties everywhere -- where `>` versus `>=` shows up."""
    assert implement(xs) == reference(xs)


@given(st.lists(st.integers()))
def test_length_clause(xs: list[int]) -> None:
    assert len(implement(xs)) == len(xs)


@given(st.lists(st.integers()))
def test_non_decreasing_clause(xs: list[int]) -> None:
    result = implement(xs)
    for i in range(1, len(result)):
        assert result[i - 1] <= result[i], f"fell at index {i}: {result[i - 1]} then {result[i]}"


@given(st.lists(st.integers()))
def test_prefix_maximum_clause(xs: list[int]) -> None:
    result = implement(xs)
    for i, seen in enumerate(result):
        assert seen == max(
            xs[: i + 1]
        ), f"index {i} says {seen}, prefix maximum is {max(xs[: i + 1])}"


@given(st.lists(st.integers()))
def test_does_not_mutate_its_input(xs: list[int]) -> None:
    """O(1) auxiliary space is not a licence to scribble on the caller's list."""
    original = list(xs)
    implement(xs)
    assert xs == original


@pytest.mark.parametrize(
    "xs",
    [
        [],  # the pre-condition explicitly allows this one
        [0],  # single element
        [7, 7],  # a tie
        [1, 1, 1, 1, 1],  # all equal
        [1, 2, 3, 4, 5],  # already sorted: result equals the input
        [5, 4, 3, 2, 1],  # reverse sorted: result is [5, 5, 5, 5, 5]
        [-1, -2, -3],  # all negative -- kills a `best = 0` initialiser
        [-5, 0, 5],  # straddling zero
        [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5],  # maximum arrives in the middle
        [2**70, 2**70 - 1],  # wider than a machine word
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
        list(range(64)),  # a new maximum every step
        list(range(64))[::-1],  # the maximum arrives first and never moves
        [7] * 64,  # every comparison a tie
        [(i * 37 + 11) % 101 for i in range(64)],
        [(i * 7919 + 13) % 4093 for i in range(512)],
    ],
)
def test_performs_a_linear_number_of_comparisons(values: list[int]) -> None:
    """Not the answer -- the procedure. The quadratic version passes every test above."""
    log = [0]
    wrapped = [Counted(v, log) for v in values]

    result = implement(wrapped)

    n = len(values)
    assert log[0] <= n, (
        f"performed {log[0]} comparisons on {n} elements. A single pass needs "
        f"n - 1 = {n - 1}: one per element after the first. Re-reading the prefix "
        f"each step costs about n squared / 2 = {n * n // 2}, which is the shape "
        f"the build brief forbids."
    )
    assert [item.value if isinstance(item, Counted) else item for item in result] == reference(
        values
    )


def _looks_quadratic() -> bool:
    """A cheap probe, so the big test below refuses to run rather than hanging.

    A thousand elements is small enough that even the quadratic version answers
    in a moment, and a comparison count above 2n on that input is already proof
    of the wrong shape. If the probe says quadratic, the two-hundred-thousand
    element test would take minutes and tell you nothing the comparison-count
    test has not already told you in one line -- so it skips, and points at it.
    """
    if _is_still_a_stub():
        return False
    log = [0]
    try:
        implement([Counted(v, log) for v in range(1_000)])
    except Exception:  # noqa: BLE001 -- a broken function is not a slow function
        return False
    return log[0] > 2_000


@pytest.mark.skipif(
    _looks_quadratic(),
    reason="the comparison count already says this is quadratic -- read that failure",
)
def test_large_input_stays_linear() -> None:
    """One size up, to catch anything that is linear only for small n."""
    xs = list(range(200_000))
    assert implement(xs) == xs
    assert implement(xs[::-1]) == [199_999] * 200_000
