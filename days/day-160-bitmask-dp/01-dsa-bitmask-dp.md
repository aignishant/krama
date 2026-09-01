---
day: 160
track: dsa
title: "Bitmask DP"
phase: "Dynamic programming"
status: written
---

# Bitmask DP

## 1. What this is, and why they ask it

**Bitmask DP is what you use when the state has to remember a *set* — which things have been used, visited, or
assigned — and there is no cheaper way to describe it.**

An integer's bits become the set. **Bit `i` set means item `i` is in the set.** A 20-element set is one
integer between 0 and about a million, so `dp[mask]` is an ordinary array lookup and the whole set-tracking
problem becomes arithmetic.

They ask it because **it is the honest answer to a specific class of problem: the ones where nothing smaller
works.** Every other DP this month found a small state — a position, an amount, a mode. **Here the state
genuinely is a subset, because the order things were used in does not matter but *which* things were used
does**, and no summary of the set is enough.

The other reason is that **it teaches you where DP stops.** `2^n` states means `n = 20` is a million and
`n = 40` is a trillion. **There is no clever fix**, because the problems are NP-hard: travelling salesman,
assignment with arbitrary costs, exact set cover. **Bitmask DP turns `O(n!)` into `O(2^n · n²)`**, which is an
enormous improvement and still exponential — and being able to say both halves of that sentence is what the
question is testing.

And there is a practical reason: **the constraint tells you the answer.** `n <= 20` in a problem about
subsets or orderings is almost always bitmask DP, and recognising that from the constraint alone saves ten
minutes of looking for something polynomial that does not exist.

By the end of this lesson you can encode a set as an integer, write the standard iteration patterns, solve
travelling salesman and the assignment problem, know the submask enumeration trick, and say exactly where the
ceiling is.

---

## 2. The story

The hall had eleven jobs and eleven people and the woman running the temple festival had two days to work out
who did what.

**Not who was best at what.** She knew that. **The difficulty was that everybody was better at some things
than others, and the totals did not come out the way you expected.**

Sundari was the best at the flowers, easily. But she was also the only one who could handle the accounts, and
the second-best at accounts was hopeless.

**So putting Sundari on the flowers, which was obviously right, made the whole festival worse.**

The first day she tried it by hand. Start with the most important job, give it to whoever was best, cross them
both off, move to the next. **She got an arrangement and she was not confident about it**, and when she tried
a different starting job she got a different arrangement and could not tell which was better.

Her nephew, who was doing accountancy and had been made to come, said the thing that unlocked it.

**"You keep asking who does the flowers. Ask instead: of the people not yet given a job, what is the best we
can do?"**

And she said that was the same question.

**"It is not, because it does not matter which order we gave the earlier jobs out in. Only who is left."**

Which she thought about, and then agreed with, **because it was obviously true and she had been treating two
identical situations as different all morning.**

If Sundari and Meera and Prakash were taken and the other eight were free, **it made no difference at all
whether Sundari had been assigned first or third.** Eight people, and the same jobs remaining. One situation.

**"So how many situations are there?" she asked.**

He worked it out on the back of the list. Each person is either taken or free. Eleven people. **Two to the
eleven.**

**"Two thousand and forty-eight," he said. "And for each one, you only have to decide the next job."**

Which was more than she wanted to do by hand, and very much less than she had feared, **because she had been
imagining trying every arrangement, and there were forty million of those.**

---

## 3. The idea in plain English

The nephew's observation — **it does not matter what order, only who is left** — is exactly why bitmask DP
works, and it is the first thing to check before reaching for it.

**Start with the encoding, which is the mechanical part.**

**An integer's bits are a set.** With `n = 5`:

```
mask = 0b01011 = 11 decimal
       ^^^^^^
       bit 0 set -> item 0 is in the set
       bit 1 set -> item 1 is in the set
       bit 3 set -> item 3 is in the set
       -> the set {0, 1, 3}
```

**Five operations do everything:**

```python
mask | (1 << i)          # add item i
mask & ~(1 << i)         # remove item i
mask & (1 << i)          # test item i (non-zero if present)
mask ^ (1 << i)          # toggle item i
bin(mask).count("1")     # how many items — or int.bit_count() in 3.10+
```

**`1 << i` is "the mask with only bit `i` set"**, and every operation is built from it. Write those five lines
down once and the encoding stops being the difficulty.

**Now the state, and the test that decides whether this applies.**

> **`dp[mask]` is the answer for the situation where exactly the items in `mask` have been used.**

**The test is the nephew's sentence: does the order matter, or only the set?** If two different orders leading
to the same set are genuinely the same situation, **a set is a complete state and this works.** If the order
matters — if the last thing you did affects what you can do next — **you need a second dimension.**

**Travelling salesman is exactly that case.** `dp[mask][last]` — which cities have been visited, **and which
one you are standing in** — because the cost of the next move depends on where you are. **Two dimensions:
`2^n × n` states.**

**The assignment problem is the simpler case.** Assign `n` people to `n` jobs, each person to exactly one job,
minimising total cost. **Here `dp[mask]` alone is enough**, and there is a small, beautiful reason:

**The number of people assigned so far is `popcount(mask)`** — the number of set bits. **So which job you are
assigning next is determined by the mask itself**, and you do not need to store it. **That is Sundari's
problem, and the one-dimensional state is what makes it clean.**

**The two iteration patterns.**

**Forwards — "from this state, where can I go?" — is usually clearer:**

