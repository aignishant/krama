---
day: 39
track: lang-go
title: "[]byte, rune, the utf8 package, and strings.Builder"
theme: "Text versus bytes"
phase: "Languages: advanced features"
status: written
---

# Day 039 · Go — []byte, rune, the utf8 package, and strings.Builder

**Today's theme:** Text versus bytes

**After today you can:** You can explain what a byte is, what a character is, and where each language draws the line.

**The interviewer asks it as:** *What is the difference between a byte and a character?*

## 1. What this is, and why it matters

A Go string is a byte sequence. range decodes UTF-8 into runes and reports byte offsets; a rune is an alias for int32 representing a code point.

You use this when discussing text versus bytes in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Zoya packs sweets into small boxes for a family visit. Some sweets fit in one space, while larger ones take two or three. When her brother says a box has twelve spaces, that does not tell her how many sweets are inside. The number of spaces and the number of sweets answer different questions.

He cuts a packed row after the fifth space to divide it between two people. One large sweet straddles that boundary and gets broken. Zoya tells him to find the edge of a sweet before dividing the row. Counting spaces is useful for the box, but it is not enough for a clean division of the contents.

They also arrange two tiny sweets together to look like one flower. A guest points to the flower and calls it one piece, while Zoya knows it contains two sweets. Even counting complete sweets does not always match what a person sees as one shape.

For the trip, Zoya writes down how the sweets were packed. Her aunt needs the same arrangement when unpacking them. Guessing the arrangement can make a perfectly good box look damaged, even though nothing changed during the journey.

Before promising how many pieces a box holds, Zoya asks what someone means by a piece: a space, a whole sweet, or a visible decoration. The right counting rule depends on the question. Treating all three as the same would make both the count and the cut unreliable.

## 3. The idea in plain English

Zoya’s box spaces correspond to string bytes. len returns their count and indexing returns one byte. The utf8 package validates encoding and counts decoded runes. A **rune** can represent a Unicode code point, but one rune is not necessarily one visible character.

Invalid UTF-8 can exist in a Go string. Range reports RuneError and advances over invalid encoding; validation must be explicit if malformed text is unacceptable. strings.Builder assembles text without repeatedly copying the whole prefix. Do not copy a non-zero Builder because it tracks ownership of its internal storage.

## 4. The picture

```text
"é": UTF-8 bytes [C3 A9] -> one code point
"e + combining accent": [65 CC 81] -> two code points, one grapheme
```

Bytes, Unicode code points, and user-perceived characters are different units.

## 5. The code, built step by step

First isolate the important operation:

```go
for offset, character := range text {
    fmt.Println(offset, character)
}
```

Range offsets are byte offsets.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "fmt"
    "strings"
    "unicode/utf8"
)
func main() {
    text := "éa"
    fmt.Println(len(text), utf8.RuneCountInString(text))
    var output strings.Builder
    for offset, character := range text {
        fmt.Printf("%d:%U\n", offset, character)
        output.WriteRune(character)
    }
    fmt.Println(output.String())
    invalid := string([]byte{0xff})
    fmt.Println(utf8.ValidString(invalid))
}
```

**Check the result:** Prints `3 2`, `0:U+00E9`, `2:U+0061`, `éa`, and `false`. Offsets are byte positions, so a begins at 2.

## 6. How the other two languages do it

**Python**

```python
encoded = text.encode("utf-8")
restored = encoded.decode("utf-8")
```

str contains Unicode text and bytes contains byte values. encode converts text to bytes; decode interprets bytes using an explicit encoding.

**C++**

```cpp
if ((byte & 0xc0) != 0x80)
    throw std::invalid_argument("invalid UTF-8");
```

std::string stores char elements and does not enforce UTF-8 validity. C++20 char8_t distinguishes UTF-8 code units, while string_view borrows storage without owning it.

Python str indexes code points, Go string indexes bytes while range decodes runes, and C++ string normally exposes bytes. None of those basic operations automatically counts grapheme clusters.

## 7. The traps

**Near-miss:** slice text[:1] and assume it holds the first character; it contains only the first byte of é. The language allows that invalid UTF-8 string. Copying a non-zero strings.Builder and then writing can panic with `strings: illegal use of non-zero Builder copied by value`. Validate encoding independently of iteration.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a byte and a character?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I distinguish bytes from runes and say that range offsets remain byte offsets. I validate with utf8.ValidString when malformed input must be rejected. I use Builder for incremental text construction and keep its ownership local. Converting to []rune makes code-point indexing available at an allocation cost, but it still does not provide user-perceived character segmentation. I test multibyte and combining sequences.

**Follow-ups**

1. **Does len(string) count runes?** No. It counts bytes.

2. **Can a string hold malformed UTF-8?** Yes. String validity is not enforced by the type.

3. **Does []rune solve grapheme segmentation?** No. It gives code points, not necessarily visible characters.

**Model answer:** A Go string is a byte sequence. range decodes UTF-8 into runes and reports byte offsets; a rune is an alias for int32 representing a code point. Rune counts still differ from grapheme counts.

## 9. Recall card

- Range offsets are byte offsets.
- Validate UTF-8 when the boundary requires it.
- Builder avoids repeated prefix construction.
- Rune counts still differ from grapheme counts.

Further reading: [Official reference](https://pkg.go.dev/unicode/utf8).
