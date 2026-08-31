---
day: 62
track: dsa
title: "Sets: membership, deduplication, and the O(1) habit"
phase: "Hashing: maps and sets"
status: written
---

# Day 062 · DSA — Sets: membership, deduplication, and the O(1) habit

**After today you can:** You replace a nested loop with a set lookup by reflex.

**The interviewer asks it as:** *Find the duplicate. Now do it in one pass.*

---

## 1. What this is, and why they ask it

A **set** is a collection that answers exactly one question quickly: *is this thing already in
here?* It holds no duplicates, it keeps no order, and it stores no values — only the keys. It is the
hash table from [day 060](../day-060-hash-tables/README.md) with the value column deleted, which is
why membership costs O(1) on average and not O(n).

They ask it because the set is the single cheapest upgrade in the whole of interviewing. A very large
number of problems have an obvious O(n²) answer — for every item, look through all the other items —
and a two-line O(n) answer that replaces the inner loop with one membership check. Interviewers use
this deliberately. They give you a problem whose brute force is easy, wait for you to write it, and
then say *now do it in one pass*. The candidates who freeze are the ones who never built the reflex.
The candidates who do well hear "one pass" and immediately reach for a **seen set** — a set that
accumulates what you have already looked at — because that is the answer to a whole family of
questions, not a trick for one of them.

The second reason is that sets are the fastest way to change a complexity in front of an interviewer.
You do not need to redesign anything. You change one line, the nested loop disappears, and you can
explain exactly why the cost fell. That is a very good ninety seconds of interview.

---

## 2. The story

The free eye check-up camp at the school in Vidyaranyapura opened its shutters at eight on a Sunday
morning, and by ten past eight there were already sixty people standing in the sun.

Suresh, who is nineteen and had volunteered mostly because his mother told him to, was put on the
door. His job was simple. Everybody who came in got one free pair of reading glasses at the end. Some
people had worked out that if you went round the building and joined the line again, you got a second
pair. So Suresh had to stop them.

The organisers had sent him everybody's name on his phone. Six hundred and forty names, in the order
people had signed up. So a man would reach the door, say "Rajanna, from Bagalur", and Suresh would
start at the top and scroll. Sometimes the name was near the top and it took four seconds. Usually it
was not. By half past nine he was taking nearly a minute on each person, because he had to start from
the very beginning every single time, and by then he had four hundred names to go past. The line went
out of the gate and down the road. A woman told him, not unkindly, that her son could have done it
faster.

At eleven o'clock the head volunteer came out, looked at the line, and went across the road to the
stationery shop. She came back with a rubber stamp and a small blue ink pad. Forty rupees.

After that, the check was this. Show me the back of your hand. Blue mark, you have already been in.
No mark, come in, and here is your mark.

It took him under a second, and — this is the part Suresh actually noticed — it took him under a
second at four hundred people in exactly the same way it had at ten people. The line was gone by
half past twelve. Two men tried it on and were caught at once, one of them laughing about it.

The only thing it cost was forty rupees and the small nuisance of carrying an ink pad about, which
he had to keep remembering to put down somewhere he would not sit on it.

---

## 3. The idea in plain English

Scrolling the whole list of names is a **linear scan**: to answer one question you touch everything.
The blue stamp is a **set**: you answer the same question with one look, and the number of people
already inside does not change how long the look takes.

Three things came out of the ink pad, and they are the three things a set gives you.

**One: membership is instant.** "Has this person been in?" costs the same at person 400 as at person
10. In code that is the `in` operator on a set.

**Two: duplicates cannot happen.** Stamping a hand that is already stamped changes nothing. A set
holds each element once, no matter how many times you add it.

**Three: it costs extra memory.** The ink pad had to be bought and carried. A set has to be built
and held in memory alongside the data you already have.

### What a set is, precisely

A set is a hash table that stores keys and no values. When you write `seen.add(x)`, Python computes
`hash(x)`, turns that into a slot, and records that the slot is taken. When you write `x in seen`, it
computes the same hash, goes straight to that slot, and compares. There is no searching. Everything
you learned about hash tables on [day 060](../day-060-hash-tables/README.md) — the hash function, the
load factor, the resize — is happening underneath, unchanged.

Two consequences follow immediately, and both get asked about.

