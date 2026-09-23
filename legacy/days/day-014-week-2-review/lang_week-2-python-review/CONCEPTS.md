---
day: 14
part: "3.1"
title: "Locate the time a value is chosen"
ids: [PY-14]
level: working
prerequisites: ["Days 8\u201313 function semantics"]
failure: true
---

# Locate the time a value is chosen

Begin with the cold assignment in [README.md](README.md). Read this repair lesson only after
the attempt, or record that you deliberately used help.

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

Classify a function bug by definition time, closure lookup, decoration, or call-time argument binding.

## The story

Three callbacks are meant to label three jobs. When finally invoked, all print the last label. The loop finished successfully; the wrong assumption was when each label would be chosen.

## The idea in plain language

Start with the cold reproduction in the assignment, then read this repair model. Binding
connects a parameter or name to an object. Different mechanisms choose that object at different
times. A regression test must detect the original mistake and verify the intended contract;
printing a plausible result once is not enough. Select one weakness for this review, not six labs.

## Why Krama needs it

[Day 15 iterator protocol](../../day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md) adds another timing question: when state is consumed.

## The source behind it

[Programming FAQ](https://docs.python.org/3.12/faq/programming.html#why-do-lambdas-defined-in-a-loop-with-different-values-all-return-the-same-result), Python 3.12, explains late lookup in loop-created functions. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

| Mechanism | When its choice happens | Repair source |
| --- | --- | --- |
| Argument binding | Each call | [Day 8](../../day-008-first-repeated-value/lang_argument-binding/CONCEPTS.md) |
| Closure free variable | When the body reads it | [Day 9](../../day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) |
| nonlocal assignment | When the statement executes | [Day 10](../../day-010-pair-sum-indices/lang_nonlocal-state/CONCEPTS.md) |
| Decorator application | When the function definition executes | [Day 11](../../day-011-group-anagrams/lang_decorator-metadata/CONCEPTS.md) |
| Decorator configuration | Factory invocation, then decoration, then calls | [Day 12](../../day-012-range-sums/lang_decorator-arguments/CONCEPTS.md) |
| partial arguments | Store references now; combine and bind on call | [Day 13](../../day-013-count-target-subarrays/lang_partial-application/CONCEPTS.md) |

For callbacks made while labels run through 'a' and 'b', an enclosing label binding ends at
'b'. Both closures later read that same binding. A default parameter evaluated during each
definition instead stores that iteration's object. Two callbacks now return 'a' and 'b'.
The repair is correct because each stored immutable label has the intended creation-time value.
Making n callbacks takes O(n) time and storage; captured objects can retain much more memory.

## When it breaks

```python
def callbacks(capture):
    result = []
    for label in ["a", "b"]:
        if capture:
            result.append(lambda label=label: label)
        else:
            result.append(lambda: label)
    return result
wrong = [f() for f in callbacks(False)]
fixed = [f() for f in callbacks(True)]
print("late lookup:", wrong, "defaults:", fixed)
try:
    assert wrong == ["a", "b"], "callbacks share the final binding"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert fixed == ["a", "b"]
```

**Line by line:** The factory makes a real enclosing function scope. The two branches isolate late lookup versus a default argument chosen during each lambda definition. Calling after the loop exposes the bug. The same expected list rejects the broken result and accepts the repair.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
late lookup: ['b', 'b'] defaults: ['a', 'b']
AssertionError: callbacks share the final binding
```

## In production

Default capture preserves an object reference, not a deep copy; mutable configuration can still change. Wrapper repairs should preserve exception behavior and metadata where that is part of the contract. In a code review, ask when configuration is bound and who owns captured state. Keep actual reproduction output and interpreter version in your personal notes.

## Check yourself

### Readiness before practice

1. What shared binding caused the wrong output?
2. Why does default capture repair this immutable-label example?
3. What changes if labels are mutable lists?
4. What assertion detects your chosen original bug?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
