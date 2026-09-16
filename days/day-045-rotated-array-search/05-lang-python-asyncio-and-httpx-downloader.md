---
day: 45
track: lang-python
title: "asyncio and httpx downloader with a progress report"
theme: "Mini project 3: a concurrent downloader"
phase: "Languages: advanced features"
status: written
---

# Day 045 · Python — asyncio and httpx downloader with a progress report

**Today's theme:** Mini project 3: a concurrent downloader

**After today you can:** You can fetch 200 URLs with a bounded pool, timeouts, and retries, in all three.

**The interviewer asks it as:** *How would you download a thousand files as fast as possible without overloading the server?*

---

## 1. What this is, and why it matters

An `httpx.AsyncClient` reuses connections while `asyncio` workers wait for
network I/O without dedicating an OS thread to each request. Four worker tasks
consume the jobs. Their number, rather than the number of URLs, sets the active
download limit.

## 2. The story

Mina is helping four friends carry shopping upstairs after a family outing.
There are twenty bags in the car. At first everyone reaches into the boot at
once, and two people grab the same handle. Mina asks them to take one bag each,
close the boot while they walk away, and return for another only when their
hands are free.

Now four bags are moving at a time. The remaining bags wait safely in the car.
Mina keeps a count on her phone as each friend comes back. After five trips each,
the car should be empty. But one bag has a torn handle. Her brother sets it down,
finds another bag to put around it, and tries again. Nobody sends all four
friends to rescue that one bag; the others continue with the remaining shopping.

It starts to rain. Mina tells everyone that if the stairs become slippery they
will stop and leave the rest in the locked car until the rain passes. Finishing
everything is less important than knowing where every bag is and making sure
no one is still struggling alone on the stairs.

At the end she checks the car and the kitchen. Nineteen bags are upstairs, and
the last one is with her brother, who is replacing its torn handle. She does
not announce that all twenty are home just because all twenty have been picked
up once. Her count means delivered, and the last trip must finish before the
job is done.

## 3. The idea in plain English

Bounded concurrency means only a fixed number of downloads run at once.
Four workers repeatedly take the next URL. A timeout limits an attempt; a retry
budget limits how often a failure is tried again. Backoff inserts a delay between
attempts so a struggling destination is not hammered immediately.

Each URL owns one numbered output file. Write to a temporary `.part` file and
publish the final filename only after the response succeeds. A progress count
means completed jobs, including reported failures; it does not mean every job
succeeded. The final summary distinguishes those outcomes.

The programs use GET, retry transport failures and 5xx responses at most three
times, and bound each file to 1 MiB. They do not retry arbitrary mutations.
The fixture below serves local content so you can test without relying on a
public website. Run in a fresh output directory for each language.

## 4. The picture

```text
200 URLs -> next-job assignment -> 4 workers -> .part files
                                      |             |
                               bounded retry     success only
                                      |             v
                                failed result    final .bin
all completed results -----------------------> summary
```

Notice where the decision happens and what information it needs.

## 5. The code, built step by step

```python
async with client.stream("GET", url) as response:
    response.raise_for_status()
```

The context closes the response on success or failure. Check status before writing a body to its destination.

```python
async with asyncio.TaskGroup() as group:
    for _ in range(4):
        group.create_task(worker())
```

TaskGroup waits for all workers and propagates cancellation. Network calls yield; the small local file writes below are synchronous.

Start the fixture from [the shared practice](03-practice.md). Install with `python -m pip install httpx`. Save as `main.py`; run `python main.py` in a fresh working directory.

Expected application output (framework access logs are omitted):

    completed 50/200
    completed 100/200
    completed 150/200
    completed 200/200
    success 200 failed 0

Complete program:

