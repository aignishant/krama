---
day: 8
track: practice
title: "Practice — Reading a problem like the interviewer wrote it"
status: written
---

# Day 008 · Practice

**DSA topic:** Reading a problem like the interviewer wrote it
**System design topic:** Processes, threads, and concurrency

**Theme:** Modelling a thing

---

## Code these, in this order

Four problems chosen because each one is easy to solve and easy to solve *wrongly*, and the
difference is entirely in how carefully you read.

Today the process is the exercise. For every problem, **before writing any code**:

1. Restate the problem in your own words, out loud.
2. Work the given example by hand and say the answer.
3. Write down the four columns: input, output, constraints, edge cases.
4. Write the edge-case list — at least six entries — and only then solve it.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Search Insert Position | LeetCode 35 (Easy) | The output is not what people assume. "Where it *would* go" is a different question from "where it is", and the target being absent is the main case, not the edge case. |
| 2 | Best Time to Buy and Sell Stock | LeetCode 121 (Easy) | The two questions that decide correctness are unstated: must the sell come after the buy, and what do you return when every trade loses money? |
| 3 | Valid Palindrome | LeetCode 125 (Easy) | Almost pure specification. What counts as a character, is case significant, is an empty string valid? Nearly every failed submission here is a reading failure, not a coding one. |
| 4 | Find First and Last Position of Element in Sorted Array | LeetCode 34 (Medium) | Duplicates are the whole problem, the array being sorted is load-bearing, and "not present" must return `[-1, -1]` rather than anything you would naturally invent. |

### On problem 2, do this properly

Before writing anything, answer these four out loud:

- Must I sell on a later day than I buy, or is any pair allowed?
- Can the list be empty? Can it have one element?
- If every price falls, do I return 0 or a negative number?
- Is one transaction the limit, or many?

Then solve it. Then check your answers against the actual constraints on LeetCode. Any
question you got wrong is one you would have got wrong in an interview.

### The specification drill

Here are four deliberately under-specified problems. For each, write **five** clarifying
questions. Do not solve them.

1. *"Find the second largest number in a list."*
2. *"Merge two sorted lists."*
3. *"Return the most frequent word in a piece of text."*
4. *"Given a list of meetings, find out whether a person can attend all of them."*

Then check your questions against these traps: duplicates in (1) — is `[5, 5, 3]`'s second
largest `5` or `3`? Whether (2) may modify the inputs. Ties and case in (3). Whether meetings
that touch at an endpoint overlap in (4). If you found the trap before reading it here, the
habit is forming.

### The edge-case categories, from memory

Say these eight out loud without looking. They apply to almost every array problem:

empty · one element · two elements · all identical · all negatives · answer at the first
position · answer at the last position · answer absent entirely

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

### DSA and system design
Three questions. Answer each one in two minutes, standing up, without looking at the
lesson.

1. *Before you write code, what questions do you have about the problem?*
   Use problem 4 above. Restate, work the example, ask four questions, read the constraint,
   state the approach. No code.

2. *What is the difference between a process and a thread?*
   Lead with memory. Quantify the costs. Get to race conditions and locks without being
   asked.

3. *Two threads both check that an account has enough money and both withdraw. What
   happened, and how do you fix it?*
   Name the shape of the bug, say why neither thread did anything wrong, give the fix, and
   state what the fix costs you.



### Languages
Three questions from today. Answer each in two minutes, standing up, no notes.

1. What is the difference between a struct and a class?
2. How does each language stop outside code from changing a field it should not, and which of the three actually stops it?
3. What is `self` in Python, what is a receiver in Go, and what is `this` in C++, and why does Go make you choose between a value receiver and a pointer receiver?

## Before you move on

- [ ] I restate every problem in my own words before touching the keyboard.
- [ ] I have the four columns memorised: input, output, constraints, edge cases.
- [ ] I can list the eight standard edge-case categories from memory.
- [ ] I read the constraint and name the target complexity out loud before choosing an
      approach.
- [ ] I can explain a race condition with the bank-balance example, unprompted, in three
      sentences.
- [ ] All three programs run and I can explain every line.
- [ ] I can say the one-line difference between the three languages on today's theme.
- [ ] I answered the DSA, system design, and language questions out loud.
