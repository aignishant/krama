---
day: 36
track: lang-cpp
title: "std::stop_token, deadlines, and checking a flag"
theme: "Timeouts and cancellation"
phase: "Languages: advanced features"
status: written
---

# Day 036 · C++ — std::stop_token, deadlines, and checking a flag

**Today's theme:** Timeouts and cancellation

**After today you can:** You can stop a long job cleanly from the outside in each language.

**The interviewer asks it as:** *How do you cancel a request that is taking too long?*

## 1. What this is, and why it matters

std::stop_token lets work observe a cooperative stop request. A deadline is a separate time condition, usually measured with steady_clock.

You use this when discussing timeouts and cancellation in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Neha asks a neighbour to bring bread before breakfast. She says they will start eating at nine. If he cannot return by then, he should stop trying and let her know. The request has both a job and a time after which completing it is no longer useful.

At half past eight, Neha finds bread in the cupboard. She calls the neighbour to say he can stop now. He is walking between shops and hears the call. He turns back. If his phone were silent and he never checked it, her wish to stop would not somehow move him home.

Before leaving a shop, he makes sure he has not left a bag or an unpaid order behind. Stopping the search does not remove the need to finish small responsibilities already taken on. Neha waits for his reply so she knows he has actually heard and finished returning.

Her brother suggests saying stop without waiting for a response. Neha points out that this would tell her only what she requested, not what happened. The neighbour might still be buying bread at another shop.

They agree to pass the same finishing time to anyone else asked to help. A second helper should not invent a new full hour just because the request reached them later. Everyone works under the original need, checks whether it still exists, and reports when their part is over.

## 3. The idea in plain English

Neha’s phone call is a stop request. A **stop token** refers to shared stop state owned by a source such as jthread. stop_requested checks it; it does not interrupt arbitrary code. request_stop signals, while join waits for completion.

The example checks both a token and a deadline between short waits. Polling delay bounds responsiveness only approximately; scheduling and a blocking operation can add delay. A stop-aware condition_variable_any wait can avoid repeated polling for appropriate designs. Objects borrowed by the worker must remain alive until it exits.

## 4. The picture

```text
caller -> stop request/deadline -> worker observes -> cleanup -> completion
         request is not completion
```

Cancellation is a cooperative protocol. A deadline must reach the operation that can block.

## 5. The code, built step by step

First isolate the important operation:

```cpp
while (!stop.stop_requested() && std::chrono::steady_clock::now() < deadline) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1));
}
```

Check the stop token at deliberate points.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <chrono>
#include <iostream>
#include <stop_token>
#include <thread>

int main() {
    using namespace std::chrono;
    bool stopped = false;
    auto deadline = steady_clock::now() + hours(1);
    std::jthread worker([&](std::stop_token stop) {
        while (!stop.stop_requested() && steady_clock::now() < deadline) {
            std::this_thread::sleep_for(milliseconds(1));
        }
        stopped = stop.stop_requested();
    });
    worker.request_stop();
    worker.join();
    std::cout << std::boolalpha << stopped << '\n';
}
```

**Check the result:** Prints `true`. Main reads stopped after joining, so that read is ordered after the worker’s write.

## 6. How the other two languages do it

**Python**

```python
async with asyncio.timeout(0.01):
    await work(stop)
```

asyncio.timeout limits an asynchronous scope using cancellation. Task cancellation is cooperative and cleanup belongs in finally blocks.

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

Python task cancellation is delivered at await points, Go context exposes Done and Err, and C++ stop_token reports a stop request. None safely kills arbitrary work at an arbitrary instruction.

## 7. The traps

**Near-miss:** assume request_stop interrupts a blocking socket call or sleep. It does not. If a worker ignores the token, a jthread destructor may wait indefinitely. A stable application diagnostic might be `deadline exceeded`, but stop_token itself throws no timeout exception and supplies no forced-termination diagnostic.

## 8. Say it out loud

**How it gets asked:** “How do you cancel a request that is taking too long?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I pass a stop token into the worker and define where it checks for stop. I use steady_clock for a deadline and ensure long blocking operations also have a bounded or stop-aware wait. I request stop, then join before destroying borrowed resources. I do not claim a stop request is an interruption primitive. A worker that never checks the token can continue running, so cancellation responsiveness is part of the operation’s contract.

**Follow-ups**

1. **Does request_stop join?** No. It signals; join waits.

2. **What clock suits an elapsed deadline?** steady_clock avoids wall-clock adjustments.

3. **Does a token interrupt an arbitrary blocking call?** No. The call needs its own timeout or cancellation integration.

**Model answer:** std::stop_token lets work observe a cooperative stop request. A deadline is a separate time condition, usually measured with steady_clock. Cooperative cancellation cannot stop code that never observes it.

## 9. Recall card

- Check the stop token at deliberate points.
- Use steady_clock for elapsed deadlines.
- Join before destroying borrowed state.
- Cooperative cancellation cannot stop code that never observes it.

Further reading: [Official reference](https://eel.is/c++draft/thread.stoptoken).
