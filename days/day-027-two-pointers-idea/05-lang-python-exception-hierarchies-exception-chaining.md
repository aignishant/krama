---
day: 27
track: lang-python
title: "Exception hierarchies, exception chaining, and ExceptionGroup"
theme: "Error handling, properly"
phase: "Languages: advanced features"
status: written
---

# Day 027 · Python — Exception hierarchies, exception chaining, and ExceptionGroup

**Today's theme:** Error handling, properly

**After today you can:** You can wrap an error with context in each language and unwrap it three layers up.

**The interviewer asks it as:** *How do you add context to an error without losing the original?*

## 1. What this is, and why it matters

Exception chaining preserves a cause when a higher layer adds context. ExceptionGroup carries several independent failures together.

You use this when discussing error handling, properly in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Asha asks her brother to collect a cake for their mother’s birthday. He asks their cousin to pick it up because she is already near the shop. Half an hour later, Asha receives a message saying only that the birthday plan has failed. She has no idea whether the shop is shut, the cake is missing, or her cousin cannot travel.

She calls back and learns that the shop could not finish the cake because its oven stopped working. That detail changes the next step. Asking the cousin to try the same shop again immediately is unlikely to help. Finding another cake might.

Asha asks everyone to keep the original reason when they pass on bad news. Her cousin can say the collection failed because the cake was not ready. Her brother can add that the birthday delivery failed because collection failed. Neither needs to erase what the shop actually said.

Two more things go wrong that afternoon. The candles are missing and the drinks are late. Asha wants to hear both problems, not whichever someone happened to mention first. She handles each with a separate response: buy candles nearby, and ask when the drinks will arrive.

By evening, they have repaired the plan. The useful messages named the job that failed and preserved the reason underneath it. A vague apology would have sounded polite but left everyone guessing what to do next.

## 3. The idea in plain English

Asha’s delivery message becomes a domain exception, while the oven problem remains its **cause**. `raise Outer(...) from error` sets that explicit cause. Catch a specific base class for failures your layer knows how to handle; catching BaseException also catches shutdown signals such as KeyboardInterrupt.

An ExceptionGroup is useful when several operations fail. `except* ValueError` handles the matching subgroup; unmatched exceptions continue outward. It is not the same as suppressing every failure in a broad except block. Chain one causal sequence; group independent failures.

## 4. The picture

```text
delivery failed -> collection failed -> oven unavailable
context added      context added       original cause
```

Context explains which operation failed; the original cause explains what response may help.

## 5. The code, built step by step

First isolate the important operation:

```python
except ValueError as error:
    raise OrderError("invalid order count") from error
```

Use raise from to preserve the cause.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
class OrderError(Exception):
    pass

def read_count(text: str) -> int:
    try:
        return int(text)
    except ValueError as error:
        raise OrderError("invalid order count") from error

try:
    read_count("many")
except OrderError as error:
    print(error)
    print(type(error.__cause__).__name__)

try:
    raise ExceptionGroup("bad rows", [ValueError("row 1"), ValueError("row 3")])
except* ValueError as group:
    print(len(group.exceptions))
```

**Check the result:** Prints `invalid order count`, `ValueError`, and `2`.

## 6. How the other two languages do it

**Go**

```go
return fmt.Errorf("read order: %w", ErrMissing)
```

fmt.Errorf with %w wraps an error. errors.Is checks identity through wrappers and errors.As extracts a matching error type.

**C++**

```cpp
return parse(text).and_then(validate).transform_error(
    [](const std::string& error) { return "order: " + error; });
```

C++ can preserve exception causes with nested exceptions or represent expected failures as std::expected<T, E>. noexcept promises that an exception will not escape.

Python chains exceptions and can group them, Go wraps errors with %w for Is/As, and C++ can nest exceptions or return expected values. Preserve structured causes instead of parsing prose.

## 7. The traps

**Near-miss:** `raise OrderError(str(error)) from None` hides the displayed cause and encourages message parsing. The underlying conversion error is `ValueError: invalid literal for int() with base 10: 'many'`. Preserve it with from error. Use bare raise when rethrowing the same exception without adding a new layer.

## 8. Say it out loud

**How it gets asked:** “How do you add context to an error without losing the original?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I catch only failures I can interpret, add the operation’s context, and preserve the cause with raise from. Callers can catch the domain category while diagnostics still expose the conversion failure. I use ExceptionGroup for independent failures, not successive layers of the same failure. My handler either repairs the condition or lets it propagate; it does not turn failed work into a successful return.

**Follow-ups**

1. **When should you use bare raise?** When propagating the current exception unchanged.

2. **Does except Exception catch KeyboardInterrupt?** No. KeyboardInterrupt derives directly from BaseException.

3. **What happens to unmatched except* members?** They propagate after the matching subgroup is handled.

**Model answer:** Exception chaining preserves a cause when a higher layer adds context. ExceptionGroup carries several independent failures together. Error context should add information without erasing the original cause.

## 9. Recall card

- Use raise from to preserve the cause.
- Catch the category you can handle.
- Groups contain independent failures.
- Error context should add information without erasing the original cause.

Further reading: [Official reference](https://docs.python.org/3.12/tutorial/errors.html).
