---
day: 68
track: dsa
title: "Stacks: last in, first out"
phase: "Stacks and queues"
status: written
---

# Day 068 · DSA — Stacks: last in, first out

**After today you can:** You can implement a stack and recognise the problems that want one.

**The interviewer asks it as:** *Implement a stack. What operations must be O(1)?*

---

## 1. What this is, and why they ask it

A **stack** is a collection where you add and remove at the same end. The last thing you put in is the
first thing you take out, which is why it is called **LIFO** — last in, first out. It has three
operations and all three are O(1): **push** (add to the top), **pop** (remove the top), and **peek**
(look at the top without removing it). You cannot reach anything except the top, and that restriction
is the point rather than a limitation.

They ask it because the stack is the smallest data structure with a real personality, and because a
whole family of problems is solved by exactly one sentence: *keep track of the most recent thing that
is not yet resolved*. Brackets, undo, expression evaluation, backtracking, the browser back button,
and — the one they will push you on — recursion itself. Every recursive function is a stack, made by
the language instead of by you.

The interview shape is specific. "Implement a stack" is a warm-up that takes four minutes and is
really checking two things: do you know that a Python `list` already is one, and do you know which
end to use. Then the real question arrives: a problem that does not mention stacks anywhere, where
recognising the sentence above is the whole difficulty.

---

## 2. The story

Meena was making lunch on a Sunday, which normally takes her about an hour and twenty minutes and on
this particular day took nearly three.

At about half past eleven she had the cooker on for the dal and had started chopping for the palya.
That was the thing she was doing.

Then the doorbell went. The gas man, with the cylinder, two weeks earlier than she expected him. So
she put the knife down and went to the door, and while he was pulling the old cylinder out from under
the counter, her mother-in-law called from the back room asking where the strip of tablets had gone.

So Meena left the gas man half-finished at the counter and went to look for the tablets. And while
she was going through the shelf in the back room, she heard the milk going over on the second burner.

Now there were three unfinished things — lunch, the gas man, the tablets — and a fourth just
starting. She did the milk, because it was the one that was happening now and because in about four
seconds it would be on the floor. Then, milk dealt with, she went back to the tablets, which was the
thing she had been doing just before that. Then, tablets found and handed over, back to the gas man.
Then, gas man paid and gone, back to the knife and the half-chopped beans.

Every single time, the thing she went back to was the most recent thing she had left. Not the oldest.
She never once came back from the milk and returned to the chopping, because the chopping had two
other unfinished things sitting on top of it, and she could not get to it until they were cleared.

This works completely fine up to about three, in her experience.

The Sunday it did not work was a month later, when there were five, and the fifth was her neighbour
at the door with a long story about a car. She dealt with the car, and the phone, and the tablets,
and the gas, in that order, correctly, and then stood in the kitchen with a distinct feeling of
having forgotten something, which turned out to be the cooker. It had been the very first thing, at
the very bottom, under everything else, and it had been sitting there for fifty minutes.

---

## 3. The idea in plain English

Meena's unfinished jobs are a **stack**. A new interruption goes on top — that is a **push**.
Finishing the current one and returning to the previous one — that is a **pop**. And "the thing I am
doing now" is whatever is on top, which is a **peek**.

Two properties fall straight out of the story, and they are the two things to say in an interview.

**One: you can only reach the top.** The chopping was still there the whole time and was completely
unreachable until the three things above it were cleared. A stack does not let you look at the
middle. That restriction is what makes all three operations O(1).

**Two: the order out is the reverse of the order in.** She was interrupted by the gas man, then the
tablets, then the milk, and she resolved them milk, tablets, gas man. Last in, first out.

And the bad Sunday is a **stack overflow**: too many unfinished things, and the one at the bottom is
forgotten.

### The three operations

```python
stack: list[int] = []

stack.append(4)      # push       stack is [4]
stack.append(7)      # push       stack is [4, 7]
stack[-1]            # peek -> 7  stack is [4, 7]   (nothing removed)
stack.pop()          # pop  -> 7  stack is [4]
len(stack) == 0      # is_empty -> False
```

