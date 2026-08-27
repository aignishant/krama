---
day: 19
track: practice
title: "Practice — What a string is, and why it is immutable"
status: written
---

# Day 019 · Practice

**DSA topic:** What a string is, and why it is immutable
**System design topic:** Authentication and authorisation

---

## Code these, in this order

Four problems that all turn on the same fact: you cannot change a string, so you decide what the
whole answer is and build it once.

Before each one, say out loud:

1. Am I building a result, or only reading? If building, where does the `join` go?
2. How long is the answer, and how many times will each character be copied?
3. Does the problem want a string back, or a list, or a count?
4. What happens on the empty string?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse String | LeetCode 344 (Easy) | That the input is given as a **list of characters**, not a string — precisely because a string cannot be reversed in place. Ask yourself why the problem is phrased that way. |
| 2 | Reverse Words in a String III | LeetCode 557 (Easy) | `split`, transform, `join`. Anyone who builds the result with `+=` inside two nested loops has not learned today's lesson. |
| 3 | Longest Common Prefix | LeetCode 14 (Easy) | Building the answer once rather than growing it character by character, and the two edge cases: an empty list, and one string being a prefix of another. |
| 4 | Reverse Words in a String | LeetCode 151 (Medium) | `split()` with no argument versus `split(" ")`. The whole difficulty is multiple spaces, leading spaces and trailing spaces. |

### On problem 1, answer the question the problem is asking

The signature hands you `s: list[str]`, not `s: str`. Say out loud why, before writing anything.
Then write the two-pointer in-place reversal from
[day 013](../day-013-reverse-and-rotate/README.md) and notice it works only because it is a list.
Then write the one-line string version, `s[::-1]`, and state its cost — `O(n)` time and `O(n)`
space, because it builds a new string.

### On problem 4, break it deliberately

Run these three and predict each first:

```python
print("  the   sky is  blue  ".split())
print("  the   sky is  blue  ".split(" "))
print(len("  the   sky is  blue  ".split(" ")))
```

Then say, in one sentence, why bare `split()` solves the whole problem and `split(" ")` creates it.

### The immutability drill

Predict the output of each, then run them.

```python
s = "hello"
s.upper()
print(s)
```

```python
s = "hello world"
s.replace("world", "there")
print(s)
```

```python
a = "hello"
b = a
a += " world"
print(a, b)
```

```python
c = "hello"
d = "".join(["hel", "lo"])
print(c == d, c is d)
```

```python
s = "hello"
s[0] = "H"
```

For the last one, read the exact error text and say it back from memory. For the fourth, say why
`is` returned what it did and why you must never use it on strings.

### The quadratic drill

Type this in and run it. The numbers matter more than the code.

```python
import time

def prepend(n: int) -> float:
    s = ""
    start = time.perf_counter()
    for _ in range(n):
        s = "x" + s
    return time.perf_counter() - start

def joined(n: int) -> float:
    parts = []
    start = time.perf_counter()
    for _ in range(n):
        parts.append("x")
    _ = "".join(parts)
    return time.perf_counter() - start

for n in (20_000, 40_000, 80_000, 160_000):
    print(n, round(prepend(n), 4), round(joined(n), 4))
```

Then answer:

1. When `n` doubles, by what factor does the first column grow? What does that factor tell you?
2. By what factor does the second column grow?
3. At `n = 160,000`, how many character copies does the first version do in total?
4. Why did the lesson use `"x" + s` rather than `s += "x"` for this measurement?

Question 4 is the one worth being able to answer, because it is the honest caveat an interviewer may
raise.

### The method drill

From memory, say what each of these returns **and** whether it changes the original:

`strip()`, `split()`, `split(",")`, `join()`, `lower()`, `replace()`, `find()`, `index()`,
`startswith()`, `sorted()`, `s[::-1]`, `list(s)`

Two of them behave differently from all the others. Name them and say how. (`sorted` returns a list,
not a string. `index` raises where `find` returns `-1`.)

### The authn/authz drill

For each situation, say **authentication** or **authorisation**, and the status code on failure:

1. Typing your password into a login form.
2. A free-tier user trying to export a report that is a paid feature.
3. An expired session token on an API request.
4. A member trying to delete another member's comment.
5. An OTP arriving on your phone.
6. A doctor opening a patient record for a patient who is not theirs.
7. A request with no `Authorization` header at all.
8. A moderator hiding a comment successfully.

Then the harder one: for number 6, argue why a hospital system might return `404` rather than `403`,
and say when you would and would not do that.

### The password-storage drill

Answer these out loud, in ninety seconds, as if it were the interview question it is:

1. Why not store passwords encrypted?
2. Why not SHA-256?
3. What is a salt, and what attack does it prevent?
4. What is a work factor, and how do you choose one?
5. Roughly how many guesses per second does a GPU manage against SHA-256, and against bcrypt at
   cost 12?
6. Why does the login endpoint hash a dummy value when the email does not exist?
7. Why must the final comparison be constant-time?

Number 6 is the one almost nobody has ready, and it is a genuinely good answer to have.

### The broken-endpoint drill

Say what is wrong with each, in one sentence, naming the flaw:

```
GET  /orders/1055            → returns the order if you are logged in
GET  /login?email=a@b.com&password=hunter2
POST /login                  → 401 "no account with that email"
POST /login                  → unlimited attempts, no rate limit
DELETE /comments/91          → the UI hides the button for non-owners
Set-Cookie: session=abc123   (no flags)
```

For the last one, name the three flags that are missing and the attack each one prevents.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Why is string concatenation in a loop slow?*
   Lead with immutability, then count `1 + 2 + ... + n` out loud, then give the number for
   `n = 100,000`, then the fix and why `join` is linear. Add the honest caveat about the CPython
   special case at the end, not the beginning.

2. *What is the difference between authentication and authorisation?*
   One sentence each, then the asymmetry — once versus every request — then a concrete example, then
   `401` versus `403`. Twenty to forty seconds. This is a question you can over-answer.

3. *How would you store passwords, and why?*
   Not plaintext, not encrypted, not a fast hash. Argon2id or bcrypt, salted, work factor tuned to
   about 250 ms, constant-time comparison, library not hand-rolled. Then the number that makes the
   argument: billions of guesses a second against SHA-256, about four a second against bcrypt.

---

## Before you move on

- [ ] I can say why a string cannot be modified, and what happens instead.
- [ ] I never build a string with `+=` in a loop, and I can count the cost out loud.
- [ ] I know that every string method returns a new string and changes nothing.
- [ ] I use `==` on strings, never `is`, and I can say why `is` sometimes appears to work.
- [ ] I use bare `split()` unless I specifically want the empty pieces.
- [ ] I can define authn and authz in one sentence each, with an example.
- [ ] I can answer the password-storage question without hesitating.
- [ ] I put ownership checks in the query, and I can name the flaw that happens when I do not.
- [ ] I can redraw the two-doors diagram from memory, in whatever tool I like.
