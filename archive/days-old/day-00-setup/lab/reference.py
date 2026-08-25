"""Day 0 — the oracle. Brute force. Correct by inspection. Slow is fine.

This is the specification transcribed, nothing more. The post-condition says
`result[i] == max(xs[:i+1])`, so the oracle computes exactly that, for every i,
from nothing. It re-reads the whole prefix each time and remembers nothing
between iterations. There is nowhere in it for a bug to hide, which is the only
property an oracle needs -- and it is also, deliberately, the O(n^2) shape the
build brief forbids you from submitting.

Both facts are load-bearing today. As an oracle it decides whether your answer
is right. As a benchmark subject it is the *other* ratio column: the one that
climbs towards 4 while a single pass sits near 2. Day 0 is about seeing those
two columns next to each other, so the slow version has to exist somewhere.
It lives here, and not in implement.py, which is yours.

The cost, since this repo derives rather than asserts. Iteration i copies a
slice of i + 1 elements and scans it, so the work is proportional to i + 1.
Summed over i from 0 to n - 1 that is 1 + 2 + ... + n = n(n + 1)/2, which is
Theta(n^2). Doubling n multiplies n(n+1)/2 by roughly 4. That is where the 4
in the ratio column comes from, and it is arithmetic, not folklore.
"""


def running_max(xs: list[int]) -> list[int]:
    """Return [max(xs[:1]), max(xs[:2]), ..., max(xs[:n])]. Empty in, empty out."""
    result: list[int] = []
    for i in range(len(xs)):
        prefix = xs[: i + 1]
        largest = prefix[0]
        for value in prefix:
            if value > largest:
                largest = value
        result.append(largest)
    return result
