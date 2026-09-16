---
day: 36
track: lang-go
title: "context.Context: WithTimeout, WithCancel, and Done()"
theme: "Timeouts and cancellation"
phase: "Languages: advanced features"
status: written
---

# Day 036 · Go — context.Context: WithTimeout, WithCancel, and Done()

**Today's theme:** Timeouts and cancellation

**After today you can:** You can stop a long job cleanly from the outside in each language.

**The interviewer asks it as:** *How do you cancel a request that is taking too long?*

## 1. What this is, and why it matters

context.Context carries cancellation and deadlines across call boundaries. Workers select on Done and report Err when the request is cancelled or expires.

You use this when discussing timeouts and cancellation in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Neha asks a neighbour to bring bread before breakfast. She says they will start eating at nine. If he cannot return by then, he should stop trying and let her know. The request has both a job and a time after which completing it is no longer useful.

At half past eight, Neha finds bread in the cupboard. She calls the neighbour to say he can stop now. He is walking between shops and hears the call. He turns back. If his phone were silent and he never checked it, her wish to stop would not somehow move him home.

Before leaving a shop, he makes sure he has not left a bag or an unpaid order behind. Stopping the search does not remove the need to finish small responsibilities already taken on. Neha waits for his reply so she knows he has actually heard and finished returning.

Her brother suggests saying stop without waiting for a response. Neha points out that this would tell her only what she requested, not what happened. The neighbour might still be buying bread at another shop.

They agree to pass the same finishing time to anyone else asked to help. A second helper should not invent a new full hour just because the request reached them later. Everyone works under the original need, checks whether it still exists, and reports when their part is over.

## 3. The idea in plain English

Neha passes one finishing time through the chain of helpers. A **context** carries that request lifetime. WithCancel returns a child and a cancel function; WithTimeout also attaches a deadline. Calling cancel releases resources associated with the derived context, so defer it even when the operation is expected to finish early.

Done is a channel closed on cancellation. Err distinguishes context.Canceled from context.DeadlineExceeded. Pass the context into actual blocking APIs or select alongside their channel operations. Checking once before a long uninterruptible call does not make that call cancellable.

## 4. The picture

```text
caller -> stop request/deadline -> worker observes -> cleanup -> completion
         request is not completion
```

Cancellation is a cooperative protocol. A deadline must reach the operation that can block.

## 5. The code, built step by step

First isolate the important operation:

```go
select {
case <-ctx.Done():
    return ctx.Err()
case value := <-jobs:
    _ = value
}
```

Propagate context to blocking operations.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "context"
    "fmt"
    "time"
)
func work(ctx context.Context) error {
    timer := time.NewTimer(time.Hour)
    defer timer.Stop()
    select {
    case <-ctx.Done(): return ctx.Err()
    case <-timer.C: return nil
    }
}
func main() {
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Millisecond)
    defer cancel()
    fmt.Println(work(ctx))
    manual, stop := context.WithCancel(context.Background())
    stop()
    fmt.Println(work(manual))
}
```

**Check the result:** Prints `context deadline exceeded` and `context canceled`.

## 6. How the other two languages do it

**Python**

```python
async with asyncio.timeout(0.01):
    await work(stop)
```

asyncio.timeout limits an asynchronous scope using cancellation. Task cancellation is cooperative and cleanup belongs in finally blocks.

**C++**

```cpp
while (!stop.stop_requested() && std::chrono::steady_clock::now() < deadline) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
}
```

std::stop_token lets work observe a cooperative stop request. A deadline is a separate time condition, usually measured with steady_clock.

Python task cancellation is delivered at await points, Go context exposes Done and Err, and C++ stop_token reports a stop request. None safely kills arbitrary work at an arbitrary instruction.

## 7. The traps

**Near-miss:** replace the child context with context.Background inside a lower layer and lose the caller’s deadline. The example preserves the distinct diagnostics `context deadline exceeded` and `context canceled`. Calling cancel does not wait for a goroutine; use a result channel or WaitGroup when completion must be observed.

## 8. Say it out loud

**How it gets asked:** “How do you cancel a request that is taking too long?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I accept context as the first parameter and pass it down to the operation that can block. I defer the cancel function for every derived context I own. The worker selects on Done, cleans up, and returns Err so the caller can classify the reason. I use a separate completion mechanism when I need to know shutdown has actually finished. A timeout cannot cancel code that ignores the context.

**Follow-ups**

1. **Does cancel wait for worker exit?** No. It signals cancellation; joining is separate.

2. **Why defer cancel after WithTimeout?** It releases associated resources when work finishes before the deadline too.

3. **Can a child deadline extend its parent’s deadline?** No. Parent cancellation still stops the child.

**Model answer:** context.Context carries cancellation and deadlines across call boundaries. Workers select on Done and report Err when the request is cancelled or expires. Cancellation signalling and completion waiting are separate responsibilities.

## 9. Recall card

- Propagate context to blocking operations.
- Release derived contexts with cancel.
- Use Err to distinguish timeout and cancellation.
- Cancellation signalling and completion waiting are separate responsibilities.

Further reading: [Official reference](https://pkg.go.dev/context).
