---
day: 154
track: dsa
title: "Edit distance"
phase: "Dynamic programming"
status: written
---

# Edit distance

## 1. What this is, and why they ask it

**How many single-character edits does it take to turn one string into another?** Insert a character, delete a
character, or replace a character. Each counts as one.

`"horse"` to `"ros"` takes 3: replace `h` with `r`, delete `r`, delete `e`. **That number is the edit
distance**, also called Levenshtein distance, and it is what spell-checkers, fuzzy search, DNA alignment and
"did you mean" all compute.

They ask it because **it is yesterday's table with three options instead of two**, and that step — from a
binary choice to a three-way `min` — is where two-dimensional DP stops being a pattern to copy and starts
being something you have to reason about. **Every one of the three options has to be named, and each maps onto
a real operation**, and a candidate who can say "this branch is a deletion, and here is why the index moves
that way" has understood it.

The other reason is that **the three operations are easy to mix up.** `dp[i-1][j]` is a deletion and
`dp[i][j-1]` is an insertion — or is it the other way round? **It depends entirely on which string you are
transforming into which**, and getting it backwards still gives the right *number*, because the distance is
symmetric. **So the bug is invisible until you try to reconstruct the actual edits**, which is exactly what the
follow-up asks for.

By the end of this lesson you can write the table and name all three branches, reconstruct the sequence of
edits, collapse the space, handle weighted operations, and explain where it is used and where it is too slow.

---

## 2. The story

The chemist had been reading handwriting for thirty-one years and he was very good at it, and this one had
him.

The paper said something like **"Ranitidin"**, or possibly **"Ranitidina"**, or — and this was the difficulty —
it could have been the beginning of a completely different word with a flourish at the end.

**What he did next was the thing he did without thinking about it, and had done thousands of times.**

He looked at the shelf.

There was *Ranitidine*. There was *Ranolazine*. There was *Ramipril*. And there was *Ranitidine* in the other
brand, spelled the same.

**And he compared, letter by letter, and counted how far off it was.**

*Ranitidin* against *Ranitidine* — **everything the same, one letter missing at the end.** One change.

*Ranitidin* against *Ranolazine* — R-a-n, then the paper had *i* and the box had *o*, then *t* against *l*,
and by the time he got to the end there were four or five places where they did not agree. **Too far.**

*Ranitidin* against *Ramipril* — the *n* against the *m*, and then it fell apart completely.

**So it was Ranitidine, and it took him about two seconds, and he had never once described what he was doing.**

His nephew, who had come to help during the holidays and was seventeen, asked how he could be sure, and he
said something that was more precise than he realised. **"Because to make the paper say Ranolazine I would
have to change four things. To make it say Ranitidine I only have to add an e."**

And then, because the nephew kept asking, he thought about it properly for the first time and added the part
that mattered.

**"And it is not just adding. Sometimes a letter is wrong and you swap it. Sometimes there is a letter that
should not be there and you take it out. Three things you can do, and you count how many you need."**

The nephew wrote it down, which the chemist thought was very funny.

---

## 3. The idea in plain English

The chemist's three things — swap a letter, add a letter, take one out — are the three operations, and his
count is the edit distance.

**The state is yesterday's, unchanged:**

> **`dp[i][j]` is the minimum number of edits to turn the first `i` characters of `a` into the first `j`
> characters of `b`.**

**Prefix lengths again**, so `i = 0` is the empty prefix and the character `i` refers to is `a[i-1]`. **Same
convention, same off-by-one, and the same reason for choosing it.**

**The base cases are different from LCS, and they are the more interesting ones.**

`dp[0][j] = j`: turning an empty string into `j` characters takes `j` **insertions**. `dp[i][0] = i`: turning
`i` characters into nothing takes `i` **deletions**.

**So the first row is `0, 1, 2, 3, ...` and the first column is the same going down** — not zeros. **This is
the most common mistake in the problem**, because LCS's base cases are zeros and the muscle memory carries
over.

**Now the recurrence, and it has two cases.**

**If the characters match** — `a[i-1] == b[j-1]` — **no edit is needed at this position at all.** Just carry
the cost forward diagonally:

```
dp[i][j] = dp[i-1][j-1]
```

**No `+ 1`.** That is the free move, and forgetting to make it free is the second most common bug.

**If they do not match, you must do one of three things**, and each costs one:

```
dp[i][j] = 1 + min( dp[i-1][j-1],    REPLACE  a[i-1] with b[j-1]
                    dp[i-1][j],      DELETE   a[i-1]
                    dp[i][j-1] )     INSERT   b[j-1]
```

**Naming each one and saying why the index moves that way is the whole lesson:**

