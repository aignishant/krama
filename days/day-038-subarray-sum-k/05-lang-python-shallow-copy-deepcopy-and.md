---
day: 38
track: lang-python
title: "Shallow copy, deepcopy, and aliasing bugs"
theme: "Copies, shares, and moves"
phase: "Languages: advanced features"
status: written
---

# Day 038 · Python — Shallow copy, deepcopy, and aliasing bugs

**Today's theme:** Copies, shares, and moves

**After today you can:** You can predict whether a change through one variable shows up in another, in each language.

**The interviewer asks it as:** *If I modify the copy, does the original change?*

## 1. What this is, and why it matters

A shallow copy creates a new outer container while retaining references to its elements. deepcopy recursively copies an object graph while preserving internal sharing through memoisation.

You use this when discussing copies, shares, and moves in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ira makes a list of food requests on her phone and sends her brother a copy. He changes the first family’s requested dish. Ira opens her own view and sees that it changed too. What looked like a separate list still led to the same family details underneath.

They try again. Her brother gets a separate outer list, so he can reorder the families without changing Ira’s order. But editing one family’s details still appears in both places. Copying the row of names did not copy every detail each name led to.

For an independent planning session, Ira duplicates the family details as well. Now her brother can experiment without changing the version she is using. It takes more work and space, so she does not do it when both people are supposed to share the same current information.

Later, Ira hands the whole job to her sister. Instead of making another full copy, she gives her responsibility for the existing list and stops using it herself. Her sister can continue where she left off. Ira still has her phone, but that particular job no longer belongs to her.

Before each handover, they ask a simple question: should a change made here be visible there? If the answer is yes, they share deliberately. If it is no, they make a sufficiently independent copy. If responsibility is moving, they agree what the previous owner may still do afterwards.

## 3. The idea in plain English

Ira’s separate row of families is a shallow list copy. The nested family lists are still shared. **Aliasing** means different paths reach the same mutable object. Use is to inspect identity and a mutation to verify the consequence.

deepcopy tracks already-copied objects so cycles and repeated references can be handled coherently. It is not a universal duplication of external resources such as open files or connections. Copying n outer references takes O(n); a deep copy costs work proportional to the reachable copied graph. Choose the depth from the ownership contract rather than calling deepcopy automatically.

## 4. The picture

```text
shallow copy: outer A -> inner X <- outer B
deep copy:    outer A -> inner X    outer B -> inner Y
move:        old owner --ownership--> new owner
```

Copying an outer container and copying its reachable data are different operations.

## 5. The code, built step by step

First isolate the important operation:

```python
shallow = original.copy()
deep = deepcopy(original)
```

Test identity at the level that can change.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from copy import deepcopy

original = [[1, 2], [3, 4]]
shallow = original.copy()
deep = deepcopy(original)
shallow[0][0] = 9
deep[1][1] = 8
print(original)
print(shallow)
print(deep)
print(original[0] is shallow[0], original[0] is deep[0])
```

**Check the result:** Prints `[[9, 2], [3, 4]]`, the same for shallow, then `[[1, 2], [3, 8]]`, and `True False`.

## 6. How the other two languages do it

**Go**

```go
independent := make([]int, len(original))
copy(independent, original)
```

Copying a slice value copies its descriptor, not its backing array. copy duplicates elements into destination storage; nested references may still be shared.

**C++**

```cpp
auto copied = original;
auto moved = std::move(original);
```

Copy and move constructors define how values acquire resources. std::move casts to an rvalue expression; the selected operation determines whether anything actually moves.

Python copy can share nested objects, Go slices share backing arrays unless elements are copied, and C++ value types define copy/move behaviour. State exactly which level is independent.

## 7. The traps

**Near-miss:** `rows = [[0] * 2] * 3` repeats references to one row. Updating rows[0][0] changes all three visible rows; construct each row independently. Trying to deepcopy an open file raises a TypeError about an unpicklable file object; copy data, not live resource handles.

## 8. Say it out loud

**How it gets asked:** “If I modify the copy, does the original change?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I draw the reference graph before deciding how to copy. A new outer list does not isolate nested mutable elements, so I test the exact mutation the caller plans to make. I use deepcopy only when duplicating the reachable graph matches the domain, and I account for its cost. Immutable children can safely remain shared. Files and other external resources need their own ownership and reopening rules.

**Follow-ups**

1. **Does a shallow list copy isolate nested lists?** No. It copies references to those lists.

2. **Does deepcopy duplicate every repeated reference separately?** No. Its memo preserves sharing within the copied graph.

3. **When is sharing desirable?** When contents are immutable or callers deliberately observe the same owned state.

**Model answer:** A shallow copy creates a new outer container while retaining references to its elements. deepcopy recursively copies an object graph while preserving internal sharing through memoisation. Copy depth should follow the mutation contract.

## 9. Recall card

- Test identity at the level that can change.
- Shallow copies share nested objects.
- deepcopy uses memoisation for the copied graph.
- Copy depth should follow the mutation contract.

Further reading: [Official reference](https://docs.python.org/3.12/library/copy.html).
