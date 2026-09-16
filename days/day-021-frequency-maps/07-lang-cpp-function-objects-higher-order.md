---
day: 21
track: lang-cpp
title: "Function objects, higher-order functions, and wrapper classes"
theme: "Wrapping behaviour"
phase: "Languages: advanced features"
status: written
---

# Day 021 · C++ — Function objects, higher-order functions, and wrapper classes

**Today's theme:** Wrapping behaviour

**After today you can:** You can add logging around any function in each language without touching the function.

**The interviewer asks it as:** *How would you add timing to every function in a module?*

## 1. What this is, and why it matters

A function object is an object with operator(). A wrapper can own another callable and add behaviour around each invocation.

You use this when discussing wrapping behaviour in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Meera makes tea for everyone after dinner. Her brother wants to know how long each round takes, but she does not want to change how she makes the tea. He offers to stand beside the kitchen door. When she begins a round, he looks at the clock. When she comes out with the cups, he looks again and tells her the difference.

The first round is for three people. The next is for five. He does not decide how much milk to use or whether anyone wants sugar. Those choices still belong to Meera. He only watches the beginning and the end. Everyone receives the same tea they would have received without him.

Halfway through the third round, the milk runs out. Meera comes back without any cups. Her brother still notes how long the attempt lasted. He does not announce that tea was served when it was not. The failed attempt remains a failed attempt, with one extra fact about how long it took.

Their aunt now asks him to announce each round as well. He can make that announcement before looking at the clock, or afterwards. Meera points out that the choice changes what the measured time includes. They agree on an order before the next round begins. The extra work surrounds the tea-making; it does not replace it.

## 3. The idea in plain English

The helper at the door becomes a `Timed` object. A **higher-order function** takes or returns a callable. A wrapper class can serve the same purpose while keeping the captured operation in a named field.

This example deliberately fixes the signature to two integers returning an integer. `std::function<int(int, int)>` stores any compatible callable behind one runtime interface. It may allocate and adds indirect-call overhead; a templated wrapper can avoid that abstraction cost when the callable type is known.

A local guard owns the timer. Its destructor runs on ordinary return and when an exception leaves the function. That is RAII applied to reporting. The guard must not throw while unwinding another exception. A fully generic wrapper also needs forwarding and careful return-type handling; the fixed signature keeps those concerns out of this first example.

## 4. The picture

```text
caller -> outer wrapper -> original operation -> result
             start clock       work             stop clock
             <--------- also finish on failure --------->
```

The wrapper owns the added behaviour. Arguments, results, and failures still belong to the original operation.

## 5. The code, built step by step

First isolate the important operation:

```cpp
int operator()(int left, int right) const {
    Timer timer;
    return operation(left, right);
}
```

A scope guard reports on normal and exceptional exits.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <chrono>
#include <cstdio>
#include <functional>
#include <iostream>
#include <utility>

struct Timer {
    std::chrono::steady_clock::time_point start = std::chrono::steady_clock::now();
    ~Timer() noexcept {
        auto elapsed = std::chrono::steady_clock::now() - start;
        std::fprintf(stderr, "elapsed %.6f seconds\n",
                     std::chrono::duration<double>(elapsed).count());
    }
};

class Timed {
    std::function<int(int, int)> operation;
public:
    explicit Timed(std::function<int(int, int)> fn) : operation(std::move(fn)) {}
    int operator()(int left, int right) const {
        Timer timer;
        return operation(left, right);
    }
};

int main() {
    Timed add([](int left, int right) { return left + right; });
    std::cout << add(2, 3) << '\n';
}
```

**Check the result:** Standard output is `5`. Standard error reports a variable elapsed duration.

## 6. How the other two languages do it

**Python**

```python
try:
    return function(*args, **kwargs)
finally:
    print(label, perf_counter() - start)
```

A decorator takes a callable and returns a callable with added behaviour. functools.wraps preserves useful identifying metadata.

**Go**

```go
return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    start := time.Now()
    defer func() { log.Println("elapsed", time.Since(start)) }()
    next.ServeHTTP(w, r)
})
```

Middleware is a function that accepts a handler and returns a handler. The returned handler can act before and after the next handler.

Python has decorator syntax, Go wraps a handler explicitly, and C++ can store a callable inside another object. In every version, wrapper order and failure handling are part of the contract.

## 7. The traps

**Near-miss:** capture a local operation by reference and return a wrapper that outlives it. The reference dangles; no diagnostic is guaranteed. Own the callable when its lifetime must extend. Calling an empty std::function throws `std::bad_function_call`; its `what()` wording is implementation-dependent. The timer destructor must not throw during exception unwinding.

## 8. Say it out loud

**How it gets asked:** “How would you add timing to every function in a module?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I give the wrapper an operator() with the required signature and store the wrapped callable by value. A local guard records elapsed time when its scope ends, including exception unwinding. I use steady_clock for an elapsed interval. For this fixed interface std::function is convenient; for performance-sensitive generic code I would template the wrapper and preserve forwarding and return categories. The wrapper must not outlive anything it borrows.

**Follow-ups**

1. **Why not measure after return?** That code is unreachable. A scope guard runs as the function exits.

2. **Does std::function always allocate?** No. Allocation depends on the target and implementation; do not promise that every callable is stored without allocation.

3. **Why use steady_clock?** It is monotonic and suitable for elapsed intervals.

**Model answer:** A function object is an object with operator(). A wrapper can own another callable and add behaviour around each invocation. Added behaviour must preserve results and exceptions.

## 9. Recall card

- A scope guard reports on normal and exceptional exits.
- operator() makes an object callable.
- Own the callable or prove borrowed lifetimes.
- Added behaviour must preserve results and exceptions.

Further reading: [Official reference](https://eel.is/c++draft/func.wrap.func).
