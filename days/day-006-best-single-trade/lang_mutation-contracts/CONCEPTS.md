---
day: 6
part: "3.1"
title: "Specify who can observe an edit"
ids: [PY-06]
level: working
prerequisites: ["Aliases", "Shallow copies"]
failure: true
---

# Specify who can observe an edit

Core: trace ownership and test both value and identity. Nested ownership is a short boundary
check; deep-copy policies are optional follow-up. The independent lab stays within 15 minutes.

## One-line answer

A mutation contract states which existing objects may change and which returned objects are new.

## The story

Two people share a shopping list. One asks for a sorted copy to plan a trip. Sorting the shared
sheet instead changes what the other person sees, even if the sorted contents look correct.

## The idea in plain language

A function parameter receives a reference to an object. Changing that object is visible through
other references; rebinding the local parameter does not redirect the caller's name. Review
[aliases](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) and
[copy depth](../../day-002-find-the-first-maximum/lang_shallow-and-deep-copies/CONCEPTS.md)
if that distinction is unclear.

A contract should answer four questions: may the input change, must the output be a fresh
container, may nested children be shared, and does the function retain references after return?
An equal output alone cannot establish these properties. Recognize ownership bugs when unrelated
callers see changed order, cached templates change, or a returned view changes unexpectedly later.

## Why Krama needs it

The DSA local merge returns new storage while its online companion mutates supplied storage.
This distinction also governs [Day 8 argument binding](../../day-008-first-repeated-value/lang_argument-binding/CONCEPTS.md):
binding arguments does not copy their objects.

## The source behind it

[5. Data Structures](https://docs.python.org/3.12/tutorial/datastructures.html)
(`spec:python-3.12-data-structures`, checked 2026-09-22) documents in-place list methods and
their `None` return convention. The following ownership fixture is an original experiment.

## The mechanism

### Worked trace

```text
before: caller ------> list A [3, 1]
        observer ----> list A

in-place sort:        list A [1, 3]       both names see the change
fresh sorted result:  list B [1, 3]       caller's list A can stay [3, 1]
```

With built-in lists, `items.sort()` edits A and returns `None`; `sorted(items)` builds a new
outer list B. For integer elements, shared children introduce no mutation risk because integers
are immutable. For dictionaries or nested lists, B still refers to the same child objects.

To test a nonmutating function on a flat list, save the original values, retain an alias to
the input, call the function, and check input equality plus output identity and value. To test
an in-place API, verify the retained alias sees the change and check its documented return
value. Why this works: these assertions check separately what is stored and where it is stored.
They do not infer ownership from one equal result. Define behavior on failure as well: an
exception does not generally promise that earlier mutations have been rolled back.

## When it breaks

```python
items = [3, 1]
observer = items
result = items.sort()
print("sort return:", result, "observer:", observer)
try:
    assert observer == [3, 1], "the caller's list changed"
except AssertionError as error:
    print(f"AssertionError: {error}")

original = [3, 1]
fresh = sorted(original)
assert original == [3, 1] and fresh == [1, 3]
assert fresh is not original
children = [[3], [1]]
outer_copy = list(children)
outer_copy[0].append(9)
assert children[0] == [3, 9]
print("fresh outer list: PASS; nested child still shared:", children[0])
```

**Line by line:** `observer` is an alias, so it exposes the in-place edit even though `result`
is `None`. The assertion catches the violated nonmutation expectation. `sorted` creates a fresh
outer list, and both content and identity are checked. `list(children)` copies only outer
references; appending through its first reference changes the same child in `children`.

Author verification on Python 3.12.10, 2026-09-22:

```text
sort return: None observer: [1, 3]
AssertionError: the caller's list changed
fresh outer list: PASS; nested child still shared: [3, 9]
```

## In production

Prefer explicit docstrings such as “reorders this list in place and returns None” or “returns
a fresh outer list and shares elements.” In-place operations can reduce allocation but require
exclusive ownership or coordination when callers share data. Copying the outer list costs
O(n) references; sorting generally costs O(n log n) comparisons and may need O(n) working
storage in CPython. Custom comparison work can dominate. Fresh storage is not free and does
not by itself give deep isolation or thread safety.

A reviewer should ask whether exceptions can leave partial changes and whether the function
stores the input in a cache for later use. The teaching checks cover plain lists; a real API
needs tests at the exact mutable layer it promises to isolate.

## Check yourself

### Readiness before practice

1. Does assigning a new list to a parameter mutate the caller's list?
2. Why does `output == input` fail to prove that the output is independent?
3. Which assertion distinguishes a fresh list from an alias?
4. Why might a fresh outer list still violate a promised nested ownership contract?

Run the block, then write your own mutating and fresh-result functions in [lab.py](lab.py),
using [the assignment](README.md#assignment). State their ownership contracts before predicting
results. Record a real failing assertion, repair, and explanation in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-006-mutation-contracts)
