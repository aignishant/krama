---
day: 9
track: practice
title: "Practice — What an array really is in memory"
status: written
---

# Day 009 · Practice

**DSA topic:** What an array really is in memory
**System design topic:** CPU, RAM, and disk: the speed hierarchy

**Theme:** Errors, three ways

---

## Code these, in this order

Four problems that all rest on one fact: you may reach any position of an array directly, and
it costs the same wherever you reach. Each one uses that differently.

For each problem:

1. Say which positions you need to reach, and in what order.
2. State whether you are walking forwards, backwards, or jumping — and whether the order
   could be made sequential.
3. Solve it, then state the time and extra space.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Build Array from Permutation | LeetCode 1920 (Easy) | The purest possible use of `O(1)` indexing: `nums[nums[i]]` is two direct reaches, not a search. If indexing were `O(n)` this problem would not exist. |
| 2 | Concatenation of Array | LeetCode 1929 (Easy) | Position arithmetic. `ans[i]` and `ans[i + n]` are both computed, both direct, both the same cost. |
| 3 | Richest Customer Wealth | LeetCode 1672 (Easy) | A 2D list is a list of references to lists. Row-by-row is the natural order and also the cache-friendly one — notice that they agree. |
| 4 | Find Pivot Index | LeetCode 724 (Easy) | Two passes over the same array, both sequential. The naive version recomputes a sum inside the loop and is `O(n²)`; spotting that is the exercise. |

### On problem 3, do this properly

After solving it, write the column-major version — the one that loops over columns on the
outside and rows on the inside — producing the same answer. Time both on a grid of about
2,000 × 2,000.

They are both `O(rows × cols)` and they will not take the same time. Say out loud why, using
the words "cache line".

### The address drill

Answer these from memory, with the arithmetic shown, in under a minute:

- An array of 4-byte integers starts at address 2000. Where is `items[12]`?
- An array of 8-byte values starts at address 5000. Where is `items[1000]`?
- Why does the answer to either take the same time as finding `items[0]`?
- What breaks if one element in the middle is 6 bytes instead of 4?
- A Python list of 1,000,000 integers — how much memory, roughly, and where does it go?

### The measurement drill

Run the complete program from §5 of the lesson. Then change one thing: make the shuffled test
use a list of 100,000 elements instead of 4,000,000, and run it again.

The ratio between ordered and shuffled should shrink dramatically. Explain why in one
sentence. (The answer involves the size of L3 cache from the system design lesson.)

### The numbers to have cold

Say these six out loud without looking:

- RAM read, in nanoseconds.
- SSD read, in microseconds.
- Spinning-disk seek, in milliseconds.
- How many times slower SSD is than RAM.
- How many times slower a disk seek is than RAM.
- A cache line, in bytes.

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

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Why is array indexing O(1)?*
   Give the formula with real addresses. Then name the requirement that makes it work. Then
   derive why front insertion is `O(n)` from the same fact.

2. *How much slower is a disk read than a memory read?*
   Give the absolute numbers, then the ratios, then the human scale. Then say what follows
   from it about caching.

3. *Two loops read the same million elements and one is five times slower. Why?*
   One sentence on cache lines, one on the RAM-versus-cache gap, one on why Big-O is still
   right.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. Should this function throw, or return an error?
2. A failure happens three functions deep. Describe what the function in the middle has to do in each language, and what it costs to get it wrong.
3. Python has `finally`, Go has `defer`, which you meet tomorrow, and C++ has neither. Why does C++ get away with that?

## Before you move on

- [ ] I can write `address = base + i × element_size` from memory and put real numbers in it.
- [ ] I can say the three requirements that make the formula work.
- [ ] I know that a Python list stores references, and roughly what a million integers costs.
- [ ] I can order register, L1, RAM, SSD, HDD and network by speed, with numbers.
- [ ] I can explain why a 90% cache hit rate is a worse position than it sounds.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
