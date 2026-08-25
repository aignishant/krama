"""Day 2 — property-based tests against the oracle, plus the two obligations, checked.

The suite skips while `implement.py` is still a stub, so a freshly cloned repo
is green. It wakes up the moment you write your first line, and from then on it
is allowed to go red -- which is what it is for.

Three kinds of test here, and they are deliberately different kinds.

`test_matches_reference` is the ordinary one: same inputs, same answers as the
oracle. `test_invariant_holds_on_the_result` checks the invariant itself rather
than the answer -- quotient * b + remainder == a with 0 <= remainder < b -- so a
failure tells you which half of the claim broke instead of only that two tuples
differ. `test_terminates_on_the_hostile_shapes` is the termination obligation,
and it is the one that cannot fail politely: a loop with a broken variant does
not fail this test, it hangs it. Read the note above that test before you run it.
"""

import pytest
from hypothesis import given
from hypothesis import strategies as st
from implement import divide as implement
from reference import divide as reference


def _is_still_a_stub() -> bool:
    try:
        implement(7, 2)
    except NotImplementedError:
        return True
    except Exception:  # noqa: BLE001 -- any other failure is a real failure, not a stub
        return False
    return False


pytestmark = pytest.mark.skipif(
    _is_still_a_stub(),
    reason="implement.py is still a stub -- write it, and this suite wakes up",
)


@given(st.integers(min_value=0, max_value=5_000), st.integers(min_value=1, max_value=5_000))
def test_matches_reference(a: int, b: int) -> None:
    assert implement(a, b) == reference(a, b)


@given(st.integers(min_value=0, max_value=5_000), st.integers(min_value=1, max_value=5_000))
def test_invariant_holds_on_the_result(a: int, b: int) -> None:
    """The claim, not the answer: quotient * b + remainder == a, and 0 <= remainder < b."""
    quotient, remainder, _ = implement(a, b)
    assert quotient * b + remainder == a, "quotient * b + remainder != a -- the invariant is gone"
    assert remainder >= 0, "a negative remainder means the variant went below its floor"
    assert remainder < b, "remainder >= b means the guard let you stop too early"


@given(st.integers(min_value=1, max_value=200), st.integers(min_value=1, max_value=50))
def test_iteration_count_is_the_variant_falling(a: int, b: int) -> None:
    """The body runs once per subtraction: a falls to the remainder in steps of b."""
    quotient, _, iterations = implement(a, b)
    assert iterations == quotient, (
        f"reported {iterations} iterations for a quotient of {quotient}. The variant "
        f"starts at a, falls by exactly b each pass, and stops below b, so the body "
        f"runs exactly quotient times."
    )


@pytest.mark.parametrize(
    ("a", "b"),
    [
        (0, 1),  # zero iterations: the invariant is true before the loop and never touched
        (0, 7),  # same, with the guard false immediately
        (1, 1),  # one iteration, remainder 0
        (7, 7),  # a == b: exactly one subtraction, and the remainder lands on 0
        (6, 7),  # a < b: the loop never runs, and the answer is the input
        (12, 4),  # divides exactly -- the `>` vs `>=` guard bug shows up here
        (13, 4),  # does not divide exactly
        (100, 1),  # b == 1: the slowest shape per unit of a
        (999, 1000),  # one short of the divisor
        (1000, 999),  # one over
        (2**20, 2**10),  # exact power-of-two division, 1024 iterations
    ],
)
def test_edge_battery(a: int, b: int) -> None:
    assert implement(a, b) == reference(a, b)


@pytest.mark.parametrize(("a", "b"), [(-1, 1), (-5, 3), (5, 0), (5, -2), (0, 0), (-1, -1)])
def test_precondition_is_enforced(a: int, b: int) -> None:
    """The domain on which the variant is well-founded, refused at the door (2.1, section 6)."""
    with pytest.raises(ValueError, match="a >= 0 and b >= 1"):
        implement(a, b)


@pytest.mark.parametrize(("a", "b"), [(50_000, 1), (10**6, 999_983), (10**6, 10**6)])
def test_terminates_on_the_hostile_shapes(a: int, b: int) -> None:
    """The termination obligation.

    If this test appears to hang rather than fail, that is not the test being
    slow. It is your variant not decreasing -- press Ctrl-C, read which line the
    traceback names, and compare it with section 8 of part 2.1. The three cases
    are the ones where a guard written with `!=`, or a body that subtracts on
    only some branch, stops making progress: the longest run, the near-miss
    where a single subtraction is enough, and the exact hit where the remainder
    lands on zero.
    """
    assert implement(a, b) == reference(a, b)
