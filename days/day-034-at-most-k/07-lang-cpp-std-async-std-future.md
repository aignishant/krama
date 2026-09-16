---
day: 34
track: lang-cpp
title: "std::async, std::future, and C++20 coroutines in outline"
theme: "Concurrency IV: async"
phase: "Languages: advanced features"
status: written
---

# Day 034 · C++ — std::async, std::future, and C++20 coroutines in outline

**Today's theme:** Concurrency IV: async

**After today you can:** You can make 100 network calls at once in each language and say where the waiting happens.

**The interviewer asks it as:** *What is the difference between concurrency and parallelism?*

## 1. What this is, and why it matters

std::async can launch a computation and return a future. get waits for its result and rethrows a stored exception.

You use this when discussing concurrency iv: async in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Anu prepares breakfast. She puts water on to boil, then slices fruit while she waits. When the water is ready, she pours tea. She does not stand beside the kettle doing nothing, but she also does not pretend her two hands can cut fruit and pour hot water at exactly the same instant.

Her brother joins and takes over the fruit. Now two people can work at the same time. That is different from Anu alone switching between jobs whenever one job is waiting. Both arrangements can finish sooner than doing everything strictly in sequence, but for different reasons.

The family asks for three kinds of toast. Anu starts them together in three available slots, then collects each when ready. The order in which they finish may differ from the order in which they were requested. She still wants to serve each person the right kind, so she keeps track of which request belongs to which result.

One slot stops heating. Anu must decide whether to stop the whole breakfast, serve the other toast, or retry that one request. Simply hearing about the first failure does not magically stop the other slots from working.

Before leaving the kitchen, she checks every started job. Some finished, one failed, and none should remain forgotten. Overlapping work is useful only when she can still explain where the results and failures go.

## 3. The idea in plain English

Anu’s requested toast becomes a **future**, an eventual value or exception. Explicit launch::async requires asynchronous execution; the default policy may choose deferred execution. A deferred operation can run only when its future is waited on or retrieved.

Keep all futures before getting results if overlap is intended. C++20 coroutines are a different mechanism: co_await can suspend a function, but the standard language feature does not supply a scheduler or complete asynchronous I/O runtime. A coroutine is not automatically a new thread. Future waiting and destruction also need attention because some async-associated futures block during cleanup.

## 4. The picture

```text
task A: start -- wait -------- finish
task B:        start -- wait -- finish
one coordinator switches while work waits
```

Overlapping waits is concurrency; simultaneous execution requires additional execution capacity.

## 5. The code, built step by step

First isolate the important operation:

```cpp
auto first = std::async(std::launch::async, work, 1);
auto second = std::async(std::launch::async, work, 2);
```

Retain futures before waiting when overlap is intended.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <chrono>
#include <future>
#include <iostream>
#include <thread>

int work(int number) {
    std::this_thread::sleep_for(std::chrono::milliseconds(10));
    return number * 10;
}
int main() {
    auto first = std::async(std::launch::async, work, 1);
    auto second = std::async(std::launch::async, work, 2);
    std::cout << first.get() << ' ' << second.get() << '\n';
}
```

**Check the result:** Prints `10 20`. Both asynchronous operations are launched before either result is retrieved.

## 6. How the other two languages do it

**Python**

```python
results = await asyncio.gather(fetch(1), fetch(2), fetch(3))
```

asyncio runs coroutines cooperatively. await allows the event loop to run other work while an operation is suspended.

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

Python asyncio uses cooperative await points, Go select chooses among channel operations, and C++ futures hold eventual results. None makes blocking work nonblocking merely by changing its name.

## 7. The traps

**Near-miss:** discard each temporary future immediately; its destruction may wait, accidentally serialising successive async calls. get consumes an ordinary future’s shared state, so do not call get twice. A promise destroyed before fulfilling its state makes get throw future_error with the broken_promise category; exact what() text varies.

## 8. Say it out loud

**How it gets asked:** “What is the difference between concurrency and parallelism?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I retain futures for all independent operations before waiting, and I choose launch::async when deferred execution would violate the intended overlap. I retrieve every result or failure and keep referenced inputs alive. Futures represent completion; they do not automatically offer cancellation. C++ coroutines provide suspension mechanics, while an executor or library supplies scheduling and I/O integration. I avoid claiming that either abstraction guarantees a speedup.

**Follow-ups**

1. **Why specify launch::async?** The default policy may choose deferred execution.

2. **Can an ordinary future be read repeatedly with get?** No. Use shared_future when repeated shared access is the intended contract.

3. **Does timing out wait_for stop the work?** No. It reports readiness; cancellation is a separate mechanism.

**Model answer:** std::async can launch a computation and return a future. get waits for its result and rethrows a stored exception. Waiting and cancellation are separate contracts.

## 9. Recall card

- Retain futures before waiting when overlap is intended.
- get transports a result or stored exception.
- Coroutines require scheduling support beyond syntax.
- Waiting and cancellation are separate contracts.

Further reading: [Official reference](https://eel.is/c++draft/futures.async).
