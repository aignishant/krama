---
day: 34
track: lang-go
title: "select, and why Go does not need async/await"
theme: "Concurrency IV: async"
phase: "Languages: advanced features"
status: written
---

# Day 034 · Go — select, and why Go does not need async/await

**Today's theme:** Concurrency IV: async

**After today you can:** You can make 100 network calls at once in each language and say where the waiting happens.

**The interviewer asks it as:** *What is the difference between concurrency and parallelism?*

## 1. What this is, and why it matters

select waits on several channel operations. Goroutines use ordinary-looking blocking code while the runtime can schedule other runnable goroutines.

You use this when discussing concurrency iv: async in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Anu prepares breakfast. She puts water on to boil, then slices fruit while she waits. When the water is ready, she pours tea. She does not stand beside the kettle doing nothing, but she also does not pretend her two hands can cut fruit and pour hot water at exactly the same instant.

Her brother joins and takes over the fruit. Now two people can work at the same time. That is different from Anu alone switching between jobs whenever one job is waiting. Both arrangements can finish sooner than doing everything strictly in sequence, but for different reasons.

The family asks for three kinds of toast. Anu starts them together in three available slots, then collects each when ready. The order in which they finish may differ from the order in which they were requested. She still wants to serve each person the right kind, so she keeps track of which request belongs to which result.

One slot stops heating. Anu must decide whether to stop the whole breakfast, serve the other toast, or retry that one request. Simply hearing about the first failure does not magically stop the other slots from working.

Before leaving the kitchen, she checks every started job. Some finished, one failed, and none should remain forgotten. Overlapping work is useful only when she can still explain where the results and failures go.

## 3. The idea in plain English

Anu waits for whichever item becomes ready. A **select** chooses one channel case that can proceed, or waits if none can. When several cases are ready, do not assume source order gives priority. A default case makes the selection nonblocking and can create a busy loop if used carelessly.

The example selects between a result and a timeout. The result channel is buffered so the worker can complete its send even if the timeout wins. That avoids one blocked send, but it does not cancel expensive work; day 36 adds a cancellation protocol. Go needs no async/await syntax for this coordination.

## 4. The picture

```text
task A: start -- wait -------- finish
task B:        start -- wait -- finish
one coordinator switches while work waits
```

Overlapping waits is concurrency; simultaneous execution requires additional execution capacity.

## 5. The code, built step by step

First isolate the important operation:

```go
select {
case value := <-result:
    fmt.Println(value)
case <-timer.C:
    fmt.Println("timed out")
}
```

Select coordinates readiness across channels.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "time"
)
func main() {
    result := make(chan int, 1)
    go func() { result <- 42 }()
    timer := time.NewTimer(time.Second)
    defer timer.Stop()
    select {
    case value := <-result:
        fmt.Println(value)
    case <-timer.C:
        fmt.Println("timed out")
    }
}
```

**Check the result:** Ordinarily prints `42`; an extreme scheduling delay can allow the timeout branch. The example intentionally makes no real-time scheduling guarantee.

## 6. How the other two languages do it

**Python**

```python
results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
```

asyncio runs coroutines cooperatively. await allows the event loop to run other work while an operation is suspended.

**C++**

```cpp
auto first = std::async(std::launch::async, work, 1);
auto second = std::async(std::launch::async, work, 2);
```

std::async can launch a computation and return a future. get waits for its result and rethrows a stored exception.

Python asyncio uses cooperative await points, Go select chooses among channel operations, and C++ futures hold eventual results. None makes blocking work nonblocking merely by changing its name.

## 7. The traps

**Near-miss:** use an unbuffered result channel, return on timeout, and leave the worker blocked sending forever. A select with no ready cases and no possible future sender can end in `fatal error: all goroutines are asleep - deadlock!`. A closed channel is always ready to receive its zero value, so remove or stop handling it when appropriate.

## 8. Say it out loud

**How it gets asked:** “What is the difference between concurrency and parallelism?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I put waiting work in goroutines and use select when several communication events can complete the next step. I do not assume a ready result beats a ready timeout by textual order. I define what happens to the producer after the receiver exits; a buffered one-shot result prevents a blocked final send, while cooperative cancellation is needed to stop the work itself. I avoid a default branch unless nonblocking polling is intentional.

**Follow-ups**

1. **Does select choose the first ready case in source order?** No. Do not use case order as a priority rule.

2. **What does default change?** It avoids blocking when no communication case is ready.

3. **Does a timeout stop the worker?** No. It only changes the waiting caller’s path unless cancellation is propagated.

**Model answer:** select waits on several channel operations. Goroutines use ordinary-looking blocking code while the runtime can schedule other runnable goroutines. Timing out a wait does not stop the underlying work.

## 9. Recall card

- Select coordinates readiness across channels.
- A default branch can cause busy polling.
- A one-shot buffered result can prevent a stranded send.
- Timing out a wait does not stop the underlying work.

Further reading: [Official reference](https://go.dev/ref/spec#Select_statements).
