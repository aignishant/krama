---
day: 32
track: lang-python
title: "queue.Queue and producer-consumer"
theme: "Concurrency II: passing messages"
phase: "Languages: advanced features"
status: written
---

# Day 032 · Python — queue.Queue and producer-consumer

**Today's theme:** Concurrency II: passing messages

**After today you can:** You can move work between threads safely in each language.

**The interviewer asks it as:** *How do two threads hand data to each other safely?*

## 1. What this is, and why it matters

queue.Queue safely transfers work between threads. A finite maxsize applies backpressure by blocking producers when the queue is full.

You use this when discussing concurrency ii: passing messages in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Tara prepares lunch boxes while her brother carries them to the dining room. At first she hands him each box directly. If he is still putting the previous box down, she has to wait. If she has not finished filling one, he has to wait. Neither loses a box because each handover happens face to face.

Their aunt places a tray between them with room for two boxes. Tara can now prepare the next box while her brother carries one away. When both spaces are full, she must pause. The tray helps them absorb small differences in pace, but it cannot hold an unlimited afternoon of work.

When Tara finishes, she tells her brother there will be no more boxes. He still carries the boxes already on the tray before stopping. An empty tray alone would not have told him she was finished; it might only have meant that she was filling the next box.

Later, a second helper joins. Tara makes sure both helpers know how the end will be announced. Otherwise one might wait beside the empty tray after everyone else has left.

They also agree who is allowed to announce the end. A helper who merely sees an empty tray cannot decide that the kitchen is done. The person who knows all filling work has finished owns that decision. The arrangement works because waiting, storage, and completion each have a clear meaning.

## 3. The idea in plain English

Tara’s tray becomes Queue(maxsize=2). **Backpressure** makes a fast producer wait rather than grow storage indefinitely. put sends an item; get waits for one. A unique sentinel marks the end because an empty queue does not mean production has finished.

task_done accounts for each retrieved item, including this example’s sentinel. Queue.join waits for unfinished-item accounting to reach zero; Thread.join waits for the consumer to terminate. They solve different problems. With several consumers, send one sentinel per consumer or use another explicit broadcast shutdown design.

## 4. The picture

```text
producer -> [ bounded queue: at most 2 items ] -> consumer
 full: producer waits             empty: consumer waits
 finished: explicit end signal; drain earlier items
```

A queue needs both a capacity policy and an end-of-stream policy.

## 5. The code, built step by step

First isolate the important operation:

```python
item = jobs.get()
try:
    if item is None:
        return
finally:
    jobs.task_done()
```

Start consumers before filling a bounded queue.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from queue import Queue
from threading import Thread

def consume(jobs: Queue[int | None], results: list[int]) -> None:
    while True:
        item = jobs.get()
        try:
            if item is None:
                return
            results.append(item * 2)
        finally:
            jobs.task_done()

jobs: Queue[int | None] = Queue(maxsize=2)
results: list[int] = []
worker = Thread(target=consume, args=(jobs, results))
worker.start()
for value in (1, 2, 3):
    jobs.put(value)
jobs.put(None)
jobs.join()
worker.join()
print(results)
```

**Check the result:** Prints `[2, 4, 6]`. Only the single consumer appends; main reads after joining.

## 6. How the other two languages do it

**Go**

```go
for value := range jobs {
    total += value
}
```

An unbuffered channel synchronises a send with a receiver. A buffered channel holds a bounded number of values; closing announces that no more values will be sent.

**C++**

```cpp
ready.wait(lock, [&] { return closed || !items.empty(); });
```

A condition_variable waits for a state change while a mutex protects the queue. The condition must be checked as a predicate under that mutex.

Python Queue combines locking and blocking operations. Go channels integrate communication with the language. C++ condition_variable coordinates waiting around a separately protected queue.

## 7. The traps

**Near-miss:** omit task_done for the sentinel and Queue.join waits forever. Calling it too often raises `ValueError: task_done() called too many times`. A bounded queue can also deadlock if main fills it before any consumer is started.

## 8. Say it out loud

**How it gets asked:** “How do two threads hand data to each other safely?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I choose a finite capacity, start consumers before filling it, and define an explicit end marker that cannot be confused with a real job. Every retrieved item is acknowledged in finally. I distinguish waiting for the queue’s tasks from waiting for the worker itself. With multiple consumers I account for every exit, and I decide how a failed consumer will be reported so the producer cannot block forever.

**Follow-ups**

1. **Does an empty queue mean done?** No. The producer may send another item later.

2. **Why a bounded capacity?** It limits queued work and pushes waiting back to the producer.

3. **How do two consumers stop?** For this sentinel design, enqueue one end marker for each consumer.

**Model answer:** queue.Queue safely transfers work between threads. A finite maxsize applies backpressure by blocking producers when the queue is full. Shutdown must account for every consumer.

## 9. Recall card

- Start consumers before filling a bounded queue.
- Acknowledge every retrieved item exactly once.
- Empty and finished are different states.
- Shutdown must account for every consumer.

Further reading: [Official reference](https://docs.python.org/3.12/library/queue.html).
