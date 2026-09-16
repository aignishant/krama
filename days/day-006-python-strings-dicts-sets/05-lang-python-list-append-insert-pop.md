---
day: 6
track: lang-python
title: "list: append, insert, pop, slicing, and the cost of each"
theme: "Growable sequences"
phase: "Languages: every language, every basic"
status: written
---

# Day 006 · Python — list: append, insert, pop, slicing, and the cost of each

**Today's theme:** Growable sequences

**After today you can:** You can grow, shrink, index and copy a sequence in each language and say when a copy really happens.

**The interviewer asks it as:** *What happens under the hood when you append to a full sequence?*

---

## 1. What this is, and why it matters

A list is a row of values in order that can grow and shrink while the program runs. Python's `list` grows at the end cheaply, grows in the middle expensively, is indexed and sliced like a string, and, unlike a string, can be changed in place. Two names can point at the same list, so changing it through one name changes what the other sees, and that is the source of most list bugs.

At work, lists are the container you reach for first and the one whose cost you misjudge most: an `insert(0, x)` in a loop turns a fast program into a slow one. Interviewers ask "what is the time complexity of append versus insert", "what happens when a list is full", and "why did modifying this list inside a loop skip an element", and all three are today.

## 2. The story

Nandini is having twenty people over for her mother's sixtieth, and everyone leaves their shoes at the door. She has a shoe rack in the hallway with eight slots.

The first guests arrive and slide their shoes into slot one, slot two, slot three. Easy. Nobody has to think. Each new pair goes in the next empty slot at the end.

At around seven the ninth pair arrives, and the rack is full. Nandini drags out the bigger rack from the storeroom, the one with sixteen slots, and moves all eight pairs across in the same order, then slides the ninth pair into slot nine. It takes her two minutes. The guests after that go straight into slots ten, eleven, twelve, and nobody has to move anything again for a while.

Her uncle, who arrived third, comes out later for a cigarette and reaches for slot three on the old rack. Empty. The rack he remembered is not the rack anymore. His shoes are in slot three of the new one, but he had remembered the place, not the shoes.

Then her mother's oldest friend arrives, and her mother insists, absolutely insists, that this woman's shoes go in slot one. So Nandini takes every single pair out, shifts each one along by one slot, and puts the new pair at the front. Eleven pairs moved for one arrival. Nobody enjoys it.

At the end of the night, people leave in reverse order, roughly. The last pair in is the first pair out, and taking a pair from the end of the rack costs nothing: lift, go. But when her uncle leaves early, from slot three, everyone after him shuffles down a slot to close the gap, because Nandini does not like gaps.

Two rules she has learned by midnight. Adding at the end is free until the rack is full, and then it costs a whole move, but only once in a while. Adding or removing anywhere else costs a shuffle of everyone behind it, every time.

## 3. The idea in plain English

A **list** is a row of values in order, written in square brackets: `["red", "blue", "black"]`. Each value has an **index**, counting from zero, and you read one with `shoes[0]` and change one with `shoes[0] = "grey"`. That last part is the difference from a string: a list is **mutable**, it can be changed in place.

Behind the scenes, a list keeps its items in one continuous block of slots, the rack, and the block is usually a bit bigger than the number of items, which is the spare slots. `len(shoes)` is how many items; the spare slots are hidden, but they are there.

`append(x)` puts `x` in the next spare slot. That is cheap: no shuffling. When there are no spare slots, Python gets a bigger block, copies every item across, and then appends. That copy is the two minutes with the bigger rack. It happens rarely, because each new block is bigger by a proportion, not a fixed amount, so the cost of the occasional copy spread over all the appends is small. This is called **amortised constant time**, and it is the answer to the interview question.

`insert(0, x)` puts `x` at the front, shifting every existing item along by one. That is the mother's oldest friend: every append behind it moves. Cost grows with the length of the list. `pop()` with no argument removes the last item, cheap; `pop(0)` removes the first, and everyone shuffles down. `remove(x)` finds `x` and does the same shuffle.

**Slicing** a list, `shoes[1:3]`, works like slicing a string, and it makes a **copy**: a new list holding those items. **Assignment** does not copy. `b = a` makes `b` a second name for the same list, so `b.append(x)` changes `a`. To copy the whole list, write `a.copy()` or `a[:]`. This is the uncle reaching for the old rack: the question is always "same rack, or a different rack with the same shoes".

## 4. The picture

```
 shoes = ["red", "blue", "black"]      len 3, block of 4 slots, 1 spare

 index:   0       1       2       3
        ┌───────┬───────┬───────┬───────┐
        │ "red" │ "blue"│"black"│  --   │
        └───────┴───────┴───────┴───────┘

 shoes.append("white")     → fills the spare slot, no copy

 shoes.append("brown")     → no spare: new block of 8, copy 4 across, then add
        ┌───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┐
        │ "red" │ "blue"│"black"│"white"│"brown"│  --   │  --   │  --   │
        └───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┘

 shoes.insert(0, "grey")   → every item shifts right by one, then "grey" at 0

 b = shoes                 → b is another name for the SAME block
 c = shoes[:]              → c is a NEW block with the same values
```

