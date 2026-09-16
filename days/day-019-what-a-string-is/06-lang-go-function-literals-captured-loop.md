---
day: 19
track: lang-go
title: "Function literals, captured loop variables, and function types"
theme: "Closures"
phase: "Languages: advanced features"
status: written
---

# Day 019 · Go — Function literals, captured loop variables, and function types

**Today's theme:** Closures

**After today you can:** You can return a function from a function in each language and say what it captured.

**The interviewer asks it as:** *What is a closure, and what does it capture?*

---

## 1. What this is, and why it matters

A Go **function value** can be stored, passed, or returned. A **function literal** is an unnamed function expression. When it refers to surrounding variables, it forms a closure sharing those variables rather than simply substituting their current values into its body.

Today you use closures to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Tara helps three children practise multiplication. She gives the first child the instruction to add two to any number she says. The second child must add five. The third must add ten. All three follow the same kind of instruction, but each remembers a different extra amount.

Tara goes to the kitchen and calls out seven. The children answer nine, twelve, and seventeen. The instructions remain useful even after she has left the room. Each child needs the remembered amount as well as the number just announced.

Then Tara changes the game. She puts a bowl of counters on the table and tells all three children to add however many counters are currently in the bowl. There are initially two. Before the next round, she adds three more. Now all three answer twelve when she calls seven. They are consulting one shared, changing thing rather than remembering three separate amounts.

Neither game is wrong, but they answer different promises. A child told to remember two should not silently switch to five. A child told to consult the bowl should notice when its contents change. Tara repeats the rule before each round so the children can predict what the next answer will be.

When she explains the game to another parent, she includes both parts: what each child should do, and which information that child carries or consults later. The action alone is not enough to determine the answer.

## 3. The idea in plain English

A Go **function value** can be stored, passed, or returned. A **function literal** is an unnamed function expression. When it refers to surrounding variables, it forms a closure sharing those variables rather than simply substituting their current values into its body.

Tara's remembered amount belongs to one invocation of makeAdder. The returned closure keeps it available. A separate invocation provides a separate amount. Captured state remains alive as needed, but sharing it between goroutines does not automatically make concurrent mutation safe.

Go 1.22 changed loop variables declared by the loop to have per-iteration semantics. In a module, the language version declared in go.mod matters. This lesson uses Go 1.22 or later semantics. A pre-existing variable assigned with `=` is still reused; it is different from a loop variable declared using `:=`. For older code, an explicit local copy inside the loop can make the intent clear.

## 4. The picture

```text
make_adder(2) ---> function + retained amount 2 ---> call(7) = 9
make_adder(5) ---> function + retained amount 5 ---> call(7) = 12

snapshot capture ---> private copied value
shared capture   ---> live binding / original object
                          |
                          v
                 later changes may be observed
```

A closure includes retained context as well as code. The second part distinguishes snapshots from shared state; use each language's precise capture rules.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
func makeAdder(amount int) func(int) int {
    return func(value int) int { return value + amount }
}
```

The return type states that callers receive a function taking an int and returning an int. Its body uses amount from this invocation and value from the later call. The loop example separately tests how per-iteration bindings are retained.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import "fmt"

func makeAdder(amount int) func(int) int {
    return func(value int) int { return value + amount }
}

func main() {
    addTwo := makeAdder(2)
    addFive := makeAdder(5)
    fmt.Println(addTwo(7), addFive(7))
    callbacks := []func() int{}
    for amount := 0; amount < 3; amount++ {
        callbacks = append(callbacks, func() int { return amount })
    }
    for _, callback := range callbacks { fmt.Print(callback(), " ") }
    fmt.Println()
}
```

**Check the result:** With Go 1.22+ language semantics, run the program. It prints `9 12` and then `0 1 2` (with a trailing space). If using a module, its go directive must enable the relevant language version.

## 6. How the other two languages do it

- **Python** — Functions can be returned and stored as values.
- **Go** — A function value preserves its parameter and result types.
- **C++** — Lambdas are callable objects with captured state.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** declare `amount := 0` before the loop and change its first clause to `amount = 0`. Now the closures share the pre-existing variable and all print `3` after the loop finishes. The declaration location changes the semantics.

**Failure to reproduce:** call `addTwo("7")`. A compiler diagnostic contains `cannot use "7"` and `as int value`. Storing a function as a value does not discard its function type. Capturing mutable state also does not remove the need for synchronisation if later used concurrently.

## 8. Say it out loud

**How it gets asked:** “What is a closure, and what does it capture?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A Go closure is a function value referring to surrounding variables. Each factory call can retain its own state. I inspect whether loop variables are newly declared per iteration or assigned into an existing binding, and I check the module's language version. The function's parameter and result types remain checked even when it is passed around as data.

**Follow-ups**

1. **Can the captured local outlive the factory?** Yes. Go preserves its lifetime as needed.

2. **Does every loop now produce independent bindings?** No. Assignment to a pre-existing variable still reuses it.

3. **Are concurrent counter calls automatically safe?** No. Shared mutable state needs appropriate synchronisation.

**Model answer:** The return type states that callers receive a function taking an int and returning an int. Its body uses amount from this invocation and value from the later call. The loop example separately tests how per-iteration bindings are retained. Check the module language version when reasoning about loop variables.

## 9. Recall card

- A function value preserves its parameter and result types.
- Closures share captured variables.
- Separate factory calls can retain separate state.
- Loop declarations and assignments have different capture consequences.
- Check the module language version when reasoning about loop variables.

The [Go 1.22 release notes](https://go.dev/doc/go1.22#language) document the per-iteration loop-variable change.
