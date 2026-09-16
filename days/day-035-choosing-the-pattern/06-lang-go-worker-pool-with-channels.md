---
day: 35
track: lang-go
title: "Worker pool with channels, fan-out and fan-in"
theme: "Worker pools and pipelines"
phase: "Languages: advanced features"
status: written
---

# Day 035 · Go — Worker pool with channels, fan-out and fan-in

**Today's theme:** Worker pools and pipelines

**After today you can:** You can run N jobs on K workers in each language and collect results in order.

**The interviewer asks it as:** *How would you process a million items with eight workers?*

## 1. What this is, and why it matters

A worker pool runs a fixed number of goroutines over a shared jobs channel. Fan-in collects their results through one output channel.

You use this when discussing worker pools and pipelines in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Kiran has forty lunch boxes to pack. He can ask four relatives to help, but the kitchen cannot fit forty people. Giving every box its own helper would make the room crowded without creating more counter space.

He places the empty boxes at one end and asks each helper to take the next unfinished one. A helper who finishes early takes another. Nobody needs to know beforehand which boxes will take longer because one needs a special meal or an extra container.

The finished boxes belong to numbered seats. Kiran puts the seat number beside each task before it is handed out. When a helper returns a box, he places it in the matching position. The order of completion does not have to be the order of presentation.

There is room for only a few waiting boxes beside the counter. Kiran brings more from storage when space opens. He does not pile all forty on the floor and make the helpers climb over them. The number of active helpers and the number of waiting boxes are two separate limits.

When the last empty box has been handed out, the helpers finish what they already hold. Kiran checks the whole row before calling everyone to eat. A helper who could not complete a special meal tells him which seat is affected, so the failure does not vanish among the completed boxes.

## 3. The idea in plain English

Kiran’s numbered boxes become Job values. **Fan-out** distributes work to several workers; fan-in combines their outputs. Each result carries its original index because completion order can differ.

The jobs buffer bounds waiting tasks, and the worker count bounds active tasks. A coordinator closes results only after every worker exits. Main drains results while production continues, preventing a cycle where producers and workers all block on full channels. Cancellation and job errors need an explicit extension; this example’s square operation cannot fail for its small inputs.

## 4. The picture

```text
input -> bounded pending jobs -> K workers -> (index, result) -> ordered output
                                    K limits active work
```

Bound active workers and queued work separately. Preserve identity when completion order varies.

## 5. The code, built step by step

First isolate the important operation:

```go
for job := range jobs {
    results <- Result{job.Index, job.Value * job.Value}
}
```

Bound jobs and worker count independently.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "sync"
)
type Job struct{ Index, Value int }
type Result struct{ Index, Value int }
func main() {
    jobs := make(chan Job, 3)
    results := make(chan Result)
    var group sync.WaitGroup
    for worker := 0; worker < 3; worker++ {
        group.Add(1)
        go func() {
            defer group.Done()
            for job := range jobs { results <- Result{job.Index, job.Value * job.Value} }
        }()
    }
    go func() {
        for i := 0; i < 6; i++ { jobs <- Job{i, i} }
        close(jobs)
    }()
    go func() { group.Wait(); close(results) }()
    output := make([]int, 6)
    for result := range results { output[result.Index] = result.Value }
    fmt.Println(output)
}
```

**Check the result:** Prints `[0 1 4 9 16 25]`. Three workers share three pending-job slots; main alone writes the output slice.

## 6. How the other two languages do it

**Python**

```python
done, pending = wait(pending, return_when=FIRST_COMPLETED)
```

ThreadPoolExecutor reuses worker threads and returns futures. ProcessPoolExecutor uses separate processes for work that benefits from parallel CPU execution.

**C++**

```cpp
task(); // packaged_task stores a value or exception for its future
```

A fixed thread pool combines worker threads with a synchronised task queue. Futures connect each submitted task to its eventual value or exception.

Python executors provide a pool, Go commonly uses worker goroutines and channels, and C++ can build a pool from threads plus a protected queue. Returning every result still needs storage proportional to the result set.

## 7. The traps

**Near-miss:** let each worker close results when it finishes. Another worker can panic with `send on closed channel`. Closing belongs to the coordinator after Wait. Filling jobs synchronously before draining unbuffered results can deadlock when workers stop taking jobs to wait for main.

## 8. Say it out loud

**How it gets asked:** “How would you process a million items with eight workers?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I start a fixed worker count, feed a bounded jobs channel, and drain results concurrently with submission. Each result keeps its index so the final slice can preserve input order. One coordinator closes the result channel after all workers stop. I would add an error field and cancellation-aware sends for fallible jobs, so early caller exit does not strand workers. Input and output storage remain separate from the pool’s bound.

**Follow-ups**

1. **Does channel capacity limit the worker count?** No. Capacity limits queued values; the number of started workers limits active jobs.

2. **Who closes results?** A coordinator after every sender has finished.

3. **What happens if a collector returns early?** Workers may block sending; propagate cancellation or keep draining.

**Model answer:** A worker pool runs a fixed number of goroutines over a shared jobs channel. Fan-in collects their results through one output channel. Early collection exit needs a plan for blocked sends.

## 9. Recall card

- Bound jobs and worker count independently.
- Carry indices when output order matters.
- Close results only after all senders exit.
- Early collection exit needs a plan for blocked sends.

Further reading: [Official reference](https://go.dev/blog/pipelines).
