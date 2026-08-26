---
day: 8
track: practice
title: "Practice — Reading a problem like the interviewer wrote it"
status: written
---

# Day 008 · Practice

**DSA topic:** Reading a problem like the interviewer wrote it
**System design topic:** Processes, threads, and concurrency

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

## Say these out loud

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

---

## Before you move on

- [ ] I restate every problem in my own words before touching the keyboard.
- [ ] I have the four columns memorised: input, output, constraints, edge cases.
- [ ] I can list the eight standard edge-case categories from memory.
- [ ] I read the constraint and name the target complexity out loud before choosing an
      approach.
- [ ] I can explain a race condition with the bank-balance example, unprompted, in three
      sentences.
