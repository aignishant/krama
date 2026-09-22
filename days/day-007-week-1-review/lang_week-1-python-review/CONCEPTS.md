---
day: 7
part: "3.1"
title: "Turn an object-semantics surprise into a regression test"
ids: [PY-07]
level: working
prerequisites: ["Days 1–6 Python experiments"]
failure: true
---

# Turn an object-semantics surprise into a regression test

**Cold assessment first:** reproduce one week-one surprise from memory in [lab.py](lab.py),
repair it, and explain it before opening this lesson. These examples support repair afterwards.

## One-line answer

A useful regression test distinguishes your intended ownership or value contract from the behavior that surprised you.

## The story

You copy a shopping folder, edit the list inside the copy, and later discover the original
list changed too. Checking that the folders have different names would never detect this mistake.

## The idea in plain language

Review starts with a prediction about an object graph: names point at objects and containers
hold references to children. A test must observe the layer whose behavior matters. A value
check can miss shared ownership; an identity check can miss wrong values. The repair is a
contract decision before it is a code edit.

Recognize an incomplete explanation when it says only “Python passes by reference” or “copy
fixes it.” Name the shared object, the operation that changes it, and the assertion that detects
the consequence. Binding, mutation, copying, equality, and truth ask different questions.

## Why Krama needs it

[Argument binding](../../day-008-first-repeated-value/lang_argument-binding/CONCEPTS.md) builds
on the same name-to-object model. Binding a supplied list to a parameter does not confer ownership.

## The source behind it

The review synthesizes the linked prior lessons. [5. Data Structures](https://docs.python.org/3.12/tutorial/datastructures.html)
(`spec:python-3.12-data-structures`, checked 2026-09-22) describes list copying; the graph and
failure fixture below are original experiments with a one-level nested list of integers.

## The mechanism

### Worked trace

Use this repair index after attempting from memory:

| Lesson | Question your test must separate |
| --- | --- |
| [Identity and equality](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) | Same object or equal contents? |
| [Copying](../../day-002-find-the-first-maximum/lang_shallow-and-deep-copies/CONCEPTS.md) | Which mutable layer is independent? |
| [Defaults](../../day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md) | Does a second call inherit state from the first? |
| [Hash and equality](../../day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md) | Do equal keys have equal hashes, stable while stored? |
| [Truth and absence](../../day-005-merge-sorted-arrays/lang_truth-and-sentinels/CONCEPTS.md) | Is a valid false value being replaced? |
| [Mutation contracts](../../day-006-best-single-trade/lang_mutation-contracts/CONCEPTS.md) | What may the caller observe changing? |

```text
template -> outer A -> child C [2]
copy     -> outer B -> child C [2]       before repair: shared child
copy     -> outer B -> child D [2]       required for independent child edits
```

On the first graph, appending 5 through B changes C, so A observes `[2, 5]` too. On the second,
only D changes. If the contract only promises independent outer membership, the first graph is
valid. If it promises independent child edits, it is insufficient. Correctness is relative to
that promise. Copying exactly the mutable layer needed makes the second graph without claiming
that arbitrary deep resources can be safely cloned.

## When it breaks

```python
template = [[2]]
copied = template.copy()
assert copied is not template
copied[0].append(5)
try:
    assert template == [[2]], "the nested child is still shared"
except AssertionError as error:
    print(f"AssertionError: {error}")
template = [[2]]
copied = [child.copy() for child in template]
copied[0].append(5)
assert template == [[2]] and copied == [[2, 5]]
assert copied[0] is not template[0]
print("independent child edit: PASS")
```

**Line by line:** the initial identity assertion passes because only the outer list is new.
The child edit exposes the contract violation. A fresh fixture avoids confusing old damage with
the repair. Copying each child creates the required second graph for this schema. Content and
child identity assertions detect both the visible regression and its ownership cause.

Author verification on Python 3.12.10, 2026-09-22:

```text
AssertionError: the nested child is still shared
independent child edit: PASS
```

## In production

Keep the smallest input and sequence of calls that exposes the defect. Mutable-default bugs,
for example, often require two calls; a one-call test can pass accidentally. State limitations:
the child-copy repair above is O(total copied references) time and space and handles this known
two-level shape, not arbitrary nesting. Extra copying may be unnecessary when shared ownership
is intentional. A reviewer should ask which layer must be independent and who pays to copy it.

## Check yourself

### Readiness after repair

1. Which passing assertion in the broken example gave false confidence?
2. Which contract would make shallow copying sufficient?
3. Can you reproduce and explain a different week-one surprise without reopening the lesson?

Run this example only after the cold attempt. The weekly gate needs your own prediction, real
failure, repair, regression test, and spoken explanation. Record help and remaining uncertainty
in [NOTES.md](NOTES.md); 3 predict + 8 experiment + 4 explain/test minutes is still the budget.

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-007-week-1-python-review)
