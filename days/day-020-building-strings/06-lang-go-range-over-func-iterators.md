---
day: 20
track: lang-go
title: "Range-over-func iterators (iter.Seq) and channels as iterators"
theme: "Iterators and generators"
phase: "Languages: advanced features"
status: written
---

# Day 020 · Go — Range-over-func iterators (iter.Seq) and channels as iterators

**Today's theme:** Iterators and generators

**After today you can:** You can produce values lazily in each language without building the whole list first.

**The interviewer asks it as:** *How do you loop over something that does not fit in memory?*

---

## 1. What this is, and why it matters

Go 1.23 introduced range over iterator functions. `iter.Seq[T]` names a function type accepting a `yield func(T) bool` callback. The producer offers one value by calling yield; false means the consumer has stopped and the producer must return.

Today you use iterators and generators to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Isha helps serve breakfast at a family gathering. There is space for only six plates beside the stove. She could try to cook every dosa before anyone starts eating, but the early ones would become cold and the kitchen would fill with trays. Instead, she cooks one when someone is ready to take it.

Her uncle stands nearby and asks for the next dosa. Isha makes it, hands it over, and waits for the next request. She remembers how much batter remains and whether the pan is hot. She does not restart the entire preparation each time someone asks.

After three servings, her uncle says he is full. Isha stops. There is no reason to cook the rest of the batter merely because it is available. The next person may begin another round later, but the first person's breakfast is finished.

Her cousin points out that the breakfast table and the serving process are different things. A tray holding six finished dosas can be visited repeatedly while the food remains there. The act of cooking the next dosa advances the meal. Asking again does not bring back the dosa that was already eaten.

Isha finds the arrangement useful for a large gathering. She keeps only the current work near the stove, serves each item when needed, and stops when the person eating stops asking. The total amount of food may be large, but she does not have to hold it all ready at once.

## 3. The idea in plain English

Go 1.23 introduced range over iterator functions. `iter.Seq[T]` names a function type accepting a `yield func(T) bool` callback. The producer offers one value by calling yield; false means the consumer has stopped and the producer must return.

Isha's serving rule becomes the callback contract. In this push-style protocol, the producer calls yield rather than exposing a next method to the consumer. A range loop provides the callback and makes consumption look like other Go loops. `iter.Seq2[K, V]` offers two values per step for key/value-style traversal.

A channel can also supply values to a range loop, but a channel-based producer running in a goroutine needs a cancellation plan when consumption stops. A synchronous iterator does not need that extra goroutine. Whether an iterator is repeatable depends on its captured state; this example starts a fresh local loop on each call, so it is reusable.

## 4. The picture

```text
source/state ---> produce one ---> consumer
     ^                              |
     |                              | wants another
     +------------------------------+
                                    | stops
                                    v
                               no later work

retained results: current item + consumer's running state
materialise all:  item 0, item 1, item 2, ... item n-1
```

Lazy traversal avoids retaining all results. The producer must obey early termination, and any borrowed resources or storage must remain valid while traversal is active.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```go
for value := 0; value < limit; value++ {
    if !yield(value * value) { return }
}
```

The callback's boolean is the stop signal. Breaking the consumer loop after 4 makes yield return false and immediately ends production. The local loop is inside each iterator invocation, so another call starts a fresh traversal.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import (
    "fmt"
    "iter"
)

func squares(limit int) iter.Seq[int] {
    return func(yield func(int) bool) {
        for value := 0; value < limit; value++ {
            if !yield(value * value) { return }
        }
    }
}

func main() {
    sequence := squares(10)
    for value := range sequence {
        fmt.Println(value)
        if value == 4 { break }
    }
    total := 0
    for value := range squares(4) { total += value }
    fmt.Println("sum", total)
}
```

**Check the result:** Use Go 1.23+ and, when in a module, a go directive of at least 1.23. Run the program to print `0`, `1`, `4`, and `sum 14`. The first loop stops after three values.

## 6. How the other two languages do it

- **Python** — An iterable supplies an iterator.
- **Go** — Go 1.23 supports range over iterator functions.
- **C++** — begin starts traversal; end marks its boundary.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** ignore the boolean returned by yield and continue calling it after the consumer breaks. The runtime detects this misuse and can panic with `runtime error: range function continued iteration after function for loop body returned false`. Return promptly on false.

**Second trap:** replace the iterator with a goroutine sending onto an unbuffered channel, then break consumption without cancellation. The producer may remain blocked sending forever. A channel is a coordination mechanism, not a free substitute for a synchronous lazy traversal.

## 8. Say it out loud

**How it gets asked:** “How do you loop over something that does not fit in memory?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A Go iterator function pushes values through a yield callback supplied by range. I stop when yield returns false, which preserves early-exit behaviour without a background producer. Channels can also be ranged over, but concurrent production needs cancellation and closing rules. I state the Go 1.23 language requirement and whether the particular iterator supports more than one traversal.

**Follow-ups**

1. **Does every iterator start a goroutine?** No. This one runs synchronously.

2. **Can this sequence be traversed twice?** Yes. Each call creates a new local loop; other iterators may be one-shot.

3. **What does Seq2 add?** It yields a pair of values per step.

**Model answer:** The callback's boolean is the stop signal. Breaking the consumer loop after 4 makes yield return false and immediately ends production. The local loop is inside each iterator invocation, so another call starts a fresh traversal. Repeatability depends on the iterator's state and design.

## 9. Recall card

- Go 1.23 supports range over iterator functions.
- iter.Seq passes values to a yield callback.
- Return as soon as yield reports false.
- A channel producer needs explicit cancellation when consumers stop.
- Repeatability depends on the iterator's state and design.

Further reading: [Go's range-over-functions explanation](https://go.dev/blog/range-functions).
