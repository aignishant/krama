---
day: 3
track: lang-go
title: "Strings are bytes, runes are characters, fmt.Sprintf"
theme: "Strings and text"
phase: "Languages: every language, every basic"
status: written
---

# Day 003 · Go — Strings are bytes, runes are characters, fmt.Sprintf

**Today's theme:** Strings and text

**After today you can:** You can build, slice, search and format text in each language, and say why a Hindi word has a different length in each.

**The interviewer asks it as:** *Why does the length of a string not always equal the number of characters?*

---

## 1. What this is, and why it matters

A Go string is an immutable sequence of bytes, and `len` tells you how many bytes, not how many characters. When you want characters, Go calls them runes and gives you a separate way to count and walk them. Formatting is done by `fmt.Sprintf`, which fills a template with `%` holes, and the `strings` package holds everything else.

At work this is the single most common Go bug in code that handles names, addresses, or anything not in English: slicing a string at a byte position and cutting a character in half. Interviewers ask "what is a rune", "why is `len` of a string not the character count", and "why does `for range` over a string give you weird indices". All three are today.

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

A **string** is a piece of text: `"Anjali"`. In Go, a string is a sequence of **bytes**, where a byte is eight on-or-off switches holding one of 256 values. That is the definition, and everything else today follows from it.

Text is stored in bytes using **UTF-8**, the scheme almost everyone uses, where an English letter takes one byte and a Hindi letter takes three. Go strings are UTF-8 by convention, and Go source files are always UTF-8, so `"अंजलि"` typed into your program is fifteen bytes.

`len(s)` counts bytes. `len("Anjali")` is 6. `len("अंजलि")` is 15. Go is the old woman with the stencil kit.

When you want the baker's count, the individual letters and marks, Go calls each one a **rune**. A rune is a single **code point**, one Unicode character, stored as a 32-bit number. The `unicode/utf8` package has `utf8.RuneCountInString(s)`, which gives 5 for the Hindi word. And when you walk a string with `for range`, Go hands you runes, one at a time, with the byte position each one starts at, which is why the positions go 0, 3, 6, 9, 12 instead of 0, 1, 2, 3, 4.

Indexing, `s[0]`, gives you a **byte**, not a character. For `"Anjali"` that is fine; `s[0]` is the byte for `A`. For `"अंजलि"`, `s[0]` is 224, the first third of `अ`, and turning it into a string gives you a Latin letter with an accent. Slicing, `s[0:3]`, is also by byte, and works for the Hindi word only because you happen to know each character is three bytes.

Go strings are **immutable**: `s[0] = 'a'` does not compile. To change one, build a new one. For building large strings, `strings.Builder` avoids copying.

`fmt.Sprintf` is Go's f-string. `fmt.Sprintf("%s is %d", name, age)` fills `%s` with a string and `%d` with a whole number and returns the result; `fmt.Printf` prints it instead of returning it. `%.2f` is two decimal places, `%10s` right-aligns in ten spaces, `%c` prints a rune as a character, `%q` prints a string in quotes.

## 4. The picture

```
 s := "अंजलि"                     len(s) = 15 bytes
 byte index:  0  1  2   3  4  5   6  7  8   9 10 11  12 13 14
             ┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐
             │E0│A4│85││E0│A4│82││E0│A4│9C││E0│A4│B2││E0│A4│BF│
             └──┴──┴──┘└──┴──┴──┘└──┴──┴──┘└──┴──┴──┘└──┴──┴──┘
 rune:           अ          ं          ज          ल          ि
 for range i:    0          3          6          9          12
```

*Notice that `for range` gives you the byte index where each rune starts, not a rune counter. Notice also that `s[1]` is the middle byte of `अ`, which by itself means nothing.*

## 5. The code, built step by step

Start `text.go` in a `day03` folder.

```go
package main

import (
	"fmt"
	"strings"
	"unicode/utf8"
)
```

Three imports. `strings` holds the text tools. `unicode/utf8` holds the rune counting. When you import more than one package, they go inside round brackets, one per line.

```go
func main() {
	name := "Anjali"
	hindi := "अंजलि"
	fmt.Println(len(name), len(hindi))
	fmt.Println(utf8.RuneCountInString(name), utf8.RuneCountInString(hindi))
}
```

```
6 15
6 5
```

Two counts, two answers. `len` is bytes, `RuneCountInString` is characters. For English they agree. For everything else they do not.

Now index and slice by byte.

```go
	fmt.Println(name[0], string(name[0]), name[0:3])
	fmt.Println(hindi[0], hindi[0:3])
```

```
65 A Anj
224 अ
```

`name[0]` is the byte `65`, which is the code for `A`; wrapping it in `string()` shows the letter. `hindi[0]` is `224`, the first byte of a three-byte character, and on its own it is not a character at all. `hindi[0:3]` happens to be exactly the three bytes of `अ`, so it prints properly. `hindi[0:2]` would print garbage.