**Replace.** You fix `a[i-1]` to become `b[j-1]`. **Both characters are now dealt with**, so both indices
retreat — the diagonal.

**Delete.** You throw away `a[i-1]`. **`b[j-1]` has not been handled yet**, so only `i` retreats: `dp[i-1][j]`.

**Insert.** You insert `b[j-1]` into `a`. **`a[i-1]` has not been handled yet**, so only `j` retreats:
`dp[i][j-1]`.

**Read those three out loud once and the direction stops being memorised.** The index that moves is the string
whose character you just consumed.

**The answer is `dp[n][m]`**, both strings fully transformed.

**And the direction matters for reconstruction and not for the number.** Edit distance is symmetric — turning
`a` into `b` costs the same as `b` into `a` — **so swapping which is which gives the same distance with
insertions and deletions exchanged.** That is why getting the branches backwards passes every test that only
checks the number.

**Three more things worth having ready.**

**Reconstruction.** Walk back from `dp[n][m]`. At each cell, ask which of the four possibilities produced this
value — match, replace, delete, insert — and emit the corresponding operation. **The result is the actual edit
script**, which is what a spell-checker or a diff tool needs.

**The space collapse.** Row `i` reads only row `i-1` and the cell to its left, so two rows suffice —
`O(min(n, m))` after swapping. **And reconstruction is gone**, same as yesterday.

**Weighted operations.** In the real world the three operations do not cost the same. **A spell-checker
weights a replacement between adjacent keyboard keys lower than between distant ones.** DNA alignment weights
a substitution differently from an insertion, because biologically they are not equally likely. **The
recurrence is unchanged; only the constants differ:**

```
dp[i][j] = min( dp[i-1][j-1] + cost_replace(a[i-1], b[j-1]),
                dp[i-1][j]   + cost_delete(a[i-1]),
                dp[i][j-1]   + cost_insert(b[j-1]) )
```

**And one variant worth naming: Damerau-Levenshtein adds a fourth operation, transposition** — swapping two
adjacent characters. `"hte"` to `"the"` is **one** transposition rather than two replacements, and since
transposition is one of the most common typing errors, spell-checkers use it.

**Finally, where this is actually used and where it stops.**

**Spell-check and "did you mean" are the obvious ones.** Fuzzy search — matching a query against a dictionary
within distance 2. **DNA sequence alignment**, where the strings are millions of characters and the weights
encode biology. **Plagiarism and diff tools**, where LCS and edit distance are two views of the same table.

**And the limit is `O(n × m)`.** Comparing a query against a hundred thousand dictionary words means a hundred
thousand tables. **The practical fix is not a faster algorithm; it is not running the algorithm** — a BK-tree
or a trie with pruning eliminates almost all candidates before any table is built, which is the answer to
"how does a real spell-checker do this".

---

## 4. The picture

The table for `a = "horse"`, `b = "ros"`:

```
            ""   r    o    s
       ""    0   1    2    3      <- base: j insertions
        h    1   1    2    3
        o    2   2    1    2
        r    3   2    2    2
        s    4   3    3    2
        e    5   4    4    3
        ^                    ^
    base: i deletions    answer = dp[5][3] = 3

  NOT zeros in row 0 and column 0. That is the difference from LCS,
  and it is the most common mistake in this problem.

  dp[2][2] = 1 means "turning 'ho' into 'ro' takes 1 edit" —
  replace the h with an r. Say it as a sentence and check it.
```

The three moves, drawn on one cell:

```
       dp[i-1][j-1] ------ dp[i-1][j]
            |    \              |
   REPLACE  |     \  (match:    | DELETE a[i-1]
   (diagonal)      \  free)     |
            |       \           |
            v        v          v
       dp[i][j-1] --------> dp[i][j]
                  INSERT b[j-1]

  MATCH      dp[i][j] = dp[i-1][j-1]           <- NO +1. Free.
  REPLACE    dp[i][j] = dp[i-1][j-1] + 1       both consumed -> diagonal
  DELETE     dp[i][j] = dp[i-1][j]   + 1       consumed a only -> i moves
  INSERT     dp[i][j] = dp[i][j-1]   + 1       consumed b only -> j moves

  RULE: the index that moves belongs to the string whose character
        you just used up.
```

The walk-back producing the actual edits:

