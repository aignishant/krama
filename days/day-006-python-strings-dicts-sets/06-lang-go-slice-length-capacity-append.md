---
day: 6
track: lang-go
title: "slice: length, capacity, append, and the backing array"
theme: "Growable sequences"
phase: "Languages: every language, every basic"
status: written
---

# Day 006 · Go — slice: length, capacity, append, and the backing array

**Today's theme:** Growable sequences

**After today you can:** You can grow, shrink, index and copy a sequence in each language and say when a copy really happens.

**The interviewer asks it as:** *What happens under the hood when you append to a full sequence?*

---

## 1. What this is, and why it matters

A Go slice is a small window onto a block of slots called the backing array: it records where the window starts, how many slots it can see, which is its length, and how many slots exist from there to the end of the block, which is its capacity. `append` writes into the next slot if capacity allows and otherwise gets a bigger block and copies. Two slices can look at the same block, so writing through one is visible through the other, and that is the single most-asked Go interview question.

At work, slices are in every Go function signature, and the bug where a function appends to a slice it was handed and silently overwrites the caller's data is one every Go programmer has shipped once. Interviewers ask "what is the difference between length and capacity", "what does `append` return and why must you assign it", and "draw what happens when you slice a slice and append to it".

## 2. The story

Nandini is having twenty people over for her mother's sixtieth, and everyone leaves their shoes at the door. She has a shoe rack in the hallway with eight slots.

The first guests arrive and slide their shoes into slot one, slot two, slot three. Easy. Nobody has to think. Each new pair goes in the next empty slot at the end.

At around seven the ninth pair arrives, and the rack is full. Nandini drags out the bigger rack from the storeroom, the one with sixteen slots, and moves all eight pairs across in the same order, then slides the ninth pair into slot nine. It takes her two minutes. The guests after that go straight into slots ten, eleven, twelve, and nobody has to move anything again for a while.

Her uncle, who arrived third, comes out later for a cigarette and reaches for slot three on the old rack. Empty. The rack he remembered is not the rack anymore. His shoes are in slot three of the new one, but he had remembered the place, not the shoes.

Then her mother's oldest friend arrives, and her mother insists, absolutely insists, that this woman's shoes go in slot one. So Nandini takes every single pair out, shifts each one along by one slot, and puts the new pair at the front. Eleven pairs moved for one arrival. Nobody enjoys it.

At the end of the night, people leave in reverse order, roughly. The last pair in is the first pair out, and taking a pair from the end of the rack costs nothing: lift, go. But when her uncle leaves early, from slot three, everyone after him shuffles down a slot to close the gap, because Nandini does not like gaps.

Two rules she has learned by midnight. Adding at the end is free until the rack is full, and then it costs a whole move, but only once in a while. Adding or removing anywhere else costs a shuffle of everyone behind it, every time.

## 3. The idea in plain English

An **array** in Go is a block of slots whose size is fixed forever: `[8]string` is eight strings and can never be nine. That is the rack. You will rarely write one directly.

A **slice** is a window onto an array. It holds three things: where in the array the window starts, which Go stores as a **pointer**, an address in the machine's storage that day 12 explains properly, its **length**, `len`, which is how many slots you can see, and its **capacity**, `cap`, which is how many slots there are from the window's start to the end of the array. `[]string{"red", "blue", "black"}` makes an array of three and a slice over all of it: `len` 3, `cap` 3.

`append(s, x)` returns a slice one longer. If `len < cap`, there is a spare slot in the array, and `append` writes `x` there and returns a window one wider, on the **same** array. If `len == cap`, the rack is full: `append` gets a new array about twice the size, copies everything, writes `x`, and returns a window on the **new** array. The old array is untouched and any other slice still looking at it does not see `x`. That is the uncle at the old rack.

Because `append` may or may not move to a new array, you must always write `s = append(s, x)`. The returned slice is the only one that is guaranteed to see the new item.

**Slicing** a slice, `s[1:3]`, makes a new window on the same array. No copy. Writing through `s[1:3]` writes into `s`. And the trap that every Go interview asks about: if `t := s[:2]` and then `t = append(t, 99)`, and `cap(t)` has room, the `99` is written into the array slot that `s[2]` also looks at. You overwrote `s` by appending to `t`.