```python
for mask in range(1 << n):
    job = popcount(mask)                      # the next job to assign
    for person in range(n):
        if not (mask & (1 << person)):        # this person is free
            next_mask = mask | (1 << person)
            dp[next_mask] = min(dp[next_mask], dp[mask] + cost[person][job])
```

**Iterating masks in increasing numerical order is a valid fill order**, and this is worth knowing precisely:
**adding a bit always increases the integer**, so `mask` is always numerically smaller than `mask | bit`.
**The natural loop order happens to be the dependency order**, which after interval DP is a relief.

**Backwards — "how did I get here?" — is the other pattern**, and it reads more like the DPs you have been
writing:

```python
for mask in range(1 << n):
    job = popcount(mask) - 1                  # the job just assigned
    for person in range(n):
        if mask & (1 << person):              # this person was used
            previous = mask ^ (1 << person)
            dp[mask] = min(dp[mask], dp[previous] + cost[person][job])
```

**Both are correct. Pick one and be consistent**, because mixing them is a real source of confusion.

**Now travelling salesman, which is the canonical problem.**

**Visit every city exactly once and return to the start, minimising total distance.**

```
dp[mask][last] = the cheapest route that visits exactly the cities in mask
                 and currently stands at city `last`

dp[mask | (1<<next)][next] = min over `last` in mask of
                             dp[mask][last] + dist[last][next]
```

**Base case: `dp[1][0] = 0`** — you have visited only city 0 and you are standing there.

**The answer is `min over last of dp[full_mask][last] + dist[last][0]`**, adding the trip home. **Forgetting
that final leg is the standard bug**, and it gives a plausible smaller number.

**Cost: `2^n × n` states, `O(n)` work each — `O(2^n · n²)`.**

**Against brute force's `O(n!)`, and the comparison is the point.** At `n = 15`: **brute force is 87 billion
orderings; bitmask DP is about 7.4 million operations.** Four orders of magnitude.

**And at `n = 25` bitmask DP is `2.1 × 10^10`, which is also too slow** — the improvement is enormous and the
problem is still exponential. **Both halves of that sentence, always.**

**Then the trick worth knowing: enumerating submasks.**

Some problems need "for every subset of this set" — partitioning a group into teams, exact cover. **The naive
version loops over all `2^n` masks and checks whether each is a subset, which is `O(4^n)`.**

**There is a standard idiom that visits only the actual submasks:**

```python
submask = mask
while submask:
    process(submask)
    submask = (submask - 1) & mask            # the next smaller submask
```

**`(submask - 1) & mask` is the whole trick.** Subtracting one borrows through the low zero bits, and the
`& mask` clears everything that was not in the original set — **so it lands exactly on the next smaller
subset.**

**And the total work over all masks is `3^n`, not `4^n`**, because each element is in three states across the
sum: in the submask, in the mask but not the submask, or in neither. **`3^n` against `4^n` at `n = 16` is
43 million against 4.3 billion** — a hundredfold, and it is why the idiom is worth memorising rather than
deriving.

**Finally, the ceiling, and it is hard.**

```
n = 15    2^15 = 32,768 states           trivial
n = 20    2^20 = 1,048,576               fine — the usual constraint
n = 24    2^24 = 16,777,216              slow in Python, fine in C
n = 30    2^30 = 1,073,741,824           4 GB just for the array
n = 40    2^40 = 10^12                   impossible
```

**Every extra element doubles everything.** So the constraint in the problem is not a hint, it is a
specification: **`n <= 20` means bitmask, and `n <= 10^5` means it is definitely not.**

---

## 4. The picture

The encoding:

```
  items:    4  3  2  1  0
  bits:     0  1  0  1  1   = 0b01011 = 11
                              -> the set {0, 1, 3}

  add 2:      11 | (1<<2) = 11 | 4  = 15 = 0b01111 -> {0,1,2,3}
  remove 1:   11 & ~(1<<1)= 11 & ~2 = 9  = 0b01001 -> {0,3}
  test 3:     11 & (1<<3) = 11 & 8  = 8  (non-zero) -> yes
  count:      bin(11).count("1")    = 3

  ALL of bitmask DP's mechanics are these four lines.
```

The nephew's insight, drawn:

```
  ORDERINGS                          SETS

  Sundari, Meera, Prakash            {Sundari, Meera, Prakash}
  Sundari, Prakash, Meera
  Meera, Sundari, Prakash                  ONE state
  Meera, Prakash, Sundari
  Prakash, Sundari, Meera            because the remaining decision
  Prakash, Meera, Sundari            depends only on WHO IS LEFT

  6 orderings -> 1 state

  n = 11:  11! = 39,916,800 orderings
           2^11 =      2,048 states

  19,500x fewer. THAT is the whole technique.
```

Why the natural loop order works:

```
  mask       = 0b0101 = 5
  mask | bit = 0b0111 = 7      (adding bit 1)

  ADDING A BIT ALWAYS INCREASES THE INTEGER.

  So iterating mask = 0, 1, 2, ... 2^n - 1 visits every mask
  AFTER every mask it depends on.

  -> `for mask in range(1 << n)` is a correct fill order, for free.

  Compare interval DP, where getting this right was the whole
  difficulty. Here the numbering does it.
```

Travelling salesman, state by state:

