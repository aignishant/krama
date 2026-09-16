---
day: 3
track: lang-cpp
title: "std::string, string literals, and std::format"
theme: "Strings and text"
phase: "Languages: every language, every basic"
status: written
---

# Day 003 · C++ — std::string, string literals, and std::format

**Today's theme:** Strings and text

**After today you can:** You can build, slice, search and format text in each language, and say why a Hindi word has a different length in each.

**The interviewer asks it as:** *Why does the length of a string not always equal the number of characters?*

---

## 1. What this is, and why it matters

C++ has two kinds of text: the quoted literal `"Anjali"`, which is a fixed row of bytes left over from C, and `std::string`, which is a growable, changeable sequence of bytes and the one you actually use. `.size()` counts bytes, there is no built-in notion of a character beyond a byte, and, unlike Python and Go, a `std::string` can be edited in place. Formatting arrived properly in C++20 as `std::format`, and it looks a great deal like Python's f-string.

At work, the literal-versus-`std::string` split is the source of a whole family of C++ bugs where adding a number to text compiles and quietly does the wrong thing. Interviewers ask "what is the difference between a string literal and `std::string`", "is `std::string` mutable", and "what does `find` return when it fails", and the last one has an answer that has bitten every C++ programmer alive.

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

Text is stored as **bytes**, eight on-or-off switches each, using **UTF-8**, where an English letter is one byte and a Hindi letter is three. Every language today agrees on that storage. They differ in what they let you count.

C++ has two kinds of text. The first is the **string literal**, anything in double quotes in your source: `"Anjali"`. It is a fixed row of bytes with an invisible zero byte at the end to mark where it stops, and it cannot grow or change. It is inherited from C, the language C++ grew out of, and it is what you get if you write quotes and nothing else. The second is **`std::string`**, from the header `<string>`, which is a proper text object: it knows its own length, it can grow, and it can be changed. Almost always, you want `std::string`, and you make one by writing `std::string name = "Anjali";`. The literal on the right is copied into the string on the left.

`.size()` counts bytes. `"Anjali"` is 6. `"अंजलि"` is 15. C++ is the old woman with the stencil kit, like Go. Unlike Go, C++ has no built-in name for a character beyond a single byte, and no built-in way to count the baker's five. You count them yourself, and today you will.

Indexing, `name[0]`, gives one byte, of type `char`. Slicing is `name.substr(start, count)`: `name.substr(0, 3)` is `"Anj"`. Searching is `name.find("j")`, which returns the position, or, when not found, a special huge value called `std::string::npos`. Not `-1`. This matters and is in the traps.

A `std::string` is **mutable**. `name[0] = 'a';` compiles and changes the string in place. Python and Go both refuse this. It makes some things fast and it means that when you hand a string to another part of the program, that part can alter it, which is a topic for day 12.

`std::format`, in the header `<format>`, is C++'s f-string: `std::format("{} is {}", name, age)` fills the braces in order, and `{:.2f}` formats a decimal with two places. It needs a compiler from 2023 or later, which is why day 1 asked for version 13.

## 4. The picture

```
 string literal "Anjali"       fixed, ends in a hidden zero byte
   ┌────┬────┬────┬────┬────┬────┬────┐
   │ A  │ n  │ j  │ a  │ l  │ i  │ \0 │
   └────┴────┴────┴────┴────┴────┴────┘

 std::string name = "Anjali"   knows its size, can grow, can change
   size = 6
   ┌────┬────┬────┬────┬────┬────┐
   │ A  │ n  │ j  │ a  │ l  │ i  │       name[0] = 'a'  →  "anjali"
   └────┴────┴────┴────┴────┴────┘

 std::string hindi = "अंजलि"    size = 15 bytes, 5 code points, you count them
   ┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐┌──┬──┬──┐
   │E0│A4│85││E0│A4│82││E0│A4│9C││E0│A4│B2││E0│A4│BF│
   └──┴──┴──┘└──┴──┴──┘└──┴──┴──┘└──┴──┴──┘└──┴──┴──┘
     ▲ start   ▲ start   ▲ start   ▲ start   ▲ start
```