The right way to walk characters.

```go
	for i, r := range hindi {
		fmt.Printf("byte %2d: %c (code point %d)\n", i, r, r)
	}
```

```
byte  0: अ (code point 2309)
byte  3: ं (code point 2306)
byte  6: ज (code point 2332)
byte  9: ल (code point 2354)
byte 12: ि (code point 2367)
```

A `for range` over a string runs the lines inside once per rune. You meet loops properly tomorrow; today just read it as "for each character". `i` is the byte index where the rune starts and `r` is the rune. `%c` prints the rune as a character and `%d` prints its number. `%2d` right-aligns the number in two spaces.

When you need the third character by position, convert to a slice of runes first.

```go
	runes := []rune(hindi)
	fmt.Println(len(runes), string(runes[2]))
```

```
5 ज
```

`[]rune(hindi)` makes a new sequence with one rune per character, so `runes[2]` is the third character. Converting back with `string(runes)` gives a normal string again.

Immutability, and the compiler's answer to it.

```go
	name[0] = 'a'
```

```
./text.go:22:2: cannot assign to name[0] (neither addressable nor a map index expression)
```

Build a new one instead: `"a" + name[1:]`.

The `strings` package.

```go
	fmt.Println(strings.ToUpper(name), strings.Contains(name, "jal"))
	fmt.Println(strings.Index(name, "j"), strings.Index(name, "z"))
	parts := strings.Split("an ja li", " ")
	fmt.Println(parts, strings.Join(parts, "-"))
```

```
ANJALI true
2 -1
[an ja li] an-ja-li
```

Every text tool is a function in `strings` that takes the string as its first argument, rather than a method on the string as in Python. `Index` gives the byte position, or `-1`. `Split` gives a slice of pieces, printed in square brackets; `Join` puts them back with a separator.

Formatting with `Sprintf`.

```go
	age := 9
	price := 50.0
	line := fmt.Sprintf("%s is %d. The cake costs %.2f rupees.", name, age, price)
	fmt.Println(line)
	fmt.Printf("%10s|%-10s|\n", name, name)
```

```
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
```

`%s` string, `%d` whole number, `%.2f` decimal with two places, `%10s` right-aligned in ten, `%-10s` left-aligned. The order of the values after the template must match the order of the holes.

Here is the run and output for the complete program.

```bash
go run text.go
```

```
Anjali: 6 bytes, 6 runes
अंजलि: 15 bytes, 5 runes
first byte 65 = A, slice Anj, hindi first byte 224
byte  0: अ (code point 2309)
byte  3: ं (code point 2306)
byte  6: ज (code point 2332)
byte  9: ल (code point 2354)
byte 12: ि (code point 2367)
third rune: ज
new name: anjali (the original is still Anjali)
ANJALI true 2 -1
[an ja li] an-ja-li
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
```

And the complete file.

```go
// text.go — day 3, bytes, runes, and Sprintf
// Run:  go run text.go
package main

import (
	"fmt"
	"strings"
	"unicode/utf8"
)

func main() {
	name := "Anjali"
	hindi := "अंजलि"

	fmt.Printf("%s: %d bytes, %d runes\n", name, len(name), utf8.RuneCountInString(name))
	fmt.Printf("%s: %d bytes, %d runes\n", hindi, len(hindi), utf8.RuneCountInString(hindi))

	fmt.Printf("first byte %d = %s, slice %s, hindi first byte %d\n",
		name[0], string(name[0]), name[0:3], hindi[0])

	for i, r := range hindi {
		fmt.Printf("byte %2d: %c (code point %d)\n", i, r, r)
	}

	runes := []rune(hindi)
	fmt.Println("third rune:", string(runes[2]))

	newName := "a" + name[1:]
	fmt.Printf("new name: %s (the original is still %s)\n", newName, name)

	fmt.Println(strings.ToUpper(name), strings.Contains(name, "jal"),
		strings.Index(name, "j"), strings.Index(name, "z"))

	parts := strings.Split("an ja li", " ")
	fmt.Println(parts, strings.Join(parts, "-"))

	age := 9
	price := 50.0
	line := fmt.Sprintf("%s is %d. The cake costs %.2f rupees.", name, age, price)
	fmt.Println(line)
	fmt.Printf("%10s|%-10s|\n", name, name)
}
```

## 6. How the other two languages do it

Python, where `len` counts characters and you have to ask for bytes:

```python
hindi = "अंजलि"
print(len(hindi))                  # 5
print(len(hindi.encode("utf-8")))  # 15
print(hindi[2])                    # ज, by character
```

C++, where `.size()` counts bytes like Go, but the string can be changed in place:

```cpp
std::string hindi = "अंजलि";
std::cout << hindi.size() << "\n";   // 15
std::string name = "Anjali";
name[0] = 'a';                        // compiles; name is now "anjali"
```

The one line of difference that matters: **Go and C++ index bytes; Python indexes characters.** `hindi[2]` is `ज` in Python and the last byte of `अ` in Go and C++. Go is the only one of the three with a built-in name for a character, `rune`, and a built-in way to walk them, `for range`. Python does not need one because its strings are already characters. C++ gives you neither, and you count code points yourself. And on mutability, Go sides with Python: a string is fixed, and C++ is the odd one out.

## 7. The traps

**The near-miss: `string()` on a byte.** You want the first character of the Hindi word.

```go
	fmt.Println(string(hindi[0]))
```

```
à
```

No error. `hindi[0]` is the byte 224, and `string(224)` is the character whose code point is 224, which is `à`. Go turned a fragment of one character into a completely different character without a word of complaint. Use `[]rune(hindi)[0]` or `for range`.

**The real error: text plus a number.** This looks like it builds a sentence.

```go
	age := 9
	fmt.Println("Anjali is " + age)
```

```
./text.go:14:14: invalid operation: "Anjali is " + age (mismatched types untyped string and int)
```

Go will not convert for you. Use `fmt.Sprintf("Anjali is %d", age)`, or `strconv.Itoa(age)` to turn the number into text first. Note this is a compile error, where Python gave you the same complaint at run time.

**The near-miss: slicing through the middle of a character.** Take the "first two characters" of the Hindi word by byte.

```go
	fmt.Println(hindi[0:2])
```

```
��
```

Two bytes of a three-byte character, printed as two replacement marks because no terminal can draw half a letter. Nothing stopped you. Any time you slice a string that might hold non-English text, slice `[]rune(s)` and convert back.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a byte and a rune in Go?"
- "Why does `len("अंजलि")` return 15?"
- "What does `for i, r := range s` actually give you?"

**What to say out loud, the first ninety seconds**

"A Go string is an immutable sequence of bytes, conventionally UTF-8. `len` returns the byte count, so for ASCII it matches the character count and for anything else it does not: a Devanagari letter is three bytes, so `"अंजलि"` has `len` 15 but only 5 characters. Go's word for a character is rune, which is a Unicode code point stored as an `int32`. `utf8.RuneCountInString` gives the rune count, and `for range` over a string decodes runes one at a time, giving the byte offset where each starts and the rune itself. That is why the indices from `range` jump by three.

Indexing with `s[i]` gives a byte, not a character, and slicing is by byte too, so slicing non-ASCII text at an arbitrary position can split a character. When I need character positions, I convert to `[]rune`, work with that, and convert back. Strings are immutable, so building large ones goes through `strings.Builder`, and formatting goes through `fmt.Sprintf` with `%s`, `%d`, `%.2f` and friends."

**The follow-ups**

1. *"Why did Go choose bytes rather than characters for strings?"* — Because most of what a server does with a string is copy it, hash it, or write it to a network or a file, and all of those want bytes. Decoding to characters is the rare case, so it is explicit.
2. *"What is `strings.Builder` for?"* — Building a string from many pieces without copying the whole thing each time. Repeated `+=` allocates a new string every time; `Builder` grows a buffer and produces the string once at the end.
3. *"What does `%q` print?"* — The string in double quotes with special characters escaped, useful in logs so that an empty string or trailing spaces are visible.

**A model answer**

"Go strings are immutable byte sequences; `len` is bytes, and UTF-8 means a non-ASCII character occupies two to four of them, so `len("अंजलि")` is 15 while `utf8.RuneCountInString` is 5. A rune is an `int32` code point. `for i, r := range s` decodes runes, yielding each rune's starting byte offset, so the indices are 0, 3, 6 for three-byte characters. `s[i]` and `s[a:b]` are byte operations, which is fast and correct for ASCII and dangerous for anything else; for character positions I use `[]rune(s)`. Formatting is `fmt.Sprintf` with verbs, concatenation with a non-string is a compile error, and bulk construction uses `strings.Builder`."

## 9. Recall card

- A string is immutable bytes; `len(s)` is bytes, `utf8.RuneCountInString(s)` is characters; `"अंजलि"` is 15 and 5.
- A rune is one code point, an `int32`; `for i, r := range s` gives each rune and the byte offset where it starts.
- `s[i]` is a byte and `s[a:b]` slices bytes; for character positions use `[]rune(s)` and convert back with `string(...)`.
- `string(s[0])` on a multi-byte character silently produces a different character; `s[0:2]` prints half a letter.
- `fmt.Sprintf("%s is %d, %.2f", ...)` formats; `"text" + 9` is a compile error; `strings.ToUpper`, `Contains`, `Index`, `Split`, `Join`.