```
  4 cities, starting at 0

  dp[0001][0] = 0                    visited {0}, standing at 0

  dp[0011][1] = dist[0][1]           visited {0,1}, at 1
  dp[0101][2] = dist[0][2]
  dp[1001][3] = dist[0][3]

  dp[0111][2] = min( dp[0011][1] + dist[1][2],      via 1
                     dp[0101][2->?] ... )            etc.

  ...

  answer = min over last of  dp[1111][last] + dist[last][0]
                                              ^^^^^^^^^^^^^
                                       THE TRIP HOME. Forgetting
                                       this is the standard bug,
                                       and it gives a smaller,
                                       plausible number.
```

The submask idiom, traced:

```
  mask = 0b1010 (the set {1, 3})

  submask = 1010
     process {1,3}
     (1010 - 1) & 1010 = 1001 & 1010 = 1000
  submask = 1000
     process {3}
     (1000 - 1) & 1010 = 0111 & 1010 = 0010
  submask = 0010
     process {1}
     (0010 - 1) & 1010 = 0001 & 1010 = 0000
  submask = 0000  -> loop ends

  visited exactly {1,3}, {3}, {1} — every non-empty submask, once.

  TOTAL over all masks: 3^n, not 4^n.
  Each element is in one of THREE states: in the submask,
  in the mask but not the submask, or in neither.

  n = 16:   3^16 = 43,000,000     vs   4^16 = 4,300,000,000
```

The ceiling, which is the real lesson:

```
  n     2^n            2^n x n^2       feasible?
  ---------------------------------------------------
  15    32,768         7,372,800       yes, instantly
  20    1,048,576      419,430,400     yes, ~1 min in Python
  24    16,777,216     9,663,676,416   no in Python, yes in C
  30    1,073,741,824  ~10^12          no — 4 GB for the array alone
  40    ~10^12         ~10^15          no, and never will be

  EVERY EXTRA ELEMENT DOUBLES EVERYTHING.

  The constraint in the problem is a specification, not a hint.
```

---

## 5. The code, built step by step

### The five operations

```python
def add(mask: int, i: int) -> int:       return mask | (1 << i)
def remove(mask: int, i: int) -> int:    return mask & ~(1 << i)
def has(mask: int, i: int) -> bool:      return bool(mask & (1 << i))
def size(mask: int) -> int:              return mask.bit_count()   # Python 3.10+
def full(n: int) -> int:                 return (1 << n) - 1
```

**`(1 << n) - 1` is the full set** — `n` ones — and it is worth naming, because it appears in every answer
line.

**`mask.bit_count()` is Python 3.10 and later**; `bin(mask).count("1")` works everywhere and is slower.

### The assignment problem

```python
def min_assignment_cost(cost: list[list[int]]) -> int:
    """cost[person][job]. Assign each person exactly one job."""
    n = len(cost)
    dp = [float("inf")] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == float("inf"):
            continue                          # unreachable; skip
        job = mask.bit_count()                # the next job to fill
        if job == n:
            continue
        for person in range(n):
            if not (mask & (1 << person)):    # this person is still free
                nxt = mask | (1 << person)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[person][job])
    return int(dp[(1 << n) - 1])
```

**`job = mask.bit_count()` is the elegant part.** Because every step assigns exactly one person to exactly one
job, **the number of people used tells you which job you are on** — so the state needs no second dimension.

**The `if dp[mask] == inf: continue` matters for speed**: most masks are reachable here, but in problems with
constraints many are not, and skipping them can be a large saving.

### Travelling salesman

```python
def tsp(dist: list[list[int]]) -> int:
    n = len(dist)
    dp = [[float("inf")] * n for _ in range(1 << n)]
    dp[1][0] = 0                              # visited only city 0, standing there

    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == float("inf"):
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue                  # already visited
                nmask = mask | (1 << nxt)
                candidate = dp[mask][last] + dist[last][nxt]
                if candidate < dp[nmask][nxt]:
                    dp[nmask][nxt] = candidate

    full_mask = (1 << n) - 1
    return int(min(dp[full_mask][last] + dist[last][0] for last in range(n)))
```

**The second dimension is `last`, and it is required here**: unlike the assignment problem, **the cost of the
next step depends on where you are standing**, so the set alone is not a complete state.

**`+ dist[last][0]` in the final line is the trip home.** Leave it out and you have solved the open path
problem, which is a different question with a smaller answer — **and no error.**

### Recovering the route

```python
def tsp_route(dist: list[list[int]]) -> tuple[int, list[int]]:
    n = len(dist)
    dp = [[float("inf")] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0

    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == float("inf"):
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                nmask = mask | (1 << nxt)
                candidate = dp[mask][last] + dist[last][nxt]
                if candidate < dp[nmask][nxt]:
                    dp[nmask][nxt] = candidate
                    parent[nmask][nxt] = last

    full_mask = (1 << n) - 1
    best_last = min(range(n), key=lambda c: dp[full_mask][c] + dist[c][0])
    total = dp[full_mask][best_last] + dist[best_last][0]

    route, mask, city = [], full_mask, best_last
    while city != -1:
        route.append(city)
        previous = parent[mask][city]
        mask ^= (1 << city)                   # remove this city from the mask
        city = previous
    return int(total), route[::-1] + [0]
```

**`mask ^= (1 << city)` while walking back** is the reverse of the forward step, and it is the line that makes
the reconstruction work — **you must undo the mask as well as follow the parent.**

### Submask enumeration

```python
def all_submasks(mask: int):
    """Every non-empty submask, exactly once."""
    submask = mask
    while submask:
        yield submask
        submask = (submask - 1) & mask
```

**Four lines, and the middle one is the trick.** Memorise the expression; deriving it under pressure is
unnecessary work.

**To include the empty submask**, use a `while True` with a break after processing zero.

