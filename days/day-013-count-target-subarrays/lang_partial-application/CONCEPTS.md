---
day: 13
part: "3.1"
title: "Partial application stores an argument plan"
ids: [PY-13]
level: working
prerequisites: ["Day 8 argument binding", "Day 9 closures"]
failure: true
---

# Partial application stores an argument plan

Core: explanation, worked trace, and readiness. Production extensions are optional depth;
continue another sitting if needed within the existing track budget.

## One-line answer

partial retains a callable and argument references, then combines them with later arguments when invoked.

## The story

A callback needs the same label on every event. You want to supply that label once while letting the event arrive later, without repeating a wrapper function at every call site.

## The idea in plain language

Partial application specializes a callable by supplying some arguments now. It does not
call the function yet. Stored positional arguments precede new positional arguments; new
keywords override stored keywords. Normal function binding then applies, including conflicts
between positional and keyword values. Review [argument binding](../../day-008-first-repeated-value/lang_argument-binding/CONCEPTS.md).
A [closure](../../day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) executes arbitrary
wrapper code and can read an enclosing binding later. A partial stores argument object
references at construction, not snapshots or a live link to the variable name.

## Why Krama needs it

The [Week 2 Python review](../../day-014-week-2-review/lang_week-2-python-review/CONCEPTS.md) distinguishes capture time, lookup time, and call-time binding.

## The source behind it

[functools — Higher-order functions and operations on callable objects](https://docs.python.org/3.12/library/functools.html#functools.partial), Python 3.12, defines partial and its stored func, args, and keywords. Checked 2026-09-22; see the dated [source ledger](../../../docs/SOURCES.md).

## The mechanism

### Worked trace

With `format_value(prefix, value)`, storing prefix positionally leaves value for the later
call. Storing prefix by keyword and later supplying a positional argument instead binds
prefix twice. Overriding a stored keyword with a new keyword is different: the keyword maps
merge before normal binding. Storing k arguments retains O(k) references and keeps those
objects alive; it does not copy their reachable contents. Calls still incur the wrapped work.

## When it breaks

```python
from functools import partial
def format_value(prefix, value):
    return f"{prefix}:{value}"
tagged = partial(format_value, "job")
print(tagged(7))
keyword_tagged = partial(format_value, prefix="job")
print(keyword_tagged(value=7, prefix="task"))
try:
    keyword_tagged(7)
except TypeError as error:
    print(f"TypeError: {error}")
items = ["old"]
bound = partial(list, items)
items.append("new")
items = ["replacement"]
print("retained object:", bound())
assert bound() == ["old", "new"]
```

**Line by line:** partial stores arguments without invoking format_value. The positional specialization accepts the remaining value. The keyword override replaces the saved prefix; keyword_tagged(7) binds prefix both ways and raises. The final calls distinguish mutation of the saved list from rebinding its former name.

Author verification on Python 3.12.10, 2026-09-22 (teaching evidence, not learner progress):

```text
job:7
task:7
TypeError: format_value() got multiple values for argument 'prefix'
retained object: ['old', 'new']
```

## In production

Use a named wrapper when validation, branching, or exception policy is needed. Stored keywords are overridable configuration, so do not treat them as an authorization boundary. Retained callbacks can prolong object lifetimes. This lesson targets Python 3.12 behavior; newer partial placeholder features are outside its contract.

## Check yourself

### Readiness before practice

1. Which arguments reach the original function in each call?
2. Why is a new keyword override legal but positional duplication an error?
3. Does rebinding a captured variable replace the stored object?
4. When would a closure be clearer?

Run the teaching block in a scratch interpreter, then explain the distinguishing failure aloud.
Use [README.md](README.md) to enter the assignment and record your own evidence.
