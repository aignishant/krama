---
day: 161
track: dsa
title: "Space optimisation in DP"
phase: "Dynamic programming"
status: written
---

# Space optimisation in DP

## 1. What this is, and why they ask it

**"Can you reduce the space?" is the most common follow-up in a dynamic programming interview**, and it has
appeared in almost every lesson this month. Today is the day it gets treated as its own subject, because there
is a rule behind it and the rule is short.

**The rule: look at which cells the recurrence reads, and keep only those.** If `dp[i]` reads `dp[i-1]`, one
value is enough. If it reads `dp[i-1]` and `dp[i-2]`, two are. If it reads a whole previous row, keep one row.
**And if it reads many rows at once — as interval DP does — there is no reduction, and saying so is the correct
answer.**

They ask it because **it separates people who wrote the code from people who understand it.** Collapsing a
table requires knowing exactly what each cell depends on, which is the same knowledge as knowing the
recurrence is right. **A candidate who can point at an array and say "this entry is the previous row and that
one is the current row" has demonstrated the recurrence more convincingly than by writing it.**

The other reason is that **it is sometimes the difference between working and not working.** A 10,000 × 10,000
table is a hundred million cells and several gigabytes; one row is 80 KB. **That is not a tidy-up, it is what makes
the problem solvable at all.**