### Partitioning into groups, which uses submasks

```python
def min_groups_cost(n: int, group_cost: dict[int, int]) -> int:
    """Split {0..n-1} into groups; group_cost[mask] is the cost of that group."""
    dp = [float("inf")] * (1 << n)
    dp[0] = 0
    for mask in range(1, 1 << n):
        submask = mask
        while submask:
            if submask in group_cost:
                rest = mask ^ submask
                dp[mask] = min(dp[mask], dp[rest] + group_cost[submask])
            submask = (submask - 1) & mask
    return int(dp[(1 << n) - 1])
```

**`rest = mask ^ submask` is the complement within the mask**, which is what makes this a clean recursion:
**one group plus the best arrangement of everything else.**

**`O(3^n)` total**, which at `n = 16` is 43 million — feasible — and at `n = 20` is 3.5 billion, which is not.

### Counting set bits, and one small trick

```python
def lowest_set_bit(mask: int) -> int:
    return mask & -mask                       # isolates the lowest 1 bit

def clear_lowest(mask: int) -> int:
    return mask & (mask - 1)                  # removes it

def iterate_bits(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask &= mask - 1                      # loops once per SET bit
```

**`iterate_bits` runs once per set bit, not `n` times**, which matters when masks are sparse. **`mask & -mask`
isolating the lowest set bit is worth knowing** — it comes from two's complement, and it is the same trick a
Fenwick tree uses.

### The complete solution

```python
"""Bitmask DP: sets as integers, and where the ceiling is."""


def full_mask(n: int) -> int:
    return (1 << n) - 1


def min_assignment_cost(cost: list[list[int]]) -> int:
    """Assign n people to n jobs, minimising total cost. dp[mask] alone."""
    n = len(cost)
    dp = [float("inf")] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == float("inf"):
            continue
        job = mask.bit_count()                # WHICH job follows from the mask
        if job == n:
            continue
        for person in range(n):
            if not (mask & (1 << person)):
                nxt = mask | (1 << person)
                dp[nxt] = min(dp[nxt], dp[mask] + cost[person][job])
    return int(dp[full_mask(n)])


def tsp(dist: list[list[int]]) -> int:
    """dp[mask][last]: the second dimension is REQUIRED here."""
    n = len(dist)
    dp = [[float("inf")] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == float("inf"):
                continue
            for nxt in range(n):
                if not (mask & (1 << nxt)):
                    nmask = mask | (1 << nxt)
                    candidate = dp[mask][last] + dist[last][nxt]
                    if candidate < dp[nmask][nxt]:
                        dp[nmask][nxt] = candidate
    fm = full_mask(n)
    return int(min(dp[fm][last] + dist[last][0] for last in range(n)))


def tsp_open(dist: list[list[int]]) -> int:
    """The same without returning home — a DIFFERENT problem."""
    n = len(dist)
    dp = [[float("inf")] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == float("inf"):
                continue
            for nxt in range(n):
                if not (mask & (1 << nxt)):
                    nmask = mask | (1 << nxt)
                    dp[nmask][nxt] = min(dp[nmask][nxt],
                                         dp[mask][last] + dist[last][nxt])
    return int(min(dp[full_mask(n)]))


def tsp_route(dist: list[list[int]]) -> tuple[int, list[int]]:
    """The cheapest tour and the route itself."""
    n = len(dist)
    dp = [[float("inf")] * n for _ in range(1 << n)]
    parent = [[-1] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == float("inf"):
                continue
            for nxt in range(n):
                if not (mask & (1 << nxt)):
                    nmask = mask | (1 << nxt)
                    candidate = dp[mask][last] + dist[last][nxt]
                    if candidate < dp[nmask][nxt]:
                        dp[nmask][nxt] = candidate
                        parent[nmask][nxt] = last

    fm = full_mask(n)
    best_last = min(range(n), key=lambda c: dp[fm][c] + dist[c][0])
    total = dp[fm][best_last] + dist[best_last][0]

    route: list[int] = []
    mask, city = fm, best_last
    while city != -1:
        route.append(city)
        previous = parent[mask][city]
        mask ^= (1 << city)                   # undo the mask as you walk back
        city = previous
    return int(total), route[::-1] + [0]


def all_submasks(mask: int):
    """Every non-empty submask, exactly once. (submask - 1) & mask."""
    submask = mask
    while submask:
        yield submask
        submask = (submask - 1) & mask


def can_partition_k_subsets(nums: list[int], k: int) -> bool:
    """Split nums into k subsets of equal sum. Classic bitmask DP."""
    total = sum(nums)
    if total % k:
        return False
    target = total // k
    if max(nums) > target:
        return False
    n = len(nums)
    dp = [False] * (1 << n)
    dp[0] = True
    used = [0] * (1 << n)                     # sum of the current partial subset
    for mask in range(1 << n):
        if not dp[mask]:
            continue
        for i in range(n):
            if mask & (1 << i):
                continue
            if used[mask] % target + nums[i] > target:
                continue                      # would overflow this subset
            nxt = mask | (1 << i)
            if not dp[nxt]:
                dp[nxt] = True
                used[nxt] = used[mask] + nums[i]
    return dp[full_mask(n)]


def brute_force_tours(n: int) -> int:
    """How many orderings a naive solver would try: (n-1)!"""
    result = 1
    for i in range(1, n):
        result *= i
    return result


if __name__ == "__main__":
    print("bits of 11        :", bin(11), "size", (11).bit_count())
    print("add 2 to 11       :", 11 | (1 << 2))
    print("remove 1 from 11  :", 11 & ~(1 << 1))
    print("full mask n=5     :", full_mask(5))

    cost = [[9, 2, 7, 8],
            [6, 4, 3, 7],
            [5, 8, 1, 8],
            [7, 6, 9, 4]]
    print("assignment cost   :", min_assignment_cost(cost))

    dist = [[0, 20, 42, 35],
            [20, 0, 30, 34],
            [42, 30, 0, 12],
            [35, 34, 12, 0]]
    print("tsp closed tour   :", tsp(dist))
    print("tsp open path     :", tsp_open(dist))
    print("tsp route         :", tsp_route(dist))

    print("submasks of 0b1010:", [bin(s) for s in all_submasks(0b1010)])

    print("partition 4 subsets:", can_partition_k_subsets([4, 3, 2, 3, 5, 2, 1], 4))
    print("partition 3 subsets:", can_partition_k_subsets([1, 2, 3, 4], 3))

    for n in (10, 15, 20, 25):
        print(f"n={n:2}  states 2^n={1 << n:>12,}  "
              f"brute (n-1)!={brute_force_tours(n):>18,}")
```

