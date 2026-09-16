---
day: 18
track: lang-go
title: "Type parameters, constraints, and any versus comparable"
theme: "Generics"
phase: "Languages: advanced features"
status: written
---

# Day 018 · Go — Type parameters, constraints, and any versus comparable

**Today's theme:** Generics

**After today you can:** You can write one Stack that works for ints and strings in each language.

**The interviewer asks it as:** *How would you write a function that works for any type?*

---

## 1. What this is, and why it matters

A **type parameter** lets a declaration work with several concrete types. A **constraint** describes which types are allowed and which operations the generic implementation can rely on. `any` accepts every type, but does not allow arbitrary operations such as adding or comparing its values.

Today you use generics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Sana works at the entrance of a community hall. After lunch, she collects clean trays into a tall pile. The next person takes the tray on top. She does not reach into the middle, because that would disturb everything above it. When the pile is empty, she says there are no trays left rather than pretending to hand one over.

In the afternoon, the hall hosts a reading group. Sana arranges spare books in a pile by the door. The same habit works: add to the top, take from the top, and say clearly when nothing remains. She does not need a new arrangement just because the objects are books rather than trays.

There are still limits. A person who can stack trays does not automatically know how to wash books. The shared arrangement supports a few actions, not every possible action someone might perform on the things inside it. Sana keeps the common procedure separate from the care each object needs.

At closing time, a helper mixes keys into the book pile. Sana stops him. The shelf was promised to people expecting books. If the next person reaches for a book and receives keys, the procedure has failed even though the keys were placed neatly on top.

Sana keeps one useful arrangement and clearly states what each pile contains. That gives her reuse without surprise. She can teach the helper the same three actions once, then apply them to several kinds of object while preserving the promise made to whoever takes the next item.

## 3. The idea in plain English

A **type parameter** lets a declaration work with several concrete types. A **constraint** describes which types are allowed and which operations the generic implementation can rely on. `any` accepts every type, but does not allow arbitrary operations such as adding or comparing its values.

Sana's pile becomes `Stack[T any]`. The stack only stores and removes T values, so any is sufficient. A map-key or equality-based operation often needs `comparable`, a constraint allowing equality comparisons. A slice type, for example, does not satisfy comparable.

Instantiation chooses a concrete type, as in `Stack[int]`. Go can infer type arguments for many function calls from their value arguments; generic types must be instantiated where used. Empty pop returns a zero value plus false. The boolean tells the caller whether that zero value was stored data or just the absence result.

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

```go
type Stack[T any] struct { items []T }
func (stack *Stack[T]) Push(value T) {
    stack.items = append(stack.items, value)
}
```

T describes both the slice's elements and Push's argument. The pointer receiver updates the stored slice descriptor after append. Pop additionally clears the removed slot so the backing storage does not unnecessarily retain referenced objects.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

type Stack[T any] struct { items []T }

func (stack *Stack[T]) Push(value T) {
    stack.items = append(stack.items, value)
}

func (stack *Stack[T]) Pop() (T, bool) {
    if len(stack.items) == 0 {
        var zero T
        return zero, false
    }
    last := len(stack.items) - 1
    value := stack.items[last]
    var zero T
    stack.items[last] = zero // release references retained by this slot
    stack.items = stack.items[:last]
    return value, true
}

func main() {
    var numbers Stack[int]
    numbers.Push(2)
    numbers.Push(3)
    first, _ := numbers.Pop()
    second, _ := numbers.Pop()
    fmt.Println(first, second)
    var words Stack[string]
    words.Push("hello")
    word, ok := words.Pop()
    fmt.Println(word, ok)
}
```

**Check the result:** With Go 1.18 or later, run `go run main.go`. It prints `3 2` and `hello true`. The ignored booleans on the number pops are justified only by the immediately preceding known pushes.

## 6. How the other two languages do it

- **Python** — TypeVar names a relationship between input and output types.
- **Go** — Type parameters make one implementation work for several types.
- **C++** — Templates describe implementations parameterised by types.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** write a generic equality function with `[T any]` and compare its arguments using `==`. The compiler rejects operations that are not valid for every permitted type. Use `[T comparable]` when equality is part of the contract.

**Failure to reproduce:** add `numbers.Push("wrong")`. A compiler diagnostic includes `cannot use "wrong"` and `as int value`. The instantiation fixed the element type before runtime. Do not throw away that guarantee by replacing every type with any-valued storage.

## 8. Say it out loud

**How it gets asked:** “How would you write a function that works for any type?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A Go type parameter is constrained by the operations the implementation needs. My stack uses any because storing and returning values does not require equality. I would choose comparable for map keys or ==. Each instantiated stack keeps its element type, and Pop returns a separate success flag so an empty result is not confused with a legitimate zero value.

**Follow-ups**

1. **Does any mean every operation is available?** No. It permits all types, so only universally supported operations are available.

2. **Why clear the removed slot?** The backing array could otherwise retain references after the logical pop.

3. **When is type inference useful?** Generic function calls often infer parameters from their arguments.

**Model answer:** T describes both the slice's elements and Push's argument. The pointer receiver updates the stored slice descriptor after append. Pop additionally clears the removed slot so the backing storage does not unnecessarily retain referenced objects. Separate empty-pop status from the zero value.

## 9. Recall card

- Type parameters make one implementation work for several types.
- Constraints determine permitted operations.
- any supports storage; comparable permits equality.
- Instantiation preserves each stack's element type.
- Separate empty-pop status from the zero value.

Further reading: [Go's generics tutorial](https://go.dev/doc/tutorial/generics).
