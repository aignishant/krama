---
day: 62
track: practice
title: "Practice — Sets: membership, deduplication, and the O(1) habit"
status: written
---

# Day 062 · Practice

**DSA topic:** Sets: membership, deduplication, and the O(1) habit
**System design topic:** Design principles revision and interview questions

---

## Code these, in this order

One rule for the whole set: **write the O(n²) version first, then delete the inner loop.** Doing it
in that order twice is what builds the reflex. Doing it in that order in an interview is what lets
you say "the brute force is quadratic, and here is why I do not need it".

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Contains Duplicate | LeetCode 217 (Easy) | The seen set in its simplest form, and whether you know why `len(set(x)) < len(x)` behaves differently on early duplicates. |
| 2 | Intersection of Two Arrays | LeetCode 349 (Easy) | Set operators instead of a nested loop, and whether you noticed the question is about distinct values. |
| 3 | Happy Number | LeetCode 202 (Easy) | A set used to detect a cycle, not a duplicate — the same tool answering a different question. |
| 4 | Longest Consecutive Sequence | LeetCode 128 (Medium) | Whether you can defend an inner `while` loop that is bounded in total rather than per iteration. |

### On problem 2, notice which "intersection" you were asked for

`[1, 2, 2, 1]` and `[2, 2]` gives `[2]`, not `[2, 2]`. LeetCode 350 is the same question with
multiplicities kept, and it needs a `Counter`, not a set. Solve 349, then say in one sentence what
you would change for 350. That sentence is tomorrow's lesson.

### On problem 3, say what the set is holding

It is not holding duplicates in the input. It is holding *states you have already visited*, and the
repeat means you are going round in a circle forever. Then answer this: the fast-and-slow pointer
method from [day 030](../day-030-fast-and-slow/README.md) solves it in O(1) space. Say which one you
would give first in an interview and why.

### On problem 4, break it on purpose before you submit

Write it without the `if number - 1 in number_set: continue` guard. Confirm it passes the sample
cases. Then run it on `list(range(50000))` and watch it stop being an answer.

### The membership drill

Time each of these on 20,000 distinct integers, then say which complexity each one is:

1. `x in a_list`
2. `x in a_set`
3. `x in a_dict`
4. `x in a_dict.keys()`
5. `x in a_dict.values()`
6. `x in a_tuple`
7. `x in a_string` (with string data)

Two of those seven are O(n) and look exactly like the O(1) ones at the call site. Name them, and say
what the ratio was at n = 20,000.

### The seen-set drill

For each question, say whether the answer is a set, a dictionary, or neither, and give the reason in
one sentence:

1. Does this list contain a duplicate?
2. Which element is the first duplicate?
3. How many times does each element appear?
4. Which two numbers add up to the target? (return their positions)
5. Which usernames are in file A but not file B?
6. Has this state occurred before in the simulation?
7. What was the last value I saw for this key?
8. Which of these strings are anagrams of each other?

Three of the eight need a dictionary because presence is not enough. Name them and say what extra
thing each one needs to remember.

### The deduplication drill

Given `["ravi", "asha", "ravi", "meena", "asha", "ravi"]`, produce each of the following, and say
which tool you used:

1. The distinct names, order irrelevant.
2. The distinct names, in first-seen order.
3. The distinct names, sorted.
4. The names that appear more than once.
5. The names that appear exactly once.
6. The count of distinct names, without building a list.

Then say why `list(set(names))` gave you a different order the second time you opened a fresh
interpreter, and what that would do to a submission.

### The unhashable drill

Trigger each error, read the exact text, and give the one-line fix:

1. `{1, 2}.add([3])`
2. `set([{"a": 1}])`
3. `{1, 2} | [3]`
4. `{"a"} < ["a"]`
5. A `for x in s:` loop that calls `s.add(...)` inside it.
6. `{[1, 2], [3, 4]}`

Then rewrite 6 so it works, twice — once where the order inside each group matters and once where it
does not.

