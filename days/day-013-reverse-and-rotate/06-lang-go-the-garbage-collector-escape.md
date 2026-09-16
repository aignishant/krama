---
day: 13
track: lang-go
title: "The garbage collector, escape analysis, and stack versus heap"
theme: "Memory: who frees what"
phase: "Languages: every language, every basic"
status: written
---

# Day 013 · Go — The garbage collector, escape analysis, and stack versus heap

**Today's theme:** Memory: who frees what

**After today you can:** You can say where a value lives, who frees it, and when, in each language.

**The interviewer asks it as:** *How does memory get freed in your language?*

---

## 1. What this is, and why it matters

Go's **garbage collector** reclaims allocations that can no longer be reached from live program state. An unreachable cycle can be reclaimed even when its members point to one another. The program does not call `delete` for ordinary Go objects.

Today you use memory: who frees what to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Anika borrows a badminton racket at the sports centre. The attendant gives her a numbered tag and says to return the racket before leaving. Anika plays one game and hands both items back. The racket is ready for the next person, and nobody has to search the building for it.

Her brother borrows a second racket, then lends it to a friend while he gets water. When he returns, the friend is still playing. He cannot return that racket merely because he has stopped using it. Someone else still needs it. The attendant waits until the last person brings it back.

Two friends make a different mistake. Each believes the other will return a pair of spare rackets. Both leave. No one is playing with them, but the rackets remain beside a bench because the responsibility has gone round in a circle. At closing time, an attendant walks through the hall and finds the forgotten equipment.

Anika notices that the three arrangements have different costs. Returning her own racket promptly is simple because responsibility is clear. Shared borrowing needs everyone to keep track of who still needs the racket. The final walk through the building finds things that ordinary handovers miss, but it takes work and happens later.

Before borrowing again, she asks who is responsible for returning the equipment and when that must happen. Being finished with something and having actually returned it are related, but they are not the same event.

## 3. The idea in plain English

Go's **garbage collector** reclaims allocations that can no longer be reached from live program state. An unreachable cycle can be reclaimed even when its members point to one another. The program does not call `delete` for ordinary Go objects.

The attendant's final walk resembles tracing reachable objects rather than counting each loan. **Escape analysis** is compiler reasoning about whether data must remain valid beyond its local use. A **stack** stores call-related data with managed call lifetimes; the **heap** supports allocations whose lifetimes are not tied to that simple pattern. Actual placement is a compiler decision, not a rule that every use of `new` must mean heap allocation.

Returning a pointer to a local variable is safe in Go: the implementation keeps the pointed-to value alive as needed. `defer` schedules a call for the surrounding function's exit and is useful for closing resources. Garbage collection does not replace `Close`, and deferred cleanup waits for the function to return, not for the end of a loop iteration.

## 4. The picture

```text
live owner / root ----> object A ----> object B
                          ^               |
                          +---------------+

Remove the outside path:
  tracing collector: A and B may become unreachable
  strong reference counts: the cycle can retain owners
  unique ownership: one responsible owner releases its object
```

Distinguish a live outside path from a cycle's internal links. Go traces reachability; CPython supplements reference counting with cyclic collection; C++ shared ownership needs cycles broken explicitly.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
func makeCounter() *Counter {
    counter := Counter{Value: 3}
    return &counter
}
```

The returned pointer remains valid even though the function has returned. Storage placement must preserve that lifetime. In main, clearing one pointer does not make the object unreachable while alias still points to it.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

type Counter struct { Value int }

func makeCounter() *Counter {
    counter := Counter{Value: 3}
    return &counter
}

func main() {
    counter := makeCounter()
    alias := counter
    counter = nil
    fmt.Println(alias.Value)
    alias.Value++
    fmt.Println(alias.Value)
}
```

**Check the result:** Run `go run main.go`. It prints `3` then `4`. `go build -gcflags=-m main.go` reports compiler escape/inlining decisions; their wording and placement decisions may vary.

## 6. How the other two languages do it

- **Python** — CPython uses reference counting plus cyclic collection.
- **Go** — Go keeps reachable objects alive.
- **C++** — RAII ties release to an owning object's lifetime.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** defer a file close on every iteration of a long loop in one function. Every open file can remain open until that whole function returns. Put each iteration's work in a helper with its own defer or close explicitly after each operation.

**Failure to reproduce:** replace `fmt.Println(alias.Value)` with `fmt.Println(counter.Value)` after setting counter to nil. The panic contains `runtime error: invalid memory address or nil pointer dereference`. The object is still alive through alias; the nil access path is the problem.

## 8. Say it out loud

**How it gets asked:** “How does memory get freed in your language?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Go traces reachable allocations and reclaims unreachable ones, including cycles. Escape analysis lets the compiler choose storage while preserving safe lifetimes, so returning a local address is valid. I separate this from resource cleanup: I close files explicitly, often with defer. Collection timing is not a contract for when a file or network connection closes.

**Follow-ups**

1. **Does new always allocate on the heap?** No. Compiler escape analysis can choose storage.

2. **Can unreachable cycles be reclaimed?** Yes. Reachability, not a positive reference count, determines liveness.

3. **When does defer run?** When the surrounding function returns, including ordinary panic unwinding.

**Model answer:** The returned pointer remains valid even though the function has returned. Storage placement must preserve that lifetime. In main, clearing one pointer does not make the object unreachable while alias still points to it. defer manages function-exit cleanup, not collection timing.

## 9. Recall card

- Go keeps reachable objects alive.
- Unreachable allocations can be reclaimed later.
- Escape analysis chooses safe storage placement.
- Returning a local address is safe in Go.
- defer manages function-exit cleanup, not collection timing.