To actually copy, use `copy(dst, src)`, which copies as many items as fit, or `slices.Clone(s)` from the `slices` package, which makes a fresh array of the right size.

Adding at the front is `append([]string{x}, s...)`, which builds a new slice and copies everything: the mother's oldest friend. Removing from the middle is `append(s[:i], s[i+1:]...)`, which shifts the tail down. Both cost the length of the slice, every time. `make([]string, 0, 8)` makes an empty slice over an array of eight, so the first eight appends never copy.

## 4. The picture

```
 shoes := []string{"red", "blue", "black"}

 slice header            backing array
 ┌───────┬─────┬─────┐   index:  0       1        2
 │ start │ len │ cap │          ┌───────┬────────┬────────┐
 │   ●───┼──3──┼──3──┼────────► │ "red" │ "blue" │"black" │
 └───────┴─────┴─────┘          └───────┴────────┴────────┘

 shoes = append(shoes, "white")    len == cap, so: new array of 6, copy 3, write 1

 ┌───────┬─────┬─────┐   index:  0       1        2        3        4     5
 │   ●───┼──4──┼──6──┼────────► │ "red" │ "blue" │"black" │"white" │  --  │ --  │
 └───────┴─────┴─────┘          └───────┴────────┴────────┴────────┴──────┴─────┘

 t := shoes[:2]                    a second window, same array, len 2, cap 6
 t = append(t, "grey")             room in cap, so writes slot 2  →  shoes[2] is now "grey"
```

*Notice that the header is tiny and the array is separate. Copying a slice header, which is what `b := a` and passing to a function both do, never copies the array. Notice that `t` and `shoes` in the last two lines share slot 2.*

## 5. The code, built step by step

Start `rack.go` in a `day06` folder.

```go
package main

import (
	"fmt"
	"slices"
)

func main() {
	shoes := []string{"red", "blue", "black"}
	fmt.Println(shoes, len(shoes), cap(shoes))
	shoes = append(shoes, "white")
	fmt.Println(shoes, len(shoes), cap(shoes))
```

```
[red blue black] 3 3
[red blue black white] 4 6
```

Length went 3 to 4. Capacity jumped 3 to 6: the rack was full, so `append` got a bigger one. From here, two more appends are free.

Watch capacity grow across twenty appends.

```go
	rack := []int{}
	lastCap := -1
	for i := 0; i < 20; i++ {
		rack = append(rack, i)
		if cap(rack) != lastCap {
			lastCap = cap(rack)
			fmt.Printf("after %2d items: len %2d cap %2d\n", len(rack), len(rack), cap(rack))
		}
	}
```

```
after  1 items: len  1 cap  1
after  2 items: len  2 cap  2
after  3 items: len  3 cap  4
after  5 items: len  5 cap  8
after  9 items: len  9 cap 16
after 17 items: len 17 cap 32
```

Six reallocations in twenty appends, each doubling. The next one is at 33. Amortised constant time, visible.

Index, change in place, slice without copying.

```go
	shoes[0] = "grey"
	middle := shoes[1:3]
	middle[0] = "navy"
	fmt.Println(shoes, middle)
```

```
[grey navy black white] [navy black]
```

`middle` is a window on the same array as `shoes`, so writing `middle[0]` changed `shoes[1]`. No copy happened anywhere in those four lines.

The interview question.

```go
	a := []int{1, 2, 3, 4}
	t := a[:2]
	t = append(t, 99)
	fmt.Println(a, t, len(t), cap(t))
```

```
[1 2 99 4] [1 2 99] 3 4
```

`t` had length 2 and capacity 4, so `append` had room and wrote `99` into slot 2 of the shared array. `a[2]` was `3` and is now `99`. Nothing warned you. If you need `t` to have its own array, clone it first.

Real copies.

```go
	own := slices.Clone(a)
	own[0] = 100
	dst := make([]int, 2)
	n := copy(dst, a)
	fmt.Println(a, own, dst, n)
```

```
[1 2 99 4] [100 2 99 4] [1 2] 2
```