That is the entire interface. In Python you do not write a `Stack` class in an interview unless you
are asked to — **a list is a stack**, and saying that immediately is the right answer.

### Which end, and why it matters enormously

The one thing you must get right:

```python
stack.append(x)      # push at the END      O(1)
stack.pop()          # pop from the END     O(1)

stack.insert(0, x)   # push at the FRONT    O(n)  <- wrong end
stack.pop(0)         # pop from the FRONT   O(n)  <- wrong end
```

Adding at the end of a Python list is amortised O(1), because the list has spare capacity and
occasionally doubles — the same amortised argument as a hash table resize from
[day 060](../day-060-hash-tables/README.md). Adding at the *front* has to shift every existing
element one place to the right, which is O(n).

Measured, and it is not a small difference:

```
 1,000,000 x (append + pop)           0.04 s
 100,000 x (insert(0) + pop(0))
   on a 10,000-element list           2.31 s
```

Ten times fewer operations, sixty times the time. If an interviewer asks "which operations must be
O(1)", the answer is *all three*, and the follow-up they are hoping for is that you know which end of
the list gives you that.

### What a stack is really for

One sentence, and it is worth memorising because it is the recognition trigger:

> **A stack is the right structure whenever you need the most recent thing that has not yet been
> resolved.**

Read that against the problems:

| Problem | The most recent unresolved thing |
|---|---|
| Are these brackets balanced? | the most recent unclosed opening bracket |
| Undo | the most recent action |
| Browser back | the most recent page you were on |
| Evaluate `3 + 4 * 2` | the most recent operator not yet applied |
| Simplify `/a/b/../c` | the most recent directory you entered |
| Depth-first search | the most recent node whose neighbours are unexplored |
| Next greater element | the most recent value with no greater element yet |

If you can phrase a problem in those words, it is a stack problem, whatever else it looks like.

### The call stack

Meena's story is literally how function calls work. When a function calls another function, the
machine pushes a **stack frame** — the local variables and the place to return to — onto a stack. The
called function runs. When it returns, its frame is popped and execution resumes exactly where it
left off, in the most recent unfinished function.

Which is why recursion has a depth limit:

```python
>>> def r(n): return r(n + 1)
>>> r(0)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
RecursionError: maximum recursion depth exceeded
```

Python's default limit is **1000** frames. Meena forgot the cooker; the machine raises instead. And
this is the reason any recursive algorithm can be rewritten with an explicit stack — you are just
doing by hand what the language was doing for you. That answer comes up constantly in tree and graph
questions from [day 098](../day-098-what-a-tree-is/README.md) onwards.

### The other options, and when to mention them

```python
from collections import deque
stack = deque()
stack.append(x); stack.pop()          # also O(1) at both ends
```

A `deque` is fine and is the right choice when you need a *queue* as well. For a pure stack a list is
marginally faster and simpler.

`queue.LifoQueue` exists and is for passing work between threads. It takes a lock on every operation,
so it is roughly a hundred times slower. Mentioning it and then saying you would not use it here is a
good, cheap signal.

---

## 4. The picture

The stack over the course of Meena's Sunday. Time runs downwards; the top of the stack is the top of
each column.

```
 t1 lunch     t2 doorbell   t3 tablets   t4 milk      t5 pop     t6 pop     t7 pop
                                         +--------+
                            +---------+  | milk   |
              +----------+  | tablets |  | tablets|  +---------+
 +---------+  | gas man  |  | gas man |  | gas man|  | gas man |  +--------+
 | lunch   |  | lunch    |  | lunch   |  | lunch  |  | lunch   |  | lunch  |  (empty)
 +---------+  +----------+  +---------+  +--------+  +---------+  +--------+
     ^             ^             ^           ^            ^           ^
    top           top           top         top          top         top
```

What to notice: `lunch` sits at the bottom from t1 to t7 and is untouchable the whole time. Every
operation happens at the top line and nowhere else. That is why push, pop and peek are all O(1) —
none of them has to move or search anything.

And the same thing drawn as a Python list, so the indices are visible:

```
 index    0        1         2         3
        +--------+---------+---------+--------+
        | lunch  | gas man | tablets | milk   |
        +--------+---------+---------+--------+
                                        ^
                                    stack[-1]
                                    append() adds here
                                    pop() removes here

 The FRONT (index 0) is the bottom. Never touch it.
 insert(0, x) would shift all four elements right: O(n).
```

---

## 5. The code, built step by step

### Step 1 — the stack class, since they will ask

```python
class Stack:
    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, item: int) -> None:
        self._items.append(item)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()
```

Two things to say while writing it. `append` and `pop` are at the end, which is the O(1) end. And the
explicit empty check is not decoration — `[].pop()` raises `IndexError: pop from empty list`, which
is a confusing message for a caller who never knew there was a list.

```python
    def peek(self) -> int:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)
```

`peek` returns `self._items[-1]` without removing it. Note it does *not* return `self._items.pop()`
and then push it back — that is a real thing people write under pressure and it is both slower and
wrong for an empty stack.

### Step 2 — the pattern, on a small problem

Remove adjacent duplicate characters: `"abbaca"` becomes `"ca"`, because `bb` cancels, then `aa`
cancels.

```python
def remove_adjacent_duplicates(text: str) -> str:
    stack: list[str] = []
    for character in text:
        if stack and stack[-1] == character:
            stack.pop()                # cancels with the most recent
        else:
            stack.append(character)
    return "".join(stack)
```

Six lines, and the sentence is exactly the recognition trigger: *does this character cancel the most
recent unresolved one?* Note `if stack and ...` — checking the stack is non-empty **before**
indexing. Forgetting that half of the condition is the commonest bug in every stack problem there is.

### Step 3 — the real problem: simplify a path

Given `"/a/./b/../../c/"`, return the canonical absolute path, which is `"/c"`. This is LeetCode 71,
and it is a good interview problem because the stack is genuinely the answer and the edge cases are
real rather than invented.

The rules: `.` means stay here, `..` means go up one, empty pieces from doubled slashes mean nothing,
and everything else is a directory name.

Split first:

```python
parts = path.split("/")
# "/a/./b/../../c/" -> ['', 'a', '.', 'b', '..', '..', 'c', '']
```

Splitting on `/` gives empty strings at both ends and wherever there were two slashes. That is
convenient rather than annoying, because it means one rule handles all of them.

Now the loop, one rule at a time:

```python
stack: list[str] = []
for part in parts:
    if part == "" or part == ".":
        continue                    # nothing to do
    if part == "..":
        if stack:
            stack.pop()             # go up — but not above the root
    else:
        stack.append(part)          # a real directory name
```

The `if stack` inside the `..` branch is the whole edge case. `/../` from the root stays at the root;
it does not go above it and it does not raise. On `"/../"` the stack is empty, `..` does nothing, and
the answer is `"/"`.

Then rebuild:

```python
return "/" + "/".join(stack)
```

An empty stack gives `"/" + ""` which is `"/"`. Correct with no special case, which is worth pointing
out as you write it.

### The complete solution

```python
class Stack:
    """A stack over a Python list. All three operations are O(1) because
    they all happen at the END of the list — the amortised-O(1) end."""

    def __init__(self) -> None:
        self._items: list[str] = []

    def push(self, item: str) -> None:
        self._items.append(item)

    def pop(self) -> str:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> str:
        if not self._items:
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)


def simplify_path(path: str) -> str:
    """Canonical absolute path. '.' stays, '..' goes up, '//' collapses.

    The stack holds the directories entered but not yet left — which is the
    'most recent unresolved thing' sentence in its purest form.
    """
    stack: list[str] = []

    for part in path.split("/"):
        if part == "" or part == ".":
            continue                       # '' comes from // and from the ends
        if part == "..":
            if stack:                      # '..' at the root is a no-op
                stack.pop()
        else:
            stack.append(part)

    return "/" + "/".join(stack)


def remove_adjacent_duplicates(text: str) -> str:
    """Repeatedly cancel equal adjacent characters. One pass, O(n)."""
    stack: list[str] = []
    for character in text:
        if stack and stack[-1] == character:
            stack.pop()
        else:
            stack.append(character)
    return "".join(stack)


def reverse_with_stack(items: list[int]) -> list[int]:
    """Out is the reverse of in — the defining property, made literal."""
    stack: list[int] = []
    for item in items:
        stack.append(item)
    return [stack.pop() for _ in range(len(stack))]


def is_balanced_simple(text: str) -> bool:
    """One bracket type. Tomorrow generalises this to three."""
    depth = 0
    for character in text:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:               # closed one that was never opened
                return False
    return depth == 0


if __name__ == "__main__":
    print(simplify_path("/home/"))              # /home
    print(simplify_path("/../"))                # /
    print(simplify_path("/home//foo/"))         # /home/foo
    print(simplify_path("/a/./b/../../c/"))     # /c
    print(simplify_path("/..."))                # /...   ('...' is a real name)
    print(remove_adjacent_duplicates("abbaca"))  # ca
    print(reverse_with_stack([1, 2, 3]))        # [3, 2, 1]
    print(is_balanced_simple("(()"))            # False

    s = Stack()
    s.push("a"); s.push("b")
    print(s.peek(), len(s))                     # b 2
    print(s.pop(), s.pop(), s.is_empty())       # b a True
```

