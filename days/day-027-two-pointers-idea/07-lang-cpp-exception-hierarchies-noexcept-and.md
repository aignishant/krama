---
day: 27
track: lang-cpp
title: "Exception hierarchies, noexcept, and std::expected chains"
theme: "Error handling, properly"
phase: "Languages: advanced features"
status: written
---

# Day 027 · C++ — Exception hierarchies, noexcept, and std::expected chains

**Today's theme:** Error handling, properly

**After today you can:** You can wrap an error with context in each language and unwrap it three layers up.

**The interviewer asks it as:** *How do you add context to an error without losing the original?*

## 1. What this is, and why it matters

C++ can preserve exception causes with nested exceptions or represent expected failures as std::expected<T, E>. noexcept promises that an exception will not escape.

You use this when discussing error handling, properly in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Asha asks her brother to collect a cake for their mother’s birthday. He asks their cousin to pick it up because she is already near the shop. Half an hour later, Asha receives a message saying only that the birthday plan has failed. She has no idea whether the shop is shut, the cake is missing, or her cousin cannot travel.

She calls back and learns that the shop could not finish the cake because its oven stopped working. That detail changes the next step. Asking the cousin to try the same shop again immediately is unlikely to help. Finding another cake might.

Asha asks everyone to keep the original reason when they pass on bad news. Her cousin can say the collection failed because the cake was not ready. Her brother can add that the birthday delivery failed because collection failed. Neither needs to erase what the shop actually said.

Two more things go wrong that afternoon. The candles are missing and the drinks are late. Asha wants to hear both problems, not whichever someone happened to mention first. She handles each with a separate response: buy candles nearby, and ask when the drinks will arrive.

By evening, they have repaired the plan. The useful messages named the job that failed and preserved the reason underneath it. A vague apology would have sounded polite but left everyone guessing what to do next.

## 3. The idea in plain English

Asha’s context can be represented by `std::throw_with_nested` and inspected using `std::rethrow_if_nested`. Catch polymorphic exceptions by const reference so derived information is not sliced away.

For ordinary validation failures, **expected** holds either a value or an error. `and_then` runs the next operation only on success; `transform_error` changes the error representation. The example composes these C++23 operations without throwing on invalid input. A noexcept function that lets an exception escape calls terminate; noexcept does not catch or convert failures.

## 4. The picture

```text
delivery failed -> collection failed -> oven unavailable
context added      context added       original cause
```

Context explains which operation failed; the original cause explains what response may help.

## 5. The code, built step by step

First isolate the important operation:

```cpp
return parse(text).and_then(validate).transform_error(
    [](const std::string& error) { return "order: " + error; });
```

and_then continues only the success path.

The complete example follows. Use a compiler and standard library with C++23 std::expected monadic operations. Save as `main.cpp`; build with `g++ -std=c++23 -Wall -Wextra main.cpp -o demo`, then run the executable.

```cpp
#include <charconv>
#include <expected>
#include <iostream>
#include <string>
#include <string_view>
#include <system_error>

std::expected<int, std::string> parse(std::string_view text) {
    int value = 0;
    auto [end, error] = std::from_chars(text.data(), text.data() + text.size(), value);
    if (error != std::errc{} || end != text.data() + text.size())
        return std::unexpected("invalid integer");
    return value;
}
std::expected<int, std::string> validate(int value) {
    if (value < 0) return std::unexpected("negative count");
    return value;
}
int main() {
    auto result = parse("-2").and_then(validate).transform_error(
        [](const std::string& error) { return "order: " + error; });
    if (result) std::cout << *result << '\n';
    else std::cout << result.error() << '\n';
}
```

**Check the result:** Prints `order: negative count`. With `"3"`, prints `3`; with `"3x"`, prints `order: invalid integer`.

## 6. How the other two languages do it

**Python**

```python
except ValueError as error:
    raise OrderError("invalid order count") from error
```

Exception chaining preserves a cause when a higher layer adds context. ExceptionGroup carries several independent failures together.

**Go**

```go
return fmt.Errorf("read order: %w", ErrMissing)
```

fmt.Errorf with %w wraps an error. errors.Is checks identity through wrappers and errors.As extracts a matching error type.

Python chains exceptions and can group them, Go wraps errors with %w for Is/As, and C++ can nest exceptions or return expected values. Preserve structured causes instead of parsing prose.

## 7. The traps

**Near-miss:** accept a successful from_chars conversion without checking end; `3x` then passes as 3. The example’s exact failure text is `order: invalid integer`. Calling value() on a failed expected throws bad_expected_access. Do not mark throwing code noexcept to silence an error: an escaping exception terminates the process.

## 8. Say it out loud

**How it gets asked:** “How do you add context to an error without losing the original?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I decide whether failure is an exceptional control transfer or an ordinary result the caller should inspect. For validation, expected makes the alternatives explicit and and_then stops the success chain on failure. For exceptions, I catch by reference and preserve causes using nested exceptions. I treat noexcept as a promise with a termination consequence, not as error recovery. I keep contextual text separate from any structured category the caller needs.

**Follow-ups**

1. **What does and_then do on failure?** It propagates the error without invoking the next success operation.

2. **Why catch by const reference?** It avoids copying and slicing a derived exception.

3. **What if an exception escapes noexcept?** The program calls std::terminate.

**Model answer:** C++ can preserve exception causes with nested exceptions or represent expected failures as std::expected<T, E>. noexcept promises that an exception will not escape. noexcept is a termination contract, not a recovery mechanism.

## 9. Recall card

- and_then continues only the success path.
- transform_error adds error context.
- Nested exceptions can preserve a causal chain.
- noexcept is a termination contract, not a recovery mechanism.

Further reading: [Official reference](https://eel.is/c++draft/expected).