*Notice the marked start bytes. In UTF-8, every byte that begins a character is below 128 or at least 192, and every byte in the middle of one is between 128 and 191. Counting the start bytes is counting characters, and that is the whole trick in section 5.*

## 5. The code, built step by step

Start `text.cpp` in a `day03` folder.

```cpp
#include <format>
#include <iostream>
#include <string>

int main() {
    std::string name = "Anjali";
    std::string hindi = "अंजलि";
    std::cout << name.size() << " " << hindi.size() << "\n";
}
```

```
6 15
```

`<string>` for `std::string`, `<format>` for `std::format`, `<iostream>` for printing. Bytes, as promised.

Index and slice.

```cpp
    std::cout << name[0] << " " << name.substr(0, 3) << " " << name.substr(3) << "\n";
    std::cout << static_cast<int>(static_cast<unsigned char>(hindi[0])) << "\n";
    std::cout << hindi.substr(0, 3) << "\n";
```

```
A Anj ali
224
अ
```

`substr(3)` with one argument means "from 3 to the end". The second line is ugly on purpose: `hindi[0]` is a `char`, which on most machines is signed and would print as `-32`; `static_cast<unsigned char>` reads it as the byte value 0 to 255, and `static_cast<int>` makes `cout` print a number rather than a character. `static_cast<T>(x)` is C++'s way of saying "treat `x` as a `T`", and you will write it often. `substr(0, 3)` happens to be the three bytes of `अ`, so it prints properly.

Now count the baker's five, by hand.

```cpp
    int code_points = 0;
    for (char c : hindi) {
        unsigned char b = c;
        if (b < 128 || b >= 192) {
            code_points = code_points + 1;
        }
    }
    std::cout << code_points << "\n";
```

```
5
```

`for (char c : hindi)` runs the lines inside once per byte; you meet loops properly tomorrow, so read it today as "for each byte". A byte that starts a character is below 128 or at least 192, and a byte in the middle of one is 128 to 191. Counting the starters counts characters. Go gave you this as `utf8.RuneCountInString`. C++ gives you nothing, and this is what nothing looks like.

Mutability.

```cpp
    name[0] = 'a';
    std::cout << name << "\n";
    name[0] = 'A';
```

```
anjali
```

It compiles and the string changes in place. Python and Go refuse the equivalent line. The third line puts it back.

Find, and what it returns.

```cpp
    std::cout << name.find("j") << " " << name.find("z") << "\n";
    std::cout << (name.find("z") == std::string::npos) << "\n";
```

```
2 18446744073709551615
1
```

Found at 2. Not found gives `std::string::npos`, which is the largest value the size type can hold, not `-1`. You always compare the result with `npos`, never with `-1` and never with `> 0`. The `1` on the second line is `true`; `cout` prints booleans as numbers unless you ask with `std::boolalpha`.

Concatenation and `std::format`.

```cpp
    std::string new_name = "a" + name.substr(1);
    int age = 9;
    double price = 50;
    std::cout << std::format("{} is {}. The cake costs {:.2f} rupees.", name, age, price) << "\n";
    std::cout << std::format("{:>10}|{:<10}|", name, name) << "\n";
```

```
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
```

`"a" + name.substr(1)` works because one side is a `std::string`; `+` between two literals does not, and that is in the traps. `std::format` fills `{}` in order; after a colon comes the format spec, exactly as in Python: `.2f`, `>10`, `<10`.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra text.cpp -o text
./text
```

```
Anjali: 6 bytes
अंजलि: 15 bytes, 5 code points
first: A slice: Anj first byte of hindi: 224
mutated: anjali, restored: Anjali
find j: 2, find z is npos: true
new name: anjali (the original is still Anjali)
Anjali is 9. The cake costs 50.00 rupees.
    Anjali|Anjali    |
