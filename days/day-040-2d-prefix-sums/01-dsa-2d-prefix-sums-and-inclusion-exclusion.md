---
day: 40
track: dsa
title: "2D prefix sums and inclusion-exclusion"
phase: "Prefix sums"
status: written
---

# Day 040 · DSA — 2D prefix sums and inclusion-exclusion

**After today you can:** You can answer any rectangle-sum query in O(1) and derive the four-term formula yourself.

**The interviewer asks it as:** *Answer many rectangle-sum queries on a fixed matrix.*

---

## 1. What this is, and why they ask it

A **2D prefix sum** extends [day 037](../day-037-prefix-sums/README.md) to matrices: precompute,
for every position, the sum of the whole rectangle from the top-left corner down to it. Any
rectangle's sum then comes from **four** stored values instead of two — big rectangle, minus the
strip above, minus the strip to the left, **plus the corner that got subtracted twice**. That
add-back is **inclusion-exclusion**, a counting principle that outlives this problem by decades of
interviews.

Interviewers use Range Sum Query 2D — LeetCode 304 — as a derivation test. The 1D version can be
memorised; the 2D formula, with its four terms and two signs, punishes memorisation the moment a
nervous mind drops a term. What they want to see is the formula *rebuilt from a picture*: overlap
counted twice, added back once. Show that and the code is eight lines; miss it and the wrong
answer arrives with confident arithmetic. The same four-corner move powers image processing
(summed-area tables), block-sum problems, and the 2D dynamic programming that arrives later in
the course.

---

## 2. The story

The sports-day forms came back on Friday, and Nirmala, who has taught Class 8 for nine years, sat
down after lunch to get the one number the sports teacher wanted: how many of her forty-two
students are playing **neither** cricket nor football, because those are the ones he needs for the
ground events.

She had two stacks of forms on the desk. Eighteen had ticked cricket. Fifteen had ticked
football. So: forty-two, minus eighteen, minus fifteen — nine students free for ground events. She
wrote 9 on the slip, and had actually stood up to send it before something itched.

Arjun. She had seen his form in the cricket stack — and she was almost sure she had seen it in her
mind's eye in the football pile too, because the boy plays everything. She sat back down and went
through properly. Seven forms had ticked **both** games.

And there was the itch, caught. When she subtracted the eighteen cricket players, Arjun went out
once. When she subtracted the fifteen football players, Arjun went out *again*. Every both-games
child had been thrown out twice — but each of them is only one child, and only needs removing
once. Her count of nine was seven short of the truth. The both-games seven had to come back in.

Forty-two, minus eighteen, minus fifteen, **plus seven**: sixteen students for the ground events.
She checked it the slow way — went through all forty-two forms, counting the ones with no ticks —
and got sixteen, and felt the particular satisfaction of a shortcut that survives an audit.

She explained it to the sports teacher in one line when he raised an eyebrow at the crossed-out 9:
when you remove two overlapping groups, the overlap leaves twice, so you must invite it back once.
He nodded slowly, the way people do when a small trick turns out to be a law.

---

## 3. The idea in plain English

Nirmala's crossed-out 9 is the bug every candidate writes. Her rule — *the overlap leaves twice,
so invite it back once* — is inclusion-exclusion, and it is the entire content of today's formula.

### The stored object

`prefix[r][c]` holds the sum of the rectangle from the matrix's top-left corner `(0, 0)` down to —
but not including — row `r` and column `c`: the first `r` rows' first `c` columns. As in
[day 037](../day-037-prefix-sums/README.md), the table is one bigger in each direction — a
**sentinel row and column of zeros** along the top and left — so `prefix` for a 5×5 matrix is 6×6,
and rectangles touching the edges need no special case. Everything from yesterday-but-three
carries over: entries live on *boundaries*, and the extra zeros are the reading before anything
was driven.

### Deriving the query, corner by corner

Wanted: the sum of the rectangle from `(r1, c1)` to `(r2, c2)`, both ends inclusive. Four stored
rectangles, all anchored at the top-left corner, do it:

1. Start with everything down to the target's bottom-right: `prefix[r2+1][c2+1]`.
2. Remove the strip **above** the target: `prefix[r1][c2+1]`.
3. Remove the strip to the **left**: `prefix[r2+1][c1]`.
4. The top-left corner block — above *and* left — was inside both strips. It left twice; it is
   Arjun. Invite it back once: `+ prefix[r1][c1]`.