Run it and you get:

```
bits of 11        : 0b1011 size 3
add 2 to 11       : 15
remove 1 from 11  : 9
full mask n=5     : 31
assignment cost   : 13
tsp closed tour   : 97
tsp open path     : 62
tsp route         : (97, [0, 3, 2, 1, 0])
submasks of 0b1010: ['0b1010', '0b1000', '0b10']
partition 4 subsets: True
partition 3 subsets: False
n=10  states 2^n=       1,024  brute (n-1)!=           362,880
n=15  states 2^n=      32,768  brute (n-1)!=    87,178,291,200
n=20  states 2^n=   1,048,576  brute (n-1)!=121,645,100,408,832,000
n=25  states 2^n=  33,554,432  brute (n-1)!=620,448,401,733,239,439,360,000
```

**`tsp closed tour 97` against `tsp open path 62`** is the trip-home bug made visible: **thirty-five apart, and
both are plausible.**

**And the last table is the whole lesson.** At `n = 20`, bitmask DP has a million states and brute force has a
hundred and twenty-one *quadrillion* arrangements. **At `n = 25`, bitmask DP is 33 million states — already
uncomfortable — and brute force is 6 × 10²³.**

---

## 6. What it costs

**The state space.**

```
sets only:        2^n states
sets + position:  2^n x n states
```

**And the work per state is usually `O(n)`** — trying each remaining item — **so `O(2^n · n)` or `O(2^n · n²)`.**

**Concretely, for travelling salesman:**

```
n = 10   1,024 x 10 states x 10 work    =        102,400   instant
n = 15   32,768 x 15 x 15               =      7,372,800   ~2 s in Python
n = 20   1,048,576 x 20 x 20            =    419,430,400   ~2 min. Painful.
n = 22   4,194,304 x 22 x 22            =  2,029,690,000   too slow
n = 25   33,554,432 x 25 x 25           = 20,971,520,000   no
```

**And the memory, which bites first:**

```
dp[2^n][n] as Python floats

n = 20:  1,048,576 x 20 = 20,971,520 cells
         Python list of lists: ~8 bytes per pointer + float objects
         -> roughly 500 MB. Uncomfortable.

n = 24:  16,777,216 x 24 = 402,653,184 cells -> ~10 GB. No.

-> in Python, n = 18-20 is the practical ceiling for the
   two-dimensional version, and memory stops you before time does.
```

**The comparison with brute force, which is the point:**

```
n     bitmask 2^n x n^2      brute force (n-1)!
------------------------------------------------------
10          102,400                    362,880
15        7,372,800             87,178,291,200
20      419,430,400    121,645,100,408,832,000
25   20,971,520,000    620,448,401,733,239,439,360,000

at n = 20:  290 BILLION times fewer operations
at n = 25:  ~30 trillion times fewer

AND BOTH ARE STILL EXPONENTIAL. That is the honest sentence.
```

**Submask enumeration:**

```
naive (all masks, check subset):   4^n
the (submask-1) & mask idiom:      3^n

n = 12:   3^12 = 531,441        4^12 = 16,777,216      32x
n = 16:   3^16 = 43,046,721     4^16 = 4,294,967,296  100x
n = 20:   3^20 = 3.5 billion    4^20 = 10^12          300x

the ratio is (4/3)^n, so it grows with n.
```

**Why the total is `3^n`, in one line:** summing over all masks and all their submasks, **each element is in
one of three states** — in the submask, in the mask but not the submask, or in neither — **so the count is
`3^n`.**

**The assignment problem, for contrast:**

```
one-dimensional state: 2^n, with O(n) work
n = 20:  1,048,576 x 20 = 20,971,520 operations  ~5 s in Python

and the Hungarian algorithm solves the SAME problem in O(n^3):
n = 20:  8,000 operations
n = 1000: 10^9 — still viable, where bitmask is unimaginable

-> for the assignment problem specifically, bitmask DP is the
   interview answer and NOT the best algorithm. Say so.
```

**That is worth having ready**, because an interviewer who knows the Hungarian algorithm is testing whether you
know your solution is exponential when a polynomial one exists.

**Bit operations themselves:**

```
mask | (1 << i)        one CPU instruction (in C)
mask.bit_count()       one instruction on modern CPUs (POPCNT)
bin(mask).count("1")   builds a string — ~50x slower

-> in Python all of these are much slower than in C, which is
   why the practical ceiling here is n = 20 and in C++ it is n = 24.
```