```

And the complete file.

```cpp
// text.cpp — day 3, std::string, literals, and std::format
// Build: g++ -std=c++20 -Wall -Wextra text.cpp -o text
// Run:   ./text
#include <format>
#include <iostream>
#include <string>

int main() {
    std::string name = "Anjali";
    std::string hindi = "अंजलि";

    int code_points = 0;
    for (char c : hindi) {
        unsigned char b = c;
        if (b < 128 || b >= 192) {
            code_points = code_points + 1;
        }
    }
    std::cout << std::format("{}: {} bytes\n", name, name.size());
    std::cout << std::format("{}: {} bytes, {} code points\n", hindi, hindi.size(), code_points);

    int first_byte = static_cast<unsigned char>(hindi[0]);
    std::cout << std::format("first: {} slice: {} first byte of hindi: {}\n",
                             name[0], name.substr(0, 3), first_byte);

    name[0] = 'a';
    std::string mutated = name;
    name[0] = 'A';
    std::cout << std::format("mutated: {}, restored: {}\n", mutated, name);

    bool missing = name.find("z") == std::string::npos;
    std::cout << std::format("find j: {}, find z is npos: {}\n", name.find("j"), missing);

    std::string new_name = "a" + name.substr(1);
    std::cout << std::format("new name: {} (the original is still {})\n", new_name, name);

    int age = 9;
    double price = 50;
    std::cout << std::format("{} is {}. The cake costs {:.2f} rupees.\n", name, age, price);
    std::cout << std::format("{:>10}|{:<10}|\n", name, name);
    return 0;
}
```

Notice `std::format` prints `bool` as `true` and `false` without being asked, unlike `std::cout`. Notice also `std::string mutated = name;` makes a full copy, so changing `name` afterwards does not touch `mutated`. That copy-on-assignment is the C++ default for everything, and day 12 is about it.

## 6. How the other two languages do it

Python, where `len` counts characters and nothing can be changed in place:

```python
name = "Anjali"
hindi = "अंजलि"
print(len(hindi))                 # 5
name[0] = "a"                     # TypeError
print(name.find("z"))             # -1
```

Go, where `len` counts bytes like C++ but a character has a name:

```go
hindi := "अंजलि"
fmt.Println(len(hindi))                     // 15
fmt.Println(utf8.RuneCountInString(hindi))  // 5
fmt.Println(strings.Index(name, "z"))       // -1
```

The one line of difference that matters: **C++ strings are mutable and the other two are not, and C++ `find` returns `npos` where the other two return `-1`.** The first means a C++ function handed a string can change the caller's copy of it, which neither Python nor Go allows. The second means the idiom `if (s.find(x) > 0)` or `!= -1`, correct in Python and Go, is a bug in C++: `npos` is the largest possible unsigned value, so it is greater than zero, and comparing it with `-1` only works by an accident of conversion you should not rely on. Compare with `std::string::npos` and nothing else.

## 7. The traps

**The near-miss: a literal plus a number.** This compiles without a single warning.

```cpp
    int age = 9;
    std::cout << "Anjali is " << "\n";
    std::cout << "Anjali is " + age << "\n";
```

```
Anjali is
 
```

The second line printed a single space. `"Anjali is "` is a row of ten bytes, and `+ 9` does not append the number; it moves the starting point nine bytes along the row, to the final space. If `age` had been 20, you would be reading bytes past the end of the literal, which is undefined behaviour. Python and Go both refuse this line. C++ accepts it because a literal is a C-style pointer to bytes and adding to a pointer is arithmetic. The fix is `std::format("Anjali is {}", age)` or `"Anjali is " + std::to_string(age)`.

**The real error: two literals with a plus.** This looks like Python.

```cpp
    std::string greeting = "Hello, " + "Anjali";