`slices.Clone` gave `own` a fresh array. `copy` filled `dst` with as many as fit, two, and returned that count.

Front and middle, and what they cost.

```go
	shoes = append([]string{"sandal"}, shoes...)
	fmt.Println(shoes)
	shoes = append(shoes[:1], shoes[2:]...)
	fmt.Println(shoes)
```

```
[sandal grey navy black white]
[sandal navy black white]
```

The first line builds a one-item slice and appends everything after it: a full copy. The second removes index 1 by appending the tail over it: a shift of everything after. Both are the shuffle from the story.

Here is the run and output for the complete program.

```bash
go run rack.go
```

```
start: [red blue black] len 3 cap 3
after append: [red blue black white] len 4 cap 6
after  1 items: len  1 cap  1
after  2 items: len  2 cap  2
after  3 items: len  3 cap  4
after  5 items: len  5 cap  8
after  9 items: len  9 cap 16
after 17 items: len 17 cap 32
shared window: [grey navy black white] [navy black]
append through a sub-slice: a=[1 2 99 4] t=[1 2 99]
clone and copy: a=[1 2 99 4] own=[100 2 99 4] dst=[1 2]
front insert: [sandal grey navy black white]
remove index 1: [sandal navy black white]
```

And the complete file.

```go
// rack.go — day 6, slices, length, capacity, and the backing array
// Run:  go run rack.go
package main

import (
	"fmt"
	"slices"
)

func main() {
	shoes := []string{"red", "blue", "black"}
	fmt.Println("start:", shoes, "len", len(shoes), "cap", cap(shoes))
	shoes = append(shoes, "white")
	fmt.Println("after append:", shoes, "len", len(shoes), "cap", cap(shoes))

	rack := []int{}
	lastCap := -1
	for i := 0; i < 20; i++ {
		rack = append(rack, i)
		if cap(rack) != lastCap {
			lastCap = cap(rack)
			fmt.Printf("after %2d items: len %2d cap %2d\n", len(rack), len(rack), cap(rack))
		}
	}

	shoes[0] = "grey"
	middle := shoes[1:3]
	middle[0] = "navy"
	fmt.Println("shared window:", shoes, middle)

	a := []int{1, 2, 3, 4}
	t := a[:2]
	t = append(t, 99)
	fmt.Printf("append through a sub-slice: a=%v t=%v\n", a, t)

	own := slices.Clone(a)
	own[0] = 100
	dst := make([]int, 2)
	copy(dst, a)
	fmt.Printf("clone and copy: a=%v own=%v dst=%v\n", a, own, dst)

	shoes = append([]string{"sandal"}, shoes...)
	fmt.Println("front insert:", shoes)
	shoes = append(shoes[:1], shoes[2:]...)
	fmt.Println("remove index 1:", shoes)
}
```

## 6. How the other two languages do it

Python, where the spare slots are hidden and `b = a` shares just as in Go:

```python
shoes = ["red", "blue", "black"]
shoes.append("white")          # amortised O(1), capacity hidden
b = shoes                      # same list; b.append changes shoes
c = shoes[1:3]                 # a COPY, unlike Go's shoes[1:3]
```

C++, where `capacity()` and `reserve()` are visible like Go's `cap` and `make`, but `=` copies:

```cpp
std::vector<std::string> shoes = {"red", "blue", "black"};
shoes.push_back("white");                  // amortised O(1)
std::vector<std::string> b = shoes;        // a full COPY
std::string& first = shoes[0];
shoes.push_back("brown");                  // may reallocate: first is now dangling
```

The one line of difference that matters: **slicing shares in Go and copies in Python; assigning shares in Go and Python and copies in C++.** Go's `s[1:3]` is a window; Python's `s[1:3]` is a new list. A Python programmer moving to Go writes `tail := s[1:]` expecting independence and gets a shared array. The C++ line to notice is the last one: a reference into a vector dies when the vector reallocates, which is the uncle at the old rack, and Go's version of that is the two windows that stop agreeing after `append` moves one of them.

## 7. The traps

**The real error: `append` without assignment.** Call `append` and throw away its answer.

```go
	append(shoes, "brown")
```

```
./rack.go:12:2: append(shoes, "brown") (value of type []string) is not used
```

