---
day: 21
track: lang-go
title: "Middleware: functions that take and return handlers"
theme: "Wrapping behaviour"
phase: "Languages: advanced features"
status: written
---

# Day 021 · Go — Middleware: functions that take and return handlers

**Today's theme:** Wrapping behaviour

**After today you can:** You can add logging around any function in each language without touching the function.

**The interviewer asks it as:** *How would you add timing to every function in a module?*

## 1. What this is, and why it matters

Middleware is a function that accepts a handler and returns a handler. The returned handler can act before and after the next handler.

You use this when discussing wrapping behaviour in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Meera makes tea for everyone after dinner. Her brother wants to know how long each round takes, but she does not want to change how she makes the tea. He offers to stand beside the kitchen door. When she begins a round, he looks at the clock. When she comes out with the cups, he looks again and tells her the difference.

The first round is for three people. The next is for five. He does not decide how much milk to use or whether anyone wants sugar. Those choices still belong to Meera. He only watches the beginning and the end. Everyone receives the same tea they would have received without him.

Halfway through the third round, the milk runs out. Meera comes back without any cups. Her brother still notes how long the attempt lasted. He does not announce that tea was served when it was not. The failed attempt remains a failed attempt, with one extra fact about how long it took.

Their aunt now asks him to announce each round as well. He can make that announcement before looking at the clock, or afterwards. Meera points out that the choice changes what the measured time includes. They agree on an order before the next round begins. The extra work surrounds the tea-making; it does not replace it.

## 3. The idea in plain English

The kitchen door becomes the request boundary. An HTTP **handler** implements `ServeHTTP(ResponseWriter, *Request)`. `http.HandlerFunc` adapts an ordinary function with that signature to the interface.

The wrapper captures `next` but receives a fresh request on every call. Passing the same writer and request lets the original handler keep doing its job. `defer` arranges work for the end of the wrapper call, including panic unwinding. It does not recover from a panic unless you explicitly call recover in a deferred function.

The example uses an in-process recorder, so it opens no listening port. Two clock reads and one log call are added per request. Shared counters in a real wrapper need synchronisation because HTTP handlers may run concurrently; a captured variable is not automatically protected.

## 4. The picture

```text
caller -> outer wrapper -> original operation -> result
             start clock       work             stop clock
             <--------- also finish on failure --------->
```

The wrapper owns the added behaviour. Arguments, results, and failures still belong to the original operation.

## 5. The code, built step by step

First isolate the important operation:

```go
return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    start := time.Now()
    defer func() { log.Println("elapsed", time.Since(start)) }()
    next.ServeHTTP(w, r)
})
```

Call next once unless intentionally short-circuiting.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "log"
    "net/http"
    "net/http/httptest"
    "time"
)

func timed(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        start := time.Now()
        defer func() { log.Println("elapsed", time.Since(start)) }()
        next.ServeHTTP(w, r)
    })
}

func main() {
    endpoint := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprint(w, "hello")
    })
    response := httptest.NewRecorder()
    timed(endpoint).ServeHTTP(response, httptest.NewRequest("GET", "/", nil))
    fmt.Println(response.Code, response.Body.String())
}
```

**Check the result:** Standard output is `200 hello`. The log on standard error includes a timestamp and a variable elapsed duration.

## 6. How the other two languages do it

**Python**

```python
try:
    return function(*args, **kwargs)
finally:
    print(label, perf_counter() - start)
```

A decorator takes a callable and returns a callable with added behaviour. functools.wraps preserves useful identifying metadata.

**C++**

```cpp
int operator()(int left, int right) const {
    Timer timer;
    return operation(left, right);
}
```

A function object is an object with operator(). A wrapper can own another callable and add behaviour around each invocation.

Python has decorator syntax, Go wraps a handler explicitly, and C++ can store a callable inside another object. In every version, wrapper order and failure handling are part of the contract.

## 7. The traps

**Near-miss:** `defer log.Println(time.Since(start))` calculates the duration immediately because defer evaluates its arguments when registered. Use the closure shown above. **Failure case:** passing a nil handler and invoking it produces a panic beginning `runtime error: invalid memory address or nil pointer dereference`; the stack and addresses depend on the Go version.

## 8. Say it out loud

**How it gets asked:** “How would you add timing to every function in a module?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I accept an http.Handler and return another http.Handler. The wrapper starts the timer, defers a closure that reads the end time, and calls next.ServeHTTP with the same request and writer. I do not call recover merely to log timing, because swallowing a panic changes the application contract. I also avoid unsynchronised shared counters. The in-process recorder gives me a way to verify response preservation without opening a network connection.

**Follow-ups**

1. **Why a closure inside defer?** Its body computes the elapsed duration when the wrapper returns, not when defer is registered.

2. **Can middleware reject a request?** Yes. It may write a response and return without calling next, for example after an authentication failure.

3. **Does the wrapper make shared state safe?** No. Concurrent requests require locks, atomics, or ownership of state.

**Model answer:** Middleware is a function that accepts a handler and returns a handler. The returned handler can act before and after the next handler. A timing wrapper should preserve the handler’s failure behaviour.

## 9. Recall card

- Call next once unless intentionally short-circuiting.
- Defer evaluates arguments immediately.
- HandlerFunc adapts a function to Handler.
- A timing wrapper should preserve the handler’s failure behaviour.

Further reading: [Official reference](https://go.dev/blog/defer-panic-and-recover).
