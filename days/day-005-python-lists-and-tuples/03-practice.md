---
day: 5
track: practice
title: "Practice — Python for DSA I: lists, tuples, and slicing"
status: written
---

# Day 005 · Practice

**DSA topic:** Python for DSA I: lists, tuples, and slicing
**System design topic:** HTTP: the request and the response

**Theme:** Functions

---

## Code these, in this order

Four problems that all reward knowing where a list is cheap and where it is not. Each one
has an obvious solution that touches the front of a list, and a better one that does not.

For each problem:

1. Solve it however comes naturally.
2. Then go back and put a finger on every list operation you used. Say its cost out loud.
3. If any `O(n)` operation is sitting inside a loop, rewrite it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Remove Element | LeetCode 27 (Easy) | The tempting solution is `remove()` or `pop(i)` in a loop, which is `O(n²)`. The write-pointer version is `O(n)` and touches nothing but the end. |
| 2 | Move Zeroes | LeetCode 283 (Easy) | Same trap, sharper. `pop(i)` then `append(0)` is quadratic; two indices walking forward is linear. This is the shape of [day 015](../day-015-the-write-pointer/README.md). |
| 3 | Implement Queue using Stacks | LeetCode 232 (Easy) | Forces you to think about which end of a list is cheap. `pop()` is free, `pop(0)` is not, and the whole problem exists because of that asymmetry. |
| 4 | Rotate Array | LeetCode 189 (Medium) | The one-line slice solution works and allocates a full copy. The reversal trick does it in `O(1)` extra space. Write both and say what each costs in memory. |

### On problem 1, do this properly

- Write the version that calls `items.remove(val)` inside a `while` loop.
- Time it on a list of 50,000 elements where every element is the target.
- Now write the write-pointer version, and time that.
- The ratio should be in the hundreds. Say which line was the hidden `O(n)`.

### The measurement drill

Run the complete program from §5 of the lesson at `N = 50_000`, then again at `N = 100_000`.

For each row, look at what the time did when the input doubled:

- Rows that roughly **doubled** are `O(n)`.
- Rows that roughly **quadrupled** are `O(n²)`.

Name the shape of every row from the ratio alone, before checking it against the lesson.
Then answer one question out loud: **which single method name is the difference between the
two groups?**

### The one to try in a terminal

```
curl -v https://httpbin.org/get
```

Read the lines starting with `>` — that is your actual request. Read the lines starting with
`<` — that is the actual response. Find the request line, four headers, the blank line and
the status code. Then run it again with `-X POST -H "Content-Type: application/json" -d
'{"a":1}'` and see what changed.

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. In each, put the function above or below `main` on purpose and see which languages care.

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Write `greet` that takes a name and a greeting word and returns one line, `"Namaste, Farhan"`. Give the greeting word a standing default of `"Namaste"` where the language allows it. Call it twice, once with the default and once with `"Hello"`. In Go, do whatever Go makes you do instead. | Can you declare, call, and return in each language, and do you know which of the three has no default arguments? |
| 2 | Write `divide` that takes two whole numbers and returns **both** the quotient and the remainder of the first by the second. Call it with 20 and 3 and print `6 remainder 2`. Then, in each language, try to take only the quotient and record what happens. | How does each language return more than one value, and what does each do when you ignore one? |
| 3 | Write `total` that takes any number of prices and returns their sum. Call it with three prices, then with none, then with an existing row of prices. Then write a second function `total_with_tax` that calls `total` and adds twelve percent, and say out loud where each argument lives while the two functions are running. | Do you know the variadic syntax in each language, and can you explain a local scope across a nested call? |

**Exercise 1, what you should notice.** Python: a default parameter. C++: a default on the declaration. Go: no such thing; either the caller always passes both, or you write `greet` and `greetWith`. Say out loud which of the three designs you would want in a codebase of a million lines and why.

**Exercise 2, what you should notice.** Python returns a tuple and lets you write `q = divide(20, 3)`, silently giving you the whole tuple, which is a bug you find later. Go refuses to compile `q := divide(20, 3)` and makes you write `q, _ :=`. C++ returns a `std::pair` and makes you unpack it or use `.first`. Three languages, three levels of protection against ignoring a result.

**Exercise 3, what you should notice.** Python `*prices`, Go `prices ...float64` spread with `row...`, C++ has no variadic in this course's sense yet, so pass a `std::vector<double>` and say so out loud. In every language, `total_with_tax` has its own local names and `total` has its own, and neither can see the other's.

## Compare

- **Python** — def, default arguments, *args, **kwargs, and returning anything. The most flexible: defaults, keywords, variadics, and a tuple for many results, with one famous trap in the mutable default.
- **Go** — func, multiple return values, named results, variadic. The strictest: many results built in and enforced, variadics with `...`, and no defaults, keywords or overloading at all.
- **C++** — Declarations, definitions, overloading, default arguments. The most ceremony: declare before you call, overload by parameter types, defaults once on the declaration, and a pair to carry two results home.

## Say these out loud

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *What is the complexity of inserting at the front of a Python list?*
   Give the answer, then the reason from the memory layout, then why `append` is different,
   then what "amortised" means, then what you would use instead if you needed a queue.

2. *Describe an HTTP request. What is in the headers, and what is in the body?*
   Name the four parts in order. Get to safe and idempotent without being asked.

3. *A payment POST times out and the client does not know whether it succeeded. What do you
   do?*
   One sentence on why `POST` is the hard case, one on idempotency keys, one on what the
   server stores.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. How does each language return more than one value?
2. Where do a function's parameters and local variables live, and what happens to them when the function returns?
3. Which language has no default arguments, and what do its designers say you should do instead?

## Before you move on

- [ ] I can give the cost of `append`, `pop()`, `insert(0, x)`, `pop(0)`, `items[i]` and
      `items[a:b]` from memory.
- [ ] I can say what "amortised O(1)" means in one sentence, with the reason.
- [ ] I know why `[[0] * 3] * 3` is a bug and what to write instead.
- [ ] I can write out a full HTTP request by hand — request line, four headers, blank line,
      body — and label every part.
- [ ] I can say the difference between 401 and 403, and between PUT and PATCH.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