### The space drill

1. Build a list of 1,000,000 integers and measure its memory.
2. Build a set of the same integers and measure its memory.
3. Compute the ratio, and say where the extra bytes went — name the three reasons.
4. Now answer, out loud: the interviewer says "same problem, O(1) extra space". Give both
   alternatives, with their complexities and their conditions.
5. Say which of your two alternatives modifies the input, and why that is a question you must ask
   before choosing it.

### The critique drill

Here is the class from today's design lesson, reproduced so you can work on it without scrolling.

```python
# reporting/report_manager.py
import csv
import smtplib
import psycopg
from decimal import Decimal
from datetime import date

TAX_RATE = None   # set at startup by main.py


class ReportManager:
    def __init__(self, conn: psycopg.Connection):
        self.conn = conn

    def generate(self, month: date, kind: str, email: bool = False,
                 as_csv: bool = False, include_tax: bool = True,
                 dry_run: bool = False) -> str:
        ...
```

Work through the six passes in order and write down what each one gives you:

1. Read the imports. How many worlds, and which teams own them?
2. Say the class in one sentence. Count the "and"s.
3. Read the signature. How many boolean combinations? How many are meaningful? Which one is
   nonsense but compiles?
4. Find the dependency-inversion violation, and say precisely why passing the connection in is not
   enough to fix it.
5. Find the common coupling. Name two concrete things it breaks.
6. Find the message chain. How many classes does that one line depend on?
7. Which principle does the `if kind ==` chain point at, and what single question decides whether
   you should act on it?
8. Rank every finding. Which one first, and what is your reason?
9. Name one thing you would deliberately leave alone, and defend it.
10. Say what command you would run before changing anything, and what result would change your mind.

### The contradiction drill

For each pair, say which principle wins, and give the deciding question:

1. DRY versus single responsibility, on two identical validators owned by two teams.
2. Open/closed versus KISS, on a three-branch `if` over a closed set.
3. Interface segregation versus discoverability, on a six-method repository.
4. Dependency inversion versus YAGNI, on a database that will never be swapped.
5. Extract-the-duplicate versus leave-it, on the second occurrence of a piece of code.

Two of the five have the same deciding question underneath. Name it.

### The "explain SOLID" drill

Answer this in sixty seconds, out loud, three times, and make each attempt shorter than the last:

*Explain SOLID.*

Rules for the attempt: one running example throughout, no reciting of five definitions in a row, and
the last sentence must say what all five have in common. If you find yourself saying "the S stands
for", start again.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the duplicate. Now do it in one pass.*
   The brute-force count first with a real number at n = 10,000, then the seen set with its
   invariant stated, then the time and extra space, then the O(1)-space alternative volunteered
   before it is asked for.

2. *Here is a class. Which principles does it violate?*
   The one-sentence description with the "and"s counted, three findings with evidence rather than
   labels, a ranking with a reason, one thing you would leave alone, and the command you would run
   first.

3. *Why is the inner `while` loop in longest-consecutive not quadratic?*
   Bounded in total rather than per iteration, each value stepped over by exactly one run's walk,
   n outer checks plus n total inner steps — and the input that breaks it without the guard.

---

## Before you move on

- [ ] I wrote the seen-set loop from memory and stated its invariant in one sentence.
- [ ] I timed `x in list` against `x in set` at n = 20,000 and can quote the ratio.
- [ ] I broke longest-consecutive by removing the guard, and found the input that exposes it.
- [ ] I can say why the inner `while` loop is O(n) in total.
- [ ] I triggered `TypeError: unhashable type: 'list'` and fixed it two different ways.
- [ ] I can give both O(1)-space alternatives, with complexities and conditions.
- [ ] I critiqued `ReportManager` through all six passes and ended with a ranking.
- [ ] I can name one thing in that class I would deliberately not change, and defend it.
- [ ] I answered all three questions above out loud.