```
sum = prefix[r2+1][c2+1] - prefix[r1][c2+1] - prefix[r2+1][c1] + prefix[r1][c1]
```

Never memorise the four terms; rebuild them. The picture in §4 takes ten seconds to draw, and the
signs fall out of it: one big, two strips minus, one corner plus.

### Building the table is the same formula, smaller

Each build step also uses inclusion-exclusion, on the three neighbours already computed:

```
prefix[r+1][c+1] = matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c]
```

The rectangle ending at `(r, c)` is: this cell, plus the rectangle above, plus the rectangle to
the left — and those two rectangles share their top-left overlap, counted twice, so it comes off
once. Same law, pointing the other way: overlap *entered* twice, so it leaves once. If you can say
both sentences — added twice therefore subtract, subtracted twice therefore add — the whole day is
yours.

### Inclusion-exclusion beyond rectangles

Nirmala's form of the law is worth keeping in its own right, because interviewers ask it bare:
*how many numbers below 100 are divisible by 3 or 5?* — 33 + 20 − 6, the shared multiples of 15
counted twice. *How many strings avoid both patterns?* — total, minus each, plus both. Two
overlapping groups: `|A or B| = |A| + |B| − |A and B|`. The rectangle formula is this law applied
to strips, and the law generalises to three and more sets with alternating signs. One principle,
many costumes — today it wears a matrix.

---

## 4. The picture

The four terms, drawn — this is the picture to rebuild in interviews:

```
 target: rows r1..r2, cols c1..c2          (X = wanted cells)

        c1      c2
     +---------------------+      prefix[r2+1][c2+1]   the big rectangle
     |  A      |    B      |      = A + B + C + X
     |         |           |
  r1 +---------+-----------|      minus prefix[r1][c2+1]  = A + B   (strip above)
     |  C      |  X X X X  |      minus prefix[r2+1][c1]  = A + C   (strip left)
     |         |  X X X X  |
  r2 +---------+-----------+      A left TWICE  ->  plus prefix[r1][c1] = A
     
     X = (A+B+C+X) - (A+B) - (A+C) + A
```

**What to notice:** every term is a rectangle anchored at the top-left corner — the only kind the
table stores — and the algebra on the last line is Nirmala's forms: A is Arjun, subtracted with
the cricket stack and again with the football stack, restored once.

The build step, same law at cell scale:

```
 prefix[r+1][c+1]:              +----------+---+
                                |  P       | Q |     Q = prefix[r][c+1] (above)
   this cell  m                 |          |   |     R = prefix[r+1][c] (left)
   + above    Q  (includes P)   +----------+---+     P = prefix[r][c]   (their overlap,
   + left     R  (includes P)   |  R       | m |         entered twice)
   - overlap  P                 +----------+---+
```

**What to notice:** the overlap `P` arrives inside both `Q` and `R` — *added* twice during the
build, so subtracted once; in the query it is *subtracted* twice, so added once. The sign flips
with the direction; the law does not.

The sentinel frame, sized:

```
 matrix 5×5  ->  prefix 6×6

        0   0   0   0   0   0      <- sentinel row: sum of zero rows
        0   .   .   .   .   .
        0   .   .   .   .   .         queries touching row 0 or col 0
        0   .   .   .   .   .         subtract a stored, honest 0 —
        0   .   .   .   .   .         no ifs, day 037's argument squared
        0   .   .   .   .   .
```

---

## 5. The code, built step by step

### The build

```python
rows, cols = len(matrix), len(matrix[0])
prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
```

The frame of zeros, both directions. Note the list-comprehension build — `[[0] * (cols + 1)] *
(rows + 1)` would alias one row object `rows + 1` times, [day 016](../day-016-2d-arrays/README.md)'s
trap, still live.

```python
for r in range(rows):
    for c in range(cols):
        prefix[r + 1][c + 1] = (matrix[r][c]
                                + prefix[r][c + 1]      # rectangle above
                                + prefix[r + 1][c]      # rectangle left
                                - prefix[r][c])         # their overlap, once
```

Row by row, each entry from three already-finished neighbours — the build order is why iterating
top-left to bottom-right matters.

### The query

```python
def sum_region(r1: int, c1: int, r2: int, c2: int) -> int:
    return (prefix[r2 + 1][c2 + 1]
            - prefix[r1][c2 + 1]        # strip above
            - prefix[r2 + 1][c1]        # strip left
            + prefix[r1][c1])           # corner back in
```

