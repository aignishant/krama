---
day: 8
track: lang-practice
title: "Practice — Modelling a thing"
status: written
---

# Day 008 · Practice

**Theme:** Modelling a thing

---

## Build these, in all three languages

Three exercises, easiest first. Every exercise is done three times: once in Python, once in Go, once in C++. For each type you write, say out loud before you start: "what is public, and why".

| # | Exercise | What it is really testing |
|---|---|---|
| 1 | Model a `Book` with a title, an author, and a page count. It has no rules. Make two books, print each in the form `"Title by Author, 320 pages"`, and check whether two books with the same values compare equal. Use the lightest tool the language has: a dataclass, a plain struct, a plain struct. | Can you write a bundle of data with a good printed form in each language, and do you reach for the light tool when there are no rules? |
| 2 | Model a `Thermostat` that holds a target temperature which must stay between 10 and 30. It has `raise_by(n)` and `lower_by(n)`, which clamp at the limits, and a way to read the current target. Prove from outside the type that you cannot set the target to 50 directly, and record how each language stops you: at run time, at compile time, or not at all. | Can you protect an invariant in each language, and do you know which of the three actually enforces it? |
| 3 | Model a `Queue` of names for the tiffin counter, backed by the language's growable sequence from day 6, with `join(name)`, `serve()` which removes and returns the front name, and `length()`. Add a description that prints the whole queue. Then, in Go, write `serve` once with a value receiver and once with a pointer receiver and print the length after each; in C++, mark `length()` `const` and call it on a `const Queue`. | Can you compose yesterday's container inside today's type, and do you understand receivers and `const` well enough to predict the outcome? |

**Exercise 1, what you should notice.** Python `@dataclass` gives you the print and the `==` for free. Go's struct compares with `==` when all fields are comparable, and printing needs a `String()` method. C++'s struct needs `operator==`, which C++20 lets you request with `= default`, and a `describe()` function; neither is free, and that is a fact about C++ worth saying out loud.

**Exercise 2, what you should notice.** Python: `_target` plus a `@property`; setting `t.target = 50` raises `AttributeError`, but `t._target = 50` still works. Go: a lowercase `target` field; from another package `t.target = 50` is a compile error, and in the same package it is allowed. C++: `private:`; `t.target_ = 50` is a compile error from anywhere outside the class. Three different answers to "who stops me".

**Exercise 3, what you should notice.** In Go, the value-receiver `serve` returns the front name and the length is unchanged, silently. In C++, without `const` on `length()`, calling it on a `const Queue` is the `discards qualifiers` error. In Python, neither problem exists, and neither protection does.

## Compare

- **Python** — class, __init__, methods, and dataclasses. Everything is a class, `self` is explicit, privacy is a convention with a property for the read-only case, and `@dataclass` is the struct.
- **Go** — struct, methods with receivers, and constructor functions. The struct is data only, methods attach from outside with a receiver, one capital letter decides public, and the pointer receiver decides whether a change survives.
- **C++** — struct, class, constructors, and member functions. One feature with two defaults, a real constructor with an initialiser list, `private:` enforced everywhere, and `const` on every method that only reads.

## Say these out loud

Three questions from today. Answer each in two minutes, standing up, no notes.

1. What is the difference between a struct and a class?
2. How does each language stop outside code from changing a field it should not, and which of the three actually stops it?
3. What is `self` in Python, what is a receiver in Go, and what is `this` in C++, and why does Go make you choose between a value receiver and a pointer receiver?

## Before you move on

- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered all three questions above out loud.
