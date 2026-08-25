"""Day 3 — property-based tests against the oracle, plus the postcondition, checked directly.

The suite skips while `implement.py` is still a stub, so a freshly cloned repo
is green. It wakes up the moment you write your first line.

Three kinds of test, deliberately different kinds.

`test_matches_reference` compares against the literal transcription of the
definition in reference.py. `test_postcondition_holds` checks the two halves of
the contract on your answer alone -- the suffix really holds, and the index
really is the smallest -- so that a failure names which half broke instead of
only reporting that two numbers differ. `test_reads_each_table_a_bounded_number
_of_times` is the cost test: it hands you lists that count their own element
reads, and fails a quadratic solution without waiting for one to finish.
"""

from typing import Any

import pytest
from hypothesis import given
from hypothesis import strategies as st
from implement import dominates_from as implement
from reference import dominates_from as reference


class CountingList(list):
    """A list that records how many elements were read out of it."""

    def __init__(self, values: list[int], log: list[int]) -> None:
        super().__init__(values)
        self.log = log

    def __getitem__(self, index: Any) -> Any:
        self.log[0] += 1
        return super().__getitem__(index)


def _is_still_a_stub() -> bool:
    try:
        implement([1], [1], 1)
    except NotImplementedError:
        return True
    except Exception:  # noqa: BLE001 -- any other failure is a real failure, not a stub
        return False
    return False


pytestmark = pytest.mark.skipif(
    _is_still_a_stub(),
    reason="implement.py is still a stub -- write it, and this suite wakes up",
)

_tables = st.lists(
    st.tuples(st.integers(min_value=0, max_value=40), st.integers(min_value=0, max_value=40)),
    max_size=60,
)


@given(_tables, st.integers(min_value=0, max_value=4))
def test_matches_reference(pairs: list[tuple[int, int]], c: int) -> None:
    f = [a for a, _ in pairs]
    g = [b for _, b in pairs]
    assert implement(f, g, c) == reference(f, g, c)


@given(_tables, st.integers(min_value=0, max_value=4))
def test_postcondition_holds(pairs: list[tuple[int, int]], c: int) -> None:
    """The claim, not the answer: the suffix holds, and the index is the smallest."""
    f = [a for a, _ in pairs]
    g = [b for _, b in pairs]
    n0 = implement(f, g, c)

    if n0 is None:
        assert f, "None on empty tables: the empty suffix holds vacuously, so 0 is the answer"
        assert f[-1] > c * g[-1], "returned None while the last entry satisfies the inequality"
        return

    assert 0 <= n0 <= len(f)
    for i in range(n0, len(f)):
        assert f[i] <= c * g[i], f"claimed n0={n0} but index {i} of the suffix violates it"
    if n0 > 0:
        assert f[n0 - 1] > c * g[n0 - 1], (
            f"n0={n0} is not the smallest: index {n0 - 1} also satisfies the inequality, "
            f"so the whole suffix from there holds too"
        )


@pytest.mark.parametrize(
    ("f", "g", "c", "expected"),
    [
        ([], [], 1, 0),  # empty: the empty suffix holds vacuously
        ([5], [5], 1, 0),  # single element, holds
        ([6], [5], 1, None),  # single element, violates: no suffix can escape it
        ([1, 1, 1], [1, 1, 1], 1, 0),  # holds everywhere
        ([9, 9, 9], [1, 1, 1], 1, None),  # violates everywhere
        ([9, 1, 1], [1, 1, 1], 1, 1),  # one violation, at the front
        ([1, 1, 9], [1, 1, 1], 1, None),  # one violation, at the very end
        ([1, 9, 1], [1, 1, 1], 1, 2),  # a violation in the middle
        ([9, 1, 9, 1], [1, 1, 1, 1], 1, 3),  # the *last* violation is what sets n0
        ([1, 9, 1, 1], [1, 1, 1, 1], 9, 0),  # a bigger c absorbs the spike
        ([0, 0], [0, 0], 0, 0),  # zeros on both sides: 0 <= 0 holds
        ([1, 0], [0, 0], 0, 1),  # g is zero, so only f == 0 can hold
        ([3, 2, 1], [1, 1, 1], 2, 1),  # boundary: 2 <= 2 holds, 3 <= 2 does not
    ],
)
def test_edge_battery(f: list[int], g: list[int], c: int, expected: int | None) -> None:
    assert implement(f, g, c) == expected


def test_unequal_lengths_raise() -> None:
    with pytest.raises(ValueError, match="equal length"):
        implement([1, 2, 3], [1, 2], 1)


@pytest.mark.parametrize("n", [1_000, 8_000])
def test_reads_each_table_a_bounded_number_of_times(n: int) -> None:
    """The cost, checked by counting reads rather than by waiting for a clock.

    A single pass touches each index a small fixed number of times, so the total
    is a small multiple of n. The oracle's re-check of every suffix is n(n+1)/2
    reads, which blows this budget by a factor of hundreds at n = 1000 -- and
    fails here in a fraction of a second instead of hanging bench.py.
    """
    log = [0]
    f = CountingList([1] * n, log)
    g = CountingList([1] * n, log)
    f[0]  # noqa: B018 -- one read, so the budget below is honest about the baseline
    baseline = log[0]

    implement(f, g, 1)

    reads = log[0] - baseline
    assert reads <= 6 * n, (
        f"read {reads} elements from tables of length {n}. A single pass over each "
        f"table is 2n; anything near n^2 means a suffix is being re-checked, which "
        f"is what reference.py does on purpose and your implementation must not."
    )


def test_large_input_is_answered() -> None:
    """One size up, with the answer known by construction."""
    n = 200_000
    f = [1] * n
    g = [1] * n
    f[n // 2] = 99  # a single violation, halfway
    assert implement(f, g, 1) == n // 2 + 1
