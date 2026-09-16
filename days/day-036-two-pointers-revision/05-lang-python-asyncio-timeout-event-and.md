---
day: 36
track: lang-python
title: "asyncio.timeout, Event, and cooperative cancellation"
theme: "Timeouts and cancellation"
phase: "Languages: advanced features"
status: written
---

# Day 036 · Python — asyncio.timeout, Event, and cooperative cancellation

**Today's theme:** Timeouts and cancellation

**After today you can:** You can stop a long job cleanly from the outside in each language.

**The interviewer asks it as:** *How do you cancel a request that is taking too long?*

## 1. What this is, and why it matters

asyncio.timeout limits an asynchronous scope using cancellation. Task cancellation is cooperative and cleanup belongs in finally blocks.

You use this when discussing timeouts and cancellation in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Neha asks a neighbour to bring bread before breakfast. She says they will start eating at nine. If he cannot return by then, he should stop trying and let her know. The request has both a job and a time after which completing it is no longer useful.

At half past eight, Neha finds bread in the cupboard. She calls the neighbour to say he can stop now. He is walking between shops and hears the call. He turns back. If his phone were silent and he never checked it, her wish to stop would not somehow move him home.

Before leaving a shop, he makes sure he has not left a bag or an unpaid order behind. Stopping the search does not remove the need to finish small responsibilities already taken on. Neha waits for his reply so she knows he has actually heard and finished returning.

Her brother suggests saying stop without waiting for a response. Neha points out that this would tell her only what she requested, not what happened. The neighbour might still be buying bread at another shop.

They agree to pass the same finishing time to anyone else asked to help. A second helper should not invent a new full hour just because the request reached them later. Everyone works under the original need, checks whether it still exists, and reports when their part is over.

## 3. The idea in plain English

Neha’s stop request becomes cancellation. **CancelledError** is raised at an opportunity where the task can observe cancellation, commonly an await. It derives from BaseException, and swallowing it can break structured timeout and task-group behaviour.

The timeout context converts its own cancellation into TimeoutError outside the context. An asyncio.Event provides a separate cooperative signal when workers should stop at chosen checkpoints. An event alone does not interrupt an unrelated blocked await. CPU loops that never yield cannot observe event-loop cancellation promptly.

## 4. The picture

```text
caller -> stop request/deadline -> worker observes -> cleanup -> completion
         request is not completion
```

Cancellation is a cooperative protocol. A deadline must reach the operation that can block.

## 5. The code, built step by step

First isolate the important operation:

```python
async with asyncio.timeout(0.01):
    await work(stop)
```

Put cleanup in finally.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
import asyncio

async def work(stop: asyncio.Event) -> None:
    try:
        while not stop.is_set():
            await asyncio.sleep(1)
    finally:
        print("cleanup")

async def main() -> None:
    stop = asyncio.Event()
    try:
        async with asyncio.timeout(0.01):
            await work(stop)
    except TimeoutError:
        print("timed out")

if __name__ == "__main__":
    asyncio.run(main())
```

**Check the result:** Prints `cleanup` and then `timed out`. The deadline is a scheduling bound for cooperative work, not a guarantee that arbitrary blocking code is forcibly interrupted.

## 6. How the other two languages do it

**Go**

```go
select {
case <-ctx.Done():
    return ctx.Err()
case value := <-jobs:
    _ = value
}
```

context.Context carries cancellation and deadlines across call boundaries. Workers select on Done and report Err when the request is cancelled or expires.

**C++**

```cpp
while (!stop.stop_requested() && std::chrono::steady_clock::now() < deadline) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
}
```

std::stop_token lets work observe a cooperative stop request. A deadline is a separate time condition, usually measured with steady_clock.

Python task cancellation is delivered at await points, Go context exposes Done and Err, and C++ stop_token reports a stop request. None safely kills arbitrary work at an arbitrary instruction.

## 7. The traps

**Near-miss:** catch CancelledError and continue forever; the timeout cannot reliably finish the intended scope. The outer handler receives `TimeoutError`. Calling stop.set in this example is checked only after sleep finishes; if immediate event responsiveness is required, await the event or race it against the operation with proper cleanup.

## 8. Say it out loud

**How it gets asked:** “How do you cancel a request that is taking too long?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I propagate a deadline into the asynchronous scope and use finally to release resources. I let CancelledError propagate unless I have a precise reason to suppress it. I distinguish requesting cancellation from waiting for the task to finish. An Event can support voluntary checkpoints, but blocking calls must also have a cancellation-aware path. A busy CPU loop needs cooperative yields or execution outside the event-loop thread.

**Follow-ups**

1. **Does cancellation forcibly kill a coroutine?** No. It is observed cooperatively at suitable suspension points.

2. **Where do you catch the timeout?** Outside the asyncio.timeout context that converts its cancellation to TimeoutError.

3. **Does setting an Event interrupt every await?** No. The awaited operation must observe or be coordinated with that event.

**Model answer:** asyncio.timeout limits an asynchronous scope using cancellation. Task cancellation is cooperative and cleanup belongs in finally blocks. A cancellation request is not proof that work has stopped.

## 9. Recall card

- Put cleanup in finally.
- Propagate cancellation after cleanup.
- Catch TimeoutError outside the timeout scope.
- A cancellation request is not proof that work has stopped.

Further reading: [Official reference](https://docs.python.org/3.12/library/asyncio-task.html#timeouts).
