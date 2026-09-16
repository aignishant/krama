---
day: 29
track: lang-go
title: "delve, and reading a goroutine panic dump"
theme: "Debugging"
phase: "Languages: advanced features"
status: written
---

# Day 029 · Go — delve, and reading a goroutine panic dump

**Today's theme:** Debugging

**After today you can:** You can set a breakpoint, step, and inspect a variable in each language.

**The interviewer asks it as:** *Your program crashes. Walk me through how you find the bug.*

## 1. What this is, and why it matters

A Go panic dump names the failing goroutine and call frames. Delve can pause that execution and inspect the values that violated an assumption.

You use this when discussing debugging in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Omar follows a recipe for a family dinner. The finished dish tastes far too salty. He could immediately add more water, but that would hide the reason and might ruin the texture. Instead, he asks everyone to stop changing it while he works out what happened.

He begins with the last step and walks backwards. His sister added a spoon of salt because the recipe said so. Before that, his brother added a ready-made sauce. The sauce already contained salt. The recipe had assumed an unsalted sauce, but nobody had noticed the difference.

Omar repeats a small portion in a separate pan. This time he pauses before the salt goes in and tastes what is already there. He checks the amount of sauce rather than guessing from the final flavour. The smaller portion gives him a way to repeat the problem without wasting another whole meal.

He changes one thing: he leaves out the extra salt. The portion tastes right. Then he tries the same change in another small portion to make sure the first result was not luck. He tells the family exactly which assumption failed.

For the next dinner, they add a check beside the recipe: taste the sauce before adding salt. They have not merely rescued tonight’s food. They have found a repeatable cause and a check that will catch the same mistake before it spoils another meal.

## 3. The idea in plain English

Omar repeats one portion; you repeat one input. A **stack frame** records an active call and its local execution context. Start with your own nearest frame in the panic dump, not an unrelated runtime function.

Delve understands Go values and goroutines. Optimisation can make variables unavailable or stepping surprising, so use its debug build for the reproducer. The intentionally broken function below uses the length as an index; a nonempty slice’s last valid index is length minus one. Inspect both numbers before editing the expression.

## 4. The picture

```text
reproduce -> stop before failure -> inspect values -> test one cause -> regression case
```

A debugger exposes the actual state; it does not choose the explanation for you.

## 5. The code, built step by step

First isolate the important operation:

```go
position := len(values)
return values[position]
```

Read the failing goroutine’s own frames.

The complete example follows. Save as `main.go`; run `go run main.go` to reproduce the panic. With Delve installed (`go install github.com/go-delve/delve/cmd/dlv@latest`), run `dlv debug main.go`, then `break main.last`, `continue`, `next`, `print position`, `print len(values)`, and `stack`.

```go
package main

import "fmt"

func last(values []int) int {
    position := len(values)
    return values[position]
}
func main() {
    values := []int{10, 20, 30}
    fmt.Println(last(values))
}
```

**Check the result:** The intentional failure starts `panic: runtime error: index out of range [3] with length 3`. File locations and stack details vary. Repair the function to return (int, error), reject an empty slice, and access values[len(values)-1]; check the error in main before printing 30.

After inspecting the failure, replace the file with this complete repair. Run the same ordinary build/run command; it prints `30`.

```go
package main

import (
    "fmt"
    "os"
)

func last(values []int) (int, error) {
    if len(values) == 0 {
        return 0, fmt.Errorf("empty input")
    }
    return values[len(values)-1], nil
}

func main() {
    value, err := last([]int{10, 20, 30})
    if err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
    fmt.Println(value)
}
```

## 6. How the other two languages do it

**Python**

```python
position = len(values)
return values[position]
```

A traceback shows the calls that led to an exception. pdb lets you stop at a line, inspect values, and step through the failing path.

**C++**

```cpp
auto position = values.size();
return values.at(position);
```

GDB exposes call frames and local values. Sanitizers instrument a program to detect selected memory errors and undefined behaviour during execution.

Python pdb, Go Delve, and C++ GDB all support breakpoints and inspection. Tracebacks identify the failing path; sanitizers add checks for C++ memory and undefined-behaviour defects.

## 7. The traps

**Near-miss:** recover the panic and return the int zero value. That hides the broken boundary. The panic says `index out of range [3] with length 3`, enough to form a hypothesis that the index equals the length. A panic in another goroutine is not caught by recover in main’s goroutine.

## 8. Say it out loud

**How it gets asked:** “Your program crashes. Walk me through how you find the bug.” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I read the panic category, identify the goroutine and my relevant frame, and reproduce with a small input. I stop before the indexed access and compare position with length. I fix the input contract and the off-by-one separately, then add regression cases. For concurrent failures I inspect goroutines instead of assuming the frame on screen is the only active work.

**Follow-ups**

1. **Why minimise the input?** It keeps the failing path and removes distractions.

2. **Can optimisation affect debugging?** Yes. Variables may be optimised away and stepping may not match source order closely.

3. **Can main recover another goroutine’s panic?** No. Recovery must run in a deferred function on the panicking goroutine.

**Model answer:** A Go panic dump names the failing goroutine and call frames. Delve can pause that execution and inspect the values that violated an assumption. Recover is not a repair for a violated indexing contract.

## 9. Recall card

- Read the failing goroutine’s own frames.
- Compare an index with length before access.
- Use a debug build for reliable inspection.
- Recover is not a repair for a violated indexing contract.

Further reading: [Official reference](https://github.com/go-delve/delve/tree/master/Documentation).
