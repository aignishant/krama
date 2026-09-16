---
day: 32
track: lang-go
title: "Channels: unbuffered, buffered, close, and range"
theme: "Concurrency II: passing messages"
phase: "Languages: advanced features"
status: written
---

# Day 032 · Go — Channels: unbuffered, buffered, close, and range

**Today's theme:** Concurrency II: passing messages

**After today you can:** You can move work between threads safely in each language.

**The interviewer asks it as:** *How do two threads hand data to each other safely?*

## 1. What this is, and why it matters

An unbuffered channel synchronises a send with a receiver. A buffered channel holds a bounded number of values; closing announces that no more values will be sent.

You use this when discussing concurrency ii: passing messages in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Tara prepares lunch boxes while her brother carries them to the dining room. At first she hands him each box directly. If he is still putting the previous box down, she has to wait. If she has not finished filling one, he has to wait. Neither loses a box because each handover happens face to face.

Their aunt places a tray between them with room for two boxes. Tara can now prepare the next box while her brother carries one away. When both spaces are full, she must pause. The tray helps them absorb small differences in pace, but it cannot hold an unlimited afternoon of work.

When Tara finishes, she tells her brother there will be no more boxes. He still carries the boxes already on the tray before stopping. An empty tray alone would not have told him she was finished; it might only have meant that she was filling the next box.

Later, a second helper joins. Tara makes sure both helpers know how the end will be announced. Otherwise one might wait beside the empty tray after everyone else has left.

They also agree who is allowed to announce the end. A helper who merely sees an empty tray cannot decide that the kitchen is done. The person who knows all filling work has finished owns that decision. The arrangement works because waiting, storage, and completion each have a clear meaning.

## 3. The idea in plain English

Tara’s direct handover is an unbuffered channel; the two-place tray is make(chan int, 2). Sends block when no receiver or buffer slot is available. A range loop receives until the channel is closed and drained.

The sending side closes after all sends finish. Receivers must not close a channel merely because they are done receiving. A received zero value alone cannot indicate closure; use the second boolean when receiving outside range. Channel operations transfer values, but sending a pointer does not remove every alias to its target.

## 4. The picture

```text
producer -> [ bounded queue: at most 2 items ] -> consumer
 full: producer waits             empty: consumer waits
 finished: explicit end signal; drain earlier items
```

A queue needs both a capacity policy and an end-of-stream policy.

## 5. The code, built step by step

First isolate the important operation:

```go
for value := range jobs {
    total += value
}
```

Range drains a closed channel before stopping.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import "fmt"

func main() {
    jobs := make(chan int, 2)
    result := make(chan int)
    go func() {
        total := 0
        for value := range jobs { total += value }
        result <- total
    }()
    for _, value := range []int{1, 2, 3} { jobs <- value }
    close(jobs)
    fmt.Println(<-result)
}
```

**Check the result:** Prints `6`. Closing does not discard buffered values; the receiver processes them before its range loop ends.

## 6. How the other two languages do it

**Python**

```python
item = jobs.get()
try:
    if item is None:
        return
finally:
    jobs.task_done()
```

queue.Queue safely transfers work between threads. A finite maxsize applies backpressure by blocking producers when the queue is full.

**C++**

```cpp
ready.wait(lock, [&] { return closed || !items.empty(); });
```

A condition_variable waits for a state change while a mutex protects the queue. The condition must be checked as a predicate under that mutex.

Python Queue combines locking and blocking operations. Go channels integrate communication with the language. C++ condition_variable coordinates waiting around a separately protected queue.

## 7. The traps

**Near-miss:** forget close and the receiver waits for more jobs while main waits for the result. When all goroutines are blocked, the runtime can report `fatal error: all goroutines are asleep - deadlock!`. Sending after close panics with `send on closed channel`; closing twice panics with `close of closed channel`.

## 8. Say it out loud

**How it gets asked:** “How do two threads hand data to each other safely?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I choose buffered or unbuffered communication according to the handoff and backlog I need. The producer closes only after all sending work has finished. Receivers drain values and then exit the range loop. I use an explicit result handoff to wait for completion. If consumers may stop early, I need cancellation on blocked sends as well; closing the work channel from a receiver is not a safe substitute.

**Follow-ups**

1. **Does close discard buffered values?** No. Receivers can drain them before observing the closed state.

2. **Who should close?** The side that knows no further sends can occur, usually the producer or its coordinator.

3. **How do two consumers stop?** Both range loops end after the one shared channel is closed and drained.

**Model answer:** An unbuffered channel synchronises a send with a receiver. A buffered channel holds a bounded number of values; closing announces that no more values will be sent. Early consumer exit needs a cancellation design for blocked producers.

## 9. Recall card

- Range drains a closed channel before stopping.
- The sending side owns closure.
- Buffer capacity limits backlog, not total work.
- Early consumer exit needs a cancellation design for blocked producers.

Further reading: [Official reference](https://go.dev/tour/concurrency/4).
