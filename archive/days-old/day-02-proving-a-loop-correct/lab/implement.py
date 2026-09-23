"""Day 2 — your implementation. You type every line."""


def divide(a: int, b: int) -> tuple[int, int, int]:
    """Divide by repeated subtraction. Return (quotient, remainder, iterations).

    This is the loop that every proof in this day is about, and it is small
    enough that you can hold the whole argument in your head while you write it.
    Before you type, write these two sentences down on paper:

        invariant: quotient * b + remainder == a, and remainder >= 0
        variant:   remainder -- a non-negative integer, strictly smaller after
                   every pass through the body

    Then write the loop so that each line discharges one of them, and be able to
    say which line does which.

    Pre:   a >= 0 and b >= 1. On anything else, raise
           ValueError("divide() requires a >= 0 and b >= 1").
    Post:  quotient * b + remainder == a, and 0 <= remainder < b.
           iterations == the number of times the loop body ran, which for this
           procedure is exactly the quotient -- the variant falls by b each
           time, from a down to the remainder.
    Time:  Theta(a / b) iterations. Note that this is linear in the *value* of
           a and therefore exponential in its size, which is the Day 1 trap
           (CPX-02) wearing a new hat. bench.py shows it.
    Space: Theta(1) auxiliary.

    Forbidden today: `//`, `%`, `divmod`, `math`, `round`, and `/`. Every one of
    them is a way of naming the answer instead of producing it, and
    test_forbidden_shapes.py reads this file's syntax tree to say so. You have
    `-`, `+`, `<`, `>` and a `while`. That is enough.

    Two things to do once it is green, both of which are the day's real work:

    1. Put `assert quotient * b + remainder == a` at the top of your loop, run
       the tests, and watch it pass on every iteration. Then move it to between
       the two statements in your body and watch it fail. Say out loud why the
       second placement proves nothing (part 1.1, section 3).
    2. Change your guard from `>=` to `>` and run the tests. Read the failure.
       That is a partial-correctness failure -- the loop stopped and lied.
       Then change it back, set b to 0 by hand, and read the other failure.
    """
    raise NotImplementedError
