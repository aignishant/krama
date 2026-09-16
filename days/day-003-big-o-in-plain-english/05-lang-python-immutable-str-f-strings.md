---
day: 3
track: lang-python
title: "Immutable str, f-strings, and slicing"
theme: "Strings and text"
phase: "Languages: every language, every basic"
status: written
---

# Day 003 · Python — Immutable str, f-strings, and slicing

**Today's theme:** Strings and text

**After today you can:** You can build, slice, search and format text in each language, and say why a Hindi word has a different length in each.

**The interviewer asks it as:** *Why does the length of a string not always equal the number of characters?*

---

## 1. What this is, and why it matters

A string is a piece of text, and in Python it is a sequence of characters that can never be changed once made. You build new strings from old ones with slicing, which cuts out a range, and with f-strings, which fill values into a template. Python counts a string's length in characters, not in the bytes that store them, and that single choice is what separates it from Go and C++ today.

At work, most of what a program does is move text around: names, addresses, log lines, file paths, JSON. Interviewers ask "are Python strings mutable", "what is the difference between a character and a byte", and the trick question in the heading, which has a different answer in each language.

## 2. The story

Anjali turns nine on Sunday, and her father orders the cake on Thursday evening. The bakery is small, three people behind the counter, and they charge extra for every letter written on top.

"Anjali, in English," her father says. The girl at the counter counts on her fingers. Six letters. Sixty rupees extra.

"And underneath, in Hindi," he says. "अंजलि."

Now the counter girl frowns, because she does not read Hindi, and she calls the baker from the back. He looks at the word on her father's phone and counts what he would actually pipe with the icing bag. The big shapes, the dot above the first one, the small hook on the last one. "Five," he says. "Five things to draw. Fifty rupees."

Anjali's father laughs. "But it is only three sounds. An, ja, li. My daughter's name is three sounds long."

The third person behind the counter is the old woman who owns the place. She makes the letters out of a plastic stencil kit, and each shape in the kit is made of small straight pieces that click together. She does not care about sounds and she does not care about shapes. She cares about how many pieces she will use up, because she has to reorder them. She counts. "Fifteen pieces for the Hindi. Six for the English. Every English letter is one piece. Every Hindi shape is three."

So the same name, written once, got three honest answers. Three, if you count what you hear. Five, if you count what you see drawn. Fifteen, if you count what it is built from.

Her father pays for the baker's five. On Sunday, Anjali reads her name off the cake as three sounds and does not think about it at all.

Nobody was wrong. They were counting different things, and each of them had a good reason to count the way they did.

## 3. The idea in plain English

A **string** is a piece of text: `"Anjali"`. In Python the type is `str`. The quotes mark where it starts and ends; they are not part of it.

Text has to be stored somehow, and a computer stores everything as **bytes**, a byte being eight on-or-off switches, enough for 256 different values. English letters fit in one byte each. Most of the world's letters do not. The scheme almost everyone uses today is called **UTF-8**, and in UTF-8 an English letter takes one byte and a Hindi letter takes three. Those are the old woman's stencil pieces.

Each individual letter or mark, whatever it costs in bytes, is called a **code point**. `अ`, `ं`, `ज`, `ल`, `ि` are five code points. Those are the baker's five shapes. Note that `ि`, the vowel sign, is a separate code point even though a reader sees it as part of `लि`.

What a reader sees as one letter, `लि`, is called a **grapheme**. Those are the father's sounds, more or less. Python does not count those for you; no language in this course does without a library.

Python's `len()` counts **code points**. `len("Anjali")` is 6 and `len("अंजलि")` is 5. Python is the baker. Go and C++ are the old woman: they count bytes, and you will see `15` for the same Hindi word, because every one of those five code points, the dot and the vowel sign included, is three bytes in UTF-8.

A Python string is **immutable**: once made, it never changes. `name[0] = "a"` is an error. Every operation that seems to change a string actually makes a new one. This is a deliberate design: it means a string can be safely shared, used as a key, and compared without anyone worrying that it changed underneath them.

**Slicing** cuts out a range: `name[0:3]` is the first three characters, positions 0, 1, 2, stopping before 3. **Indexing** takes one: `name[0]` is `"A"`, `name[-1]` is the last. Counting starts at zero, always.

An **f-string** is a template: `f"{name} is {age}"` fills the holes with values. You saw one yesterday. Today you learn it can also format: `f"{price:.2f}"` shows two decimal places.

## 4. The picture

