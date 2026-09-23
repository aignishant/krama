---
day: 47
track: practice
title: "Practice — Minimise the maximum: the capacity family"
status: written
---

# Day 047 · Practice

**DSA topic:** Minimise the maximum: the capacity family
**System design topic:** Polymorphism

---

## Code these, in this order

For every problem, **ask the direction question out loud before writing anything**: does more of this
quantity make the task easier or harder? Write the answer down. Then the range, the check, and the
monotonicity sentence — then the loop, copied unchanged.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Minimized Maximum of Products Distributed to Any Store | LeetCode 2064 (Medium) | The gentlest minimise-the-maximum, with a ceiling-division check. |
| 2 | Split Array Largest Sum | LeetCode 410 (Hard) | Whether you reach for binary search instead of dynamic programming. |
| 3 | Magnetic Force Between Two Balls | LeetCode 1552 (Medium) | The mirror: maximise the minimum, and the sort you must not forget. |
| 4 | Divide Chocolate | LeetCode 1231 (Hard) | The same mirror behind deliberately confusing wording. |

### On problem 1, get the ceiling right

`(q + limit - 1) // limit` is the number of stores a quantity of `q` needs at a limit of `limit`.
Check it by hand on `q = 11, limit = 3`: four stores, not three. Then confirm `lo = 1` and not 0 by
running the check with `limit = 0` and collecting the
`ZeroDivisionError: integer division or modulo by zero`.

### On problem 2, write the DP first, then throw it away

Spend ten minutes writing the `O(n²k)` dynamic-programming solution. Get it right or get it nearly
right — it does not matter. Then write the binary search version and time both on a thousand elements
with k = 50. Say the ratio out loud. Having felt the difference once is what makes you reach for the
right tool under pressure, and being able to say "there's a DP at O(n²k) and I'm not using it because"
is stronger than not knowing it exists.

### On problem 3, break it two ways deliberately

First, run it on unsorted input and watch the answer come out wrong with no error. Then run the
version that uses the minimise-the-maximum direction — `if can_place(mid): hi = mid` — and watch it
return 1 every time. Say which failure each one is: a broken precondition on the check, and a search
pointed at the wrong end. They look the same from the outside and they are completely different bugs.

### On problem 4, translate the wording first

Before coding, rewrite the problem in your own words as a decision question with a limit in it. It is
"can I cut the bar into at least k+1 pieces, every piece summing to at least s?" — and once that
sentence exists the code is problem 3 with a different check. If you cannot produce that sentence,
you do not understand the problem yet, and no amount of coding will fix that.

### The direction drill

For each, say **easier or harder**, therefore **first True or last True**, in under five seconds:

1. A bigger ship capacity, with a day limit.
2. A bigger required gap between placed items.
3. A faster eating speed, with an hour limit.
4. A bigger allowed part sum, with a part-count limit.
5. A bigger minimum sweetness per piece, with a piece-count target.
6. A bigger budget, maximising items bought.

### The translation drill

Turn each optimisation phrase into a `works(x) -> bool` sentence, out loud, in one line each:

1. "Minimise the largest part sum over k contiguous parts."
2. "Maximise the smallest distance between c placed items."
3. "Minimise the maximum products any of n stores handles."
4. "Maximise the smallest piece when cutting into k+1 pieces."
5. "Minimise the number of days to finish, given a fixed daily rate."

Then say which of the five has a check that needs its input sorted first, and why the others do not.

### The greedy-proof drill

Say the exchange argument out loud, in under ninety seconds, for the contiguous-split check: why is
filling each part as full as possible optimal? Then answer the harder half — what exactly breaks when
the parts no longer have to be contiguous, and what is the honest thing to say to an interviewer at
that point?

### The hang drill

Write the mirrored maximise template with `mid = (lo + hi) // 2` and run it. Kill it with Ctrl-C and
read the traceback. Then fix it with the ceiling midpoint. Then delete both and write the
first-False-minus-one version instead, and say why that is the one to keep.

### The switch-removal drill

Take this and refactor it out loud in four minutes:

```python
def notify(user, message, channel):
    if channel == "email":
        smtp.send(user.email, message)
    elif channel == "sms":
        gateway.post(user.phone, message)
    elif channel == "push":
        fcm.push(user.device_token, message)
    else:
        raise ValueError(channel)
```

1. Run the six-step recipe from the lesson, naming each step as you do it.
2. Name the question the switch is answering — that becomes the method name.
3. Say what step six is and why skipping it means the switch comes back next year.
4. Count the edits to add WhatsApp, both ways.
5. Say the one cost you have accepted by refactoring.
6. Then answer the pushback: *"isn't that the same amount of code, just spread out?"*

### The is-it-polymorphism drill

For each, say whether polymorphism is the right tool, or whether an `if` should stay — with the
reason:

1. Four vehicle types, branched on in three separate functions.
2. `if amount > 10000: require_approval()`.
3. Seven days of the week, each with a different opening time.
4. Three payment gateways, with a fourth expected next quarter.
5. `if order.status == "CANCELLED": return`.
6. Two export formats today, and the product manager keeps asking for more.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Split the array into k parts, minimising the largest part sum.*
   The direction question, the decision restatement, the range with reasons, the greedy check, the
   exchange argument, and the DP you are choosing not to write, with numbers.

2. *What is polymorphism? Show me, do not tell me.*
   Write the switch, say what is wrong with it, write the polymorphic version, count the edits both
   ways, and name the cost you accepted.

3. *Maximise the minimum gap. How do you do it without writing a second template?*
   Negate the question, search the first False with `hi + 1`, subtract one — and say what goes wrong
   with the mirrored version if the midpoint does not round up.

---

## Before you move on

- [ ] I asked the direction question before writing code on all four problems.
- [ ] I wrote the DP for LeetCode 410, timed it against the binary search, and can quote the ratio.
- [ ] I broke the placement problem both ways — unsorted input, and the wrong direction — and can tell
      the two failures apart.
- [ ] I made the mirrored template hang, read the traceback, and then chose the version that cannot.
- [ ] I ran the switch-removal recipe on the notifier, including step six.
- [ ] I can sort all six cases into "polymorphism" and "leave the `if`" with a reason each.
- [ ] I answered all three questions above out loud.
