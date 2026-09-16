---
day: 38
track: lang-go
title: "Slices share backing arrays; copy(); append aliasing"
theme: "Copies, shares, and moves"
phase: "Languages: advanced features"
status: written
---

# Day 038 · Go — Slices share backing arrays; copy(); append aliasing

**Today's theme:** Copies, shares, and moves

**After today you can:** You can predict whether a change through one variable shows up in another, in each language.

**The interviewer asks it as:** *If I modify the copy, does the original change?*

## 1. What this is, and why it matters

Copying a slice value copies its descriptor, not its backing array. copy duplicates elements into destination storage; nested references may still be shared.

You use this when discussing copies, shares, and moves in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Ira makes a list of food requests on her phone and sends her brother a copy. He changes the first family’s requested dish. Ira opens her own view and sees that it changed too. What looked like a separate list still led to the same family details underneath.

They try again. Her brother gets a separate outer list, so he can reorder the families without changing Ira’s order. But editing one family’s details still appears in both places. Copying the row of names did not copy every detail each name led to.

For an independent planning session, Ira duplicates the family details as well. Now her brother can experiment without changing the version she is using. It takes more work and space, so she does not do it when both people are supposed to share the same current information.

Later, Ira hands the whole job to her sister. Instead of making another full copy, she gives her responsibility for the existing list and stops using it herself. Her sister can continue where she left off. Ira still has her phone, but that particular job no longer belongs to her.

Before each handover, they ask a simple question: should a change made here be visible there? If the answer is yes, they share deliberately. If it is no, they make a sufficiently independent copy. If responsibility is moving, they agree what the previous owner may still do afterwards.

## 3. The idea in plain English

Ira’s second view is a copied slice descriptor with pointer, length, and capacity. Both slices can refer to the same underlying elements. **Capacity** determines whether append can reuse that array or must allocate another one.

The copy builtin copies min(len(destination), len(source)) elements and returns that count. It works with overlapping slices. Appending to a full-capacity slice creates new backing storage, but appending with spare capacity may overwrite elements visible through another slice. For slices of slices, copying only the outer elements leaves inner arrays shared.

## 4. The picture

```text
shallow copy: outer A -> inner X <- outer B
deep copy:    outer A -> inner X    outer B -> inner Y
move:        old owner --ownership--> new owner
```

Copying an outer container and copying its reachable data are different operations.

## 5. The code, built step by step

First isolate the important operation:

```go
independent := make([]int, len(original))
copy(independent, original)
```

Assignment shares the backing array.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

func main() {
    original := []int{1, 2, 3}
    shared := original[:2]
    shared[0] = 9
    independent := make([]int, len(original))
    copy(independent, original)
    independent[0] = 7
    extended := append(shared, 8)
    fmt.Println(original)
    fmt.Println(extended)
    fmt.Println(independent)
    isolatedAppend := append(original[:2:2], 6)
    fmt.Println(original, isolatedAppend)
}
```

**Check the result:** Prints `[9 2 8]`, `[9 2 8]`, `[7 2 3]`, and `[9 2 8] [9 2 6]`. The full slice expression limits capacity for the last append.

## 6. How the other two languages do it

**Python**

```python
shallow = original.copy()
deep = deepcopy(original)
```

A shallow copy creates a new outer container while retaining references to its elements. deepcopy recursively copies an object graph while preserving internal sharing through memoisation.

**C++**

```cpp
auto copied = original;
auto moved = std::move(original);
```

Copy and move constructors define how values acquire resources. std::move casts to an rvalue expression; the selected operation determines whether anything actually moves.

Python copy can share nested objects, Go slices share backing arrays unless elements are copied, and C++ value types define copy/move behaviour. State exactly which level is independent.

## 7. The traps

**Near-miss:** allocate `make([]int, 0, len(original))` then call copy; its length is zero, so zero elements are copied. Indexing destination[0] then panics with `index out of range [0] with length 0`. Capacity is not length. Limiting capacity prevents shared append reuse but does not make existing elements independent.

## 8. Say it out loud

**How it gets asked:** “If I modify the copy, does the original change?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I inspect the backing array relationship, length, and capacity. Assignment shares storage; make plus copy isolates the copied elements. Append may or may not reuse the backing array, so I do not infer isolation merely from receiving a new slice value. I use a full slice expression to constrain append capacity when needed, while remembering that existing elements remain shared. Nested slices require copying at each mutable level.

**Follow-ups**

1. **Does slice assignment copy elements?** No. It copies the descriptor.

2. **How many elements does copy copy?** The smaller of source and destination lengths.

3. **Does a full slice expression isolate existing elements?** No. It limits capacity, not current-element sharing.

**Model answer:** Copying a slice value copies its descriptor, not its backing array. copy duplicates elements into destination storage; nested references may still be shared. Restricting capacity does not deep-copy existing data.

## 9. Recall card

- Assignment shares the backing array.
- Allocate destination length before copy.
- Append reuse depends on capacity.
- Restricting capacity does not deep-copy existing data.

Further reading: [Official reference](https://go.dev/blog/slices-intro).
