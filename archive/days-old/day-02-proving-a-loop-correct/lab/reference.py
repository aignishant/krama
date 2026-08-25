"""Day 2 — the oracle. Brute force. Correct by inspection. Slow is fine.

The oracle is allowed everything today's lab forbids, which is the point of
having one: it names the answer with `divmod` rather than producing it, so
there is nowhere for a bug to hide, and it is therefore trustworthy in exactly
the way your implementation is not yet.

The iteration count is asserted rather than counted. A procedure that subtracts
b from a until what is left is smaller than b runs its body exactly a // b
times -- the variant starts at a, falls by b each pass, and stops below b. So
the oracle states that number as part of the contract.

That alone cannot catch an implementation that computes a // b directly and
*reports* it as an iteration count. Nothing about the returned values can. The
job of noticing that is done by reading your syntax tree, in
test_forbidden_shapes.py, which is the only instrument that can tell a procedure
from a claim about one.
"""


def divide(a: int, b: int) -> tuple[int, int, int]:
    """Return (a // b, a % b, a // b) for a >= 0, b >= 1. Raises otherwise."""
    if a < 0 or b < 1:
        raise ValueError("divide() requires a >= 0 and b >= 1")

    quotient, remainder = divmod(a, b)
    return quotient, remainder, quotient
