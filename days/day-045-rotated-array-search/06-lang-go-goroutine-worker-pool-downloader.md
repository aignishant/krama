---
day: 45
track: lang-go
title: "Goroutine worker-pool downloader with context"
theme: "Mini project 3: a concurrent downloader"
phase: "Languages: advanced features"
status: written
---

# Day 045 · Go — Goroutine worker-pool downloader with context

**Today's theme:** Mini project 3: a concurrent downloader

**After today you can:** You can fetch 200 URLs with a bounded pool, timeouts, and retries, in all three.

**The interviewer asks it as:** *How would you download a thousand files as fast as possible without overloading the server?*

---

## 1. What this is, and why it matters

A Go worker pool sends job numbers through a channel to four goroutines.
A shared `http.Client` reuses its transport safely. Request contexts carry
cancellation and deadlines through the HTTP operation; result collection waits
until every worker has stopped.

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

```go
attemptCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
req, err := http.NewRequestWithContext(attemptCtx, http.MethodGet, url, nil)
```

Cancel each attempt's context when the attempt finishes. Handle request construction errors before using req.

```go
for i := 0; i < 4; i++ {
	wg.Add(1)
	go func() {
		defer wg.Done()
		for number := range jobs { results <- download(number) }
	}()
}
```

Workers own one job at a time. Close results only after Wait returns, never while a worker can still send.

Start the fixture in [the shared practice](03-practice.md). Save as `main.go`; run `gofmt -w main.go`, then `go run main.go` in a fresh directory.

Expected application output (framework access logs are omitted):

    completed 50/200
    completed 100/200
    completed 150/200
    completed 200/200
    success 200 failed 0

Complete program:

```go
package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"
)

func attempt(ctx context.Context, client *http.Client, url, part string) (bool, bool) {
	ctx, cancel := context.WithTimeout(ctx, 2*time.Second)
	defer cancel()
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil { return false, false }
	resp, err := client.Do(req)
	if err != nil { return false, true }
	defer resp.Body.Close()
	if resp.StatusCode >= 500 { return false, true }
	if resp.StatusCode != 200 { return false, false }
	file, err := os.Create(part)
	if err != nil { return false, false }
	n, copyErr := io.Copy(file, io.LimitReader(resp.Body, 1024*1024+1))
	closeErr := file.Close()
	if n > 1024*1024 || closeErr != nil { return false, false }
	return copyErr == nil, copyErr != nil
}

func fetch(ctx context.Context, client *http.Client, url, dest string) bool {
	part := dest + ".part"
	defer func() {
		if err := os.Remove(part); err != nil && !os.IsNotExist(err) { fmt.Fprintln(os.Stderr, err) }
	}()
	for tries := 0; tries < 3; tries++ {
		if ctx.Err() != nil { return false }
		ok, retry := attempt(ctx, client, url, part)
		if ok {
			if err := os.Rename(part, dest); err != nil { return false }
			return true
		}
		if !retry || tries == 2 { return false }
		select {
		case <-ctx.Done(): return false
		case <-time.After(time.Duration(100*(1<<tries)) * time.Millisecond):
		}
	}
	return false
}

func main() {
	if err := os.MkdirAll("downloads-go", 0755); err != nil { fmt.Println(err); return }
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	client := &http.Client{Timeout: 2*time.Second, CheckRedirect: func(*http.Request, []*http.Request) error { return http.ErrUseLastResponse }}
	defer client.CloseIdleConnections()
	jobs := make(chan int)
	results := make(chan bool)
	var wg sync.WaitGroup
	for i := 0; i < 4; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			for number := range jobs {
				dest := filepath.Join("downloads-go", fmt.Sprintf("%03d.bin", number))
				results <- fetch(ctx, client, "http://127.0.0.1:8090/ok", dest)
			}
		}()
	}
	go func() { defer close(jobs); for i := 0; i < 200; i++ { jobs <- i } }()
	go func() { wg.Wait(); close(results) }()
	done, success := 0, 0
	for ok := range results {
		done++
		if ok { success++ }
		if done%50 == 0 { fmt.Printf("completed %d/200\n", done) }
	}
	fmt.Println("success", success, "failed", done-success)
}
```

## 6. How the other two languages do it

**Python**

```python
async with client.stream("GET", url) as response:
    response.raise_for_status()
```

The context closes the response on success or failure. Check status before writing a body to its destination.

**Cpp**

```cpp
curl_easy_setopt(handle, CURLOPT_TIMEOUT_MS, 2000L);
curl_easy_setopt(handle, CURLOPT_NOSIGNAL, 1L);
```

A total transfer timeout bounds each attempt. NOSIGNAL is the documented setting for threaded applications; resolver capabilities affect timeout details.

**The difference that matters:** Bound active work independently of the URL count.

## 7. The traps

**Near-miss:** deferring every response close inside a long worker loop
keeps bodies open until the worker returns. The attempt helper gives each
response and context a short scope. Reading through EOF on success enables
connection reuse; closing a rejected unread body may sacrifice reuse, not
correctness.

**Real failure:** changing the fixture URL to `/missing` yields
`success 0 failed 200`. These HTTP responses are failures even though `Do`
returned no transport error.

The total context is 30 seconds; after expiry, pending jobs are accounted for
as failures without new HTTP calls. The current producer still assigns those
numbers so the summary covers all 200. For a very large input, stop the producer
on cancellation and report unstarted jobs separately. A context does not cancel
arbitrary disk I/O; keep filesystem assumptions explicit.

Reference: [Go HTTP client](https://pkg.go.dev/net/http) and [Go context](https://pkg.go.dev/context).

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