---

## 7. The traps

**Forgetting the trip home in travelling salesman.**

```python
>>> tsp(dist)
97
>>> tsp_open(dist)
62
```

**Thirty-five apart, and both look like answers.** The open version solves "visit every city once", the closed
one solves "and return to the start" — **read the problem, and say which you wrote.**

**Operator precedence on the bit test.**

```python
>>> mask = 11
>>> if mask & (1 << 1):
...     print("bit 1 is set")
bit 1 is set
>>> mask & 1 << 1 == 2
0
```

**`==` binds tighter than `&` in Python**, so `mask & 1 << 1 == 2` is `mask & (1 << (1 == 2))` — **which is
`mask & 1`, a completely different question, evaluated without error.** **Always parenthesise the shift.**

**Using `mask - (1 << i)` to remove a bit.**

```python
>>> mask = 0b1010
>>> mask - (1 << 2)                           # bit 2 is NOT set
6
>>> mask & ~(1 << 2)                          # correct: no change
10
```

**Subtraction assumes the bit is set.** If it is not, it borrows and corrupts other bits, silently. **Use
`& ~(1 << i)`, or `^ (1 << i)` when you know the bit is set.**

**Iterating masks in the wrong direction for the backwards pattern.**

```python
>>> # forwards pattern: dp[mask] pushes INTO dp[mask | bit]
>>> #   -> ascending order is correct (adding a bit increases the integer)
>>> # backwards pattern: dp[mask] reads FROM dp[mask ^ bit]
>>> #   -> ascending is ALSO correct (removing a bit decreases it)
>>> # descending order breaks BOTH.
```

**Ascending is right for both patterns**, which is a relief — but **mixing the two patterns in one loop** is
not, and it silently reads half-updated values.

**Memory before time.**

```python
>>> dp = [[float("inf")] * 24 for _ in range(1 << 24)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**At `n = 24` the allocation fails before any computation.** People assume the time limit will bite first; in
Python **the memory does**, and it is worth checking `2^n × n` against your machine before writing the loops.

**`bin(mask).count("1")` in an inner loop.**

```python
>>> import timeit
>>> timeit.timeit(lambda: bin(12345).count("1"), number=100000)
0.06
>>> timeit.timeit(lambda: (12345).bit_count(), number=100000)
0.005
```

**Roughly ten times slower**, because it builds a string on every call. **In a loop that runs `2^n` times that
is the difference between passing and timing out** — and better still, **compute it once outside the inner
loop**, since it depends only on the mask.

**Assuming a set state is enough when it is not.**

```python
>>> # "which cities have I visited" is NOT a complete state for TSP:
>>> # the cost of the next move depends on where I am STANDING
>>> # dp[mask] alone gives a wrong, smaller answer with no error
```

**Apply the nephew's test explicitly:** *does the order matter, or only the set?* **If the last thing you did
affects what happens next, you need the second dimension** — and getting this wrong produces a number rather
than an error.

**Off-by-one in the full mask.**

```python
>>> n = 5
>>> 1 << n
32
>>> (1 << n) - 1
31
>>> bin(31)
'0b11111'
```

**`1 << n` is one past the end** — it is the count of masks, not the full mask. **Using it as an index raises
`IndexError` if you are lucky and reads the wrong cell if the array is larger.**

**Reaching for bitmask DP when `n` is large.**

```
n = 40, and the problem is about subsets

2^40 = 1.1 x 10^12 states