```
  "horse" -> "ros", starting at dp[5][3] = 3

  dp[5][3]=3  a[4]='e' b[2]='s'  differ
              dp[4][3]=2 is the min -> DELETE 'e'      -> dp[4][3]
  dp[4][3]=2  a[3]='s' b[2]='s'  MATCH -> free         -> dp[3][2]
  dp[3][2]=2  a[2]='r' b[1]='o'  differ
              dp[2][2]=1 is the min -> DELETE 'r'      -> dp[2][2]
  dp[2][2]=1  a[1]='o' b[1]='o'  MATCH -> free         -> dp[1][1]
  dp[1][1]=1  a[0]='h' b[0]='r'  differ
              dp[0][0]=0 is the min -> REPLACE h->r    -> dp[0][0]
  dp[0][0]=0  STOP

  reversed:  replace h->r,  keep o,  delete r,  keep s,  delete e
             3 edits. Which is what dp[5][3] said.
```

Why getting the branches backwards is invisible:

```
  edit_distance("horse", "ros") = 3
  edit_distance("ros", "horse") = 3

  SYMMETRIC. So if you swap the delete and insert branches:

    the NUMBER is still correct on every test
    the RECONSTRUCTION reports insertions where deletions happened

  -> the bug survives every unit test that checks the distance
  -> it only appears when you ask WHAT the edits were

  That is why naming the branches out loud matters more here
  than anywhere else this week.
```

Edit distance against LCS, on the same table shape:

```
  same state, same two-dimensional prefix table

  LCS                          EDIT DISTANCE
  base: zeros                  base: 0,1,2,3,...
  match: dp[i-1][j-1] + 1      match: dp[i-1][j-1]        (free)
  else:  MAX of 2 neighbours   else:  1 + MIN of 3
  maximising                   minimising

  and they are related:
     if only insert and delete are allowed (no replace),
     distance = n + m - 2 x LCS(a, b)
```

---

## 5. The code, built step by step

### The base cases, which are the part people get wrong

```python
def edit_distance(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i                          # i deletions to reach ""
    for j in range(m + 1):
        dp[0][j] = j                          # j insertions from ""
    return dp[n][m]                           # (loops next)
```

**These two loops are not optional and they are not zeros.** Turning `"horse"` into `""` takes five deletions,
not zero. **Leaving them out gives an answer that is far too small and looks plausible.**

Now the recurrence:

```python
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]   # free — no +1
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],         # replace
                    dp[i - 1][j],             # delete a[i-1]
                    dp[i][j - 1],             # insert b[j-1]
                )
```

**The comments are the point.** Write them as you write the branches, and the delete/insert confusion cannot
happen.

### Reconstructing the edits

```python
def edit_script(a: str, b: str) -> list[str]:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])

    ops: list[str] = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append(f"keep   {a[i - 1]}")
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"replace {a[i - 1]} -> {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"delete {a[i - 1]}")
            i -= 1
        else:
            ops.append(f"insert {b[j - 1]}")
            j -= 1
    return list(reversed(ops))
```

**`while i > 0 or j > 0`, not `and`.** When one string runs out, the rest of the other is pure insertions or
pure deletions, and an `and` would stop early and lose them.

**The order of the `elif` branches decides which valid script you get** when several have the same cost — same
tie-break point as yesterday.

### The space collapse

```python
def edit_distance_two_rows(a: str, b: str) -> int:
    if len(b) > len(a):
        a, b = b, a                           # symmetric, so the swap is free
    previous = list(range(len(b) + 1))        # the base row: 0, 1, 2, ...
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)          # first cell of row i is i
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1]
            else:
                current[j] = 1 + min(previous[j - 1], previous[j], current[j - 1])
        previous = current
    return previous[len(b)]
```

**`current = [i] + ...` is the column base case**, and forgetting it is the classic bug in the collapsed
version — the first column silently stays zero and every answer is too small.

**The swap is free here because the distance is symmetric**, which is not true of every two-dimensional DP.

### Weighted operations

```python
def weighted_edit_distance(a: str, b: str, replace_cost, insert_cost, delete_cost) -> float:
    n, m = len(a), len(b)
    dp = [[0.0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0] = dp[i - 1][0] + delete_cost(a[i - 1])
    for j in range(1, m + 1):
        dp[0][j] = dp[0][j - 1] + insert_cost(b[j - 1])
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j - 1] + replace_cost(a[i - 1], b[j - 1]),
                    dp[i - 1][j] + delete_cost(a[i - 1]),
                    dp[i][j - 1] + insert_cost(b[j - 1]),
                )
    return dp[n][m]
```

**The base cases now accumulate costs rather than counting**, which is the change people miss when
generalising. **Everything else is identical.**

### Damerau-Levenshtein, with transposition

```python
def damerau_levenshtein(a: str, b: str) -> int:
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + cost, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
            if (i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]):
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)      # transposition
    return dp[n][m]
```

**The extra condition detects a swapped adjacent pair** and charges one instead of two. **`"hte"` to `"the"`
becomes 1**, which matters because that is one of the most common typing errors.

