---
day: 45
track: lang-cpp
title: "Thread-pool downloader with libcurl"
theme: "Mini project 3: a concurrent downloader"
phase: "Languages: advanced features"
status: written
---

# Day 045 · C++ — Thread-pool downloader with libcurl

**Today's theme:** Mini project 3: a concurrent downloader

**After today you can:** You can fetch 200 URLs with a bounded pool, timeouts, and retries, in all three.

**The interviewer asks it as:** *How would you download a thousand files as fast as possible without overloading the server?*

---

## 1. What this is, and why it matters

A fixed group of C++ threads can download concurrently with libcurl.
Each worker owns its own easy handle; sharing one handle concurrently is not
allowed. Initialise libcurl before starting workers and clean it up only after
they have all joined.

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

```cpp
curl_easy_setopt(handle, CURLOPT_TIMEOUT_MS, 2000L);
curl_easy_setopt(handle, CURLOPT_NOSIGNAL, 1L);
```

A total transfer timeout bounds each attempt. NOSIGNAL is the documented setting for threaded applications; resolver capabilities affect timeout details.

```cpp
std::atomic<int> next{0};
int number = next.fetch_add(1);
```

An atomic counter assigns each number once. The program's mutex separately serialises progress output and completed-result counters.

Start the fixture in [the shared practice](03-practice.md). Save as `main.cpp`.
On Linux with a C++20 compiler and libcurl development headers installed, run
`g++ -Wall -Wextra -std=c++20 -pthread main.cpp -lcurl -o downloader`, then
`./downloader`. A Windows build needs a matching libcurl development package
and its documented include/library paths; the Unix command is not a Windows
dependency installer.

Expected application output (framework access logs are omitted):

    completed 50/200
    completed 100/200
    completed 150/200
    completed 200/200
    success 200 failed 0

Complete program:

```cpp
#include <curl/curl.h>
#include <atomic>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

struct Sink { std::ofstream file; std::size_t bytes = 0; };

std::size_t write_body(char* data, std::size_t size, std::size_t count, void* user) {
    auto& sink = *static_cast<Sink*>(user);
    const auto n = size * count;
    if (n > 1024 * 1024 - sink.bytes) return 0;
    sink.file.write(data, static_cast<std::streamsize>(n));
    if (!sink.file) return 0;
    sink.bytes += n;
    return n;
}

bool fetch(const std::string& url, const std::filesystem::path& dest) {
    const auto part = std::filesystem::path(dest.string() + ".part");
    for (int attempt = 0; attempt < 3; ++attempt) {
        std::unique_ptr<CURL, decltype(&curl_easy_cleanup)> handle(curl_easy_init(), curl_easy_cleanup);
        if (!handle) return false;
        Sink sink{std::ofstream(part, std::ios::binary), 0};
        if (!sink.file) return false;
        CURL* h = handle.get();
        const bool configured =
            curl_easy_setopt(h, CURLOPT_URL, url.c_str()) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_TIMEOUT_MS, 2000L) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_NOSIGNAL, 1L) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_WRITEFUNCTION, write_body) == CURLE_OK &&
            curl_easy_setopt(h, CURLOPT_WRITEDATA, &sink) == CURLE_OK;
        const CURLcode result = configured ? curl_easy_perform(h) : CURLE_FAILED_INIT;
        long status = 0;
        const auto info = curl_easy_getinfo(h, CURLINFO_RESPONSE_CODE, &status);
        sink.file.close();
        std::error_code ec;
        if (result == CURLE_OK && info == CURLE_OK && status == 200 && sink.file) {
            std::filesystem::rename(part, dest, ec);
            if (!ec) return true;
        }
        std::filesystem::remove(part, ec);
        if (ec) return false;
        if (!configured || result == CURLE_WRITE_ERROR || (result == CURLE_OK && status < 500)) return false;
        if (attempt < 2) std::this_thread::sleep_for(std::chrono::milliseconds(100 * (1 << attempt)));
    }
    return false;
}

int main() {
    std::error_code ec;
    std::filesystem::create_directories("downloads-cpp", ec);
    if (ec) { std::cerr << ec.message() << '\n'; return 1; }
    if (curl_global_init(CURL_GLOBAL_DEFAULT) != CURLE_OK) return 1;
    std::atomic<int> next{0};
    std::mutex mutex;
    int done = 0, success = 0;
    {
        std::vector<std::jthread> workers;
        for (int i = 0; i < 4; ++i) workers.emplace_back([&] {
            for (;;) {
                const int number = next.fetch_add(1);
                if (number >= 200) break;
                const auto digits = std::to_string(1000 + number).substr(1);
                const bool ok = fetch("http://127.0.0.1:8090/ok", "downloads-cpp/" + digits + ".bin");
                std::lock_guard lock(mutex);
                ++done;
                success += ok;
                if (done % 50 == 0) std::cout << "completed " << done << "/200\n";
            }
        });
    }
    curl_global_cleanup();
    std::cout << "success " << success << " failed " << done - success << '\n';
}
```

## 6. How the other two languages do it

**Python**

```python
async with client.stream("GET", url) as response:
    response.raise_for_status()
```

The context closes the response on success or failure. Check status before writing a body to its destination.

**Go**

```go
attemptCtx, cancel := context.WithTimeout(ctx, 2*time.Second)
req, err := http.NewRequestWithContext(attemptCtx, http.MethodGet, url, nil)
```

Cancel each attempt's context when the attempt finishes. Handle request construction errors before using req.

**The difference that matters:** Bound active work independently of the URL count.

## 7. The traps

**Near-miss:** using one easy handle from all four workers is not made
safe by libcurl being usable in threaded programs. Each attempt here owns its
handle. Reusing a handle sequentially within a worker can improve connection
reuse; this teaching version constructs one per attempt.

**Real failure:** `/missing` produces `success 0 failed 200`, even though
libcurl can successfully transfer the 404 body. HTTP status and transfer status
are distinct. A callback returning zero aborts a body that exceeds the size
limit or cannot be written.

`jthread` joins on destruction but does not magically interrupt a synchronous
libcurl call. This version has a finite per-attempt deadline and retry budget;
add an explicit stop flag/progress callback for user-driven cancellation.
Filesystem exceptions and allocation failures need a worker-level exception
boundary in a production version. Do not let unexpected exceptions escape a
thread and terminate the process without recording failed work.

Reference: [libcurl thread safety](https://curl.se/libcurl/c/threadsafe.html) and [easy interface](https://curl.se/libcurl/c/libcurl-easy.html).

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
