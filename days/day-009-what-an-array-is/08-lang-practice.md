---
day: 9
track: lang-practice
title: "Practice — Errors, three ways"
status: written
---

# Day 009 · Practice

**Theme:** Errors, three ways

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. Before each one, say out loud which route this language takes: phone or slip.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Write `safe_divide(a, b)` that fails when `b` is zero. Call it with `(10, 2)` and `(10, 0)` and print either the result or a message that includes both numbers. Python raises; Go returns an error; C++ do it twice, once throwing and once with `std::expected`. | Can you make a function fail and make the caller handle it, in each language's native style? |
| 2 | Write `parse_age(text)` that turns text into a number and fails with a clear message for `"abc"`, `"-5"`, and `"200"`. Build it on top of the language's text-to-number function and its failure. Call it in a loop over `["30", "abc", "-5", "200"]` and print one line per input. Then remove the handling and run it once with `"abc"`, and read exactly what an unhandled failure looks like in each language. | Can you translate a library's failure into your own, and do you know what each language prints when nobody catches? |
| 3 | Three layers: `read_config()` fails, `start_service()` calls it, `main` calls `start_service()`. In Python, put no handling in `start_service` and catch in `main`. In Go, wrap at each layer with `%w` and print the full message, then use `errors.Is` to check for the original. In C++, do the throwing version with no handling in the middle, and then write a one-line comment above `start_service` saying what happens to its local variables when the exception passes through. | Do you understand how a failure crosses a function that does not mention it, in each language, and what happens to that function's state? |

**Exercise 1, what you should notice.** Python: `raise ZeroDivisionError` or your own `ValueError`. Go: `return 0, fmt.Errorf("divide %d by %d: division by zero", a, b)`. C++: `throw std::invalid_argument(...)` in one version and `return std::unexpected(...)` in the other; the second needs `-std=c++23`.

**Exercise 2, what you should notice.** The library failures are `ValueError`, the `error` from `strconv.Atoi`, and `std::invalid_argument` from `std::stoi`. Unhandled: Python prints a traceback with every frame; Go, if you `panic(err)`, prints the message and a goroutine trace; C++ prints `terminate called after throwing an instance of ...` and the `what()` and nothing else. Say out loud which one you would rather see at three in the morning.

**Exercise 3, what you should notice.** In Python and C++, `start_service` has zero lines about failure and still behaves correctly. In Go, `start_service` has three lines it cannot leave out, and the final message reads `start service: read config: file missing`. For the C++ comment, the answer is that every local object in `start_service` is destroyed properly as the exception passes, which is RAII and day 13.

## Compare

- **Python** — Exceptions: try, except, raise, finally. Phone route only; failures climb through silent functions, `finally` does the cleanup, and the traceback tells the whole story.
- **Go** — Error values: if err != nil, errors.New, fmt.Errorf. Slip route only; every function passes the error up by hand, wraps it with `%w`, and the signature tells you it can fail.
- **C++** — Exceptions and std::expected: throw, catch, and returning failure. Both routes, one per module; destructors do the cleanup, and `std::expected` is the slip in a single box.

## Say these out loud

Three questions from today. Answer each in two minutes, standing up, no notes.

1. Should this function throw, or return an error?
2. A failure happens three functions deep. Describe what the function in the middle has to do in each language, and what it costs to get it wrong.
3. Python has `finally`, Go has `defer`, which you meet tomorrow, and C++ has neither. Why does C++ get away with that?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
