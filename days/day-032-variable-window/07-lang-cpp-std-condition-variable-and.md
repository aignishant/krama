---
day: 32
track: lang-cpp
title: "std::condition_variable and a hand-built thread-safe queue"
theme: "Concurrency II: passing messages"
phase: "Languages: advanced features"
status: written
---

# Day 032 · C++ — std::condition_variable and a hand-built thread-safe queue

**Today's theme:** Concurrency II: passing messages

**After today you can:** You can move work between threads safely in each language.

**The interviewer asks it as:** *How do two threads hand data to each other safely?*

## 1. What this is, and why it matters

A condition_variable waits for a state change while a mutex protects the queue. The condition must be checked as a predicate under that mutex.

You use this when discussing concurrency ii: passing messages in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Tara prepares lunch boxes while her brother carries them to the dining room. At first she hands him each box directly. If he is still putting the previous box down, she has to wait. If she has not finished filling one, he has to wait. Neither loses a box because each handover happens face to face.

Their aunt places a tray between them with room for two boxes. Tara can now prepare the next box while her brother carries one away. When both spaces are full, she must pause. The tray helps them absorb small differences in pace, but it cannot hold an unlimited afternoon of work.

When Tara finishes, she tells her brother there will be no more boxes. He still carries the boxes already on the tray before stopping. An empty tray alone would not have told him she was finished; it might only have meant that she was filling the next box.

Later, a second helper joins. Tara makes sure both helpers know how the end will be announced. Otherwise one might wait beside the empty tray after everyone else has left.

They also agree who is allowed to announce the end. A helper who merely sees an empty tray cannot decide that the kitchen is done. The person who knows all filling work has finished owns that decision. The arrangement works because waiting, storage, and completion each have a clear meaning.

## 3. The idea in plain English

Tara’s tray becomes a queue plus a capacity limit. A **condition variable** lets a thread sleep while releasing its lock, then reacquire it before checking shared state. Waits may wake without the desired condition being true, called a spurious wakeup.

The predicate version of wait rechecks the condition. Producers wait for space; consumers wait for an item or closure. The closed flag is protected by the same mutex as the queue. notify_all after closing wakes every waiter so each can observe the final state. Closing is a state transition, not a magic feature of std::queue.

## 4. The picture

```text
producer -> [ bounded queue: at most 2 items ] -> consumer
 full: producer waits             empty: consumer waits
 finished: explicit end signal; drain earlier items
```

A queue needs both a capacity policy and an end-of-stream policy.

## 5. The code, built step by step

First isolate the important operation:

```cpp
ready.wait(lock, [&] { return closed || !items.empty(); });
```

Use predicate waits under the protecting mutex.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <optional>
#include <queue>
#include <stdexcept>
#include <thread>

class Queue {
    std::mutex mutex;
    std::condition_variable ready;
    std::queue<int> items;
    bool closed = false;
public:
    void put(int value) {
        std::unique_lock lock(mutex);
        ready.wait(lock, [&] { return closed || items.size() < 2; });
        if (closed) throw std::logic_error("queue closed");
        items.push(value);
        ready.notify_all();
    }
    std::optional<int> get() {
        std::unique_lock lock(mutex);
        ready.wait(lock, [&] { return closed || !items.empty(); });
        if (items.empty()) return std::nullopt;
        int value = items.front(); items.pop();
        ready.notify_all();
        return value;
    }
    void close() {
        std::lock_guard lock(mutex);
        closed = true;
        ready.notify_all();
    }
};
int main() {
    Queue jobs;
    int total = 0;
    std::jthread worker([&] { while (auto value = jobs.get()) total += *value; });
    for (int value : {1, 2, 3}) jobs.put(value);
    jobs.close();
    worker.join();
    std::cout << total << '\n';
}
```

**Check the result:** Prints `6`. The queue drains after close, then get returns nullopt.

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

**Go**

```go
for value := range jobs {
    total += value
}
```

An unbuffered channel synchronises a send with a receiver. A buffered channel holds a bounded number of values; closing announces that no more values will be sent.

Python Queue combines locking and blocking operations. Go channels integrate communication with the language. C++ condition_variable coordinates waiting around a separately protected queue.

## 7. The traps

**Near-miss:** use wait without a predicate and read front from an empty queue after an unrelated wakeup. That violates the container’s precondition; no diagnostic is guaranteed. Putting after close throws std::logic_error with the explicit message `queue closed`. Always protect the closed flag with the queue’s mutex.

## 8. Say it out loud

**How it gets asked:** “How do two threads hand data to each other safely?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I keep the data and its completion flag under one mutex. A producer waits for space; a consumer waits for data or final closure. Predicate waits handle spurious wakeups and recheck state after acquiring the lock. Closing wakes all waiters, and consumers drain prior items before returning absence. I keep the queue alive until every worker has joined and define what a put after close means.

**Follow-ups**

1. **Does an empty queue mean done?** No. It is final only when closed is also true.

2. **Why recheck after waking?** Another consumer may take the item first, or the wakeup may be spurious.

3. **How do two consumers stop?** Close sets shared state and notifies all; both eventually observe closed plus empty.

**Model answer:** A condition_variable waits for a state change while a mutex protects the queue. The condition must be checked as a predicate under that mutex. Queue lifetime must extend until every waiting worker exits.

## 9. Recall card

- Use predicate waits under the protecting mutex.
- Protect the closed flag with the queue state.
- Wake all waiters when closing.
- Queue lifetime must extend until every waiting worker exits.

Further reading: [Official reference](https://eel.is/c++draft/thread.condition.condvar).
