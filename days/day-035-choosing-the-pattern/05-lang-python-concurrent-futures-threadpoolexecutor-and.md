---
day: 35
track: lang-python
title: "concurrent.futures: ThreadPoolExecutor and ProcessPoolExecutor"
theme: "Worker pools and pipelines"
phase: "Languages: advanced features"
status: written
---

# Day 035 · Python — concurrent.futures: ThreadPoolExecutor and ProcessPoolExecutor

**Today's theme:** Worker pools and pipelines

**After today you can:** You can run N jobs on K workers in each language and collect results in order.

**The interviewer asks it as:** *How would you process a million items with eight workers?*

## 1. What this is, and why it matters

ThreadPoolExecutor reuses worker threads and returns futures. ProcessPoolExecutor uses separate processes for work that benefits from parallel CPU execution.

You use this when discussing worker pools and pipelines in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Kiran has forty lunch boxes to pack. He can ask four relatives to help, but the kitchen cannot fit forty people. Giving every box its own helper would make the room crowded without creating more counter space.

He places the empty boxes at one end and asks each helper to take the next unfinished one. A helper who finishes early takes another. Nobody needs to know beforehand which boxes will take longer because one needs a special meal or an extra container.

The finished boxes belong to numbered seats. Kiran puts the seat number beside each task before it is handed out. When a helper returns a box, he places it in the matching position. The order of completion does not have to be the order of presentation.

There is room for only a few waiting boxes beside the counter. Kiran brings more from storage when space opens. He does not pile all forty on the floor and make the helpers climb over them. The number of active helpers and the number of waiting boxes are two separate limits.

When the last empty box has been handed out, the helpers finish what they already hold. Kiran checks the whole row before calling everyone to eat. A helper who could not complete a special meal tells him which seat is affected, so the failure does not vanish among the completed boxes.

## 3. The idea in plain English

Kiran’s four helpers become a fixed worker count. A **pool** reuses execution resources instead of creating one thread per item. Future.result returns a value or rethrows the job’s exception. With a process pool, submitted functions and arguments must be serialisable, and the main guard is essential on spawn-based platforms.

In Python 3.12, executor.map can eagerly collect inputs, so limiting max_workers alone does not bound queued work. The example explicitly keeps at most twice the worker count in flight and stores results by input index. Returning all results still needs O(n) space. For a true streaming output contract, yield results or persist them instead.

## 4. The picture

```text
input -> bounded pending jobs -> K workers -> (index, result) -> ordered output
                                    K limits active work
```

Bound active workers and queued work separately. Preserve identity when completion order varies.

## 5. The code, built step by step

First isolate the important operation:

```python
done, pending = wait(pending, return_when=FIRST_COMPLETED)
```

Bound submission as well as active workers.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

def square(value: int) -> int:
    return value * value

def run(values: list[int], workers: int = 3) -> list[int]:
    if workers < 1:
        raise ValueError("workers must be positive")
    output = [0] * len(values)
    source = iter(enumerate(values))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = {}
        exhausted = False
        while pending or not exhausted:
            while not exhausted and len(pending) < 2 * workers:
                item = next(source, None)
                if item is None:
                    exhausted = True
                else:
                    index, value = item
                    pending[pool.submit(square, value)] = index
            if not pending:
                break
            done, _ = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                output[pending.pop(future)] = future.result()
    return output

if __name__ == "__main__":
    print(run(list(range(6))))
```

**Check the result:** Prints `[0, 1, 4, 9, 16, 25]`. At most three jobs execute at once and at most six futures are pending in this coordinator.

## 6. How the other two languages do it

**Go**

```go
for job := range jobs {
    results <- Result{job.Index, job.Value * job.Value}
}
```

A worker pool runs a fixed number of goroutines over a shared jobs channel. Fan-in collects their results through one output channel.

**C++**

```cpp
task(); // packaged_task stores a value or exception for its future
```

A fixed thread pool combines worker threads with a synchronised task queue. Futures connect each submitted task to its eventual value or exception.

Python executors provide a pool, Go commonly uses worker goroutines and channels, and C++ can build a pool from threads plus a protected queue. Returning every result still needs storage proportional to the result set.

## 7. The traps

**Near-miss:** submit a million jobs at once and call that bounded because max_workers is eight. The queue and future objects still grow. Passing zero workers to this implementation raises `ValueError: workers must be positive`. Waiting inside a worker for another job on the same saturated pool can deadlock.

## 8. Say it out loud

**How it gets asked:** “How would you process a million items with eight workers?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I bound both execution and submission, attach an index to each job, and retrieve every future’s result or failure. Threads suit overlapping blocking I/O; processes can help CPU-heavy Python at a serialisation cost. I avoid workers waiting on tasks in their own exhausted pool. If a caller requests every result, I acknowledge that output storage remains linear even when the pool itself is bounded.

**Follow-ups**

1. **Does max_workers bound every queued job?** No. Submission must also be bounded if memory is constrained.

2. **Why keep input indices?** They restore input order after completion-order collection.

3. **What happens to an exception in a future?** result rethrows it in the collecting thread; choose how to handle remaining work.

**Model answer:** ThreadPoolExecutor reuses worker threads and returns futures. ProcessPoolExecutor uses separate processes for work that benefits from parallel CPU execution. A bounded pool does not make retained results constant-space.

## 9. Recall card

- Bound submission as well as active workers.
- Retrieve futures to observe failures.
- Use input indices for ordered output.
- A bounded pool does not make retained results constant-space.

Further reading: [Official reference](https://docs.python.org/3.12/library/concurrent.futures.html).