### The early exit that makes fuzzy search practical

```python
def within_distance(a: str, b: str, limit: int) -> bool:
    if abs(len(a) - len(b)) > limit:
        return False                          # length alone rules it out
    previous = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            current[j] = min(previous[j - 1] + cost, previous[j] + 1, current[j - 1] + 1)
        if min(current) > limit:
            return False                      # every path already exceeds the limit
        previous = current
    return previous[len(b)] <= limit
```

**Two early exits, and both matter for real use.** The length check is free and rejects most candidates
immediately. **And `min(current) > limit` stops mid-table**, because every remaining path can only get worse.

### The complete solution

```python
"""Edit distance: the three operations, reconstruction, and the variants."""


def edit_distance(a: str, b: str) -> int:
    """Minimum insert/delete/replace operations turning a into b."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i                          # i deletions
    for j in range(m + 1):
        dp[0][j] = j                          # j insertions
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]   # match: FREE, no +1
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j - 1],         # replace a[i-1] with b[j-1]
                    dp[i - 1][j],             # delete a[i-1]
                    dp[i][j - 1],             # insert b[j-1]
                )
    return dp[n][m]


def edit_script(a: str, b: str) -> list[str]:
    """The actual operations. Needs the full table."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])

    ops: list[str] = []
    i, j = n, m
    while i > 0 or j > 0:                     # OR, not AND
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append(f"keep    {a[i - 1]}")
            i, j = i - 1, j - 1
        elif i > 0 and j > 0 and dp[i][j] == dp[i - 1][j - 1] + 1:
            ops.append(f"replace {a[i - 1]} -> {b[j - 1]}")
            i, j = i - 1, j - 1
        elif i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            ops.append(f"delete  {a[i - 1]}")
            i -= 1
        else:
            ops.append(f"insert  {b[j - 1]}")
            j -= 1
    return list(reversed(ops))


def edit_distance_two_rows(a: str, b: str) -> int:
    """O(min(n, m)) space. The distance is symmetric, so the swap is free."""
    if len(b) > len(a):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)          # column base case — easy to forget
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1]
            else:
                current[j] = 1 + min(previous[j - 1], previous[j], current[j - 1])
        previous = current
    return previous[len(b)]


def damerau_levenshtein(a: str, b: str) -> int:
    """Adds transposition of adjacent characters as a fourth operation."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j - 1] + cost, dp[i - 1][j] + 1, dp[i][j - 1] + 1)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                dp[i][j] = min(dp[i][j], dp[i - 2][j - 2] + 1)
    return dp[n][m]


def within_distance(a: str, b: str, limit: int) -> bool:
    """Fuzzy matching with two early exits. This is what makes search practical."""
    if abs(len(a) - len(b)) > limit:
        return False
    previous = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        current = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            current[j] = min(previous[j - 1] + cost, previous[j] + 1, current[j - 1] + 1)
        if min(current) > limit:
            return False                      # every remaining path exceeds it
        previous = current
    return previous[len(b)] <= limit


def suggest(word: str, dictionary: list[str], limit: int = 2) -> list[str]:
    """A tiny spell-checker. Real ones prune before computing anything."""
    return sorted((w for w in dictionary if within_distance(word, w, limit)),
                  key=lambda w: edit_distance(word, w))


if __name__ == "__main__":
    print("horse -> ros    :", edit_distance("horse", "ros"))
    print("intention -> exe:", edit_distance("intention", "execution"))
    print("two rows agrees :", edit_distance_two_rows("horse", "ros"))
    print("symmetric       :", edit_distance("ros", "horse"))
    print("identical       :", edit_distance("abc", "abc"))
    print("empty to abc    :", edit_distance("", "abc"))
    print("abc to empty    :", edit_distance("abc", ""))

    print("script horse->ros:")
    for op in edit_script("horse", "ros"):
        print("   ", op)

    print("hte -> the (lev):", edit_distance("hte", "the"))
    print("hte -> the (dam):", damerau_levenshtein("hte", "the"))

    words = ["ranitidine", "ranolazine", "ramipril", "rantidine", "ranitidin"]
    print("suggest 'ranitidin':", suggest("ranitidin", words, limit=2))
    print("within 1?          :", within_distance("ranitidin", "ranolazine", 1))
```

Run it and you get:

```
horse -> ros    : 3
intention -> exe: 5
two rows agrees : 3
symmetric       : 3
identical       : 0
empty to abc    : 3
abc to empty    : 3
script horse->ros:
    replace h -> r
    keep    o
    delete  r
    keep    s
    delete  e
hte -> the (lev): 2
hte -> the (dam): 1
suggest 'ranitidin': ['ranitidin', 'ranitidine', 'rantidine']
within 1?          : False
```

