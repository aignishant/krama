---
day: 35
track: lang-cpp
title: "A thread pool class with a task queue"
theme: "Worker pools and pipelines"
phase: "Languages: advanced features"
status: written
---

# Day 035 · C++ — A thread pool class with a task queue

**Today's theme:** Worker pools and pipelines

**After today you can:** You can run N jobs on K workers in each language and collect results in order.

**The interviewer asks it as:** *How would you process a million items with eight workers?*

## 1. What this is, and why it matters

A fixed thread pool combines worker threads with a synchronised task queue. Futures connect each submitted task to its eventual value or exception.

You use this when discussing worker pools and pipelines in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Kiran has forty lunch boxes to pack. He can ask four relatives to help, but the kitchen cannot fit forty people. Giving every box its own helper would make the room crowded without creating more counter space.

He places the empty boxes at one end and asks each helper to take the next unfinished one. A helper who finishes early takes another. Nobody needs to know beforehand which boxes will take longer because one needs a special meal or an extra container.

The finished boxes belong to numbered seats. Kiran puts the seat number beside each task before it is handed out. When a helper returns a box, he places it in the matching position. The order of completion does not have to be the order of presentation.

There is room for only a few waiting boxes beside the counter. Kiran brings more from storage when space opens. He does not pile all forty on the floor and make the helpers climb over them. The number of active helpers and the number of waiting boxes are two separate limits.

When the last empty box has been handed out, the helpers finish what they already hold. Kiran checks the whole row before calling everyone to eat. A helper who could not complete a special meal tells him which seat is affected, so the failure does not vanish among the completed boxes.

## 3. The idea in plain English

Kiran’s helpers become threads that repeatedly remove tasks from one queue. A **packaged_task** stores either its callable’s return value or its exception in a state observed through a future. This avoids letting a normal job exception escape the worker entry point.

The pool below deliberately supports integer-returning tasks only. Its bounded queue blocks submission when pending work reaches capacity. Destruction marks stopping, wakes workers, drains queued work, and joins. Submission and destruction must not race. Constructor failure also joins any workers already created, so partial construction does not leave live threads accessing a destroyed pool.

## 4. The picture

```text
input -> bounded pending jobs -> K workers -> (index, result) -> ordered output
                                    K limits active work
```

Bound active workers and queued work separately. Preserve identity when completion order varies.

## 5. The code, built step by step

First isolate the important operation:

```cpp
task(); // packaged_task stores a value or exception for its future
```

Release the queue lock before executing a task.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <condition_variable>
#include <functional>
#include <future>
#include <iostream>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <vector>

class Pool {
    std::mutex mutex;
    std::condition_variable changed;
    std::queue<std::packaged_task<int()>> jobs;
    std::vector<std::thread> workers;
    std::size_t capacity;
    bool stopping = false;
    void work() {
        for (;;) {
            std::packaged_task<int()> task;
            {
                std::unique_lock lock(mutex);
                changed.wait(lock, [&] { return stopping || !jobs.empty(); });
                if (jobs.empty()) return;
                task = std::move(jobs.front()); jobs.pop();
            }
            changed.notify_all();
            task();
        }
    }
    void stop() {
        { std::lock_guard lock(mutex); stopping = true; }
        changed.notify_all();
        for (auto& worker : workers) if (worker.joinable()) worker.join();
    }
public:
    Pool(std::size_t count, std::size_t bound) : capacity(bound) {
        if (!count || !bound) throw std::invalid_argument("positive bounds required");
        try {
            for (std::size_t i = 0; i < count; ++i) workers.emplace_back([this] { work(); });
        } catch (...) { stop(); throw; }
    }
    ~Pool() { stop(); }
    std::future<int> submit(std::function<int()> fn) {
        std::packaged_task<int()> task(std::move(fn));
        auto result = task.get_future();
        std::unique_lock lock(mutex);
        changed.wait(lock, [&] { return stopping || jobs.size() < capacity; });
        if (stopping) throw std::runtime_error("pool stopped");
        jobs.push(std::move(task));
        lock.unlock(); changed.notify_all();
        return result;
    }
};
int main() {
    Pool pool(3, 3);
    std::vector<std::future<int>> results;
    for (int i = 0; i < 6; ++i) results.push_back(pool.submit([i] { return i * i; }));
    for (auto& result : results) std::cout << result.get() << ' ';
    std::cout << '\n';
}
```

**Check the result:** Prints `0 1 4 9 16 25`. Futures are retrieved in submission order even if jobs finish in a different order.

## 6. How the other two languages do it

**Python**

```python
done, pending = wait(pending, return_when=FIRST_COMPLETED)
```

ThreadPoolExecutor reuses worker threads and returns futures. ProcessPoolExecutor uses separate processes for work that benefits from parallel CPU execution.

**Go**

```go
for job := range jobs {
    results <- Result{job.Index, job.Value * job.Value}
}
```

A worker pool runs a fixed number of goroutines over a shared jobs channel. Fan-in collects their results through one output channel.

Python executors provide a pool, Go commonly uses worker goroutines and channels, and C++ can build a pool from threads plus a protected queue. Returning every result still needs storage proportional to the result set.

## 7. The traps

**Near-miss:** hold the queue mutex while executing a job, serialising workers and risking deadlock if a job submits work. The example releases it first. Invalid bounds throw std::invalid_argument with `positive bounds required`. Do not submit nested jobs and wait for them in every worker of a saturated pool.

## 8. Say it out loud

**How it gets asked:** “How would you process a million items with eight workers?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate the queue’s short critical section from job execution and bound pending tasks. Each packaged task carries its own result state, so exceptions reach future.get rather than escape the worker. Shutdown stops admission, drains accepted work, and joins before storage is destroyed. I also handle partial constructor failure. This educational pool does not support cancellation or safe concurrent destruction; those are separate API contracts.

**Follow-ups**

1. **Does queue capacity bound retained futures?** No. The caller can still keep a future for every submitted job.

2. **Why execute outside the lock?** Otherwise one job blocks all dequeue operations and may deadlock on nested submission.

3. **How is a job exception delivered?** packaged_task stores it and future.get rethrows it.

**Model answer:** A fixed thread pool combines worker threads with a synchronised task queue. Futures connect each submitted task to its eventual value or exception. Futures transport failures but do not provide cancellation.

## 9. Recall card

- Release the queue lock before executing a task.
- Bound pending tasks separately from threads.
- Join before destroying shared pool state.
- Futures transport failures but do not provide cancellation.

Further reading: [Official reference](https://eel.is/c++draft/futures.task).