Four lookups, three additions. No loop, no matrix access, any rectangle size.

### The complete solutions

```python
class NumMatrix:
    """LeetCode 304. Build once in O(rows × cols); every rectangle in O(1)."""

    def __init__(self, matrix: list[list[int]]) -> None:
        rows, cols = len(matrix), len(matrix[0])
        self.prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.prefix[r + 1][c + 1] = (matrix[r][c]
                                             + self.prefix[r][c + 1]
                                             + self.prefix[r + 1][c]
                                             - self.prefix[r][c])

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        p = self.prefix
        return (p[row2 + 1][col2 + 1]
                - p[row1][col2 + 1]
                - p[row2 + 1][col1]
                + p[row1][col1])


def matrix_block_sum(mat: list[list[int]], k: int) -> list[list[int]]:
    """LeetCode 1314. For every cell: the sum of the (2k+1)-square around it,
    clamped at the edges — one 2D prefix table, then one O(1) query per cell."""
    rows, cols = len(mat), len(mat[0])
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]
    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = (mat[r][c] + prefix[r][c + 1]
                                    + prefix[r + 1][c] - prefix[r][c])

    answer = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            r1, c1 = max(0, r - k), max(0, c - k)
            r2, c2 = min(rows - 1, r + k), min(cols - 1, c + k)
            answer[r][c] = (prefix[r2 + 1][c2 + 1] - prefix[r1][c2 + 1]
                            - prefix[r2 + 1][c1] + prefix[r1][c1])
    return answer


if __name__ == "__main__":
    m = [[3, 0, 1, 4, 2],
         [5, 6, 3, 2, 1],
         [1, 2, 0, 1, 5],
         [4, 1, 0, 1, 7],
         [1, 0, 3, 0, 5]]
    nm = NumMatrix(m)
    print(nm.sumRegion(2, 1, 4, 3))    # 8
    print(nm.sumRegion(1, 1, 2, 2))    # 11
    print(nm.sumRegion(1, 2, 2, 4))    # 12
    print(nm.sumRegion(0, 0, 4, 4))    # 58 — the whole matrix, edges included

    print(matrix_block_sum([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1))
    # [[12, 21, 16], [27, 45, 33], [24, 39, 28]]
```

`matrix_block_sum` is the pattern's second gear: the prefix table built once, then a *loop of
O(1) queries* — 9 cells, 9 rectangle sums, one table. The clamping (`max`/`min`) is where the
sentinel frame pays again: a block hanging off the edge clamps to a smaller rectangle and the
formula just works.

---

## 6. What it costs

### Build and query, counted

```
build: rows × cols cells, constant work each          -> O(rows × cols) time
store: (rows + 1) × (cols + 1) entries                -> O(rows × cols) space
query: 4 lookups, 3 additions, any rectangle          -> O(1)
```

### Against the alternatives, at 1,000 × 1,000 with 100,000 queries

```
sum each rectangle by loops   : 100,000 × up to 10⁶ cells  ≈ 10¹¹ ops
row-prefixes only (day 037
  per row, sum r2-r1+1 rows)  : 100,000 × up to 1,000 rows ≈ 10⁸ ops
2D prefix                     : 10⁶ build + 100,000 × 4    ≈ 1.4 × 10⁶ ops
```

The middle row is worth knowing: per-row 1D prefixes are the halfway house a candidate invents
under pressure — a real improvement, `O(rows)` per query, and still a thousand times short of the
four-corner answer. Name it as the stepping stone, then step past it.

### The number to have ready

> One O(rows × cols) build — a million cells, a million operations — then every rectangle costs
> four lookups. A hundred thousand queries: about 1.4 million operations total, against a hundred
> billion by re-summing. Same deal as 1D: memory and one pass, traded for O(1) answers on a matrix
> that holds still.

---

## 7. The traps

### The near-miss: forgetting the add-back

Drop the fourth term — the most common 2D error in existence:

```python
return p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1]     # no + p[r1][c1]
```

```
0
```

On the §5 matrix, region `(2,1)-(4,3)` should be 8; this returns 0, because the corner block —
worth exactly 8 here — left twice and was never invited back. The wrongness is data-dependent:
regions touching the top or left edges have an empty corner and come out *right*, so casual tests
pass and interior queries lie. **Rebuild the picture, read off the signs** — Nirmala's nine stood
up from the desk before the itch caught it.

### The real error: no sentinel frame

Store the prefix table the same size as the matrix and query a region starting at row 0:

```python
prefix = [[...]] # rows × cols, no zero frame
return prefix[r2][c2] - prefix[r1 - 1][c2] - prefix[r2][c1 - 1] + prefix[r1 - 1][c1 - 1]
```

With `r1 = 0`, `prefix[-1][...]` reads the **bottom row** — the same silent negative-index wrap as
[day 037](../day-037-prefix-sums/README.md), now with two chances per query to trigger it. And the
build without a frame needs three `if` guards per cell for its missing neighbours. The frame of
zeros deletes all of it: build with no guards, query with no guards, wrong answers with no route
in. Day 037's sentinel argument, squared — literally.

### The real error: the aliased rows

```python
prefix = [[0] * (cols + 1)] * (rows + 1)      # one row object, many names
prefix[1][2] = 5
print(prefix[3][2])
```

```
5
```

Every "row" is the same list, so the build smears each row's values over all of them and the
table is garbage — [day 016](../day-016-2d-arrays/README.md)'s trap, and 2D prefix sums are where
it classically resurfaces. Always the comprehension: `[[0] * (cols + 1) for _ in range(rows + 1)]`.

### The near-miss: mixing the two index worlds

The formula lives in *prefix* coordinates (`r2 + 1`), the clamping in *matrix* coordinates
(`min(rows - 1, r + k)`). Blur them — clamp with `min(rows, r + k)` — and the bottom edge reads
one row too many; blur the other way and every block loses its last row. The discipline that
prevents it: convert **once**, at the formula's brackets — every `prefix[...]` index is a matrix
index plus one on the bottom-right terms, verbatim — and never let a `+ 1` drift anywhere else.

### The contract corner: inclusive ends, again

LeetCode 304's `(row2, col2)` is inclusive. [Day 039](../day-039-difference-arrays/README.md)'s
question — last meal or last night — applies in two dimensions now, and an exclusive-end variant
shifts two of the four `+ 1`s. Ask once, then anchor on the sentence from day 037, upgraded:
*through the bottom-right, minus the strips before the top and left, plus the corner before both.*

---

## 8. In the interview

### How it gets asked

- *"Answer many rectangle-sum queries on a fixed matrix."* — LeetCode 304, the direct form.
- *"For every cell, the sum of the k-neighbourhood around it."* — LeetCode 1314; the table plus a
  loop of O(1) queries, with edge clamping.
- *"How many integers under N are divisible by a or b?"* — inclusion-exclusion bare, no matrix
  anywhere.
- *"Count the submatrices whose sum equals k."* — the escalation: fix a pair of rows, collapse
  columns to a 1D array, and run [day 038](../day-038-subarray-sum-k/README.md)'s map — 2D prefix
  meeting prefix-plus-map, a genuinely hard follow-up worth recognising by name.

### What to say out loud, in the first ninety seconds

1. **Name the shape and the trade.** *"Many queries, matrix fixed — 2D precompute: O(rows × cols)
   once, O(1) per rectangle."*
2. **Define the stored object.** *"prefix[r][c] is the sum of the first r rows' first c columns —
   one size bigger each way, with a zero frame on top and left so edge queries need no cases."*
3. **Derive, don't recite.** *"Any rectangle: everything through its bottom-right, minus the strip
   above, minus the strip left — and the top-left corner came off twice, so it comes back once.
   That's inclusion-exclusion; I'd rather rebuild it from the picture than trust memory on the
   signs."*
4. **Say the build uses the same law.** *"Each build cell: value plus above plus left minus their
   overlap — added twice, subtracted once."*
5. **Give the numbers.** *"Million-cell build, then four lookups per query — a hundred thousand
   queries land around 1.4 million operations against a hundred billion by re-summing."*

### The follow-ups

**"Prove the four-term formula — why exactly those signs?"**
Name the four disjoint blocks: A is the corner above-and-left of the target, B the strip directly
above, C the strip directly left, X the target. The stored table only knows rectangles anchored at
the origin, and four of them cover the situation: the big one is A + B + C + X, the above-strip is
A + B, the left-strip is A + C, the corner is A. Then it is bookkeeping: start with A + B + C + X,
subtract A + B, subtract A + C — B and C are gone once each, correct, but A has been removed
twice — add A back once and exactly X remains. The general law underneath is inclusion-exclusion —
subtracting two overlapping sets over-subtracts their intersection once — and it is the same law
the build step uses in reverse, where the above-rectangle and left-rectangle *include* their
overlap twice, so it is subtracted. If I ever doubt the signs under pressure, I redraw the
four-block picture and read them off; it is ten seconds and it cannot be misremembered.