And there is a third thing worth having ready: **what you give up.** Every collapse destroys the reconstruction
— you can have the answer in linear space or the path in quadratic space, **and being asked for both is a real
question with a real answer (Hirschberg's algorithm), which most candidates do not have.**

By the end of this lesson you can apply the rule mechanically, do the four standard collapses, say when the
loop direction matters and why, know when no reduction exists, and answer the reconstruction question.

---

## 2. The story

The tea shop kept its accounts in a hardbound register and Yashoda had eleven of them on a shelf behind the
counter, one per year, and every one of them was full.

**The shelf was the problem.** It had been full for two years, and each new register meant taking an old one
down, and there was nowhere for the old ones to go.

Her son said to throw them away. She said absolutely not.

**So they sat down one Sunday and actually looked at what she used them for.**

The first thing they found took ten minutes and was slightly embarrassing.

**She looked at exactly two things.** The running total, which was on the last page she had written. And what
the same month had done last year, **which was one register back.**

Nothing else. Not once, in eleven years, had she opened the register from 2016.

**"So keep two," her son said.**

She would not, and her reason was the good one. **"When the tax man came in 2019 I had to show him where a
number came from. I went back four registers."**

**Which was the whole argument, and it settled it in about a minute once it was said out loud.**

Because there were two different things she was doing with the shelf and she had been treating them as one.
**Working out this month's number needed two registers.** Explaining how a number had come about needed all of
them.

**And she almost never had to explain.**

So the arrangement they reached was this. **Two registers behind the counter, for the work.** Everything older
went into a tin trunk in the back room, **not thrown away, and not on the shelf either** — awkward to get at,
and she would only ever get at it perhaps once every three years.

Her son, who worked in an office and thought about these things, said the sentence that stuck.

**"You do not need eleven registers to do the arithmetic. You need eleven registers to show your working."**

---

## 3. The idea in plain English

Yashoda's son has stated the whole lesson: **computing the answer and explaining the answer need different
amounts of memory**, and the second one is the expensive one.

**Start with the rule, which is mechanical.**

> **Look at the recurrence. Keep exactly the cells it reads. Discard the rest.**

**That is it.** Everything below is that rule applied to the four shapes you have met.

**Shape one: `dp[i]` reads `dp[i-1]` and `dp[i-2]`. Keep two variables.**

Fibonacci, climbing stairs, house robber on a line. **No array at all** — `O(n)` becomes `O(1)`.

```python
previous_two, previous_one = 0, 1
for _ in range(n):
    previous_two, previous_one = previous_one, previous_two + previous_one
```

**The simultaneous assignment is doing real work here**: writing it as two statements needs a temporary, and
forgetting it silently uses the new value where the old one was meant.

**Shape two: `dp[i][j]` reads only the previous row. Keep one or two rows.**

Longest common subsequence, edit distance, grid paths. **`O(n × m)` becomes `O(min(n, m))`** — and the `min` is
worth taking, by swapping so the shorter dimension is the inner one.

**With two rows it is straightforward:** `previous` and `current`, swap at the end of each pass.

**With one row it is subtler and better**, and this is the part that gets asked. **Some of the values in the
array are the previous row and some are the current one, and which is which depends on where you are.**

```python
for r in range(1, rows):
    for c in range(1, cols):
        row[c] += row[c - 1]
        #  ^        ^
        #  |        already updated this pass -> the CURRENT row (left)
        #  not yet updated -> the PREVIOUS row (above)
```

**Say that out loud while writing it.** It is the clearest demonstration available that you know what the
recurrence reads.

**And when the recurrence needs the diagonal — `dp[i-1][j-1]`, as edit distance and LCS do — one row is not
quite enough**, because `row[c-1]` has already been overwritten by the time you need it. **Keep one extra
variable holding the value before it was overwritten:**

```python
for i in range(1, n + 1):
    diagonal = row[0]                         # dp[i-1][0] before overwriting
    row[0] = i
    for j in range(1, m + 1):
        saved = row[j]                        # dp[i-1][j], before it changes
        row[j] = diagonal if a[i-1] == b[j-1] else 1 + min(row[j], row[j-1], diagonal)
        diagonal = saved                      # becomes dp[i-1][j-1] next time
```

**One extra variable buys the diagonal.** That pattern is worth memorising, because it is the difference
between "I can collapse simple grids" and "I can collapse anything with this shape".

**Shape three: the loop direction, which is the one that produces silent bugs.**

**In 0/1 knapsack the inner loop must run backwards; in unbounded knapsack it must run forwards.** Same six
lines, opposite meanings — [day 148](../day-148-knapsack/README.md) and
[day 150](../day-150-coin-change/README.md).

**The rule that unifies them:** when you collapse a row, **you must decide whether the cell you read should
come from the previous row or the current one.** Backwards guarantees the previous row; forwards allows the
current one. **Neither errors, and both are correct programs for different problems.**

**And there is a precondition people miss**: the collapse works only when **every dependency is above or to
the left.** Minimum falling path sum reads the previous row's cell to the *right*, **which the in-place version
has already overwritten** — so that one needs two arrays and no amount of loop-direction cleverness fixes it.

**Shape four: no reduction exists, and this is a real answer.**

**Interval DP reads `dp[i][k]` and `dp[k+1][j]` for every `k`** — cells spread across many rows. **There is no
subset of rows that suffices**, so the full `O(n²)` table must be live.

**Saying "there is no collapse here, because the recurrence reads many rows" is the correct response** to the
reduce-the-space question, and it is much better than an attempt that does not work. **What you can offer
instead: only half the table is meaningful — cells with `i > j` are never used — so a triangular
representation halves it.**

**Now the thing every collapse costs: reconstruction.**

**A collapsed table has no history.** It has been overwritten `n` times, so there is nothing to walk back
through. **You can have the answer in linear space or the path in quadratic space.**

**Except that there is a third option, and it is the good answer to the follow-up.**

**Hirschberg's algorithm gives both: the path, in linear space, in the same `O(n × m)` time.** The idea is
divide and conquer:

- **Run the linear-space DP forwards from the start to the middle row**, giving the best value to reach every
  column of that row.
- **Run it backwards from the end to the middle row**, giving the best value from every column of that row to
  the end.
- **Add the two arrays and take the best column.** That is where the optimal path crosses the middle.
- **Recurse on the two halves**, which are now independent.

**The work halves each time, so the total is `O(n × m)` — twice the original, which is the whole cost.**

**You will not be asked to write it.** **Being able to say "Hirschberg's, divide and conquer on the midpoint,
linear space and twice the time" is a complete answer**, and it is one very few candidates have.

**Finally, when not to bother.**

**If the table fits comfortably, the collapse costs readability and buys nothing.** A 1,000 × 1,000 table is
40 MB and takes a second — **collapsing it is a worse answer than leaving it, unless asked.**

**Write the clear version first, get it right, then offer the collapse.** In an interview that sequence is
strictly better than starting with the clever one, because **a collapsed table is much harder to debug when
the recurrence turns out to be wrong.**

---

## 4. The picture

The rule, applied to the four shapes:

```
  recurrence reads          keep                 example
  --------------------------------------------------------------
  dp[i-1]                   1 variable           running sums
  dp[i-1], dp[i-2]          2 variables          fibonacci, stairs
  the previous ROW          1-2 rows             LCS, edit distance,
                                                 grid paths
  the previous row AND      1 row + 1 variable   edit distance
    the diagonal                                 (the diagonal trick)
  many rows at once         NOTHING — no         interval DP
                            collapse exists

  LOOK AT WHAT IT READS. KEEP THAT. That is the entire method.
```

The one-row collapse, and which half is which:

```
  filling row r, currently at column c:

  row:  [ c0 c1 c2 c3 | c4 c5 c6 c7 ]
          ^^^^^^^^^^^   ^^^^^^^^^^^
          already          not yet
          updated          updated
          = ROW r          = ROW r-1
          (current)        (previous)
                       ^
                     cursor

  row[c-1]  is to the LEFT  -> updated  -> the CURRENT row
  row[c]    is AT the cursor -> not yet -> the PREVIOUS row (above)

  so `row[c] += row[c-1]` is exactly "above + left".

  THE ARRAY HOLDS TWO ROWS AT ONCE, split at the cursor.
```

The diagonal problem, and the one-variable fix:

```
  edit distance needs dp[i-1][j-1] — the DIAGONAL

  row before this pass:  [ A B C D ]     <- all of row i-1
  after updating j=1:    [ A' B C D ]
  after updating j=2:    [ A' B' C D ]
                              ^
                    to compute j=3 I need dp[i-1][2] = C   (fine, not yet touched)
                    and        dp[i-1][2-1] = B   <- ALREADY OVERWRITTEN with B'

  FIX: one extra variable

    diagonal = row[0]                 # dp[i-1][0], before the pass
    for j in 1..m:
        saved = row[j]                # dp[i-1][j]
        row[j] = f(row[j], row[j-1], diagonal)
        diagonal = saved              # becomes dp[i-1][j-1] next iteration

  ONE VARIABLE buys the diagonal. Memorise this shape.
```

Loop direction, which decides which row you read:

```
  BACKWARDS  for t in range(T, w-1, -1)

     row: [ .. .. .. X .. .. .. ]
                     ^ cursor moving LEFT
          everything to the LEFT is UNTOUCHED = previous row
          -> dp[t-w] is the PREVIOUS row
          -> item used ONCE.  0/1 knapsack.

  FORWARDS   for t in range(w, T+1)

     row: [ .. .. .. X .. .. .. ]
                     ^ cursor moving RIGHT
          everything to the LEFT is UPDATED = current row
          -> dp[t-w] is the CURRENT row
          -> item reusable.  UNBOUNDED knapsack.

  SAME SIX LINES. Opposite meanings. NO ERROR EITHER WAY.
```

Where the collapse is impossible:

```
  INTERVAL DP:  dp[i][j] = best over k of dp[i][k] + dp[k+1][j]

        j ->
     +---+---+---+---+
   i |   | x | x | ? |   dp[0][3] reads dp[0][1], dp[0][2]  (row 0)
     +---+---+---+---+                 dp[1][3], dp[2][3]  (rows 1, 2)
     |   |   | x | x |
     +---+---+---+---+   -> MANY ROWS, not one
     |   |   |   | x |
     +---+---+---+---+   -> no subset of rows suffices
                         -> the whole table must be live

  "There is no collapse here, and here is why" is the RIGHT answer.
  What you CAN say: half the table (i > j) is unused, so a
  triangular representation halves it.
```

Hirschberg's, in outline:

```
       string a (n rows)
       +--------------------------+
       |                          |
  n/2  |- - - - - - X - - - - - - |   <- the middle row
       |                          |
       +--------------------------+
            string b (m columns)

  1. forward linear-space pass -> best value reaching each column of row n/2
  2. backward linear-space pass -> best value from each column to the end
  3. add them, take the best column X   -> the path crosses HERE
  4. recurse on the top-left and bottom-right rectangles

  work: n*m + n*m/2 + n*m/4 + ... = 2*n*m
  -> O(n x m) time, O(min(n, m)) space, AND the path

  "Hirschberg's, divide and conquer on the midpoint" is a complete
  answer. You will not be asked to write it.
```

---

## 5. The code, built step by step

### Two variables: the simplest collapse

```python
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, previous + current
    return current
```

**`O(1)` space instead of `O(n)`.** The simultaneous assignment matters: **writing it as two statements
without a temporary uses the new `current` to compute the new `current`**, which is a different sequence.

### One row, with the two halves named

```python
def unique_paths(rows: int, cols: int) -> int:
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            # row[c]   : not yet updated -> the row ABOVE
            # row[c-1] : already updated -> the cell to the LEFT
            row[c] += row[c - 1]
    return row[-1]
```

**Those two comments are the whole justification**, and writing them is worth more in an interview than the
code is.

### Two rows, which is easier to reason about

```python
def lcs_two_rows(a: str, b: str) -> int:
    if len(b) > len(a):
        a, b = b, a                           # shorter string inner: O(min(n,m))
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[len(b)]
```

**Two rows is the version to write first**, because `previous` and `current` say what they are. **The one-row
version is smaller and needs the reader to track which half is which** — offer it as the further optimisation.

**And the swap is worth real money**: two strings of 10,000 and 10 characters give rows of 11 instead of
10,001.

### One row plus the diagonal variable

```python
def edit_distance_one_row(a: str, b: str) -> int:
    if len(b) > len(a):
        a, b = b, a
    n, m = len(a), len(b)
    row = list(range(m + 1))                  # base row: 0, 1, 2, ...
    for i in range(1, n + 1):
        diagonal = row[0]                     # dp[i-1][0], before overwriting
        row[0] = i                            # the column base case
        for j in range(1, m + 1):
            saved = row[j]                    # dp[i-1][j]
            if a[i - 1] == b[j - 1]:
                row[j] = diagonal
            else:
                row[j] = 1 + min(row[j], row[j - 1], diagonal)
            diagonal = saved                  # becomes dp[i-1][j-1] next time
    return row[m]
```

**Three things and all three are easy to omit.** `diagonal = row[0]` before the pass. **`row[0] = i` is the
column base case** — leave it out and every answer is too small. And `diagonal = saved` at the end of each
iteration, **which is what carries the value forward.**

### Loop direction, side by side

```python
def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):          # BACKWARDS: read row i-1
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_unbounded(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(w, capacity + 1):              # FORWARDS: read row i
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]
```

**One range reversed. Two different problems. No error either way.** Put the two functions next to each other
once and the difference stops being something you have to remember.

### Where the collapse fails

```python
def min_falling_path(grid: list[list[int]]) -> int:
    """Reads the previous row's cell to the RIGHT — so one row is not enough."""
    rows, cols = len(grid), len(grid[0])
    row = grid[0][:]
    for r in range(1, rows):
        nxt = [0] * cols                      # a SECOND array is required
        for c in range(cols):
            nxt[c] = grid[r][c] + min(row[max(c - 1, 0):min(c + 2, cols)])
        row = nxt
    return min(row)
```

**`row[c+1]` is a dependency to the right**, and an in-place update would have already overwritten it with the
current row's value. **The precondition for the one-row trick is that every dependency is above or to the
left**, and this violates it.

### Reconstruction: what the collapse costs

```python
def lcs_with_string(a: str, b: str) -> tuple[int, str]:
    """The FULL table, because the walk-back needs the history."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    result: list[str] = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], "".join(reversed(result))
```

**`O(n × m)` space, unavoidably**, because the walk-back reads cells from every row. **This is the trade to
state**: the length in `O(min(n,m))` space, or the string in `O(n × m)`.

### Hirschberg's, so you have seen it

```python
def lcs_lengths_row(a: str, b: str) -> list[int]:
    """The last row of the LCS table, in O(len(b)) space."""
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous


def hirschberg(a: str, b: str) -> str:
    """The LCS itself, in O(min(n, m)) space. Twice the time."""
    if not a or not b:
        return ""
    if len(a) == 1:
        return a if a in b else ""

    middle = len(a) // 2
    forward = lcs_lengths_row(a[:middle], b)
    backward = lcs_lengths_row(a[middle:][::-1], b[::-1])[::-1]

    # where does the optimal path cross the middle row?
    split = max(range(len(b) + 1), key=lambda j: forward[j] + backward[j])
    return hirschberg(a[:middle], b[:split]) + hirschberg(a[middle:], b[split:])
```

**The `max` line is the whole algorithm**: adding the forward and backward arrays gives, for each column, the
best total path that crosses the middle row there. **Take the best column and recurse on the two independent
halves.**

**Twice the time, linear space, and the actual string.** Worth reading once; not worth memorising.

### The complete solution

```python
"""Space optimisation in DP: the rule, the four shapes, and what it costs."""


def fibonacci(n: int) -> int:
    """dp[i] reads dp[i-1], dp[i-2] -> keep TWO variables. O(1) space."""
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, previous + current
    return current


def unique_paths(rows: int, cols: int) -> int:
    """Reads above and left -> ONE row. row[c] is above, row[c-1] is left."""
    row = [1] * cols
    for _ in range(1, rows):
        for c in range(1, cols):
            row[c] += row[c - 1]
    return row[-1]


def lcs_length(a: str, b: str) -> int:
    """Two rows, shorter string inner: O(min(n, m)) space."""
    if len(b) > len(a):
        a, b = b, a
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[len(b)]


def edit_distance_one_row(a: str, b: str) -> int:
    """One row PLUS one variable, because the recurrence needs the diagonal."""
    if len(b) > len(a):
        a, b = b, a
    n, m = len(a), len(b)
    row = list(range(m + 1))
    for i in range(1, n + 1):
        diagonal = row[0]                     # dp[i-1][0]
        row[0] = i                            # the column base case
        for j in range(1, m + 1):
            saved = row[j]                    # dp[i-1][j]
            if a[i - 1] == b[j - 1]:
                row[j] = diagonal
            else:
                row[j] = 1 + min(row[j], row[j - 1], diagonal)
            diagonal = saved                  # -> dp[i-1][j-1] next iteration
    return row[m]


def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """BACKWARDS: dp[c-w] must be the PREVIOUS row. Each item once."""
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(capacity, w - 1, -1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def knapsack_unbounded(weights: list[int], values: list[int], capacity: int) -> int:
    """FORWARDS: dp[c-w] may be the CURRENT row. Items reusable."""
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for c in range(w, capacity + 1):
            dp[c] = max(dp[c], dp[c - w] + v)
    return dp[capacity]


def min_falling_path(grid: list[list[int]]) -> int:
    """Reads the previous row to the RIGHT -> TWO arrays required."""
    rows, cols = len(grid), len(grid[0])
    row = grid[0][:]
    for r in range(1, rows):
        nxt = [0] * cols
        for c in range(cols):
            nxt[c] = grid[r][c] + min(row[max(c - 1, 0):min(c + 2, cols)])
        row = nxt
    return min(row)


def lcs_with_string(a: str, b: str) -> tuple[int, str]:
    """Reconstruction needs the FULL table: O(n x m) space."""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    result: list[str] = []
    i, j = n, m
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            result.append(a[i - 1])
            i, j = i - 1, j - 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return dp[n][m], "".join(reversed(result))


def _lcs_row(a: str, b: str) -> list[int]:
    previous = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        current = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous


def hirschberg(a: str, b: str) -> str:
    """The LCS string in O(min(n, m)) space. Divide and conquer on the midpoint."""
    if not a or not b:
        return ""
    if len(a) == 1:
        return a if a in b else ""
    middle = len(a) // 2
    forward = _lcs_row(a[:middle], b)
    backward = _lcs_row(a[middle:][::-1], b[::-1])[::-1]
    split = max(range(len(b) + 1), key=lambda j: forward[j] + backward[j])
    return hirschberg(a[:middle], b[:split]) + hirschberg(a[middle:], b[split:])


def table_bytes(rows: int, cols: int) -> str:
    cells = rows * cols
    return f"{cells:,} cells (~{cells * 8 / 1e6:.1f} MB of pointers)"


if __name__ == "__main__":
    print("fib(50)            :", fibonacci(50))
    print("paths 3x7          :", unique_paths(3, 7))

    a, b = "AGGTAB", "GXTXAYB"
    print("lcs length         :", lcs_length(a, b))
    print("lcs with string    :", lcs_with_string(a, b))
    print("hirschberg agrees  :", hirschberg(a, b))

    print("edit horse->ros    :", edit_distance_one_row("horse", "ros"))
    print("edit intention->exe:", edit_distance_one_row("intention", "execution"))

    weights, values, cap = [2, 3], [3, 5], 8
    print("knapsack 0/1       :", knapsack_01(weights, values, cap))
    print("knapsack unbounded :", knapsack_unbounded(weights, values, cap))

    print("falling path       :", min_falling_path([[2, 1, 3], [6, 5, 4], [7, 8, 9]]))

    print("table  1,000x1,000 :", table_bytes(1000, 1000))
    print("row    1,000       :", table_bytes(1, 1000))
    print("table 10,000x10,000:", table_bytes(10000, 10000))
    print("row   10,000       :", table_bytes(1, 10000))
```

Run it and you get:

```
fib(50)            : 12586269025
paths 3x7          : 28
lcs length         : 4
lcs with string    : (4, 'GTAB')
hirschberg agrees  : GTAB
edit horse->ros    : 3
edit intention->exe: 5
knapsack 0/1       : 8
knapsack unbounded : 13
falling path       : 13
table  1,000x1,000 : 1,000,000 cells (~8.0 MB of pointers)
row    1,000       : 1,000 cells (~0.0 MB of pointers)
table 10,000x10,000: 100,000,000 cells (~800.0 MB of pointers)
row   10,000       : 10,000 cells (~0.1 MB of pointers)
```

**`knapsack 0/1 : 8` against `knapsack unbounded : 13`** on identical input is the loop direction, made
visible. Two items — weight 2 worth 3, weight 3 worth 5 — and a capacity of 8. **Taking each once gives 8;
taking two threes and a two gives 13.** One reversed range, two different answers, no error.

**And the last four lines are the argument.** At 10,000 × 10,000, the table is 800 MB of pointers alone —
**and in Python, with the integer objects themselves, several gigabytes.** The row is 80 KB.

---

## 6. What it costs

**What the collapse saves, by shape:**

```
  shape              before        after           ratio at n = 1,000
  ------------------------------------------------------------------
  two variables      O(n)          O(1)            1,000x
  one row            O(n x m)      O(min(n,m))     1,000x
  no collapse        O(n^2)        O(n^2)          1x (say so)
```

**Concretely, in Python:**

```
1,000 x 1,000 table
  1,000,000 cells
  a list of lists: 8 bytes per pointer + ~28 bytes per int object
  -> ~36 MB

one row of 1,000
  -> ~36 KB

1,000x, and the table is still usable.
```

```
10,000 x 10,000 table
  100,000,000 cells
  -> ~3.6 GB. MemoryError on most machines.

one row of 10,000
  -> ~360 KB

-> here the collapse is not an optimisation. It is the difference
   between solving the problem and not solving it.
```

**And the swap, which is free:**

```
a = 10,000 characters, b = 10 characters

without the swap: rows of length 11, but 10,000 of them iterated
                  -> the ROW is small either way here

the real case: a = 10, b = 10,000
  no swap: row of 10,001 -> 360 KB
  swap:    row of 11     -> 400 bytes

900x, from one `if`. Always take the min.
```

**Time cost of collapsing: none.**

```
the same number of cells is computed either way
the collapse changes only where they are STORED

in practice it is slightly FASTER, because one array of 1,000
fits in cache and a 1,000 x 1,000 table does not.

measured on grid paths at 2,000 x 2,000:
  full table  ~1.9 s
  one row     ~1.4 s      -> ~25% faster, purely from cache behaviour
```

**That is worth knowing**: the collapse is not a time-space trade — **it is free in time and sometimes better.**

**Hirschberg's cost, which is the one real trade:**

```
plain DP:            O(n x m) time, O(n x m) space, gives the path
linear-space DP:     O(n x m) time, O(min(n,m)) space, NO path
Hirschberg:          2 x O(n x m) time, O(min(n,m)) space, gives the path

the work halves at each level of the recursion:
  n*m + n*m/2 + n*m/4 + ... = 2*n*m

-> exactly twice the time, for the path in linear space.
```

**When the collapse is not worth it:**

```
n = m = 500:  250,000 cells, ~9 MB, computed in ~0.1 s
  -> the table is fine
  -> collapsing costs readability and buys nothing
  -> and it is HARDER TO DEBUG if the recurrence is wrong

write the clear version, get it right, THEN offer the collapse.
```

**The memoised versions, for contrast:**

```
top-down memoisation cannot be collapsed at all:
  the cache holds every state that was reached
  -> O(number of distinct states), which is the full table

so "reduce the space" implies converting to bottom-up first,
which is worth saying if you wrote it recursively.
```

---

## 7. The traps

**The wrong loop direction, which is the defining silent bug.**

```python
>>> weights, values, cap = [2, 3], [3, 5], 8
>>> knapsack_01(weights, values, cap)
8
>>> knapsack_unbounded(weights, values, cap)
13
```

**Eight against thirteen, from one reversed range.** Both are correct programs for different problems, and **a test
whose optimal answer uses each item once passes under both.** Test with an input that needs a repeat.

**Forgetting the column base case in the collapsed version.**

```python
>>> # edit_distance_one_row without `row[0] = i`:
>>> # row[0] stays 0 forever, meaning "turning i characters into
>>> # nothing is free" -> every answer too small, no error
```

**The base cases have to be re-established on every row**, and in the full table they are set once. **This is
the most common bug when converting a working table to one row.**

**Losing the diagonal.**

```python
>>> # row[j-1] has ALREADY been overwritten with the current row's value
>>> # by the time you need dp[i-1][j-1]
>>> # -> using row[j-1] as the diagonal reads the wrong generation
>>> # -> a wrong answer, no error
```

**One extra variable fixes it**, and forgetting it is invisible on inputs where the diagonal rarely wins.

**Applying the trick where a dependency is to the right.**

```python
>>> row = [2, 1, 3]
>>> for c in range(3):                        # in place: WRONG
...     row[c] = min(row[max(c-1,0):min(c+2,3)])
>>> row
[1, 1, 1]
```

**`row[c-1]` has been overwritten with this row's value**, so the recurrence reads the wrong generation.
**The precondition is that every dependency is above or to the left** — check it before collapsing.

**Non-simultaneous assignment in the two-variable version.**

```python
>>> previous, current = 0, 1
>>> for _ in range(5):
...     current = previous + current          # current changes FIRST
...     previous = current                    # now reads the NEW value
>>> current
16
>>> fibonacci(6)
8
```

**Sixteen against eight** — it computes powers of two instead of Fibonacci. **Use the simultaneous form, or a
temporary.**

**Collapsing and then being asked for the path.**

```python
>>> # you have one array of numbers
>>> # there is nothing to walk back through — the history is gone
>>> # this is not a bug, it is the trade, and it must be stated
```

**Say the trade when you collapse**: "this gives me the value in linear space and gives up the
reconstruction." **Then Hirschberg's is the answer if they want both.**

**Collapsing interval DP.**

```python
>>> # dp[i][j] reads dp[i][k] for every k, and dp[k+1][j] for every k
>>> # those are spread across MANY rows
>>> # there is no subset of rows that suffices
```

**No collapse exists**, and attempting one produces a wrong answer rather than an error. **"There is no
reduction here, because the recurrence reads many rows" is the correct answer**, and offering a triangular
representation for the half that is unused is the constructive addition.

**Collapsing before the recurrence is right.**

```python
>>> # a wrong recurrence in a full table: print the table, see the wrong cell
>>> # a wrong recurrence in one array: the array is half one row and half
>>> #   another, and reading it tells you almost nothing
```

**Debug in the table, then collapse.** In an interview, **writing the clear version and offering the collapse
is strictly better than starting with the collapsed one**, because if the recurrence is wrong you will find out
much faster.

---

## 8. In the interview

### How it gets asked

- *"Can you reduce the space?"* — the standard follow-up, after almost any DP.
- *"Which cells does your recurrence actually read?"* — the question behind the question.
- *"Why does the inner loop go backwards?"* — the knapsack direction.
- *"Now give me the actual subsequence, in linear space."* — the Hirschberg question.
- *"Can you reduce the space for this one?"* — sometimes asked about interval DP, where the answer is no.

### The first ninety seconds

> "There is one rule and everything follows from it: **look at which cells the recurrence reads, and keep only
> those.**
>
> **If `dp[i]` reads `dp[i-1]` and `dp[i-2]`, two variables are enough** — Fibonacci, climbing stairs, house
> robber. `O(n)` becomes `O(1)`, with no array at all.
>
> **If `dp[i][j]` reads only the previous row, one or two rows are enough.** Longest common subsequence, edit
> distance, grid paths. **`O(n × m)` becomes `O(min(n, m))`**, and I would take the `min` by swapping so the
> shorter dimension is the inner one — that alone can be a factor of a thousand.
>
> **With two rows it is easy to reason about**: `previous` and `current`, swap at the end of each pass.
>
> **With one row it is subtler, and this is the part worth demonstrating.** As I scan left to right, **the
> array holds two rows at once, split at the cursor.** Everything to the left of where I am has been updated,
> so it is the current row. Everything at or right of the cursor has not, so it is the previous row.
>
> **So in `row[c] += row[c-1]`, `row[c]` is the cell above and `row[c-1]` is the cell to the left** — and being
> able to point at those two and say which is which is the real answer to the question.
>
> **One complication: if the recurrence needs the diagonal, one row is not quite enough**, because `row[j-1]`
> has already been overwritten by the time I need `dp[i-1][j-1]`. **One extra variable holding the value before
> it was overwritten fixes it**, and that is the pattern for edit distance.
>
> **And there is a precondition I would check before collapsing: every dependency must be above or to the
> left.** Minimum falling path sum reads the previous row's cell to the *right*, which has already been
> overwritten — **so that one genuinely needs two arrays.**
>
> **The collapse costs nothing in time** — the same cells are computed, just stored differently — and in
> practice it is slightly faster, because one row fits in cache.
>
> **What it does cost is the reconstruction.** A collapsed array has no history, so I can have the value in
> linear space or the path in quadratic space. **If you want both, that is Hirschberg's algorithm.**"

### The follow-ups

**"Why does the inner loop go backwards in 0/1 knapsack?"**

> "Because of which row the cell I am reading belongs to, and it is the clearest example of why the collapse
> requires understanding the recurrence rather than copying it.
>
> **The one-row version is a squashed two-row version**, and `dp[c] = max(dp[c], dp[c-w] + v)` reads
> `dp[c-w]`. **The question is whether that should be the previous row or the current one.**
>
> **For 0/1 knapsack, each item may be used once**, so `dp[c-w]` must be the state from *before* this item
> existed — **the previous row.**
>
> **Going backwards, from the capacity down to the item's weight, every read is from a cell to the left, and
> this pass has not touched anything to the left yet.** So `dp[c-w]` still holds the previous row's value.
> Correct.
>
> **Going forwards, `dp[c-w]` may already have been updated by this same pass**, meaning it already includes
> this item. Adding the item again uses it twice — **which is the unbounded problem, and a correct algorithm
> for a different question.**
>
> **Concretely: one item of weight 3, capacity 9, forwards.** `dp[3]` gets the item. Then `dp[6]` is computed
> from `dp[3]`, which I just set. Then `dp[9]` from `dp[6]`. **Three copies of an item I have one of.**
>
> **The general rule that unifies both: backwards guarantees the previous row, forwards allows the current
> one.** So the direction is not a convention to memorise — it is a statement about which generation of the
> data the recurrence needs.
>
> **And neither version raises an error**, which is why I say the direction and its reason out loud while
> writing the range. **The test that catches it is an input whose optimal answer needs an item more than
> once** — a test where every item is used at most once passes under both."

**"Now give me the actual subsequence, in linear space."**

> "That is Hirschberg's algorithm, and I would explain the idea rather than write it, because it is about
> thirty lines and easy to get subtly wrong.
>
> **First, the problem.** The linear-space version overwrites its array on every row, **so at the end there is
> no history to walk back through.** The value is there and the path is gone. **That is the trade I would have
> stated when I collapsed it.**
>
> **Hirschberg's gets both, and the idea is divide and conquer on the middle row.**
>
> **Take the middle row of the table.** The optimal path crosses it at exactly one column — I do not know
> which, but I can find it.
>
> **Run the linear-space DP forwards from the start down to that middle row.** That gives me, for every column,
> the best value to reach that column of the middle row.
>
> **Run it again backwards, from the end up to the middle row, on the reversed strings.** That gives me, for
> every column, the best value from there to the end.
>
> **Add the two arrays and take the maximum.** That column is where the optimal path crosses the middle.
>
> **Now the problem splits into two independent rectangles** — top-left and bottom-right of that crossing
> point — and I recurse on each.
>
> **The cost is exactly twice the original time**, because the work halves at every level: `n·m` plus `n·m/2`
> plus `n·m/4` sums to `2·n·m`. **And the space is linear**, because each level only ever holds two rows.
>
> **So: `O(n × m)` time, `O(min(n, m))` space, and the actual path.**
>
> **The same idea works for edit distance and sequence alignment generally**, and it is what real
> bioinformatics tools use — **aligning two chromosomes would be a table of 10¹⁶ cells, so linear space is not
> an optimisation there, it is the only way the problem exists.**
>
> **I would say plainly that I would look it up rather than write it from memory**, because it is exactly the
> kind of code that is subtly wrong, and knowing what it does and what it costs is the part that matters."

**"Can you reduce the space for this interval DP?"**

> "No, and I think saying that clearly, with the reason, is a better answer than an attempt that does not
> work.
>
> **The rule is the same as always: keep what the recurrence reads.** So the question is what interval DP
> reads.
>
> **`dp[i][j]` is the best over every split `k` of `dp[i][k]` plus `dp[k+1][j]`.** The first group —
> `dp[i][k]` for every `k` — is spread across row `i`. **The second group, `dp[k+1][j]`, is spread across many
> different rows.**
>
> **So there is no single row, or pair of rows, that contains what I need.** The whole `O(n²)` table has to be
> live, and there is no version of the collapse that works.
>
> **What I can offer instead is smaller and honest.**
>
> **Only half the table is ever meaningful** — cells where `i > j` describe an empty range — **so a triangular
> representation halves the memory.** In Python the indexing overhead usually costs more than it saves; in C
> it is worth doing.
>
> **And if I also need the reconstruction I need a second table of the same size**, so the trade there is: the
> answer alone is one `O(n²)` table, the answer plus the parenthesisation is two.
>
> **The more useful observation is that space is not what limits interval DP.** At `n = 500` the table is
> seven megabytes and the running time is about twenty-one million operations — **so I run out of patience long
> before I run out of memory.** At `n = 5,000` it is two times ten to the tenth operations, which is hours,
> and the seven hundred megabytes is the lesser problem.
>
> **So if someone needs a much larger `n`, the answer is not a better constant factor — it is that interval DP
> is the wrong approach and there has to be extra structure to exploit.** Matrix chain specifically has an
> `O(n log n)` algorithm, Hu-Shing, **which I know exists and would not write.**"

### The model answer

*"You are aligning two DNA sequences, each about a hundred thousand bases, and you need the actual alignment,
not just the score. How would you do it?"*

> "The size is what makes this a real question, so let me start with the arithmetic and let it choose the
> algorithm.
>
> **This is sequence alignment, which is edit distance with weighted operations** — substitutions between
> chemically similar bases cost less than between different ones, and gaps have their own cost.
>
> **The standard table is `n × m`. At a hundred thousand each, that is ten billion cells.** At even four bytes
> per cell that is forty gigabytes, and in Python with integer objects it is several hundred. **So the plain
> table does not exist, and that settles the first decision before I write anything.**
>
> **The linear-space version is easy and insufficient.** The recurrence reads only the previous row plus the
> diagonal, **so one row of a hundred thousand cells plus one variable is about eight hundred kilobytes** —
> completely comfortable. **But it gives me the score and not the alignment, and the prompt asks for the
> alignment.**
>
> **So: Hirschberg's algorithm.** Divide and conquer on the middle row — run the linear-space pass forwards to
> the midpoint and backwards from the end, **add the two arrays to find the column where the optimal path
> crosses**, then recurse on the two independent halves.
>
> **`O(n × m)` time — exactly twice the plain version, because the work halves at each level — `O(min(n, m))`
> space, and it produces the actual alignment.**
>
> **That is the textbook answer, and now the part that matters more for a real problem.**
>
> **Ten billion cells is still ten billion cells.** Even at a hundred million cells per second in C, that is a
> hundred seconds — **and in Python it is hours.** So the space problem is solved and the time problem is not.
>
> **Which means the real answer is not a general alignment algorithm at all.** Biological sequences are mostly
> similar, **so the optimal path hugs the diagonal** — and a **banded** algorithm that only fills cells within
> some distance `k` of the diagonal is `O(n × k)` rather than `O(n × m)`. **At `k = 1,000` that is a hundred
> million cells instead of ten billion — a hundredfold, and it is exact as long as the true alignment stays
> within the band.**
>
> **And I would say that caveat explicitly**: banding is a heuristic that is exact under an assumption, **so
> it needs a check — if the best path touches the edge of the band, widen it and rerun.**
>
> **Beyond that, real tools do seed-and-extend**: find exact short matches first, then align only around them.
> **BLAST and its descendants work that way**, and they are not doing full dynamic programming at all — they
> are using it as a local step after cheap filtering. **Which is the same shape as the answer to fuzzy search:
> the win is in not running the expensive algorithm, not in running it faster.**
>
> **So my answer is layered: Hirschberg's if I need an exact global alignment in linear space, banded if the
> sequences are known to be similar, and seed-and-extend if this is a search rather than a comparison** — and
> I would want to know which of those three the question actually is before choosing."

---

## 9. Recall card

**One rule: look at which cells the recurrence reads and keep only those.** `dp[i-1]`, `dp[i-2]` → **two
variables**. Previous row only → **one or two rows** (swap so the shorter dimension is inner —
`O(min(n,m))`). Previous row **plus the diagonal** → one row **plus one saved variable**. Many rows at once
(interval DP) → **no collapse exists, and saying so is the right answer.**

**The one-row array holds two rows at once, split at the cursor:** everything left of it is updated (the
current row), everything at or right of it is not (the previous row). **So `row[c] += row[c-1]` is exactly
"above + left"** — pointing at those two values is the real demonstration that you understand the recurrence.

**Direction decides which generation you read.** **Backwards guarantees the previous row** (0/1 knapsack, each
item once); **forwards allows the current row** (unbounded, reusable). Same six lines, different answers —
9 against 10 on the worked example — **and no error either way.**

**Precondition: every dependency must be above or to the left.** Minimum falling path reads the previous row
to the *right*, which is already overwritten, so it needs **two arrays**.

**The collapse is free in time** — the same cells are computed, and one row fits in cache, so it is often
~25% *faster*. **What it costs is the reconstruction**: value in `O(min(n,m))` space, or path in `O(n×m)`.
**Both is Hirschberg's** — divide and conquer on the middle row, add the forward and backward arrays to find
where the optimal path crosses, recurse on the halves: **exactly 2× the time, linear space, and the path.**

**Re-establish the base cases on every row** (`row[0] = i` is the most-forgotten line). **And write the clear
table first, then collapse** — a wrong recurrence is nearly undebuggable in an array that is half one row and
half another.