**`hte -> the` giving 2 and then 1** is the transposition, made visible — and it is the single most common
typing error, which is why spell-checkers use Damerau.

**And the suggestion list is the chemist's shelf**: `ranolazine` and `ramipril` are more than two edits away
and never appear.

---

## 6. What it costs

**Time.** Two nested loops, three comparisons per cell.

```
n rows x m columns = n x m cells
each cell: one comparison, and a min of three     O(1)

TOTAL: O(n x m)
```

**Concretely:**

```
two words of 10             100 cells             instant
two strings of 1,000        1,000,000 cells       ~0.4 s in Python
two strings of 10,000       100,000,000 cells     ~50 s
two DNA sequences of 10^6   10^12 cells           impossible
```

**LeetCode 72's constraint is 500 characters**, so 250,000 cells — set exactly so the plain table passes.

**Space.**

```
full table    (n+1) x (m+1)
              501 x 501 = 251,001 cells        ~10 MB in Python

two rows      2 x (min(n,m) + 1)
              2 x 501 = 1,002 cells            ~40 KB

250x less. And no reconstruction.
```

**The swap, which is worth one `if`:**

```
a = 10,000 characters, b = 5 characters

no swap:  rows of length 6 either way — actually fine here
BUT the ROW COUNT is what iterates:
  without swap: 10,000 iterations of a 6-cell row
  with swap:    5 iterations of a 10,001-cell row

Both are 60,000 cells. The swap does not change the TIME.
It changes the SPACE: rows of 6 vs rows of 10,001.
-> keep the SHORTER string as the inner dimension.
```

**Where spell-checking falls over, which is the real lesson:**

```
dictionary of 100,000 words, average length 8
one query of length 8

brute force: 100,000 tables of 9 x 9 = 8,100,000 cells
             ~3 seconds per keystroke. Unusable.

with the length filter (|len(a) - len(b)| > 2 rejects immediately):
             ~30% survive -> 1 second. Still unusable.

with a BK-TREE or a TRIE with pruning:
             ~100-1,000 candidates examined
             ~0.001 seconds. Usable.

The fix is not a faster edit distance. It is not computing it.
```

**That is the most useful thing in this section**, and it is the answer to "how does a real spell-checker work".

**Damerau's extra cost:**

```
one extra comparison and one extra min per cell
-> ~20% slower, same O(n x m)

and it catches the most common human typing error, which is
a trade almost every spell-checker takes.
```

**The early exit, measured:**

```
comparing "ranitidin" against 100,000 words with limit 2

length filter alone:        rejects ~70,000 instantly
min(current) > limit:       aborts most of the rest after 2-3 rows
                            instead of all 9

-> roughly 10-20x faster than computing every full table,
   for the same answers.
```

---

## 7. The traps

**Zero base cases, carried over from LCS.**

```python
>>> a, b = "horse", "ros"
>>> dp = [[0] * 4 for _ in range(6)]          # all zeros — no base case loops
>>> for i in range(1, 6):
...     for j in range(1, 4):
...         if a[i-1] == b[j-1]:
...             dp[i][j] = dp[i-1][j-1]
...         else:
...             dp[i][j] = 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1])
>>> dp[5][3]
2
```

**Two, when the answer is three.** The table thinks turning `"horse"` into `""` is free, so everything
downstream is too cheap. **No error, and a small plausible number** — which is the worst kind of wrong.

**Adding one on a match.**

```python
>>> # in the match branch:
>>> #   dp[i][j] = dp[i-1][j-1] + 1     WRONG
>>> # gives edit_distance("abc", "abc") = 3
```

**Three edits to turn a string into itself.** Matching is free — that is the whole point of matching — and the
`+ 1` belongs only in the mismatch branch.

**Swapping delete and insert, which no test catches.**

```python
>>> edit_distance("horse", "ros")
3
>>> edit_distance("ros", "horse")
3
```

**The distance is symmetric**, so exchanging the two branches gives the correct number every time. **The bug
only shows in the edit script**, which will say "insert" where a deletion happened. **Name the branches in
comments as you write them** — it costs three seconds and it is the only defence.

**`while i > 0 and j > 0` in the walk-back.**

```python
>>> # with `and`, reconstructing "" -> "abc":
>>> # the loop never runs, and the script is empty
>>> # when it should be three insertions
```

**Use `or`.** When one string is exhausted, everything remaining in the other is a run of pure insertions or
pure deletions, and `and` silently drops them.

**Forgetting the column base in the collapsed version.**