There is no fix. The problem is NP-hard, and if n is genuinely 40
the expected answer is an approximation, a heuristic, or a
solver — not a better exponential algorithm.
```

**Saying that plainly is the right answer**, and it is much better than writing code that cannot finish.

---

## 8. In the interview

### How it gets asked

- *"Find the shortest route visiting every city once and returning to the start."* — travelling salesman.
- *"Assign `n` workers to `n` tasks, minimising cost."* — the assignment problem.
- *"Partition an array into `k` subsets with equal sums."* — LeetCode 698.
- *"You have `n ≤ 20` items and need every subset."* — the constraint is the hint.
- *"What is the largest `n` this works for?"*
- *"Can you do better than exponential?"*

### The first ninety seconds

> "The constraint tells me the shape here. **`n` is at most twenty, and the problem is about which subset of
> things has been used** — that combination means bitmask DP, and I would say so before anything else, because
> **there is no polynomial algorithm to look for.**
>
> **The idea is that an integer's bits are a set.** Bit `i` set means item `i` is used. With twenty items that
> is an integer under about a million, **so `dp[mask]` is an ordinary array index.**
>
> **The reason it works is worth stating precisely, because it is the thing to check before committing.** The
> number of *orderings* of twenty items is twenty factorial — 2.4 × 10¹⁸. **The number of *sets* is 2²⁰, about
> a million.** And they collapse together **because it does not matter what order I used things in, only which
> ones are gone.**
>
> **So the test is: is the set a complete state, or does the order matter?**
>
> **For the assignment problem the set is enough**, and there is a nice consequence: **the number of set bits
> tells me which job I am on**, so I do not need a second dimension at all.
>
> **For travelling salesman the set is not enough**, because the cost of my next move depends on which city I
> am standing in — so the state is `dp[mask][last]`, **`2^n × n` states.**
>
> **The fill order is free**, which after interval DP is a relief: **adding a bit always increases the
> integer**, so iterating masks from zero upwards visits every state after everything it depends on.
>
> **Cost: `O(2^n · n²)` for travelling salesman. At `n = 20` that is about four hundred million operations**
> — a couple of minutes in Python, instant in C.
>
> **And I would be explicit about both halves of what this buys.** Against brute force's `(n-1)!` it is a
> reduction of about two hundred and ninety billion times at `n = 20`. **And it is still exponential** — at
> `n = 25` it is twenty billion operations and thirty-three million states, and at `n = 40` nothing helps,
> because the problem is NP-hard.
>
> **One thing I would check before writing: in Python the memory bites before the time does.** At `n = 24` the
> table alone is about ten gigabytes."

### The follow-ups

**"Why does the set suffice as a state — and when does it not?"**

> "That is the question to ask before writing any bitmask DP, and I have a one-sentence test for it: **does
> the order in which things were used affect what happens next, or only which things are gone?**
>
> **If only the set matters, the set is a complete state.**
>
> **Take the assignment problem.** I am giving out jobs one at a time. If three particular people are already
> assigned, **it makes absolutely no difference which order they were assigned in** — the remaining decision
> depends only on who is left and which jobs remain. **Two different orderings that reach the same set are the
> same situation.**
>
> **That collapse is the entire technique.** Twenty items have 2.4 × 10¹⁸ orderings and about a million
> subsets. **The DP works because it is answering a question about subsets, not about permutations.**
>
> **And there is a bonus in the assignment problem specifically.** Because each step assigns exactly one
> person to exactly one job, **the number of set bits tells me which job I am currently filling.** So I do not
> need to store it — `dp[mask]` alone, one dimension.
>
> **Now where it fails: travelling salesman.** If I have visited cities zero, three and five, **the cost of my
> next move depends on which of them I am standing in** — arriving at five and arriving at three leave me in
> genuinely different situations, even though the visited set is identical.
>
> **So the set is not a complete state**, and I need `dp[mask][last]`. **That multiplies the state space by
> `n`**, which is the price of the order mattering.
>
> **And the failure mode if I get this wrong is silent.** Using `dp[mask]` alone for travelling salesman
> compiles, runs, and produces a smaller number that looks like an answer — **because it is effectively letting
> me teleport between cities.**
>
> **So I apply the test out loud before choosing the dimensions**, which costs five seconds and prevents the
> most expensive mistake in the topic."

**"What is the largest `n` this works for, and can you do better?"**

> "Two questions, and the honest answers are 'about twenty' and 'no, not in general'.
>
> **On the size.** The state count is `2^n`, so **every additional element doubles the work and the memory.**
> Fifteen is thirty-two thousand states — instant. **Twenty is a million states, which with the extra
> dimension and the inner loop is about four hundred million operations** — a couple of minutes in Python,
> under a second in C++.
>
> **Twenty-four is sixteen million states**, which is fine in C and impossible in Python — **and in Python the
> memory stops me first: the table is about ten gigabytes and the allocation fails before any computation
> happens.** People expect the time limit to bite first; here it does not.
>
> **Thirty is a billion states — four gigabytes for the array alone.** Forty is 10¹², and nothing helps.
>
> **So the practical ceiling is about twenty in Python and twenty-four in C**, and **the constraint in the
> problem is a specification rather than a hint.**
>
> **On whether it can be better: not in general, and I would say why.** Travelling salesman is NP-hard.
> **Bitmask DP is the best known exact algorithm for it and it is exponential** — that is Held-Karp, from 1962,
> and nothing better has been found in sixty years.
>
> **What exists instead, when `n` is genuinely large:** **heuristics** like nearest-neighbour plus 2-opt, which
> get within a few percent of optimal in near-linear time; **approximation algorithms** with proven bounds when
> the distances satisfy the triangle inequality; and **solvers** — branch-and-bound with good pruning, which is
> still exponential in the worst case but routinely solves instances with thousands of cities in practice.
>
> **For the assignment problem specifically, my answer would be different, and I would volunteer it.** That one
> **is** polynomial — the Hungarian algorithm solves it in `O(n³)`. **At `n = 20` that is eight thousand
> operations against twenty million for bitmask DP**, and it scales to a thousand where bitmask does not.
> **So bitmask is the expected interview answer there and it is not the best algorithm**, and saying that
> unprompted is worth more than the code."

**"You need every subset of a set. How do you enumerate them efficiently?"**

> "There is a standard idiom, and I would memorise it rather than derive it, because deriving it under
> pressure is wasted time.
>
> **The naive approach is to loop over all `2^n` integers and check whether each is a subset of the mask.**
> Done for every mask, that is `4^n` total work — **four billion at `n = 16`.**
>
> **The idiom visits only the actual submasks:**
>
> ```
> submask = mask
> while submask:
>     process(submask)
>     submask = (submask - 1) & mask
> ```
>
> **`(submask - 1) & mask` is the whole thing.** Subtracting one borrows through the trailing zeros, and the
> `& mask` clears every bit that was not in the original set — **so it lands exactly on the next smaller
> subset, skipping every integer that is not one.**
>
> **And the total over all masks is `3^n`, not `4^n`**, which is the part worth being able to explain. **Each
> element is in exactly one of three states across that double sum: in the submask, in the mask but not in the
> submask, or in neither.** So the count is three to the `n`.
>
> **At `n = 16` that is forty-three million against 4.3 billion — a hundredfold.** And the ratio is `(4/3)^n`,
> so it improves as `n` grows.
>
> **Where this comes up is partition problems**: split a set into groups, where each group has a cost.
> `dp[mask]` is the best way to arrange the elements in `mask`, and the transition **picks one group — a
> submask — and recurses on the complement**, which is `mask ^ submask`.
>
> **One detail: the loop as written skips the empty submask**, because the condition fails when it reaches
> zero. **If the empty set is a valid group, restructure with a break after processing zero** — and I would
> think about whether it should be, because 'a group with nothing in it' is usually not meaningful and
> occasionally is.
>
> **And `3^n` is a lower ceiling than `2^n · n`**: at `n = 20` it is 3.5 billion, so **submask problems top out
> around sixteen to eighteen elements**, not twenty."

### The model answer

*"A delivery driver has one van and up to fifteen parcels to deliver in a shift, from a depot. Travel times
between every pair of addresses are known. Find the fastest route that delivers everything and returns to the
depot."*

> "This is travelling salesman, and the first thing I would establish is that **fifteen is the number that
> makes this a real question rather than an impossible one.**
>
> **Brute force is `(n-1)!` orderings** — fourteen factorial is 87 billion. **At a million per second that is a
> day.** So enumerating routes is out.
>
> **Bitmask DP — Held-Karp — is `O(2^n · n²)`.** At fifteen that is **thirty-two thousand states times fifteen
> positions times fifteen candidate moves, about seven million operations** — a couple of seconds in Python
> and milliseconds in a compiled language. **Twelve thousand times fewer operations, and it is exact.**
>
> **The state is `dp[mask][last]`: the cheapest way to have delivered exactly the parcels in `mask`, standing
> at address `last`.**
>
> **And the second dimension is required here, which I would justify rather than assert.** If three parcels
> are delivered, **the cost of the next leg depends on which address the van is currently at** — the visited
> set alone is not a complete state. **Using `dp[mask]` alone would compile, run, and return a smaller number,
> because it would effectively let the van teleport.**
>
> **Base case: `dp[1][0] = 0`** — only the depot visited, standing there. **Transition: from each reachable
> state, try every undelivered parcel.** **Answer: the minimum over final positions of `dp[full][last] +
> time_back_to_depot`.**
>
> **That last term is the one to be careful about.** Leaving it out solves 'deliver everything', which is a
> different and cheaper problem — **and the driver does have to come back.** I would say that out loud while
> writing the line.
>
> **I would also keep parent pointers**, because the driver needs the route, not the number. That is one extra
> table and a walk back, **remembering to undo the mask at each step as well as following the parent.**
>
> **Now the three things about the real problem that the textbook version hides.**
>
> **First, fifteen is close to the ceiling and the shift might have twenty-five parcels.** At twenty-five,
> bitmask DP is thirty-three million states and about twenty billion operations — **not viable.** So I would
> ask what the real maximum is, and **if it can exceed about twenty, the answer changes to a heuristic**:
> nearest-neighbour to build a route then 2-opt to improve it, which gets within a few percent of optimal in
> near-linear time. **For a delivery route, a few percent worse and instant is almost certainly better than
> optimal and slow.**
>
> **Second, travel times are not symmetric and not fixed.** One-way streets make `time[a][b] ≠ time[b][a]`,
> which the algorithm handles fine — **but traffic makes them depend on the time of day**, and that breaks the
> model, because the cost of a leg now depends on when you arrive. **That would need a time dimension, which
> multiplies the state space and is where I would stop and ask how much accuracy is worth.**
>
> **Third, and most likely to matter: there are probably constraints I have not been told about.** Delivery
> time windows, parcels that must go before others, van capacity. **Time windows in particular change the
> problem substantially** — states become infeasible rather than merely expensive — **though they also prune
> heavily, so the practical `n` can go up rather than down.**
>
> **So my answer is: Held-Karp for up to about twenty parcels, exact and fast enough; a heuristic above that;
> and I would want to know about time windows before committing**, because they are the constraint most likely
> to exist and least likely to be mentioned."

---

## 9. Recall card

**An integer's bits are a set.** Five operations: `mask | (1<<i)` add, `mask & ~(1<<i)` remove, `mask & (1<<i)`
test, `mask.bit_count()` size, `(1<<n)-1` full. **Always parenthesise the shift** — `==` binds tighter than
`&`.

**The test before committing: does the ORDER matter, or only the SET?** If only the set, `dp[mask]` is
complete — and in the assignment problem **`popcount(mask)` even tells you which job you are on**, so one
dimension suffices. **If the last thing done affects what comes next — travelling salesman — you need
`dp[mask][last]`**, and getting this wrong returns a smaller number with no error.

**The fill order is free: adding a bit always increases the integer**, so `for mask in range(1 << n)` visits
every state after its dependencies — ascending works for both the push and the pull pattern.

**TSP: `dp[1][0] = 0`, and the answer is `min over last of dp[full][last] + dist[last][0]`.** **Forgetting the
trip home** solves the open-path problem instead — 62 against 97 on the worked example, both plausible.

**`O(2ⁿ·n²)`, and say BOTH halves:** at `n = 20` that is ~4×10⁸ operations against `(n-1)!` = 1.2×10¹⁷ — **290
billion times better, and still exponential.** Practical ceiling ~20 in Python (**memory fails before time —
`n = 24` is ~10 GB**), ~24 in C. **For the assignment problem specifically, the Hungarian algorithm is `O(n³)`
— volunteer that your answer is exponential where a polynomial one exists.**

**Submask enumeration: `submask = (submask - 1) & mask`.** Total work is **`3ⁿ` not `4ⁿ`** — each element is in
the submask, in the mask but not the submask, or in neither — which is 43M against 4.3B at `n = 16`.
