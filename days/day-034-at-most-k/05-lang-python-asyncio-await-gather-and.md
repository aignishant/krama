---
day: 34
track: lang-python
title: "asyncio, await, gather, and the event loop"
theme: "Concurrency IV: async"
phase: "Languages: advanced features"
status: written
---

# Day 034 · Python — asyncio, await, gather, and the event loop

**Today's theme:** Concurrency IV: async

**After today you can:** You can make 100 network calls at once in each language and say where the waiting happens.

**The interviewer asks it as:** *What is the difference between concurrency and parallelism?*

## 1. What this is, and why it matters

asyncio runs coroutines cooperatively. await allows the event loop to run other work while an operation is suspended.

You use this when discussing concurrency iv: async in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Anu prepares breakfast. She puts water on to boil, then slices fruit while she waits. When the water is ready, she pours tea. She does not stand beside the kettle doing nothing, but she also does not pretend her two hands can cut fruit and pour hot water at exactly the same instant.

Her brother joins and takes over the fruit. Now two people can work at the same time. That is different from Anu alone switching between jobs whenever one job is waiting. Both arrangements can finish sooner than doing everything strictly in sequence, but for different reasons.

The family asks for three kinds of toast. Anu starts them together in three available slots, then collects each when ready. The order in which they finish may differ from the order in which they were requested. She still wants to serve each person the right kind, so she keeps track of which request belongs to which result.

One slot stops heating. Anu must decide whether to stop the whole breakfast, serve the other toast, or retry that one request. Simply hearing about the first failure does not magically stop the other slots from working.

Before leaving the kitchen, she checks every started job. Some finished, one failed, and none should remain forgotten. Overlapping work is useful only when she can still explain where the results and failures go.

## 3. The idea in plain English

Anu’s switching becomes an **event loop**, a coordinator that resumes ready tasks. Calling an async function creates a coroutine; it does not by itself schedule the work. gather schedules supplied coroutines and returns results in input order.

await one call followed by await another is sequential. gather overlaps their waits. A blocking time.sleep inside a coroutine blocks the event-loop thread; use asyncio.sleep for an asynchronous delay. With default gather behaviour, the first propagated exception does not automatically cancel every sibling. TaskGroup offers a stronger grouped-lifetime and failure policy when that is required.

## 4. The picture

```text
task A: start -- wait -------- finish
task B:        start -- wait -- finish
one coordinator switches while work waits
```

Overlapping waits is concurrency; simultaneous execution requires additional execution capacity.

## 5. The code, built step by step

First isolate the important operation:

```python
results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
```

Await or schedule every coroutine that should run.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
import asyncio

async def fetch(number: int) -> int:
    await asyncio.sleep(0.01 * (4 - number))
    return number * 10

async def main() -> None:
    results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```

**Check the result:** Prints `[10, 20, 30]` although task 3 has the shortest delay. Delays overlap, but scheduling overhead means elapsed time is not an exact guarantee.

## 6. How the other two languages do it

**Go**

```go
select {
case value := <-result:
    fmt.Println(value)
case <-timer.C:
    fmt.Println("timed out")
}
```

select waits on several channel operations. Goroutines use ordinary-looking blocking code while the runtime can schedule other runnable goroutines.

**C++**

```cpp
auto first = std::async(std::launch::async, work, 1);
auto second = std::async(std::launch::async, work, 2);
```

std::async can launch a computation and return a future. get waits for its result and rethrows a stored exception.

Python asyncio uses cooperative await points, Go select chooses among channel operations, and C++ futures hold eventual results. None makes blocking work nonblocking merely by changing its name.

## 7. The traps

**Near-miss:** call fetch(1) and discard the coroutine. Python warns `RuntimeWarning: coroutine 'fetch' was never awaited`. Another mistake is using blocking I/O directly in the event loop. An async keyword does not turn the body into parallel execution.

## 8. Say it out loud

**How it gets asked:** “What is the difference between concurrency and parallelism?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I distinguish a coroutine object from a scheduled task. I overlap independent waits with gather and rely on its input-order result contract. I keep blocking operations out of the event-loop thread and specify how failures affect siblings. For bounded workloads I use a semaphore or a worker pool rather than launching an unbounded number of calls. I await all work whose lifetime belongs to this operation.

**Follow-ups**

1. **Does async imply parallel execution?** No. Coroutines on one event loop cooperate at suspension points.

2. **Does gather return completion order?** No. Its result list follows input order.

3. **Does one failure automatically cancel every sibling?** Not with default gather semantics; choose and implement the desired failure policy.

**Model answer:** asyncio runs coroutines cooperatively. await allows the event loop to run other work while an operation is suspended. Concurrency needs an explicit policy for sibling failures.

## 9. Recall card

- Await or schedule every coroutine that should run.
- Keep blocking calls out of the event loop.
- gather preserves input result order.
- Concurrency needs an explicit policy for sibling failures.

Further reading: [Official reference](https://docs.python.org/3.12/library/asyncio-task.html#asyncio.gather).