```python
import asyncio
from pathlib import Path
import httpx

async def fetch(client: httpx.AsyncClient, url: str, dest: Path) -> bool:
    part = dest.with_suffix(".part")
    try:
        for attempt in range(3):
            try:
                async with asyncio.timeout(2):
                    async with client.stream("GET", url) as response:
                        if 400 <= response.status_code < 500:
                            return False
                        response.raise_for_status()
                        total = 0
                        with part.open("wb") as output:
                            async for chunk in response.aiter_bytes():
                                total += len(chunk)
                                if total > 1024 * 1024:
                                    return False
                                output.write(chunk)
                part.replace(dest)
                return True
            except (httpx.HTTPError, TimeoutError):
                if attempt < 2:
                    await asyncio.sleep(0.1 * 2**attempt)
            except OSError:
                return False
        return False
    finally:
        part.unlink(missing_ok=True)

async def main() -> None:
    out = Path("downloads-python")
    out.mkdir(exist_ok=True)
    jobs = iter(enumerate(["http://127.0.0.1:8090/ok"] * 200))
    results: list[bool] = []
    async with httpx.AsyncClient(timeout=2, follow_redirects=False) as client:
        async def worker() -> None:
            for number, url in jobs:
                ok = await fetch(client, url, out / f"{number:03}.bin")
                results.append(ok)
                if len(results) % 50 == 0:
                    print(f"completed {len(results)}/200")
        async with asyncio.TaskGroup() as group:
            for _ in range(4):
                group.create_task(worker())
    print("success", sum(results), "failed", len(results) - sum(results))

if __name__ == "__main__":
    asyncio.run(main())
```

## 6. How the other two languages do it

**Go**

```go
attemptCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
req, err := http.NewRequestWithContext(attemptCtx, http.MethodGet, url, nil)
```

Cancel each attempt's context when the attempt finishes. Handle request construction errors before using req.

**Cpp**

```cpp
curl_easy_setopt(handle, CURLOPT_TIMEOUT_MS, 2000L);
curl_easy_setopt(handle, CURLOPT_NOSIGNAL, 1L);
```

A total transfer timeout bounds each attempt. NOSIGNAL is the documented setting for threaded applications; resolver capabilities affect timeout details.

**The difference that matters:** Bound active work independently of the URL count.

## 7. The traps

**Near-miss:** `gather(*(fetch(...) for url in urls))` schedules one task
per URL without a worker bound. A semaphore bounds active calls but still
creates all those tasks; four consumers make the ownership easier to see.

**Real failure:** replace `/ok` with `/missing`; the application ends with
`success 0 failed 200` and no final files in a fresh output directory. No
exception is silently converted to success.

Do not swallow `CancelledError`; cleanup belongs in `finally`, as above.
`asyncio.timeout` covers the attempt, while HTTPX's timeout also limits network
wait phases. Synchronous disk writes can delay the event loop on a slow disk;
a production large-file downloader needs bounded offloading or an appropriate
asynchronous file strategy. This example deliberately caps each response.

Reference: [HTTPX async support](https://www.python-httpx.org/async/) and [asyncio task groups](https://docs.python.org/3/library/asyncio-task.html).

## 8. Say it out loud

**How it gets asked**

- How would you download a thousand files as fast as possible without overloading the server?
- Why do partial files need different names from successful downloads?
- What stops a retry loop or cancellation from leaving workers running forever?

**What to say out loud**

I separate how many jobs exist from how many requests may be active. I use
a fixed worker count and reuse HTTP clients where the library supports it.
Every attempt has a timeout, and every job has a finite retry budget. A retry
starts a fresh temporary file so partial bytes cannot be mistaken for a complete
download. I classify failures: a 404 is usually final; selected 5xx responses
may justify backoff. I bound body sizes and keep final output names unique.
When cancellation is requested I stop admitting new work and ensure current
operations finish or hit a deadline. I report successes and failures separately
and tune concurrency using measured throughput and the destination's limits.

**The follow-ups**

- **Why not 200 workers?** The limit protects connections, memory, disk, and the remote service; more waiting tasks do not guarantee more throughput.

- **What can be retried?** These GETs are safe to repeat; other operations require an idempotency contract.

- **What happens to a partial file?** It keeps a temporary name and is removed on failure; only a successful attempt becomes the final file.

**A model answer**

I would begin with four workers, per-attempt deadlines, three total attempts,
and a summary that identifies each failed URL. I would measure before raising
the limit. For a service I would also enforce a total operation deadline, honour
Retry-After where applicable, and consider a separate per-host limit. I would
test a timeout, a 404, a transient 500, and cancellation against a local fixture.
A run is complete only after the workers stop and every admitted job has an
accounted-for result.

## 9. Recall card

- Bound active work independently of the URL count.
- Timeout each attempt and cap total attempts.
- Retry safe operations with backoff, not every failure.
- Publish a final filename only after success.
- Join workers and report failures as well as successes.