```

```
text.cpp: In function 'int main()':
text.cpp:6:39: error: invalid operands of types 'const char [8]' and 'const char [7]' to binary 'operator+'
    6 |     std::string greeting = "Hello, " + "Anjali";
      |                            ~~~~~~~~~ ^ ~~~~~~~~
      |                            |           |
      |                            |           const char [7]
      |                            const char [8]
```

Two literals cannot be added, because neither is a `std::string`. Make one of them a string: `std::string("Hello, ") + "Anjali"`, or write `"Hello, " "Anjali"` with no plus at all, which the compiler joins for you.

**The near-miss: `find` compared with zero.** You want to know whether the name contains a `z`.

```cpp
    if (name.find("z") > 0) {
        std::cout << "found z\n";
    }
```

```
found z
```

There is no `z`. `find` returned `npos`, which is 18 446 744 073 709 551 615, which is greater than zero. Always `!= std::string::npos`. This one is famous enough that interviewers ask it directly.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a string literal and a `std::string`?"
- "What does `std::string::find` return when it does not find anything?"
- "Is `std::string` mutable, and does `size()` return characters or bytes?"

**What to say out loud, the first ninety seconds**

"C++ has two kinds of text. A string literal, `"Anjali"` in quotes, is a fixed array of bytes with a terminating zero, inherited from C; it cannot grow or change, and arithmetic on it is pointer arithmetic, which is why `"text" + 9` compiles and does something silent and wrong. `std::string` is the real string type: it owns its bytes, knows its size, grows on demand, and is mutable, so `s[0] = 'a'` changes it in place, unlike Python or Go.

`size()` returns bytes. A Devanagari letter is three bytes in UTF-8, so `"अंजलि"` has size 15 and five code points, and C++ gives no built-in way to count the five; I count lead bytes or use a library. `find` returns a position, or `std::string::npos`, which is the maximum value of the size type, not minus one; the only correct check is `!= npos`. For formatting I use C++20's `std::format`, which works like Python's f-string with `{}` placeholders and specs like `{:.2f}`."

**The follow-ups**

1. *"Why does `"a" + "b"` not compile but `std::string("a") + "b"` does?"* — `+` on two literals is an attempt to add two pointers, which is meaningless; once one side is a `std::string`, the overloaded `operator+` for strings is chosen.
2. *"Is `std::string` UTF-8 aware?"* — No. It is a container of bytes. It stores UTF-8 happily but every operation is byte-based, so `substr` can cut a character in half and `size()` is not a character count.
3. *"What is `std::string_view`?"* — A non-owning view of a range of characters, cheap to pass around, used to avoid copying when a function only needs to read a string. It arrives on day 12.

**A model answer**

"A string literal is a `const char` array with a null terminator; `std::string` is an owning, growable, mutable byte container from `<string>`. `size()` counts bytes, so non-ASCII text reports more than its character count, and the standard library offers no code-point count. `find` returns `std::string::npos` on failure, the maximum `size_t`, so `> 0` and `== -1` are both wrong; compare with `npos`. Because literals are pointers, `"text" + 9` compiles as pointer arithmetic; I format with `std::format` or convert with `std::to_string`. And because `std::string` is mutable and copies on assignment, a function receiving one by value gets its own copy, which is the topic of value semantics later in the course."

## 9. Recall card

- `"Anjali"` is a fixed C-style byte array; `std::string name = "Anjali";` is the real, growable, mutable string.
- `.size()` is bytes: `"अंजलि"` is 15; count characters yourself by counting bytes below 128 or at least 192.
- `find` returns `std::string::npos` on failure, never `-1`; `> 0` is a bug that prints "found".
- `"text" + 9` compiles and moves the pointer; `"a" + "b"` does not compile; use `std::format("{} {}", a, b)` or `std::to_string`.
- `std::format("{:.2f}", price)` and `"{:>10}"` work like Python; needs `<format>` and a 2023-or-later compiler.