*Notice that `append` only ever touches the end, until the rare moment the block is full. Notice that `b = shoes` draws no new block at all.*

## 5. The code, built step by step

Start `rack.py` in a `day06` folder.

```python
shoes = ["red", "blue", "black"]
shoes.append("white")
print(shoes, len(shoes))
print(shoes[0], shoes[-1], shoes[1:3])
```

```
['red', 'blue', 'black', 'white'] 4
red white ['blue', 'black']
```

`append` adds at the end. Indexing and slicing work exactly as on strings, and the slice is a new list.

Change in place, which strings did not allow.

```python
shoes[0] = "grey"
print(shoes)
```

```
['grey', 'blue', 'black', 'white']
```

Watch the block grow. `sys.getsizeof` reports how many bytes the list itself occupies, which jumps each time Python gets a bigger block.

```python
import sys

rack: list[int] = []
last_size = 0
for i in range(20):
    rack.append(i)
    if sys.getsizeof(rack) != last_size:
        last_size = sys.getsizeof(rack)
        print(f"after {len(rack):2d} items the block is {last_size} bytes")
```

```
after  1 items the block is 88 bytes
after  5 items the block is 120 bytes
after  9 items the block is 184 bytes
after 17 items the block is 248 bytes
```

Twenty appends, four copies. The block grew at 1, 5, 9, and 17 items, and stayed put for all the appends in between. That is the whole of "amortised constant time" in four lines of output. The hint `list[int]` says this is a list of ints.

The front is expensive.

```python
shoes.insert(0, "sandal")
print(shoes)
print(shoes.pop(), shoes)
print(shoes.pop(0), shoes)
```

```
['sandal', 'grey', 'blue', 'black', 'white']
white ['sandal', 'grey', 'blue', 'black']
sandal ['grey', 'blue', 'black']
```

`insert(0, ...)` shifted four items. `pop()` took the last for free. `pop(0)` took the first and shifted three items down. On a list of a million, that shift is a million moves, every time.

Two names, one rack.

```python
a = ["red", "blue"]
b = a
c = a[:]
b.append("black")
print(a, b, c)
print(a is b, a is c)
```

```
['red', 'blue', 'black'] ['red', 'blue', 'black'] ['red', 'blue']
True False
```

`b = a` did not copy. Appending through `b` changed `a`, because they are the same list. `c` was a slice, so it is a separate list and did not change. `is` asks "are these the very same object", which is the question that matters here.

Here is the run and output for the complete program.

```bash
python3 rack.py
```

```
start: ['red', 'blue', 'black'] len 3
after append: ['red', 'blue', 'black', 'white']
first red, last white, middle ['blue', 'black']
after shoes[0] = 'grey': ['grey', 'blue', 'black', 'white']
after  1 items the block is 88 bytes
after  5 items the block is 120 bytes
after  9 items the block is 184 bytes
after 17 items the block is 248 bytes
insert at front: ['sandal', 'grey', 'blue', 'black', 'white']
pop() gave white, pop(0) gave sandal: ['grey', 'blue', 'black']
same list? True, copy changed? False
```

And the complete file.

```python
# rack.py — day 6, lists and what each operation costs
# Run:  python3 rack.py
import sys

shoes = ["red", "blue", "black"]
print(f"start: {shoes} len {len(shoes)}")

shoes.append("white")
print(f"after append: {shoes}")
print(f"first {shoes[0]}, last {shoes[-1]}, middle {shoes[1:3]}")

shoes[0] = "grey"
print(f"after shoes[0] = 'grey': {shoes}")

rack: list[int] = []
last_size = 0
for i in range(20):
    rack.append(i)
    if sys.getsizeof(rack) != last_size:
        last_size = sys.getsizeof(rack)
        print(f"after {len(rack):2d} items the block is {last_size} bytes")

shoes.insert(0, "sandal")
print(f"insert at front: {shoes}")
last = shoes.pop()
first = shoes.pop(0)
print(f"pop() gave {last}, pop(0) gave {first}: {shoes}")

alias = shoes
copy = shoes[:]
alias.append("brown")
print(f"same list? {alias is shoes}, copy changed? {'brown' in copy}")
```

## 6. How the other two languages do it

Go, where the spare slots have a name, `cap`, and you can watch them:

```go
rack := []int{}
for i := 0; i < 20; i++ {
	rack = append(rack, i)
	fmt.Println(len(rack), cap(rack))   // cap goes 1, 2, 4, 8, 16, 32
}
b := rack          // same backing array, like Python's b = a
```

C++, where the spare slots are `capacity()` and you can ask for them up front:

```cpp
std::vector<int> rack;
rack.reserve(20);                 // one block of 20, no copies for 20 push_backs
for (int i = 0; i < 20; ++i) {
    rack.push_back(i);
}
std::vector<int> b = rack;        // a full COPY, unlike Python and Go
```

The one line of difference that matters: **`b = a` shares the list in Python and Go, and copies it in C++.** A Python programmer writing C++ will copy a million-element vector by accident with an innocent `=`. A C++ programmer writing Python will change a list through what they thought was a copy. The second difference is visibility: Go and C++ let you see and set the spare capacity, `cap` and `reserve`; Python hides it and you peek with `getsizeof`.

## 7. The traps

**The near-miss: removing while walking.** Remove every blue and black shoe.

```python
shoes = ["red", "blue", "black", "white"]
for shoe in shoes:
    if shoe in ("blue", "black"):
        shoes.remove(shoe)
print(shoes)
```

```
['red', 'black', 'white']
```

`black` survived. When `blue` at index 1 was removed, `black` shifted into index 1, and the loop moved on to index 2, skipping it. Never change the length of a list you are walking. Walk a copy, `for shoe in shoes[:]`, or build a new list of what you want to keep.

**The real error: one past the end.** Index the fourth item of a three-item list.

```python
shoes = ["red", "blue", "black"]
print(shoes[3])
```

```
Traceback (most recent call last):
  File "/home/you/day06/rack.py", line 2, in <module>
    print(shoes[3])
          ~~~~~^^^
IndexError: list index out of range
```

Indices run from 0 to `len - 1`. Slices forgive going past the end; indexing does not. Hold on to this error: Go's version panics, and C++'s version says nothing at all.

**The near-miss: the shared default, again.** Yesterday's trap, and it is really a list trap.

```python
def add(shoe: str, rack: list[str] = []) -> list[str]:
    rack.append(shoe)
    return rack
```

One list, created once, shared by every call. Now that you know `b = a` shares, you know why: the default is one object, and every call appends to it.

## 8. Say it out loud

**How it gets asked**

- "What happens under the hood when you append to a full list?"
- "What is the time complexity of `append`, `insert(0, x)`, `pop()` and `pop(0)`?"
- "What is the difference between `b = a` and `b = a[:]`?"

**What to say out loud, the first ninety seconds**

"A Python list is a contiguous block of references with some spare capacity at the end. `append` writes into the next spare slot, which is constant time. When there is no spare slot, Python allocates a larger block, roughly proportionally larger, copies the existing references across, and then appends. Because the growth is proportional, the copies are rare enough that the average cost per append is constant; that is amortised O(1). I can see the reallocations happen by watching `sys.getsizeof` jump at 1, 5, 9 and 17 items.

`insert(0, x)` and `pop(0)` shift every element, so they are O(n); `pop()` from the end is O(1). For a queue that grows at one end and shrinks at the other I use `collections.deque`, not a list.

`b = a` binds a second name to the same list object; mutations through either are visible through both. `b = a[:]` or `a.copy()` makes a new list with the same elements, a shallow copy. Slicing always copies. And I never remove from a list while iterating over it, because the shift skips the next element."

**The follow-ups**

1. *"What is a shallow copy?"* — A new list whose elements are the same objects as the original's. If those elements are themselves lists, both copies share them. `copy.deepcopy` copies all the way down.
2. *"How would you remove items while iterating safely?"* — Iterate over a copy, or build a new list with a comprehension of the items to keep, `[s for s in shoes if s not in bad]`, and rebind.
3. *"Why is `deque` better than a list for a queue?"* — `deque.popleft()` is O(1) because it is a doubly linked block structure; `list.pop(0)` is O(n) because every element shifts.

**A model answer**

"`list` is a dynamic array: a contiguous buffer of object references with over-allocated capacity. `append` is amortised O(1): it fills spare capacity, and on overflow reallocates to a proportionally larger buffer and copies, which happens at geometrically spaced sizes. `insert` and `pop` at index 0 are O(n) due to element shifting; `pop()` from the end is O(1). Slicing copies the selected range into a new list; assignment `b = a` aliases the same object, so mutations are shared, and `a[:]` or `a.copy()` gives a shallow copy. Mutating a list's length during iteration skips or repeats elements, so I iterate over a copy or build a new list. For queue behaviour I use `collections.deque`."

## 9. Recall card

- `append` fills a spare slot, amortised O(1); when full, Python gets a bigger block and copies, at 1, 5, 9, 17 items for small lists.
- `insert(0, x)`, `pop(0)`, `remove(x)` shift everything after them, O(n); `pop()` is O(1); use `deque` for a queue.
- `b = a` is the same list; `a[:]` and `a.copy()` are new lists; slicing always copies; `is` asks "same object".
- `shoes[len(shoes)]` is `IndexError: list index out of range`; slices forgive, indexes do not.
- Never remove from a list while walking it; walk a copy or build a new list.
