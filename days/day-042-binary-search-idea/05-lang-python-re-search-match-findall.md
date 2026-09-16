---
day: 42
track: lang-python
title: "re: search, match, findall, groups, and compiled patterns"
theme: "Regular expressions"
phase: "Languages: advanced features"
status: written
---

# Day 042 · Python — re: search, match, findall, groups, and compiled patterns

**Today's theme:** Regular expressions

**After today you can:** You can extract dates and emails from text in each language and say when regex is the wrong tool.

**The interviewer asks it as:** *Write a pattern that matches an email address. Now say why it is wrong.*

---

## 1. What this is, and why it matters

Python's `re` module searches, captures, and replaces text described by a
pattern. `search` looks anywhere; `match` starts at the beginning; `fullmatch`
requires the whole input. You use these operations to extract fields from logs
without confusing a successful search with valid input.

## 2. The story

Anya is looking through the family chat for the day her cousin arrives. There
are photographs, greetings, and long arguments about who will collect him. She
does not read every message with equal care. She looks for four digits, a dash,
two digits, another dash, and two more digits. That is how her cousin usually
writes the day of a journey.

She finds 2026-09-16 in a sentence about a train. She also finds 2026-99-40 in a
message where her uncle has made a joke. Both have the arrangement she was
looking for. Only one can name a real day. Her way of spotting likely dates has
saved her some reading, but it has not settled which ones to trust.

Her mother asks her to find the cousin's email address too. Anya looks for a
short stretch without spaces, then an at sign, then another stretch containing
a dot. She finds an address in a message and copies it. Her mother asks whether
that means the address still works. Anya shakes her head. The cousin might have
stopped using it years ago. They will have to send a message and hear back.

Before she closes the chat, Anya checks the train booking itself. The shapes
helped her find candidates. The booking and a reply supply the facts she actually
needs. She keeps those two jobs separate the next time she searches.

## 3. The idea in plain English

A regular expression, or regex, describes a text shape. `[0-9]` accepts one
ASCII digit; `{4}` repeats the preceding piece four times. Parentheses capture
part of a match so you can retrieve the year separately. `+` means one or more,
and `.` normally accepts almost any character; write `\.` for a literal dot.

Searching asks whether the shape occurs anywhere. Whole-input matching asks
whether every character belongs to the shape. Neither validates a calendar or
proves ownership of a mailbox. Use a date parser after extraction and a
confirmation message when ownership matters. Prefer a literal substring search
when you have no variable shape to describe.

## 4. The picture

```text
text:  arrive 2026-09-16 please
              |year| mm dd
+search --------------------> candidate
+date parser ----------------> real calendar date?
```

Notice where the decision happens and what information it needs.

## 5. The code, built step by step

```python
date = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
```

A raw literal preserves backslashes for the regex parser. Compiling returns a reusable pattern object.

```python
found = date.search("arrive 2026-09-16")
if found is not None:
    print(found.group(1))
```

Check for absence first. Group zero is the entire match; groups one through three are the pieces.

Save as `main.py`; run `python main.py`.

Expected application output (framework access logs are omitted):

    year 2026
    start False
    whole False
    parts [('2026', '09', '16'), ('2026', '09', '18')]
    invalid: unterminated character set at position 0

Complete program:

```python
import re

def main() -> None:
    date = re.compile(r"([0-9]{4})-([0-9]{2})-([0-9]{2})")
    text = "arrive 2026-09-16; leave 2026-09-18"
    found = date.search(text)
    if found is not None:
        print("year", found.group(1))
    print("start", date.match(text) is not None)
    print("whole", date.fullmatch("2026-09-16x") is not None)
    print("parts", date.findall(text))
    try:
        re.compile("[")
    except re.error as exc:
        print("invalid:", exc)

if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
pattern, err := regexp.Compile(`([0-9]{4})-([0-9]{2})-([0-9]{2})`)
```

Use Compile for a pattern that can fail and handle its error. MustCompile is appropriate only for a trusted program constant whose failure is a programming mistake.

**Cpp**

```cpp
const std::regex date(R"(([0-9]{4})-([0-9]{2})-([0-9]{2}))");
```

A raw C++ literal avoids doubling regex backslashes. The default grammar is ECMAScript, not Python's entire syntax.

**The difference that matters:** Choose search or whole-input matching deliberately.

## 7. The traps

**Near-miss:** `re.match(r"[0-9]+", "12cats")` succeeds. Use `fullmatch` for
a numeric field. `findall` returns tuples when there are several capturing
groups; use `finditer` if you need full match objects and positions.

**Real error:** the complete program catches the invalid pattern `[` and prints
`invalid: unterminated character set at position 0`. Catch `re.error` on Python
3.12; newer Python also names this exception `PatternError`.

Python's engine can backtrack: it revisits earlier choices. Nested ambiguous
repetition such as `(a+)+$` can become very expensive on a long almost-match.
Compiling does not remove this risk. Avoid such patterns on untrusted input;
bound input length and choose a suitable engine when predictable cost matters.

Reference: [Python re reference](https://docs.python.org/3/library/re.html).

## 8. Say it out loud

**How it gets asked**

- Write a pattern that matches an email address. Now say why it is wrong.
- Why does a regex accepting a date not prove that the date exists?
- Which engine can promise linear matching for a fixed pattern, and what syntax does it give up?

**What to say out loud**

I first clarify whether you want extraction or validation. To extract a date,
I can search for four ASCII digits, a dash, two digits, a dash, and two digits,
with boundaries appropriate to the input format. Capturing groups return its
pieces. To validate a whole field I require the entire input to match and then
ask a date parser to check month lengths and leap years. For email I would call
a small pattern a product input rule, not a complete definition of valid email.
It cannot tell me whether an inbox exists. I also ask about untrusted input:
pattern syntax and worst-case matching cost depend on the engine.

**The follow-ups**

- **Why compile a pattern once?** It separates pattern construction from repeated matching and makes reuse explicit.

- **Why not parse JSON with regex?** Nested structure and escapes belong to a JSON parser; regex is useful for bounded flat fields.

- **Does a matching email exist?** No. Syntax, deliverability, and ownership are separate checks.

**A model answer**

For an agreed simple ASCII field I might start with
`[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` and require a whole-input match.
It still accepts consecutive dots and other invalid arrangements and rejects
some legitimate address forms. I would state those limitations, apply the
product's documented policy, and confirm ownership separately. I would not
claim that adding more punctuation to the pattern makes it an email parser.

## 9. Recall card

- Choose search or whole-input matching deliberately.
- Capture parentheses return pieces, not semantic validity.
- Use ASCII ranges when the contract says ASCII.
- Compile reusable patterns once; understand the engine's cost.
- Parse dates; confirm email ownership.