The `"/..."` case is worth running. Three dots is not `..`; it is a perfectly legal directory name,
and code that checks `part.startswith("..")` gets it wrong.

---

## 6. What it costs

### The three operations

```
 push (append at the end)   O(1) amortised
 pop  (remove from the end) O(1)
 peek (read index -1)       O(1)
 is_empty                   O(1)
```

`push` is *amortised* O(1), not strictly O(1), and the distinction is the same one as the hash-table
resize. A Python list holds spare capacity; when it fills, it allocates a bigger block and copies
everything, which is O(n) on that one append. But the doublings are `8 + 16 + 32 + … + n/2 ≈ n`, so
across n appends the total copying is about n, and each append averages constant time. Say
"amortised" and be ready to explain it in that one sentence.

### The wrong end, counted

`insert(0, x)` shifts every existing element right by one. On a stack of size k that is k moves.
Doing it n times:

```
 1 + 2 + 3 + ... + n  =  n(n-1)/2
```

At n = 100,000: **five billion** element moves instead of 100,000 appends. Measured, at only 100,000
operations on a 10,000-element list, it was 2.31 seconds against 0.04 seconds for a million
append-and-pop pairs.

### The problems

`simplify_path` splits the string, which is O(n), then walks the parts. Every part is pushed at most
once and popped at most once, so the loop does at most `2n` stack operations.

```
 split:      O(n)
 loop:       each part pushed <= 1, popped <= 1  ->  O(n) total
 join:       O(n)
 --------------------------------------------
 total:      O(n) time
```

**"Each element is pushed at most once and popped at most once"** is the counting argument for
almost every stack problem, and it is the sentence to say. It is what makes the nested-looking loops
in [day 071](../day-071-monotonic-stack/README.md) linear rather than quadratic.

Space is **O(n)** in the worst case: a path of all directory names with no `..` pushes everything.

### The call stack, priced

Each Python stack frame is roughly a few hundred bytes. The default recursion limit of 1000 exists
because the C stack underneath is finite — typically 1 MB or 8 MB — and blowing it segfaults the
interpreter rather than raising cleanly.

```
 recursion depth 1,000     ~ default limit, RecursionError beyond
 an explicit stack         limited only by heap memory: millions of entries
```

That is the practical argument for converting recursion to an explicit stack, and it is a real
follow-up: *"this tree is a million nodes deep — will your recursive solution work?"* No, and the
explicit stack version will.

---

## 7. The traps

### Trap 1 — popping an empty stack

```python
>>> [].pop()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: pop from empty list
```

And peeking:

```python
>>> [][-1]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: list index out of range
```

Every stack problem has at least one input that empties the stack early — `")("`, `"/../"`,
`"aa"` — and if you have written `if stack[-1] == x` without `if stack and ...`, that input finds it.
**Write the emptiness check as part of the condition, not as an afterthought.**

The `deque` version says it slightly differently, which is worth recognising:

```
IndexError: pop from an empty deque
```

### Trap 2 — the wrong end of the list

```python
stack.insert(0, x)   # and stack.pop(0)
```