**Elements must be hashable.** Numbers, strings and tuples can go in a set. Lists and dictionaries
cannot, because they can be changed after you put them in, which would make them unfindable. This is
the same rule as dictionary keys.

**There is no order.** A set does not remember the order you added things in. This matters when you
deduplicate, and it catches people out.

### Making one

```python
seen: set[int] = set()          # the empty set. Not {} — that is an empty dict.
letters = {"a", "b", "c"}       # a set literal
digits = set("hello")           # from any iterable: {'h','e','l','o'}
```

`{}` is the one that bites. An empty pair of braces is an empty **dictionary**, because dictionaries
got the syntax first. The empty set has to be written `set()`.

### The four operations you actually use

```python
seen.add(7)          # put 7 in. Doing it twice is harmless.
seen.discard(7)      # take 7 out. No error if it was not there.
seen.remove(7)       # take 7 out. KeyError if it was not there.
7 in seen            # True or False, in O(1) average
```

`add` and `in` cover perhaps ninety percent of interview use. `discard` is the safe removal;
`remove` is the one that raises.

### The set operations

Sets also do the things you drew in school with two overlapping circles, and they are genuinely
useful in interviews when the question is about two collections.

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
a | b    # union            -> {1, 2, 3, 4, 5}   in either
a & b    # intersection     -> {3, 4}            in both
a - b    # difference       -> {1, 2}            in a, not in b
a ^ b    # symmetric diff   -> {1, 2, 5}         in exactly one
a <= b   # subset           -> False
```

Every one of those runs in time proportional to the size of the smaller set, not the product of the
two. "Which usernames appear in both files" is `a & b`, and it is O(n), not O(n²).

### The seen-set pattern

This is the shape you will write more than any other. Walk the data once. Before dealing with each
element, ask the set whether you have met it. Then add it.

```python
seen = set()
for item in items:
    if item in seen:
        ...          # this is a repeat — do whatever the problem wants
    seen.add(item)
```

Read the loop and notice the invariant, in the sense of
[day 028](../day-028-opposite-ends/README.md): **at the top of every iteration, `seen` holds exactly
the elements before the current one.** That sentence is the whole pattern, and saying it out loud in
an interview is worth more than writing the loop quickly.

### Deduplicating, and the order trap

```python
names = ["ravi", "asha", "ravi", "meena", "asha"]
list(set(names))            # ['meena', 'asha', 'ravi'] — order is not yours
list(dict.fromkeys(names))  # ['ravi', 'asha', 'meena'] — first-seen order kept
```

`set(names)` is the fast, correct way to get the distinct values when you do not care about order.
When order matters — and in interviews it very often does, because the expected output is written in
the original order — use `dict.fromkeys`, which keeps insertion order because Python dictionaries
have done so since version 3.7. Say which one you are choosing and why. It is a small thing that
reads as care.

---

## 4. The picture

Two ways to answer "have I seen this before?", drawn side by side on the same input.

```
 input   [ 4 , 7 , 2 , 7 , 9 ]
 index     0   1   2   3   4

 (a) the nested loop: for element 3, compare with everything before it
     ------------------------------------------------------------
     i = 3  (value 7)
              j = 0 -> 4 vs 7   no
              j = 1 -> 7 vs 7   YES
     3 comparisons for one element. Element 400 would need 400.

 (b) the seen set: for element 3, ask once
     ------------------------------------------------------------
     seen = { 4 , 7 , 2 }
     "is 7 in seen?"  ->  hash(7) -> slot 5 -> occupied -> YES
     1 look-up for one element. Element 400 also needs 1.
```

Notice what changes and what does not. In (a) the work per element grows as the input grows. In (b)
it does not. That is the entire difference between O(n²) and O(n), and it is the sentence to say out
loud.

Now watch the set fill up as the loop runs. The column under `seen before it` is what the set holds
*before* that element is looked at.

```
 step   element   seen before it        answer
 ----   -------   -------------------   ---------------
   0       4      { }                   not seen
   1       7      { 4 }                 not seen
   2       2      { 4, 7 }              not seen
   3       7      { 4, 7, 2 }           SEEN  <- the duplicate
   4       9      { 4, 7, 2 }           not seen   (7 was already in)
