---
day: 20
track: practice
title: "Practice — Building strings without the quadratic trap"
status: written
---

# Day 020 · Practice

**DSA topic:** Building strings without the quadratic trap
**System design topic:** JWT, sessions, and OAuth

---

## Code these, in this order

Four problems that all produce a string as their answer. In every one of them, say the words *"I'll
collect into a list and join"* **before** you write the loop. That sentence is the skill.

Before each one, say out loud:

1. Does the signature give me `str` or `list[str]`? Which technique is that asking for?
2. How long is the output, and how many times will each character be copied?
3. Is there a "last group" that ends by running out rather than by changing?
4. What happens on the empty input?

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Reverse Words in a String III | LeetCode 557 (Easy) | `split`, transform each word, `join`. Two minutes if you use the pattern, and a nested-loop `+=` disaster if you do not. |
| 2 | Add Strings | LeetCode 415 (Easy) | Digit-by-digit addition with a carry, built backwards into a list and reversed before joining. The carry after the loop is the same "flush the last thing" reflex as the run-length encoder. |
| 3 | String Compression | LeetCode 443 (Medium) | The signature is `list[str]`, so this is the write pointer in `O(1)` space, **not** a join problem. Solve it wrong on purpose first, then right. |
| 4 | Encode and Decode Strings | LeetCode 271 (Medium) | Designing your own format. Length-prefixing beats delimiters, and working out why is the whole exercise. |

### On problem 3, do it both ways deliberately

First write the `join` version — walk the list, build parts, return `"".join(parts)` — and confirm it
produces the right characters. Then read the problem statement again and notice it wants the answer
**inside the input list**, with the new length returned.

Then write the write-pointer version. Then answer, out loud:

1. Which version uses `O(n)` extra space and which uses `O(1)`?
2. Why is the in-place write always safe? Give the run-length argument.
3. What does a run of 12 produce, and how many cells does it occupy?
4. What does a run of 1 produce, and why is that special-cased?

### On problem 4, design before you code

Try the obvious answer first — join the strings with a separator like `#` — and then find the input
that breaks it. It will not take long: a string that *contains* a `#`.

Then design the length-prefixed format: write each string as its length, a delimiter, then the
string itself, so `["ab", "c#d"]` becomes `2#ab3#c#d`. Say out loud why the delimiter inside `c#d` is
now harmless. That reasoning — *the length tells the reader exactly how far to read, so the content
can be anything* — is the same reasoning behind every binary protocol you will meet later.

### The pattern drill

Rewrite each of these using the list-and-join pattern, then say what the original cost was:

```python
# 1
out = ""
for row in rows:
    for cell in row:
        out += str(cell) + ","
    out += "\n"
```

```python
# 2
result = ""
for word in words:
    result += word + ", "
result = result[:-2]
```

```python
# 3
html = "<ul>"
for item in items:
    html += "<li>" + item + "</li>"
html += "</ul>"
```

For number 2, also say what goes wrong when `words` is empty — and why `", ".join(words)` has no such
problem.

### The measurement drill

Run this and read the numbers.

```python
import io, time

n = 200_000

def timed(f):
    start = time.perf_counter(); f(); return time.perf_counter() - start

def grow():
    s = ""
    for _ in range(n):
        s = "x" + s

def listjoin():
    p = []
    for _ in range(n):
        p.append("x")
    "".join(p)

def stringio():
    b = io.StringIO()
    for _ in range(n):
        b.write("x")
    b.getvalue()

for name, f in (("grow", grow), ("list+join", listjoin), ("StringIO", stringio)):
    print(f"{name:12} {timed(f):.4f}s")
```

Then answer:

1. What is the ratio between the first and second?
2. How many character copies does `grow` do in total at `n = 200,000`?
3. Why are `list+join` and `StringIO` almost identical?
4. Name the one situation where you would choose `StringIO` over `list+join`.

### The error drill

Predict, then run:

```python
print(",".join([3, 1, 4]))
```

```python
print("count: " + 5)
```

```python
print("-".join("abc"))
```

For the third: there is no error and the output is probably not what was intended. Say what happened
and why it is dangerous.

### The auth-mechanism drill

Answer each in one or two sentences, out loud:

1. HTTP is stateless. What does that force the client to do on every request?
2. What is actually inside a session cookie, and what is inside a JWT?
3. Is a JWT encrypted? What does the signature guarantee, and what does it not?
4. Name the three cookie flags and the attack each prevents.
5. Why `RS256` rather than `HS256` once more than one service verifies tokens?
6. What is the `alg: none` attack, and what is the fix?
7. Why does the OAuth flow return a code and then exchange it, rather than returning the token
   straight away?
8. OAuth or OIDC — which one is "Log in with Google", and which is authorisation?

### The revocation drill

This is the question the whole topic exists for. Take each scenario and say what happens under
sessions, and what happens under JWTs:

1. A user clicks "log out".
2. A user clicks "log out of all other devices".
3. An admin bans an account for abuse at 14:32.
4. A user changes their password after their laptop is stolen.
5. A moderator is demoted to ordinary member.

Then answer: for scenario 3, if access tokens live 15 minutes, when is the banned user actually out?
And what would you change to make it faster, and what does that change cost you?

### The arithmetic drill

From memory, in under two minutes, for an API at 10,000 requests a second:

- Session lookup at 0.5 ms — how much waiting per second, and is that a problem for Redis?
- JWT verification at 0.1 ms of CPU — how many cores?
- 800-byte JWT versus a 32-byte cookie — how much extra traffic per day?
- 10 million users, 20% with a live session at 200 bytes — how much Redis?
- 10 million users on 15-minute access tokens — how many refresh calls per second, and why does that
  number undercut the word "stateless"?

The last one is the strongest thing you can say in this topic. Have it ready.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Build a string of n characters efficiently.*
   Immutability, then the count `1 + 2 + ... + n`, then the fix, then why `join` is linear — one
   pass to measure, one allocation, one copy per character. Finish with the cross-language point:
   `StringBuilder` in Java, `strings.Builder` in Go, the same idea.

2. *How do you keep a user logged in across requests?*
   Start from statelessness. Two shapes, one sentence each. Then the trade — revocation against a
   lookup — then the numbers, then what you would actually build and why. Finish with the honest
   line: short-lived tokens plus revocable refresh tokens is a session store with extra steps.

3. *Compress the string: `aabbccc` becomes `a2b2c3`.*
   Read the signature out loud first and say what it implies. Then the loop that consumes a whole run
   at a time, then the flush-the-last-group point, then why the in-place write can never overtake
   the read.

---

## Before you move on

- [ ] I say "collect into a list and join" before writing any loop that produces a string.
- [ ] I can count out loud why growing a string is `O(n²)` and joining is `O(n)`.
- [ ] I check whether the signature says `str` or `list[str]` before choosing a technique.
- [ ] I flush the last group after any loop that groups consecutive items.
- [ ] I never build separators by hand — `join` handles the last element.
- [ ] I can explain a session and a JWT in one sentence each, and name the trade between them.
- [ ] I know a JWT is encoded, not encrypted, and what the signature actually guarantees.
- [ ] I can walk through the OAuth authorisation-code flow and say why the code step exists.
- [ ] I can redraw the where-the-truth-lives diagram from memory, in whatever tool I like.
