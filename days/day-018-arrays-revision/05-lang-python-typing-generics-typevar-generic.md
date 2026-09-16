---
day: 18
track: lang-python
title: "typing generics: TypeVar, Generic, and list[T]"
theme: "Generics"
phase: "Languages: advanced features"
status: written
---

# Day 018 · Python — typing generics: TypeVar, Generic, and list[T]

**Today's theme:** Generics

**After today you can:** You can write one Stack that works for ints and strings in each language.

**The interviewer asks it as:** *How would you write a function that works for any type?*

---

## 1. What this is, and why it matters

A **generic** class describes a relationship between types without fixing one concrete element type. `TypeVar` names the varying type and `Generic[T]` declares that relationship. `list[T]` says every element is intended to have type T; a static checker can preserve that information through push and pop.

Today you use generics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Sana works at the entrance of a community hall. After lunch, she collects clean trays into a tall pile. The next person takes the tray on top. She does not reach into the middle, because that would disturb everything above it. When the pile is empty, she says there are no trays left rather than pretending to hand one over.

In the afternoon, the hall hosts a reading group. Sana arranges spare books in a pile by the door. The same habit works: add to the top, take from the top, and say clearly when nothing remains. She does not need a new arrangement just because the objects are books rather than trays.

There are still limits. A person who can stack trays does not automatically know how to wash books. The shared arrangement supports a few actions, not every possible action someone might perform on the things inside it. Sana keeps the common procedure separate from the care each object needs.

At closing time, a helper mixes keys into the book pile. Sana stops him. The shelf was promised to people expecting books. If the next person reaches for a book and receives keys, the procedure has failed even though the keys were placed neatly on top.

Sana keeps one useful arrangement and clearly states what each pile contains. That gives her reuse without surprise. She can teach the helper the same three actions once, then apply them to several kinds of object while preserving the promise made to whoever takes the next item.

## 3. The idea in plain English

A **generic** class describes a relationship between types without fixing one concrete element type. `TypeVar` names the varying type and `Generic[T]` declares that relationship. `list[T]` says every element is intended to have type T; a static checker can preserve that information through push and pop.

Sana's shared piling procedure becomes Stack[T]. The stack does not need arithmetic or ordering, only storage and removal. A Stack[int] should return an int when popped, and a Stack[str] should return a str. Type annotations describe this promise to tools rather than validating every operation at runtime.

An empty stack needs a policy independent of its element type. Here pop raises a clear IndexError instead of returning an unrelated sentinel. The older TypeVar/Generic notation used below works on Python 3.12; the newer `class Stack[T]` syntax is another spelling available there. Do not mix syntax versions without stating the minimum Python version.

## 4. The picture

```text
one Stack[T] implementation
          /            \
         v              v
    Stack[int]      Stack[string / str]
    push 2, 3       push hello
    top -> 3        top -> hello
    next -> 2

empty pop ---> explicit failure policy, regardless of T
```

The operations stay the same while the element contract changes. Python relies on separate static checking; Go and C++ enforce the concrete uses during compilation.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
T = TypeVar("T")
class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []
```

The same T connects the container's annotation to push's argument and pop's return type. Each instance gets its own list in __init__, rather than sharing a mutable class attribute. Static checking can follow int and str uses separately.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: list[T] = []

    def push(self, value: T) -> None:
        self.items.append(value)

    def pop(self) -> T:
        if not self.items:
            raise IndexError("empty stack")
        return self.items.pop()

numbers = Stack[int]()
numbers.push(2)
numbers.push(3)
words = Stack[str]()
words.push("hello")
print(numbers.pop(), numbers.pop())
print(words.pop())
```

**Check the result:** Run `python main.py`. It prints `3 2` and `hello`. To enforce annotations during development, run a Python static type checker as a separate step.

## 6. How the other two languages do it

- **Python** — TypeVar names a relationship between input and output types.
- **Go** — Type parameters make one implementation work for several types.
- **C++** — Templates describe implementations parameterised by types.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** call `numbers.push("wrong")` and expect Python itself to reject the annotation mismatch. The runtime list accepts it; a static checker should flag it. Generics do not turn ordinary Python objects into runtime-validated containers.

**Failure to reproduce:** after the two successful number pops, call `numbers.pop()` again. The program raises `IndexError: empty stack`. That explicit policy is more informative than making callers guess whether None means empty or is a legitimate stored value.

## 8. Say it out loud

**How it gets asked:** “How would you write a function that works for any type?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I use a generic stack to preserve the relationship between what is pushed and what is returned. TypeVar names that relationship, and a static checker specialises it for each use. Runtime Python still needs explicit validation at external boundaries. I also specify empty-stack behaviour separately, because type parameters do not remove ordinary data-structure edge cases.

**Follow-ups**

1. **Does Generic[int] validate each append?** No. This is primarily a static typing contract.

2. **Why not annotate pop as object?** That loses the connection to the pushed element type.

3. **Can T support every operation?** No. State a bound or protocol when the implementation needs specific operations.

**Model answer:** The same T connects the container's annotation to push's argument and pop's return type. Each instance gets its own list in __init__, rather than sharing a mutable class attribute. Static checking can follow int and str uses separately. Specify empty-container behaviour independently.

## 9. Recall card

- TypeVar names a relationship between input and output types.
- Generic[T] carries that relationship through a class.
- Static checkers preserve the concrete element type.
- Runtime Python does not enforce ordinary annotations.
- Specify empty-container behaviour independently.
