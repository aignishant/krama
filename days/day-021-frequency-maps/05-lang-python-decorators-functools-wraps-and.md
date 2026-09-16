---
day: 21
track: lang-python
title: "Decorators, functools.wraps, and decorators with arguments"
theme: "Wrapping behaviour"
phase: "Languages: advanced features"
status: written
---

# Day 021 · Python — Decorators, functools.wraps, and decorators with arguments

**Today's theme:** Wrapping behaviour

**After today you can:** You can add logging around any function in each language without touching the function.

**The interviewer asks it as:** *How would you add timing to every function in a module?*

## 1. What this is, and why it matters

A decorator takes a callable and returns a callable with added behaviour. functools.wraps preserves useful identifying metadata.

You use this when discussing wrapping behaviour in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Meera makes tea for everyone after dinner. Her brother wants to know how long each round takes, but she does not want to change how she makes the tea. He offers to stand beside the kitchen door. When she begins a round, he looks at the clock. When she comes out with the cups, he looks again and tells her the difference.

The first round is for three people. The next is for five. He does not decide how much milk to use or whether anyone wants sugar. Those choices still belong to Meera. He only watches the beginning and the end. Everyone receives the same tea they would have received without him.

Halfway through the third round, the milk runs out. Meera comes back without any cups. Her brother still notes how long the attempt lasted. He does not announce that tea was served when it was not. The failed attempt remains a failed attempt, with one extra fact about how long it took.

Their aunt now asks him to announce each round as well. He can make that announcement before looking at the clock, or afterwards. Meera points out that the choice changes what the measured time includes. They agree on an order before the next round begins. The extra work surrounds the tea-making; it does not replace it.

## 3. The idea in plain English

Meera is the original callable; her brother is the wrapper. A **decorator factory** first accepts configuration, then returns the decorator. Here `@labelled("sum")` means `add = labelled("sum")(add)` after `add` is defined.

The inner wrapper forwards positional and keyword arguments unchanged. It returns the original result. A `finally` block runs even when the original call raises. `perf_counter` measures elapsed intervals without depending on changes to the wall clock. `ParamSpec` preserves the parameter types for a static checker; it does not validate arguments at runtime. `wraps` exposes `__wrapped__` and copies metadata such as the name and documentation.

Decoration happens when the definition executes, not once per invocation. Each invocation still pays for two clock reads and one report. If a function takes T seconds, the wrapper adds its own fixed work plus output cost; it does not make T disappear.

## 4. The picture

```text
caller -> outer wrapper -> original operation -> result
             start clock       work             stop clock
             <--------- also finish on failure --------->
```

The wrapper owns the added behaviour. Arguments, results, and failures still belong to the original operation.

## 5. The code, built step by step

First isolate the important operation:

```python
try:
    return function(*args, **kwargs)
finally:
    print(label, perf_counter() - start)
```

Forward arguments and return the wrapped result.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from collections.abc import Callable
from functools import wraps
from time import perf_counter
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")

def labelled(label: str) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorate(function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = perf_counter()
            try:
                return function(*args, **kwargs)
            finally:
                print(label, "elapsed", perf_counter() - start)
        return wrapper
    return decorate

@labelled("sum")
def add(left: int, right: int) -> int:
    return left + right

print(add(2, right=3))
print(add.__name__)
```

**Check the result:** The first line starts with `sum elapsed` and has a variable duration. The next lines are `5` and `add`.

## 6. How the other two languages do it

**Go**

```go
return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
    start := time.Now()
    defer func() { log.Println("elapsed", time.Since(start)) }()
    next.ServeHTTP(w, r)
})
```

Middleware is a function that accepts a handler and returns a handler. The returned handler can act before and after the next handler.

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

**Near-miss:** call the function but forget `return`; `add(2, 3)` becomes `None`. **Failure case:** a wrapper that accepts only positional arguments rejects `right=3` with a `TypeError` ending in `got an unexpected keyword argument 'right'`. A return inside `finally` can suppress the original exception, so do not put one there.

## 8. Say it out loud

**How it gets asked:** “How would you add timing to every function in a module?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I add one wrapper at the boundary where calls enter. It forwards arguments, returns the result, and lets failures propagate. I measure elapsed time with a monotonic performance clock and report in finally so failed calls are measured too. A factory holds configuration, and wraps keeps the original identity visible. Stacking wrappers changes the order, so I choose whether logging itself belongs inside the measured interval.

**Follow-ups**

1. **Does decoration call the original function?** No. This decorator returns a wrapper; the original runs when that wrapper is invoked.

2. **What does wraps preserve?** Metadata and a reference through __wrapped__; it does not enforce runtime types.

3. **Will this time an async function correctly?** No. It times coroutine creation. An async wrapper must await the call inside try/finally.

**Model answer:** A decorator takes a callable and returns a callable with added behaviour. functools.wraps preserves useful identifying metadata. Wrapper order determines what the timer includes.

## 9. Recall card

- Forward arguments and return the wrapped result.
- Use finally for reporting on failure.
- Decorator factories hold configuration.
- Wrapper order determines what the timer includes.

Further reading: [Official reference](https://docs.python.org/3.12/library/functools.html#functools.wraps).