This is correct and it is O(n). Nothing will fail, no test will complain, and your O(n) solution is
quietly O(n²). This is exactly the `seen = []` trap from
[day 062](../day-062-sets/README.md) in a new costume: identical-looking code, different complexity.

### Trap 3 — `peek` implemented as pop-then-push

```python
def peek(self):
    item = self._items.pop()
    self._items.append(item)
    return item
```

Works on a non-empty stack, raises on an empty one where `self._items[-1]` would have raised more
clearly, and does twice the work. More importantly, in any concurrent or generator context the stack
is briefly in a state that does not include the item. Use `[-1]`.

### Trap 4 — forgetting that the answer is reversed

The stack gives you things in reverse order of insertion. If you build a result by popping, you get
it backwards.

```python
result = []
while stack:
    result.append(stack.pop())
# result is now in reverse order of the stack's bottom-to-top order
```

In `simplify_path` this is why the answer is `"/".join(stack)` — joining the list directly, in
bottom-to-top order — rather than popping into a list. Popping would give `"c"` before `"a"` and the
path would be backwards.

### Trap 5 — `..` versus `...`

```python
if part.startswith(".."):     # WRONG
```

`"..."` is a valid directory name and `"..foo"` is too. The check must be `part == ".."` exactly.
`simplify_path("/...")` should return `"/..."`, and the `startswith` version returns `"/"`.

### Trap 6 — recursion depth

```python
>>> def r(n): return r(n + 1)
>>> r(0)
RecursionError: maximum recursion depth exceeded
```

Default limit 1000. Raising it with `sys.setrecursionlimit` is not a fix; it moves the failure from a
clean Python exception to a segmentation fault when the real C stack runs out. The fix is an explicit
stack.

### Trap 7 — reaching into the middle

```python
stack[2]           # legal on a Python list, and it is not a stack operation
```

Python will let you do it because a list is not really a stack. If you find yourself indexing
anything other than `-1`, either you do not want a stack, or you have a bug. Say this out loud if you
do it deliberately — "I am peeking two down, which means this is not a pure stack" — because an
interviewer will notice.

---

## 8. In the interview

### How it gets asked

- The warm-up: *"Implement a stack. What operations must be O(1)?"* Four minutes, and the real
  content is the "which end" answer.
- *"Implement a stack using an array. Now what if the array is fixed size?"* — leads to resizing and
  the amortised argument.
- The disguised one, which is the real question: *"Given a path like `/a/./b/../c`, return the
  canonical form."* Nobody says stack.
- The connection: *"Rewrite this recursive function iteratively."* The answer is always an explicit
  stack, because that is what recursion already was.

### What to say out loud, in the first ninety seconds

1. **Say what a stack is by its restriction, not its operations.** "A stack only lets you touch one
   end. That restriction is what makes all three operations constant time."
2. **Say the recognition sentence.** "I reach for a stack when the problem needs the most recent
   thing that is not yet resolved. Here, that is the most recent directory I entered and have not
   left."
3. **Say the implementation in one line and move on.** "In Python a list is a stack — `append` and
   `pop` at the end. I would not write a class unless you want one."
4. **Name the counting argument before writing.** "Each element is pushed at most once and popped at
   most once, so this is O(n) even though there is a pop inside the loop."
5. **Say the empty-stack case before the interviewer finds it.** "The case I need to handle is `..`
   when the stack is empty — that is `/../`, which should stay at the root rather than go above it or
   raise."

### The follow-ups

**"Why is push amortised O(1) and not just O(1)?"**
"Because the list occasionally has to grow. When it is full, Python allocates a bigger block and
copies everything, which is O(n) on that one append. But the growth is geometric, so across n appends
the total copying is about n, and each one averages constant. It matters if you care about tail
latency — one unlucky push is slow — and it does not matter for the total."

**"Implement it with a fixed-size array."**
"Then push has to check `top == capacity - 1` and either reject or resize. If I resize, I double,
which is what gives me the amortised bound. If I reject, I have a bounded stack and push can fail,
which changes the interface — `push` now returns a boolean or raises `StackOverflow`."