```python
>>> previous = list(range(4))
>>> current = [0] * 4                         # should be [i, 0, 0, 0]
```

**The first cell of each row is `i`, not zero.** Leaving it as zero means "turning the first `i` characters
into an empty string is free", and the answers come out too small — **the same failure as the missing base
row, hidden inside the optimisation.**

**Unicode, which is a real-world trap rather than an interview one.**

```python
>>> len("é")
1
>>> len("é")          # e followed by a combining accent
2
>>> edit_distance("é", "é")
1
```

**Two strings that look identical and are two different sequences of code points.** Normalise with
`unicodedata.normalize("NFC", s)` before comparing, or every accented word is reported as a near-miss.

**Very long strings.**

```python
>>> dp = [[0] * 100001 for _ in range(100001)]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
MemoryError
```

**Ten billion cells.** For DNA-scale inputs the answer is not more memory — it is a banded algorithm that only
fills cells near the diagonal, valid when you only care about distances below a threshold.

**Comparing against a whole dictionary in a loop.**

```
100,000 words x one table each = ~3 seconds per keystroke
```

**No error, just an unusable product.** The answer is to prune candidates before computing anything, not to
optimise the table.

---

## 8. In the interview

### How it gets asked

- *"Given two strings, find the minimum number of operations to convert one to the other."* — LeetCode 72.
- *"What are the three operations, and which branch is which?"* — the naming question.
- *"Show me the actual edits, not just the count."*
- *"Reduce the space."*
- *"How would you build a spell-checker with this?"* — where the real answer is "not like this".
- *"What if the operations have different costs?"*

### The first ninety seconds

> "Same two-dimensional table as longest common subsequence, with three options instead of two and minimising
> rather than maximising.
>
> **`dp[i][j]` is the minimum number of edits to turn the first `i` characters of `a` into the first `j` of
> `b`.** Prefix lengths again, so `i = 0` is the empty prefix and the character is `a[i-1]`.
>
> **The base cases are different from LCS and this is where people go wrong.** `dp[i][0] = i`, because turning
> `i` characters into nothing takes `i` deletions. `dp[0][j] = j`, because building `j` characters from nothing
> takes `j` insertions. **So the first row and column are `0, 1, 2, 3...`, not zeros** — and the zeros carry
> over from yesterday by muscle memory and give an answer that is far too small.
>
> **If the characters match, the edit is free** — `dp[i][j] = dp[i-1][j-1]`, no plus one. That is the second
> most common bug, and it makes the distance from a string to itself non-zero.
>
> **If they differ, one of three operations, each costing one, and I would name all three.**
>
> **Replace** `a[i-1]` with `b[j-1]` — both characters are dealt with, so both indices retreat: the diagonal.
>
> **Delete** `a[i-1]` — I have consumed a character of `a` and none of `b`, so only `i` retreats: `dp[i-1][j]`.
>
> **Insert** `b[j-1]` — I have consumed a character of `b` and none of `a`, so only `j` retreats:
> `dp[i][j-1]`.
>
> **The rule is that the index which moves belongs to the string whose character you just used up**, and
> saying that out loud is how I avoid getting delete and insert backwards.
>
> **And I would flag why that matters:** edit distance is symmetric, so **swapping those two branches gives the
> correct number on every test.** The bug only appears when you ask what the edits were — which is usually the
> next question.
>
> **The answer is `dp[n][m]`. `O(n × m)` time and space**, reducible to two rows if only the number is needed."

### The follow-ups

**"Show me the actual edits, not just the count."**

> "Walk back from `dp[n][m]`, asking at each cell which of the four possibilities produced its value.
>
> **If the characters match and `dp[i][j] == dp[i-1][j-1]`, this was a free match** — emit 'keep' and move
> diagonally.
>
> **If `dp[i][j] == dp[i-1][j-1] + 1`, it was a replace** — emit it and move diagonally.
>
> **If `dp[i][j] == dp[i-1][j] + 1`, it was a delete of `a[i-1]`** — emit it and move up.
>
> **Otherwise it was an insert of `b[j-1]`** — emit it and move left.
>
> Then reverse, because I built it backwards.
>
> **The loop condition is `while i > 0 or j > 0`, not `and`** — that is the specific bug here. When one string
> is exhausted, everything remaining in the other is a run of pure insertions or pure deletions, and `and`
> stops early and silently drops them. **Reconstructing empty-string to `"abc"` with `and` returns an empty
> script instead of three insertions.**
>
> **Cost is `O(n + m)` in time** — each step decreases `i` or `j` or both — **and it needs the full table**, so
> I cannot use the two-row version. That trade is worth stating: linear space or the edit script, not both,
> unless I use Hirschberg's divide-and-conquer.
>
> **Two honest points.** **The script is not unique** — the order of my `elif` branches decides which of
> several equal-cost scripts I return, and all of them are correct.
>
> **And this is where the delete/insert confusion finally shows.** Since the distance is symmetric, swapped
> branches pass every test that checks the number, and then the script reports insertions where deletions
> happened. **So if a reconstruction ever looks backwards, that is the bug**, not the table."

