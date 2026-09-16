---
day: 27
track: lang-go
title: "errors.Is, errors.As, %w wrapping, and sentinel errors"
theme: "Error handling, properly"
phase: "Languages: advanced features"
status: written
---

# Day 027 · Go — errors.Is, errors.As, %w wrapping, and sentinel errors

**Today's theme:** Error handling, properly

**After today you can:** You can wrap an error with context in each language and unwrap it three layers up.

**The interviewer asks it as:** *How do you add context to an error without losing the original?*

## 1. What this is, and why it matters

fmt.Errorf with %w wraps an error. errors.Is checks identity through wrappers and errors.As extracts a matching error type.

You use this when discussing error handling, properly in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Asha asks her brother to collect a cake for their mother’s birthday. He asks their cousin to pick it up because she is already near the shop. Half an hour later, Asha receives a message saying only that the birthday plan has failed. She has no idea whether the shop is shut, the cake is missing, or her cousin cannot travel.

She calls back and learns that the shop could not finish the cake because its oven stopped working. That detail changes the next step. Asking the cousin to try the same shop again immediately is unlikely to help. Finding another cake might.

Asha asks everyone to keep the original reason when they pass on bad news. Her cousin can say the collection failed because the cake was not ready. Her brother can add that the birthday delivery failed because collection failed. Neither needs to erase what the shop actually said.

Two more things go wrong that afternoon. The candles are missing and the drinks are late. Asha wants to hear both problems, not whichever someone happened to mention first. She handles each with a separate response: buy candles nearby, and ask when the drinks will arrive.

By evening, they have repaired the plan. The useful messages named the job that failed and preserved the reason underneath it. A vague apology would have sounded polite but left everyone guessing what to do next.

## 3. The idea in plain English

A **sentinel error** is a shared value representing a known condition. A custom error type can carry fields, such as a row number. Wrapping adds context while exposing the cause through Unwrap. Is and As traverse that structure, so callers do not need to compare message strings.

Using %v instead of %w keeps only formatted text. As needs a pointer to the variable that should receive the matched error. A typed nil inside an error interface is still non-nil, as day 23 explained.

## 4. The picture

```text
delivery failed -> collection failed -> oven unavailable
context added      context added       original cause
```

Context explains which operation failed; the original cause explains what response may help.

## 5. The code, built step by step

First isolate the important operation:

```go
return fmt.Errorf("read order: %w", ErrMissing)
```

Use %w to retain an unwrap chain.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "errors"
    "fmt"
)
var ErrMissing = errors.New("missing")
type RowError struct{ Row int }
func (e *RowError) Error() string { return fmt.Sprintf("bad row %d", e.Row) }
func main() {
    missing := fmt.Errorf("read order: %w", ErrMissing)
    fmt.Println(missing, errors.Is(missing, ErrMissing))
    wrapped := fmt.Errorf("import: %w", &RowError{Row: 3})
    var row *RowError
    if errors.As(wrapped, &row) { fmt.Println(row.Row) }
}
```

**Check the result:** Prints `read order: missing true` and `3`.

## 6. How the other two languages do it

**Python**

```python
except ValueError as error:
    raise OrderError("invalid order count") from error
```

Exception chaining preserves a cause when a higher layer adds context. ExceptionGroup carries several independent failures together.

**C++**

```cpp
return parse(text).and_then(validate).transform_error(
    [](const std::string& error) { return "order: " + error; });
```

C++ can preserve exception causes with nested exceptions or represent expected failures as std::expected<T, E>. noexcept promises that an exception will not escape.

Python chains exceptions and can group them, Go wraps errors with %w for Is/As, and C++ can nest exceptions or return expected values. Preserve structured causes instead of parsing prose.

## 7. The traps

**Near-miss:** replacing %w with %v makes errors.Is return false. Passing a non-pointer target to errors.As can panic with `errors: target must be a non-nil pointer`. Compare causes or extract fields; do not inspect whether an error message contains the word missing.

## 8. Say it out loud

**How it gets asked:** “How do you add context to an error without losing the original?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I wrap failures at boundaries with a short operation name and %w. I use Is when a caller needs to recognise a known condition and As when it needs fields from a typed error. I preserve the cause only when it belongs in the API contract, because callers may then depend on that category. I avoid wrapping nil and return plain nil on success.

**Follow-ups**

1. **Why not compare error strings?** Messages change and lose structured identity.

2. **When do you choose As?** When a matching error type carries fields the caller needs.

3. **Does %v preserve an unwrap chain?** No. It only formats the error into text.

**Model answer:** fmt.Errorf with %w wraps an error. errors.Is checks identity through wrappers and errors.As extracts a matching error type. Readable error text is not a substitute for structured causes.

## 9. Recall card

- Use %w to retain an unwrap chain.
- Use Is for a known condition.
- Use As for a matching type and its fields.
- Readable error text is not a substitute for structured causes.

Further reading: [Official reference](https://pkg.go.dev/errors).