**"Could you use a linked list instead?"**
"Yes, and push and pop become strictly O(1) rather than amortised, because there is no reallocation.
The costs are one allocation per element and terrible cache behaviour — the nodes are scattered in
memory, while an array is contiguous. In practice the array version is faster for almost everything,
which is why every standard library uses one."

**"This tree could be a million nodes deep. Will your recursive solution work?"**
"No. Python's recursion limit is 1000 frames by default, and raising it just moves the crash from a
clean `RecursionError` to a segfault when the C stack runs out. I would convert it to an explicit
stack — which is doing by hand exactly what the call stack was doing for me — and then the only limit
is heap memory."

**"How is a stack different from a queue?"**
"Which end you remove from. A stack removes from the end you added to, so the order out is reversed.
A queue removes from the other end, so the order is preserved. Both are O(1) if you use the right
structure — but a Python list is only a good stack, not a good queue, because removing from the front
is O(n). That is what `collections.deque` is for."

### A model answer

Asked: *implement a stack. What operations must be O(1)?*

> "A stack is a collection where you add and remove at the same end, so the last thing in is the
> first thing out. The defining property is the restriction: you can only touch the top. You cannot
> look at the middle, and that is exactly why every operation is constant time — nothing ever has to
> search or shift.
>
> Three operations, and all three must be O(1): push, pop and peek. I would add `is_empty` as a
> fourth, because every real use needs it.
>
> In Python I would not normally write a class. A list is a stack: `append` to push, `pop` to pop,
> and `[-1]` to peek. The one thing that matters is **which end**. `append` and `pop` work at the end
> of the list, which is amortised constant time. If I used `insert(0, x)` and `pop(0)` instead, every
> operation would shift the whole list and I would have an O(n) stack that looks identical on the
> screen. Measured, that is about sixty times slower at only a hundred thousand operations.
>
> Push is amortised constant rather than strictly constant, because when the list fills, Python
> allocates a larger block and copies. The growth is geometric, so across n pushes the total copying
> is about n and each push averages constant. It matters for tail latency and not for throughput.
>
> If you want it written out, I would guard both `pop` and `peek` against an empty stack and raise a
> message that mentions the stack — otherwise a caller gets `IndexError: pop from empty list`, which
> mentions a list they never knew existed.
>
> Two things I would mention unprompted. `collections.deque` is also O(1) at both ends and is what I
> would use if I needed a queue as well. And `queue.LifoQueue` exists but takes a lock on every
> operation for thread safety, so it is roughly a hundred times slower and I would not use it unless
> threads were actually involved.
>
> And the reason I care about stacks beyond the interface is that the call stack is one. Every
> recursive function is pushing a frame per call, which is why Python raises `RecursionError` at a
> thousand deep, and why any recursion can be rewritten with an explicit stack when the depth is a
> problem."

---

## 9. Recall card

- **A stack is defined by its restriction: you can only touch one end.** That is *why* push, pop and
  peek are all O(1) — nothing searches, nothing shifts. LIFO, so the order out is the reverse of the
  order in.
- **In Python, a list is a stack.** `append` / `pop` / `[-1]`. **The end is the O(1) end** —
  `insert(0, x)` and `pop(0)` shift everything and are O(n), giving an identical-looking O(n²)
  solution (2.31 s vs 0.04 s in the measurement). `deque` if you also need a queue; never
  `queue.LifoQueue` outside threads (~100× slower).
- **The recognition sentence: reach for a stack when you need *the most recent thing not yet
  resolved*.** Unclosed bracket · last action to undo · last page visited · operator not yet applied
  · directory entered but not left · node whose neighbours are unexplored.
- **The counting argument for every stack problem: each element is pushed at most once and popped at
  most once, so it is O(n)** — even with a `pop` inside the loop. Push is **amortised** O(1) because
  the list grows geometrically (`8+16+…+n/2 ≈ n`).
- **The call stack is a stack**, which is why `RecursionError: maximum recursion depth exceeded` fires
  at **1000** frames and why any recursion can become an explicit stack (limited only by heap).
  Traps: `IndexError: pop from empty list` — always write `if stack and stack[-1] == x` · `part ==
  ".."` not `startswith("..")`, because `"..."` is a real name · and remember the stack gives you
  things **backwards**.