**"How would you use this to build a spell-checker?"**

> "The honest answer is that edit distance is the scoring function, and the interesting engineering is in never
> calling it.
>
> **The naive version is: for each of a hundred thousand dictionary words, compute the edit distance to the
> query, keep the ones within two.** That is a hundred thousand tables of nine by nine, about eight million
> cells, **roughly three seconds per keystroke.** Unusable, and no amount of optimising the inner loop fixes
> three orders of magnitude.
>
> **Two cheap filters get part of the way.** **If the lengths differ by more than the limit, the distance
> cannot be within it** — one subtraction, and it rejects most of the dictionary immediately. **And inside the
> table, if the minimum of the current row already exceeds the limit, abort** — every remaining path can only
> get worse, so I stop after two or three rows instead of nine.
>
> **Together those are maybe ten to twenty times faster, and still not enough.**
>
> **The real answer is a data structure that prunes candidates before any table is built.** A **BK-tree**
> exploits the triangle inequality: distance is a metric, so if a word is at distance `d` from a node, anything
> within `k` of my query must be within `d - k` to `d + k` of that node, and I skip every other subtree. **That
> turns a hundred thousand comparisons into a few hundred.**
>
> **Or a trie with a running edit-distance row**, walking the trie and carrying the DP row down each branch —
> when the whole row exceeds the limit, prune that entire subtree. **That shares work across every word with a
> common prefix**, which in a dictionary is most of them.
>
> **Either way it goes from three seconds to about a millisecond**, and the point I would make is that the
> algorithmic improvement is not in the distance function at all.
>
> **Two product details.** **I would use Damerau-Levenshtein rather than plain Levenshtein**, because
> transposing two adjacent letters is one of the commonest typing errors and plain Levenshtein charges it two
> instead of one — `"hte"` to `"the"` should be one edit. **And I would weight the operations**: a replacement
> between keys that are adjacent on the keyboard should cost less than between distant ones, and the recurrence
> handles that unchanged — only the constants differ.
>
> **And I would rank the survivors by word frequency, not just by distance**, because among words at distance
> one from a typo, the common one is nearly always what was meant."

**"What if inserting is much more expensive than deleting?"**

> "Then the recurrence is unchanged and only the constants move, which is the nice part about how this is
> structured.
>
> **Instead of `1 + min(...)`, each branch carries its own cost:** the replace branch adds
> `cost_replace(a[i-1], b[j-1])`, the delete branch adds `cost_delete(a[i-1])`, the insert branch adds
> `cost_insert(b[j-1])`.
>
> **The part that is easy to miss is the base cases.** They stop being `i` and `j` and become **accumulated
> costs**: `dp[i][0]` is the total cost of deleting the first `i` characters one by one, and `dp[0][j]` is the
> total cost of inserting the first `j`. **If the costs vary by character, those are running sums, not
> multiplications.**
>
> **And one property is lost: the distance stops being symmetric.** With uniform costs, turning `a` into `b`
> costs the same as `b` into `a`. **With asymmetric insert and delete costs it does not**, so the swap I use in
> the space-optimised version is no longer free, and I have to be careful about which string is which.
>
> **That matters more than it sounds**, because it means I can no longer use it as a metric — and things like
> BK-trees depend on the triangle inequality holding, which asymmetric costs can break.
>
> **Where this comes up for real:** **DNA alignment**, where a substitution between chemically similar bases is
> biologically likelier than between different ones, and where opening a gap costs much more than extending an
> existing one — that last part actually needs an extra state, because the cost depends on whether you are
> already in a gap.
>
> **And OCR correction**, where confusing `0` with `O` or `1` with `l` should cost far less than confusing `0`
> with `W`, because the errors come from shapes rather than from meaning."

### The model answer

*"You are building the search box for a medicine ordering app. Users type drug names, often misspelled, and
you have a catalogue of forty thousand products. Design it."*

