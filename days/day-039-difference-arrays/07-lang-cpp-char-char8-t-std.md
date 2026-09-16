---
day: 39
track: lang-cpp
title: "char, char8_t, std::string_view, and UTF-8 by hand"
theme: "Text versus bytes"
phase: "Languages: advanced features"
status: written
---

# Day 039 · C++ — char, char8_t, std::string_view, and UTF-8 by hand

**Today's theme:** Text versus bytes

**After today you can:** You can explain what a byte is, what a character is, and where each language draws the line.

**The interviewer asks it as:** *What is the difference between a byte and a character?*

## 1. What this is, and why it matters

std::string stores char elements and does not enforce UTF-8 validity. C++20 char8_t distinguishes UTF-8 code units, while string_view borrows storage without owning it.

You use this when discussing text versus bytes in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Zoya packs sweets into small boxes for a family visit. Some sweets fit in one space, while larger ones take two or three. When her brother says a box has twelve spaces, that does not tell her how many sweets are inside. The number of spaces and the number of sweets answer different questions.

He cuts a packed row after the fifth space to divide it between two people. One large sweet straddles that boundary and gets broken. Zoya tells him to find the edge of a sweet before dividing the row. Counting spaces is useful for the box, but it is not enough for a clean division of the contents.

They also arrange two tiny sweets together to look like one flower. A guest points to the flower and calls it one piece, while Zoya knows it contains two sweets. Even counting complete sweets does not always match what a person sees as one shape.

For the trip, Zoya writes down how the sweets were packed. Her aunt needs the same arrangement when unpacking them. Guessing the arrangement can make a perfectly good box look damaged, even though nothing changed during the journey.

Before promising how many pieces a box holds, Zoya asks what someone means by a piece: a space, a whole sweet, or a visible decoration. The right counting rule depends on the question. Treating all three as the same would make both the count and the cut unreliable.

## 3. The idea in plain English

Zoya’s spaces correspond to code units. A **code unit** is one storage element of an encoding; UTF-8 uses eight-bit units. u8string stores char8_t units, but indexing still does not decode a full code point. A string_view avoids copying only while its source storage remains valid.

The example validates UTF-8 manually to make the rules visible: continuation bytes must be 80–BF, sequences must not be overlong, surrogate values are forbidden, and code points must not exceed 10FFFF. Production code should use a maintained Unicode library for segmentation and broader text policy. Code-point counting below is still not grapheme counting.

## 4. The picture

```text
"é": UTF-8 bytes [C3 A9] -> one code point
"e + combining accent": [65 CC 81] -> two code points, one grapheme
```

Bytes, Unicode code points, and user-perceived characters are different units.

## 5. The code, built step by step

First isolate the important operation:

```cpp
if ((byte & 0xc0) != 0x80)
    throw std::invalid_argument("invalid UTF-8");
```

Validate complete UTF-8 sequences, not only leading bytes.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <string_view>

std::size_t count_codepoints(std::string_view text) {
    std::size_t count = 0;
    for (std::size_t i = 0; i < text.size(); ++count) {
        auto first = static_cast<unsigned char>(text[i++]);
        unsigned value = 0, minimum = 0;
        int remaining = 0;
        if (first < 0x80) value = first;
        else if (first >= 0xc2 && first <= 0xdf) { value = first & 0x1f; remaining = 1; minimum = 0x80; }
        else if (first >= 0xe0 && first <= 0xef) { value = first & 0x0f; remaining = 2; minimum = 0x800; }
        else if (first >= 0xf0 && first <= 0xf4) { value = first & 7; remaining = 3; minimum = 0x10000; }
        else throw std::invalid_argument("invalid UTF-8");
        while (remaining--) {
            if (i == text.size()) throw std::invalid_argument("invalid UTF-8");
            auto byte = static_cast<unsigned char>(text[i++]);
            if ((byte & 0xc0) != 0x80) throw std::invalid_argument("invalid UTF-8");
            value = (value << 6) | (byte & 0x3f);
        }
        if (value < minimum || value > 0x10ffff || (value >= 0xd800 && value <= 0xdfff))
            throw std::invalid_argument("invalid UTF-8");
    }
    return count;
}
int main() {
    std::string text = "\xc3\xa9";
    std::u8string units = u8"\u00e9";
    std::cout << text.size() << ' ' << count_codepoints(text) << ' ' << units.size() << '\n';
    try { count_codepoints(std::string(1, static_cast<char>(0xff))); }
    catch (const std::invalid_argument& error) { std::cout << error.what() << '\n'; }
}
```

**Check the result:** Prints `2 1 2` and `invalid UTF-8`. Test truncated sequences, isolated continuation bytes, overlong encodings, surrogates, and values beyond U+10FFFF before changing this decoder.

## 6. How the other two languages do it

**Python**

```python
encoded = text.encode("utf-8")
restored = encoded.decode("utf-8")
```

str contains Unicode text and bytes contains byte values. encode converts text to bytes; decode interprets bytes using an explicit encoding.

**Go**

```go
for offset, character := range text {
    fmt.Println(offset, character)
}
```

A Go string is a byte sequence. range decodes UTF-8 into runes and reports byte offsets; a rune is an alias for int32 representing a code point.

Python str indexes code points, Go string indexes bytes while range decodes runes, and C++ string normally exposes bytes. None of those basic operations automatically counts grapheme clusters.

## 7. The traps

**Near-miss:** count every non-continuation byte as a code point without validating the sequence; malformed bytes then pass. The example rejects them with `std::invalid_argument` carrying `invalid UTF-8`. Returning a string_view into a temporary string dangles; no encoding check can repair an invalid lifetime.

## 8. Say it out loud

**How it gets asked:** “What is the difference between a byte and a character?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I state the encoding and distinguish storage units from decoded code points. char8_t improves type distinction but does not validate or segment text by itself. I validate complete UTF-8 sequences when decoding manually and reject overlong encodings, surrogates, and out-of-range values. For visible-character operations I use a Unicode segmentation library. Any borrowed string_view also needs a source lifetime that covers every use.

**Follow-ups**

1. **Does string::size count characters?** It counts char elements, normally bytes, not decoded code points.

2. **Does char8_t guarantee valid text?** No. A sequence of code units still needs validation.

3. **Does a string_view own its source?** No. The original storage must outlive the view’s use.

**Model answer:** std::string stores char elements and does not enforce UTF-8 validity. C++20 char8_t distinguishes UTF-8 code units, while string_view borrows storage without owning it. Encoding correctness and storage lifetime are separate requirements.

## 9. Recall card

- Validate complete UTF-8 sequences, not only leading bytes.
- char8_t represents a UTF-8 code unit.
- string_view is non-owning.
- Encoding correctness and storage lifetime are separate requirements.

Further reading: [Official reference](https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-3/).
