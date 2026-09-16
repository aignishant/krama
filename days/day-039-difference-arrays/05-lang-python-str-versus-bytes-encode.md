---
day: 39
track: lang-python
title: "str versus bytes, encode, decode, and UnicodeDecodeError"
theme: "Text versus bytes"
phase: "Languages: advanced features"
status: written
---

# Day 039 · Python — str versus bytes, encode, decode, and UnicodeDecodeError

**Today's theme:** Text versus bytes

**After today you can:** You can explain what a byte is, what a character is, and where each language draws the line.

**The interviewer asks it as:** *What is the difference between a byte and a character?*

## 1. What this is, and why it matters

str contains Unicode text and bytes contains byte values. encode converts text to bytes; decode interprets bytes using an explicit encoding.

You use this when discussing text versus bytes in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Zoya packs sweets into small boxes for a family visit. Some sweets fit in one space, while larger ones take two or three. When her brother says a box has twelve spaces, that does not tell her how many sweets are inside. The number of spaces and the number of sweets answer different questions.

He cuts a packed row after the fifth space to divide it between two people. One large sweet straddles that boundary and gets broken. Zoya tells him to find the edge of a sweet before dividing the row. Counting spaces is useful for the box, but it is not enough for a clean division of the contents.

They also arrange two tiny sweets together to look like one flower. A guest points to the flower and calls it one piece, while Zoya knows it contains two sweets. Even counting complete sweets does not always match what a person sees as one shape.

For the trip, Zoya writes down how the sweets were packed. Her aunt needs the same arrangement when unpacking them. Guessing the arrangement can make a perfectly good box look damaged, even though nothing changed during the journey.

Before promising how many pieces a box holds, Zoya asks what someone means by a piece: a space, a whole sweet, or a visible decoration. The right counting rule depends on the question. Treating all three as the same would make both the count and the cut unreliable.

## 3. The idea in plain English

Zoya’s spaces are bytes; complete sweets are code points. A **code point** is a numbered Unicode element. A **grapheme cluster** is a user-perceived character, which may contain several code points. Python len(str) counts code points, not UTF-8 bytes and not necessarily graphemes.

Encoding é in UTF-8 produces two bytes. The visually similar sequence e plus a combining accent contains two code points. Normalisation can reconcile some equivalent sequences, but it is a separate policy. The default strict decoder rejects malformed input; errors="replace" inserts replacement characters and loses information. Use that only when the application’s contract permits it.

## 4. The picture

```text
"é": UTF-8 bytes [C3 A9] -> one code point
"e + combining accent": [65 CC 81] -> two code points, one grapheme
```

Bytes, Unicode code points, and user-perceived characters are different units.

## 5. The code, built step by step

First isolate the important operation:

```python
encoded = text.encode("utf-8")
restored = encoded.decode("utf-8")
```

State the counting unit before choosing an operation.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
import unicodedata

text = "é"
encoded = text.encode("utf-8")
print(len(text), len(encoded))
print(encoded.decode("utf-8") == text)
decomposed = "e\u0301"
print(len(decomposed), unicodedata.normalize("NFC", decomposed) == text)
try:
    b"\xff".decode("utf-8")
except UnicodeDecodeError as error:
    print(type(error).__name__, error.reason)
```

**Check the result:** Prints `1 2`, `True`, `2 True`, and `UnicodeDecodeError invalid start byte`.

## 6. How the other two languages do it

**Go**

```go
for offset, character := range text {
    fmt.Println(offset, character)
}
```

A Go string is a byte sequence. range decodes UTF-8 into runes and reports byte offsets; a rune is an alias for int32 representing a code point.

**C++**

```cpp
if ((byte & 0xc0) != 0x80)
    throw std::invalid_argument("invalid UTF-8");
```

std::string stores char elements and does not enforce UTF-8 validity. C++20 char8_t distinguishes UTF-8 code units, while string_view borrows storage without owning it.

Python str indexes code points, Go string indexes bytes while range decodes runes, and C++ string normally exposes bytes. None of those basic operations automatically counts grapheme clusters.

## 7. The traps

**Near-miss:** reverse encoded bytes and decode; you can split a multibyte sequence. The malformed example raises `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte`. Reversing str avoids broken UTF-8 but can still detach a combining accent from its intended base.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a byte and a character?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I ask whether the requirement concerns bytes, code points, or visible characters. I encode and decode explicitly at I/O boundaries and reject malformed input unless replacement is a stated policy. Python str handles code points, which simplifies many tasks but does not solve grapheme segmentation. I choose normalisation when the domain needs equivalent spellings to compare equal and test combining marks rather than only ASCII.

**Follow-ups**

1. **Does len(str) count visible characters?** It counts code points; a visible grapheme may contain several.

2. **What does errors="replace" cost?** It replaces malformed data and therefore loses the original byte information.

3. **Does text reversal preserve graphemes?** Not automatically. Code-point reversal can reorder combining sequences.

**Model answer:** str contains Unicode text and bytes contains byte values. encode converts text to bytes; decode interprets bytes using an explicit encoding. Code points and user-perceived characters are not interchangeable.

## 9. Recall card

- State the counting unit before choosing an operation.
- Encode and decode with an explicit encoding.
- Strict decoding rejects malformed bytes.
- Code points and user-perceived characters are not interchangeable.

Further reading: [Official reference](https://docs.python.org/3.12/howto/unicode.html).