```

Notice row 4. Adding 7 a second time did nothing to the set — the size stayed at three. That is
duplicates being impossible, not duplicates being filtered afterwards.

---

## 5. The code, built step by step

Four problems, each one a small step up. The last is the problem interviewers actually use to find
out whether you understand sets or have only memorised them.

### Step 1 — does this contain a duplicate at all?

```python
def has_duplicate(numbers: list[int]) -> bool:
    seen: set[int] = set()
    for number in numbers:
        if number in seen:
            return True
        seen.add(number)
    return False
```

Six lines. Walk once, ask, add. It returns as soon as it finds the first repeat, so on
`[1, 1, 2, 3, ..., 999999]` it stops after two elements instead of reading a million.

There is a one-line version, and you should know both:

```python
def has_duplicate_short(numbers: list[int]) -> bool:
    return len(set(numbers)) < len(numbers)
```

If the distinct count is smaller than the total count, something repeated. It is elegant, and it is
the one to mention — but say the difference out loud: the short version always reads the whole input
and always builds the whole set, so on `[1, 1, ...]` with a million elements the loop version stops
after two and this one does not. Same O(n), very different real behaviour.

### Step 2 — which element repeats first?

```python
def first_duplicate(numbers: list[int]) -> int | None:
    seen: set[int] = set()
    for number in numbers:
        if number in seen:
            return number
        seen.add(number)
    return None
```

Almost the same code, returning the value instead of `True`. The reason it is worth writing
separately is the ambiguity hiding in "first". On `[2, 1, 3, 1, 2]`, is the answer `1` — whose second
copy comes first — or `2` — whose first copy comes first? This code gives `1`. **Ask the interviewer
which one they mean.** That question is one of the cheapest points available in the whole interview,
because the two answers need genuinely different code.

### Step 3 — what do two collections share?

```python
def common(first: list[int], second: list[int]) -> list[int]:
    return list(set(first) & set(second))
```

Building both sets costs O(n + m). The intersection then walks the smaller one and checks the larger,
so the whole thing is linear. The nested-loop version is O(n × m): with two lists of 10,000 that is
100,000,000 comparisons against 20,000 operations.

If you only need to check one list against another, do not build a set of the first as well:

```python
def common_streaming(first: list[int], second: list[int]) -> list[int]:
    lookup = set(second)                       # build once
    return [x for x in first if x in lookup]   # then one O(1) check each
```

This keeps duplicates from `first` and keeps its order, which the set version does not. Two
different answers to two different questions. Say which one you are giving.

### Step 4 — the longest run of consecutive numbers

Given `[100, 4, 200, 1, 3, 2]`, the longest run of consecutive integers is `1, 2, 3, 4`, so the
answer is 4. The order in the input means nothing. This is LeetCode 128, and it is asked constantly,
because the obvious answer is to sort — O(n log n) — and the interviewer wants O(n).

Start with the set.

```python
number_set = set(numbers)
```

Now you can ask "is 57 present?" instantly, which is the only question this problem needs.

The naive next step is: for every number, walk upward while the next one exists.

```python
for number in number_set:
    length = 1
    while number + length in number_set:
        length += 1
```

This is correct and it is too slow. On `[1, 2, 3, ..., n]` it starts at 1 and walks n steps, then
starts at 2 and walks n-1 steps, and so on — O(n²). This is the step people get wrong, and it looks
right because every individual line is right.

The fix is one condition, and it is the whole idea of the problem: **only start walking from a number
that begins a run.**

```python
for number in number_set:
    if number - 1 in number_set:
        continue                     # not a start — somebody else will count this run
    ...
```

If `number - 1` exists, then `number` is in the middle of a run, and that run's true starting point
will do the walking. So each run is walked exactly once, by its smallest element.

Put the two together:

```python
for number in number_set:
    if number - 1 in number_set:
        continue
    length = 1
    while number + length in number_set:
        length += 1
    best = max(best, length)
```

### The complete solution

```python
def longest_consecutive(numbers: list[int]) -> int:
    """Length of the longest run of consecutive integers, in O(n) time.

    Order in `numbers` is irrelevant. Duplicates are ignored, because the set
    holds each value once.
    """
    number_set: set[int] = set(numbers)
    best = 0

    for number in number_set:
        # Only a number with no left-hand neighbour starts a run. Every other
        # number sits in the middle of a run that its own start will walk.
        if number - 1 in number_set:
            continue

        length = 1
        while number + length in number_set:
            length += 1

        best = max(best, length)

    return best