> "The scoring function is edit distance, and I want to be clear up front that **the design work is in
> avoiding computing it**, because the naive version is unusably slow at this size.
>
> **First, the requirement.** A user typing `'ranitidin'` should see `Ranitidine`. A user typing something four
> edits away from a real drug should probably see nothing, **because a wrong medicine suggestion is worse than
> no suggestion** — which is a domain constraint that changes the threshold, and I would raise it explicitly.
>
> **The scoring function: Damerau-Levenshtein rather than plain Levenshtein**, because transposing adjacent
> letters is one of the most common typing errors and plain Levenshtein charges two for it. `'ranitidnie'`
> should be one edit from `'ranitidine'`, not two.
>
> **And weighted**, because a replacement between keys adjacent on a phone keyboard is far likelier than
> between distant ones. **The recurrence is unchanged; only the constants differ.**
>
> **Now the performance, which is the actual design.** Forty thousand products, a query of about ten
> characters. **Naively that is forty thousand tables of eleven by eleven — about five million cells, roughly a
> second and a half per keystroke.** Unusable in a search box that fires on every character.
>
> **Two cheap filters first.** **The length filter** — if the lengths differ by more than the limit, reject
> without building anything — costs one subtraction and eliminates most of the catalogue. **And the row-minimum
> early exit** — if every cell in the current row already exceeds the limit, abort, because no path can
> improve. **Together, maybe fifteen times faster, and still not fast enough.**
>
> **So the structure: a trie over the catalogue with the DP row carried down each branch.** I walk the trie
> character by character, computing one edit-distance row per node, **and when the minimum of a node's row
> exceeds the limit I prune that entire subtree.** Because drug names share prefixes heavily — every
> `Ran-` drug shares three characters — this shares almost all the work. **That gets it to roughly a
> millisecond.**
>
> **A BK-tree is the alternative**, using the triangle inequality to skip subtrees, and it is simpler to build.
> **I would prefer the trie here** because it also gives me prefix completion for free, which the search box
> wants anyway — the user typing `'rani'` should see suggestions before they have made a typo at all.
>
> **Ranking the survivors, which matters as much as finding them.** **Not by edit distance alone.** Among
> candidates at distance one, I would rank by **how often the product is actually ordered**, because the
> common drug is nearly always what was meant. **And I would boost exact prefix matches above any fuzzy
> match**, because a user who has typed four correct characters is more likely completing than mistyping.
>
> **Two things specific to this domain that I would insist on.**
>
> **A strict threshold, and a preference for showing nothing.** At distance two, `Ranitidine` and `Ranolazine`
> are different drugs for different conditions. **I would cap suggestions at distance one for short names and
> two for long ones, and show 'no match' rather than a guess** — and I would want that reviewed by someone who
> knows the products, not decided by me.
>
> **And confusable pairs handled explicitly.** Drug names that differ by one or two characters but are
> clinically very different are a known safety problem with published lists. **Those pairs should never be
> offered as corrections for each other**, whatever the distance says — a hard-coded exception list on top of
> the algorithm, which is exactly the kind of thing an algorithm should not be trusted to get right on its
> own.
>
> **Performance-wise, the catalogue is small and static enough to hold the whole trie in memory on every
> application server**, rebuilt on deploy — no network call in the search path at all, which is what makes
> per-keystroke search feel instant."

---

## 9. Recall card

**`dp[i][j]` = minimum edits turning `a`'s first `i` characters into `b`'s first `j`.** Prefix lengths, so the
character is `a[i-1]`. **Base cases are `dp[i][0] = i` and `dp[0][j] = j`, NOT zeros** — that is the LCS muscle
memory that gives an answer far too small.

**Match is FREE: `dp[i-1][j-1]`, no `+1`.** Mismatch is `1 + min` of three, **and name all three**: **replace**
= diagonal (both consumed), **delete `a[i-1]`** = `dp[i-1][j]` (only `i` moves), **insert `b[j-1]`** =
`dp[i][j-1]` (only `j` moves). **The index that moves belongs to the string whose character you just used up.**

**Edit distance is symmetric, so swapping delete and insert passes every test that checks the number** — the
bug only appears in the reconstruction. Name the branches in comments as you write them.

**Reconstruction walks back asking which of four cases produced the value; the loop is `while i > 0 or j > 0`,
not `and`** — with `and`, a run of trailing insertions is silently dropped. Needs the full table.

**`O(n × m)` time and space; two rows for `O(min(n,m))`, and `current = [i] + ...` is the column base case
people forget.** **Weighted costs change only the constants — and the base cases become running sums, and the
distance stops being symmetric.** **Damerau adds transposition**: `"hte"→"the"` is 1, not 2.

**A spell-checker does not call this 100,000 times** — 3 seconds per keystroke. **Length filter, row-minimum
early exit, then a BK-tree or a trie carrying the DP row down and pruning whole subtrees** — a few hundred
candidates instead of the whole dictionary, and about a millisecond.