```
 "Anjali"       index:  0    1    2    3    4    5
                       ┌────┬────┬────┬────┬────┬────┐
                       │ A  │ n  │ j  │ a  │ l  │ i  │   len = 6
                       └────┴────┴────┴────┴────┴────┘
                       name[0:3] = "Anj"   name[-1] = "i"

 "अंजलि"        index:  0    1    2    3    4
                       ┌────┬────┬────┬────┬────┐
                       │ अ  │ ं  │ ज  │ ल  │ ि  │          len = 5 code points
                       └────┴────┴────┴────┴────┘
                       stored as 15 bytes:  E0 A4 85  E0 A4 82  E0 A4 9C  E0 A4 B2  E0 A4 BF
```

*Notice that Python's index steps through the top row, one code point at a time, and never shows you the bottom row unless you ask with `.encode()`. Go and C++ index the bottom row.*

## 5. The code, built step by step

Start `text.py` in a `day03` folder.

```python
name = "Anjali"
print(len(name))
print(name[0], name[-1])
print(name[0:3], name[3:])
```

```
6
A i
Anj ali
```

`name[3:]` with nothing after the colon means "from 3 to the end". `name[:3]` would mean "from the start to 3". Slices never fail on the ends: `name[0:100]` is just the whole string.

```python
hindi = "अंजलि"
print(len(hindi))
print(len(hindi.encode("utf-8")))
```

```
5
15
```

`len` counts code points. `.encode("utf-8")` turns the string into its bytes, and `len` of that is the byte count. Fifteen, three per code point. This is the whole answer to today's interview question, and you will see Go and C++ give `15` from `len` directly.

```python
print(name.upper(), name.lower())
print(name.find("j"), name.find("z"))
print("jal" in name)
print(name.replace("i", "ee"))
```

```
ANJALI anjali
2 -1
True
Anjalee
```

Each of these hands back a **new** string; `name` itself is untouched. `find` gives the position, or `-1` if absent. `in` is the cleanest way to ask "does this contain that".

Now prove the immutability.

```python
name[0] = "a"
```

```
Traceback (most recent call last):
  File "/home/you/day03/text.py", line 12, in <module>
    name[0] = "a"
    ~~~~^^^
TypeError: 'str' object does not support item assignment
```

If you want a lowercase first letter you build a new string: `"a" + name[1:]`.

f-strings, with formatting.

```python
age = 9
price = 50
print(f"{name} is {age}. The cake costs {price:.2f} rupees.")
print(f"{name:>10}|{name:<10}|")
```

```
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
```

After the colon comes a format spec. `.2f` means "as a decimal with two places". `>10` means "right-aligned in ten spaces", `<10` left-aligned. You will use `.2f` for money and `>10` for tables more than anything else.

Splitting and joining, which you will do every day of your working life.

```python
sentence = "an ja li"
parts = sentence.split(" ")
print(parts)
print("-".join(parts))
```

```
['an', 'ja', 'li']
an-ja-li
```

`split` cuts a string into a list of pieces at each separator. `join` is written the other way round from how people expect: the separator is in front, the pieces are inside. Read `"-".join(parts)` as "join these parts using a dash".

Here is the run and output for the complete program.

```bash
python3 text.py
```

```
Anjali has 6 characters and 6 bytes
अंजलि has 5 characters and 15 bytes
first: A last: i slice: Anj
upper: ANJALI  contains 'jal': True  position of 'j': 2
new name: anjali (the original is still Anjali)
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
['an', 'ja', 'li'] -> an-ja-li
```

And the complete file.

```python
# text.py — day 3, immutable strings, slicing, f-strings
# Run:  python3 text.py

name = "Anjali"
hindi = "अंजलि"

print(f"{name} has {len(name)} characters and {len(name.encode('utf-8'))} bytes")
print(f"{hindi} has {len(hindi)} characters and {len(hindi.encode('utf-8'))} bytes")

print(f"first: {name[0]} last: {name[-1]} slice: {name[0:3]}")
print(f"upper: {name.upper()}  contains 'jal': {'jal' in name}  position of 'j': {name.find('j')}")

new_name = "a" + name[1:]
print(f"new name: {new_name} (the original is still {name})")

age = 9
price = 50
print(f"{name} is {age}. The cake costs {price:.2f} rupees.")
print(f"{name:>10}|{name:<10}|")

parts = "an ja li".split(" ")
print(f"{parts} -> {'-'.join(parts)}")
```

Notice the quotes inside the f-strings: single quotes inside double quotes. Python lets you use either kind, and you need a different kind inside than outside so it knows where the string ends.

## 6. How the other two languages do it

Go, where `len` counts bytes and you ask separately for characters:

```go
import "unicode/utf8"

hindi := "अंजलि"
fmt.Println(len(hindi))                    // 15
fmt.Println(utf8.RuneCountInString(hindi)) // 5
```

C++, where `.size()` counts bytes and there is no built-in way to count characters at all:

```cpp
std::string hindi = "अंजलि";
std::cout << hindi.size() << "\n";   // 15
hindi[0] = 'A';                       // allowed: C++ strings are mutable
```

The one line of difference that matters: **Python's `len` counts characters; Go's `len` and C++'s `.size()` count bytes.** So `"Anjali"` is 6 in all three, and `"अंजलि"` is 5 in Python and 15 in the other two. The second thing to notice is the last C++ line: it compiles. C++ strings can be changed in place. Python and Go strings cannot. A Python programmer moving to C++ will be surprised that a function can alter a string it was handed; a C++ programmer moving to Python will be surprised that building a long string by repeated `+` in a loop copies the whole thing every time.

## 7. The traps

**The near-miss: indexing a Hindi string by what you see.** You want the third letter of `"अंजलि"`, which a reader would say is `लि`.

```python
print(hindi[2])
```

```
ज
```

Not `लि`. Index 2 is the third **code point**, and the anusvara dot at index 1 counted as one. What a reader sees as a letter and what Python counts as one are not the same thing, and no slice will give you `लि` as one unit without a library. Store and count in code points; only worry about what a reader sees when you are drawing on a screen.

**The real error: a number in the middle of text.** This looks like it builds a sentence.

```python
age = 9
print("Anjali is " + age)
```

```
Traceback (most recent call last):
  File "/home/you/day03/text.py", line 2, in <module>
    print("Anjali is " + age)
          ~~~~~~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

Yesterday's error, from the other side. Use an f-string, `f"Anjali is {age}"`, and it never happens.

**The near-miss: the off-by-one slice.** You want the last three characters.

```python
print(name[3:5])
```

```
al
```

Only two. The end of a slice is exclusive: `[3:5]` is positions 3 and 4. For the last three, `name[3:6]` or, better, `name[-3:]`, which does not need you to know the length.

## 8. Say it out loud

**How it gets asked**

- "Are Python strings mutable? What does that mean in practice?"
- "Why does the length of a string not always equal the number of characters?"
- "What is the difference between `len(s)` and `len(s.encode())`?"

**What to say out loud, the first ninety seconds**

"A Python string is an immutable sequence of Unicode code points. Immutable means it cannot be changed after it is created; every method like `upper` or `replace` returns a new string. That makes strings safe to share and to use as dictionary keys, and it means building a large string by repeated concatenation copies everything each time, so I use `join` for that.

`len` counts code points, not bytes. An English letter is one code point and one byte, but a Hindi letter like `अ` is one code point and three bytes in UTF-8. So `len('अंजलि')` is 5, and `len('अंजलि'.encode('utf-8'))` is 15. Go and C++ count bytes by default, so the same word has length 15 there. And neither count is quite what a reader sees, because a vowel sign is its own code point but draws as part of the letter before it. So the honest answer is: length of what? Bytes, code points, or what a reader sees are three different numbers."

**The follow-ups**

1. *"How do you build a big string efficiently in Python?"* — Collect the pieces in a list and call `"".join(pieces)` once. Repeated `+=` is quadratic in the worst case.
2. *"What is UTF-8?"* — A way to store code points as bytes, using one byte for the first 128 code points and two to four bytes for the rest. It is the default almost everywhere, and Python's `encode` and `decode` use it unless told otherwise.
3. *"What is `s[::-1]`?"* — A slice with a step of minus one, which walks the string backwards: the reversed string. It reverses code points, so combining marks end up on the wrong letter; fine for interview puzzles, wrong for real text.

**A model answer**

"Python strings are immutable sequences of code points. Slicing with `s[a:b]` returns a new string from index `a` up to but not including `b`, negative indices count from the end, and f-strings interpolate values with optional format specs like `:.2f`. `len` returns the number of code points, which equals the byte count only for ASCII; `s.encode('utf-8')` gives the bytes, and for Devanagari each code point is three bytes. Go's `len` and C++'s `size()` return bytes, so the same text reports a different length there. Because strings are immutable, I use `join` rather than `+=` in a loop, and I remember that no built-in count gives me user-perceived characters."

## 9. Recall card

- `str` is immutable: `s[0] = "a"` is a `TypeError`; every method returns a new string; build big strings with `"".join(parts)`.
- `len(s)` counts code points; `len(s.encode("utf-8"))` counts bytes; `"अंजलि"` is 5 and 15. Go and C++ say 15.
- `s[a:b]` is `a` up to but not including `b`; `s[-1]` is the last; `s[-3:]` is the last three.
- `f"{price:.2f}"` two decimals, `f"{name:>10}"` right-aligned in ten.
- `"Anjali is " + 9` is a `TypeError`; f-strings make it go away.