def has_duplicate(numbers: list[int]) -> bool:
    """True if any value appears twice. Stops at the first repeat."""
    seen: set[int] = set()
    for number in numbers:
        if number in seen:
            return True
        seen.add(number)
    return False


def first_duplicate(numbers: list[int]) -> int | None:
    """The value whose second occurrence appears earliest, or None."""
    seen: set[int] = set()
    for number in numbers:
        if number in seen:
            return number
        seen.add(number)
    return None


def deduplicate_keeping_order(items: list[str]) -> list[str]:
    """Distinct values in first-seen order. set() alone would lose the order."""
    return list(dict.fromkeys(items))


if __name__ == "__main__":
    print(longest_consecutive([100, 4, 200, 1, 3, 2]))          # 4
    print(longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9
    print(longest_consecutive([]))                              # 0
    print(has_duplicate([1, 2, 3, 1]))                          # True
    print(first_duplicate([2, 1, 3, 1, 2]))                     # 1
    print(deduplicate_keeping_order(["ravi", "asha", "ravi"]))   # ['ravi', 'asha']
```

Note the empty-input case returns 0 because `best` starts at 0 and the loop never runs. Say that out
loud rather than adding an `if not numbers` guard — the interviewer is watching for whether you
checked, not for the guard itself.

---

## 6. What it costs

### The nested loop, counted

For `has_duplicate` written the brute-force way — for each element, compare with every earlier one —
element 0 does 0 comparisons, element 1 does 1, element 2 does 2, and so on to element n-1, which
does n-1.

```
 0 + 1 + 2 + ... + (n-1)  =  n(n-1)/2
```

At n = 10,000 that is `10000 × 9999 / 2 = 49,995,000` comparisons. Roughly fifty million.

### The set version, counted

The loop runs n times. Each iteration does one membership check and one add. Both are O(1) on
average, so the total is `n × constant`.

At n = 10,000 that is 10,000 checks and at most 10,000 adds — call it 20,000 operations. **Fifty
million against twenty thousand: a factor of 2,500.** That is the number to quote, not the letters.

### `longest_consecutive`, counted properly

This is the one that gets probed, because the code has a `while` loop inside a `for` loop and it
still is not quadratic. Count it as two separate things.

The `for` loop runs once per distinct number: n iterations. Each does one membership check,
`number - 1 in number_set`.

The `while` loop is the interesting half. It only runs for numbers that start a run. Across the whole
execution, each number is stepped over by exactly one `while` loop — the one belonging to its run's
smallest element. So all the `while` loops together do at most n steps, however they are distributed.

```
 for-loop checks:        n
 all while-loop steps:   n  (total, across every run)
 -------------------------------------------------
 total:                  2n   ->  O(n)
```

That is the sentence: *the inner loop is not bounded per iteration, it is bounded in total.* Say it
exactly like that.

### Space

`set(numbers)` holds up to n distinct values. That is **O(n) extra space** — extra, not total, so on
top of the input you were given.

It is not free, and it is worth being honest about. A Python `set` of a million small integers is
roughly 32 MB, against about 8 MB for the same integers in a `list`, because a set stores hash
values, keeps its table two-thirds empty by design, and holds pointers to objects. If the interviewer
says "now do it in O(1) space", the set is exactly what they are taking away, and the answer is
usually sorting instead — O(n log n) time for O(1) extra space. That trade is
[day 066](../day-066-when-hashing-is-wrong/README.md)'s whole subject.

---

## 7. The traps

### Trap 1 — the seen "set" that is secretly a list

This is the commonest one, and it is invisible on the screen because the code reads identically.

```python
def has_duplicate_slow(numbers: list[int]) -> bool:
    seen = []                      # <- a list
    for number in numbers:
        if number in seen:         # <- looks exactly the same
            return True
        seen.append(number)
    return False
```

`in` works on a list too. It just scans it. So this is O(n²) wearing the clothes of an O(n) solution,
and it will pass every small test you write.

Measure it once and you will never do it again. With 20,000 distinct integers:

```
 seen = set()    0.004 s
 seen = []       2.9 s
```

Roughly seven hundred times slower, on an input small enough to fit on a screen. `in` on a list is
O(n); `in` on a set or a dict is O(1). The operator is the same; the structure is the whole story.

### Trap 2 — `longest_consecutive` without the start check

Drop the `if number - 1 in number_set: continue` line and the code still returns the right answer on
every example in the problem statement. It fails on time, not on correctness, which is the worst kind
of failure because your tests pass.

The input that kills it is the most boring one imaginable: `list(range(100000))` — a single run of a
hundred thousand consecutive numbers.

```
 with the guard:      0.02 s
 without the guard:   about 100000^2 / 2 = 5 x 10^9 steps — you will not wait for it
```

The interviewer's follow-up is *what is the worst case of that loop?*, and if you have not thought
about it you will say O(n) and be wrong.

### Trap 3 — unhashable elements

Try to put a list into a set and Python stops you:

```python
>>> {1, 2}.add([3])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'list'
```

Same for a dictionary:

```python
>>> set([{"a": 1}])
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unhashable type: 'dict'
```

This bites in real problems whenever the thing you want to remember is a group rather than a single
value — deduplicating rows, remembering which pairs you have used, grouping anagrams. **The fix is a
tuple.** `(2, 5)` is hashable; `[2, 5]` is not. For an unordered group, `frozenset` is the hashable
set:

```python
seen_pairs: set[tuple[int, int]] = set()
seen_pairs.add((2, 5))                    # fine
seen_groups: set[frozenset[str]] = set()
seen_groups.add(frozenset({"a", "b"}))    # fine, and order-independent
```

### Trap 4 — mixing sets and lists in the operators

```python
>>> {1, 2} | [3]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for |: 'set' and 'list'
```

The operators demand sets on both sides. The method forms are more forgiving — `{1, 2}.union([3])`
works and gives `{1, 2, 3}` — because they accept any iterable. Know both, and know why one raises.

### Trap 5 — changing a set while iterating over it

```python
>>> s = {1, 2, 3}
>>> for x in s:
...     s.add(x + 10)
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RuntimeError: Set changed size during iteration
```

Identical in spirit to the dictionary version from [day 060](../day-060-hash-tables/README.md). If
you must add while walking, iterate over a copy — `for x in list(s):` — or collect the additions and
apply them after the loop.

### Trap 6 — assuming order

```python
>>> list({"ravi", "asha", "meena"})
['meena', 'asha', 'ravi']
```

Run it in a fresh interpreter and the order can differ, because string hashing is randomised per
process ([day 060](../day-060-hash-tables/README.md)). If you return `list(set(x))` from a function
whose expected output is order-sensitive, your submission fails on a test you cannot reproduce
locally. Use `dict.fromkeys` when order matters, or sort the result if the problem asks for sorted
output. Never rely on the order a set gives you, not even for small sets, not even when it looks
stable.

---

## 8. In the interview

### How it gets asked

- *"Does this array contain any duplicates?"* — the warm-up. It is almost never the real question.
- *"Find the first repeating element. Now do it in one pass."* The words **one pass** are the signal.
  They mean: no nested loop, no sort, walk the data once.
- *"Given an unsorted array of integers, return the length of the longest consecutive sequence. Your
  algorithm should run in O(n)."* The complexity is stated in the question, which is the interviewer
  telling you that sorting is not the answer.
- The vague version: *"Two files each have a million user ids. Which ids are in both?"* No complexity
  mentioned, no hint. This one separates people, because you have to notice for yourself that the
  obvious answer is a hundred trillion comparisons.

### What to say out loud, in the first ninety seconds

1. **Restate what makes it hard.** "The brute force is: for every element, look at every other
   element. That is n squared. With a million ids that is 10 to the twelfth comparisons, so it is not
   an answer."
2. **Name the tool before you write it.** "I want to turn the inner loop into a constant-time
   question. A set gives me that — membership in O(1) average, because it is a hash table with no
   values."
3. **State the invariant.** "I will walk the input once, keeping a set of everything I have already
   seen. At the top of each iteration, that set is exactly the elements before the current one."
4. **State the cost before you write.** "Time O(n), extra space O(n). I am buying time with memory,
   and if you want O(1) space I would sort instead and pay O(n log n)."
5. **Ask the one clarifying question that matters.** For duplicates: "when you say the first
   duplicate, do you mean the earliest second occurrence, or the element whose first occurrence is
   earliest?" For anything with output: "does the order of the result matter?"

Then write it. The code is six lines, so most of your value is in steps 1 to 5.

### The follow-ups

**"What is the worst-case time, not the average?"**
O(n) per operation, so O(n²) overall, if every element collides into one bucket. In practice that
needs either a deliberately hostile input or a bad custom hash, and Python randomises string hashing
per process to stop the first — see [day 061](../day-061-collisions/README.md). Then say the honest
part: "I would still quote O(n) average in a design discussion, but I would not quote it for a
service that hashes untrusted keys."

**"Now do it in O(1) extra space."**
"Then I give up the set. If I may modify the input, sorting makes duplicates adjacent, so one pass
after the sort finds them — O(n log n) time, O(1) extra space. If the values happen to lie in a known
small range, say 1 to n, I can mark them in the input itself by negating, which is O(n) time and O(1)
extra space." Naming both alternatives, with their conditions, is what a strong answer looks like.

**"Why is your inner `while` loop not making that quadratic?"**
"Because it is bounded in total, not per iteration. Only a number with no left-hand neighbour enters
the `while` at all, so every value is stepped over by exactly one run's walk. All the `while` loops
together do at most n steps."

**"Would you use a set or a dictionary here?"**
"A set, because I only need presence. The moment I need to remember *where* I saw it, or how many
times, it becomes a dictionary — the set is the dictionary with the values thrown away. Two Sum is
the classic example: I need the position, so it has to be a map."

### A model answer

Asked: *given an unsorted list of integers, return the length of the longest run of consecutive
integers, in O(n) time.*

> "The obvious approach is to sort and then walk, looking for consecutive values. That is correct and
> it is O(n log n), and since you have asked for O(n), the sort has to go.
>
> The only question this problem actually needs to ask is 'is the number 57 present?'. Order does not
> matter, and duplicates do not matter. A set answers that in constant time, so my first line puts
> everything in a set.
>
> Now, if I take each number and walk upward while the next value exists, I get the right answer but
> the wrong complexity — on the input 1 to n, I start at 1 and walk n steps, then start at 2 and walk
> n minus 1, and so on. That is quadratic.
>
> The fix is to only start walking from a number that begins a run, which I can test in one line: if
> `number - 1` is in the set, this number sits in the middle of a run, so I skip it. Its run will be
> counted by its own smallest element. That means every run is walked exactly once, by its start.
>
> So the cost is n membership checks for the outer loop, plus at most n steps across all the inner
> walks put together — O(n) time. Space is O(n) for the set.
>
> Edge cases: an empty input returns 0, because my best starts at 0 and the loop never runs.
> Duplicates take care of themselves, because the set holds each value once. Negative numbers are
> fine — nothing here assumes the values are positive."

That answer is about ninety seconds spoken, it names the wrong approach and says why it is wrong, and
it gives the complexity argument that the follow-up would otherwise have to drag out of you.

---

## 9. Recall card

- **A set is a hash table with the values deleted.** `in` is O(1) average, duplicates are impossible,
  order does not exist, elements must be hashable — so tuples and `frozenset`, never lists or dicts.
- **The seen-set pattern is the reflex:** walk once, `if x in seen`, then `seen.add(x)`. The
  invariant is *`seen` holds exactly the elements before the current one*. It turns 50,000,000
  comparisons at n = 10,000 into 20,000 operations.
- **`seen = []` is the trap** — `in` on a list is O(n), so identical-looking code runs 700× slower at
  n = 20,000. And `{}` is an empty dict; the empty set is `set()`.
- **Longest consecutive: put it in a set, and only walk from a number whose `number - 1` is absent.**
  Without that guard `range(100000)` is 5 × 10⁹ steps. The `while` is bounded **in total, not per
  iteration** — n outer checks plus n total inner steps.
- **You are trading memory for time** — O(n) extra space, roughly 32 MB per million integers. Asked
  for O(1) space, sort instead (O(n log n)) or mark in place when the range is known. Real errors:
  `TypeError: unhashable type: 'list'`, `RuntimeError: Set changed size during iteration`.