The compiler catches this one because the result is unused. The version it cannot catch is passing `shoes` to a function that appends inside and does not return the new slice: the caller's `shoes` never sees the item, or worse, sees it only sometimes, depending on whether capacity had room.

**The real error: one past the end.** Index the fourth item of a three-item slice.

```go
	three := []string{"red", "blue", "black"}
	fmt.Println(three[3])
```

```
panic: runtime error: index out of range [3] with length 3

goroutine 1 [main]:
main.main()
	/home/you/day06/rack.go:14 +0x1d
exit status 2
```

A **panic** stops the program and prints where it happened. Go checks every index at run time. Python raised `IndexError`; C++ will check nothing and read whatever is there.

**The near-miss: the sub-slice that overwrites.** The interview question, one more time, in the form it appears at work.

```go
	first := shoes[:2]
	first = append(first, "extra")
	fmt.Println(shoes)
```

If `shoes` had spare capacity, `shoes[2]` is now `"extra"`, and the line that changed it does not mention `shoes` at all. When you hand out a sub-slice that the receiver might append to, either clone it or cap it with the three-index form `shoes[:2:2]`, which sets capacity equal to length so that any `append` is forced to reallocate.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between the length and the capacity of a slice?"
- "What happens when you append to a slice, and why do you assign the result?"
- "If I slice a slice and append to the sub-slice, what happens to the original?"

**What to say out loud, the first ninety seconds**

"A slice is a three-word header: a pointer to a backing array, a length, and a capacity. Length is how many elements the slice sees; capacity is how many exist from its start to the end of the array. `append` checks whether length is less than capacity. If so, it writes into the next slot of the same array and returns a header with length plus one. If not, it allocates a new array, roughly double for small slices, copies the elements, writes the new one, and returns a header pointing at the new array. Because the result may point somewhere new, I always assign it back: `s = append(s, x)`.

Slicing creates a new header on the same array, with no copy, so `t := s[:2]` shares storage with `s`. If I then append to `t` and `t` has spare capacity, the write lands in `s`'s array and overwrites `s[2]`. To prevent that I clone with `slices.Clone`, or use the full slice expression `s[:2:2]` to set capacity equal to length so the next append must reallocate."

**The follow-ups**

1. *"What does passing a slice to a function copy?"* — The header: pointer, length, capacity. The function sees the same array, so element writes are visible to the caller; an `append` that reallocates is not, unless the function returns the new slice.
2. *"How does capacity grow?"* — Doubling while the slice is small, then more slowly, about one and a quarter times, once it passes a few hundred elements. The exact numbers are an implementation detail; the doubling pattern is what matters.
3. *"What is a nil slice?"* — `var s []int` has a nil pointer, length 0 and capacity 0. `append` works on it, `len` is 0, `range` runs zero times. It is the normal way to start an empty slice.

**A model answer**

"A Go slice is a descriptor of pointer, length and capacity over a backing array. `append` uses spare capacity in place, otherwise allocates a larger array, copies, and returns a new descriptor; the caller must rebind the result because reallocation changes the pointer. Slicing shares the array, so sub-slices alias the original, and appending to a sub-slice with spare capacity overwrites the original's elements silently. Defensive copies use `copy` or `slices.Clone`, and the three-index form `s[a:b:b]` caps capacity to force reallocation on the next append. Indexing out of range panics at run time. `make([]T, 0, n)` pre-sizes capacity to avoid reallocation, and growth doubles for small slices, giving amortised O(1) append."

## 9. Recall card

- A slice is pointer, `len`, `cap` over a backing array; `s[1:3]` is a new window on the same array, not a copy.
- `s = append(s, x)`: writes in place if `len < cap`, else new array about twice as big, copy, and a new pointer; always assign the result.
- Cap grows 1, 2, 4, 8, 16, 32 from empty; `make([]T, 0, n)` skips the early copies.
- `t := s[:2]; t = append(t, 99)` overwrites `s[2]` if cap allows; use `slices.Clone(s)` or `s[:2:2]` to stop it.
- `s[len(s)]` panics with `index out of range [3] with length 3`; front insert and middle delete are `append` with `...` and cost O(n).