**"Now count the submatrices summing to exactly k."**
Recognise it as two known tools composed. Fix a top row and bottom row — O(rows²) pairs. For a
fixed pair, collapse the matrix between them into a 1D array of column sums, where entry c is the
sum of column c from the top row to the bottom row — maintainable incrementally as the bottom row
extends, or read from the 2D prefix table. Now "submatrices spanning these rows summing to k" is
exactly "subarrays of this 1D array summing to k" — day 038's prefix-plus-hash-map, O(cols) per
row pair with the seen-map and its {0: 1} sentinel, negatives welcome. Total: O(rows² × cols),
against O(rows² × cols²) enumerating column pairs too — on a 200×200 matrix, eight million steps
against 1.6 billion. The composition is the answer they want to hear: 2D prefix collapses a
dimension, then the 1D machine finishes — the course's tools stacking rather than a new trick.

**"The matrix gets one cell update between queries. How bad is it?"**
One changed cell dirties every prefix entry below and to its right — from a corner cell, that is
the entire table, so the honest cost is an O(rows × cols) rebuild per update, and patching only
the dirty region is the same order in the worst case. Day 037's escalation, squared. The upgrade
path mirrors 1D: a 2D Fenwick tree gives O(log rows × log cols) for both point-update and
rectangle-query — the four-corner query survives, each corner becoming a tree query — and heavier
machinery (2D segment trees) exists beyond it. I would state the ratio rule before choosing:
rare updates and floods of queries, rebuild and keep O(1) reads; genuinely mixed traffic, 2D
Fenwick; and say the implementation cost out loud, since a 2D Fenwick under interview pressure is
a decision, not a reflex.

### A model answer

> "Many rectangle sums on a fixed matrix — a precompute shape. I'll build a 2D prefix table:
> prefix[r][c] is the sum of the first r rows' first c columns, one size bigger than the matrix
> in each direction with a frame of zeros on the top and left, so rectangles touching the edges
> subtract an honest zero instead of needing special cases — the 1D sentinel argument, squared.
>
> The build is one pass: each entry is its cell, plus the rectangle above, plus the rectangle to
> the left, minus their overlap — the overlap entered twice, so it leaves once.
>
> For a query from (r1, c1) to (r2, c2) inclusive, I'd rather derive than recite: take everything
> through the bottom-right corner; remove the strip above the target; remove the strip to its
> left; and the block that is both above and left has now been removed twice, so it comes back
> once —
>
> ```python
> p[r2+1][c2+1] - p[r1][c2+1] - p[r2+1][c1] + p[r1][c1]
> ```
>
> That plus-term is inclusion-exclusion, and dropping it is the classic bug — edge-touching
> queries still pass, because their corner block is empty, and interior queries quietly lie.
>
> Costs: O(rows × cols) build and space — a million operations on a thousand-square matrix — then
> four lookups per query. A hundred thousand queries: about 1.4 million operations, against a
> hundred billion re-summing, and about a hundred million even with clever per-row 1D prefixes.
>
> Two cautions from the build: construct the table with a comprehension, because multiplying a
> row list aliases one object across all rows and smears the build; and if updates arrive between
> queries, the deal changes — one cell dirties everything below-right, so it's rebuild-if-rare or
> a 2D Fenwick tree at log-times-log, and I'd say which before coding either."

---

## 9. Recall card

- **prefix[r][c] = sum of first r rows × first c columns** — table one bigger each way, zero
  frame top and left; build with `cell + above + left − overlap`.
- **Query = big − strip above − strip left + corner:**
  `p[r2+1][c2+1] − p[r1][c2+1] − p[r2+1][c1] + p[r1][c1]`. Derive from the picture; never trust
  memorised signs.
- **The law: removed twice → add back once; added twice → subtract once.** Inclusion-exclusion —
  the same answer for "divisible by 3 or 5" with no matrix in sight.
- **Costs: O(rows × cols) build, O(1) per rectangle** — 1.4M ops for 100k queries where
  re-summing needs 10¹¹. Updates break the deal → rebuild-if-rare or 2D Fenwick.
- **Two build traps:** `[[0]*(c+1)]*(r+1)` aliases rows (day 016); no zero frame → `prefix[-1]`
  wraps silently (day 037, squared). Comprehension + frame, always.
