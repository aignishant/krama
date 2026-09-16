---
day: 5
track: lang-practice
title: "Practice — Functions"
status: written
---

# Day 005 · Practice

**Theme:** Functions

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

Three questions from today. Answer each in two minutes, standing up, no notes.

1. How does each language return more than one value?
2. Where do a function's parameters and local variables live, and what happens to them when the function returns?
3. Which language has no default arguments, and what do its designers say you should do instead?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
