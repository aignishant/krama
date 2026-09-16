---
day: 2
track: lang-cpp
title: "Fixed-width ints, overflow, and auto"
theme: "Variables, types, and numbers"
phase: "Languages: every language, every basic"
status: written
---

# Day 002 · C++ — Fixed-width ints, overflow, and auto

**Today's theme:** Variables, types, and numbers

**After today you can:** You can declare a number in each language, say how wide it is, and predict what 2 000 000 000 + 2 000 000 000 prints.

**The interviewer asks it as:** *What is the difference between a statically and a dynamically typed language?*

---

## 1. What this is, and why it matters

In C++ every variable has a type fixed when it is declared, whole numbers have a width in bits you should choose on purpose, and when a signed whole number is pushed past its top, the language makes **no promise at all** about what happens. Today you meet `int`, the fixed-width types from `<cstdint>`, the keyword `auto`, and the phrase you will hear in every C++ interview: undefined behaviour.

At work, most C++ bugs that make the news are about a number or a size that was one bit wider than the type holding it. Interviewers ask "what is `int32_t` and why not just `int`", "what does signed overflow do in C++", and "what does `auto` deduce here". Today gives you all three.

## 2. The story

Ravi's uncle has run the gate at the neighbourhood temple for eleven years, and every festival evening he counts the people coming in. He does it with a small metal clicker in his left hand. Press the button, the number goes up by one. It has four little wheels, so it shows numbers from 0000 up to 9999.

Last Diwali the crowd was bigger than anyone expected. At around eight in the evening, Ravi's uncle looked down and the clicker read 0213. He was sure he had clicked more than ten thousand times. He had. The wheels had gone all the way round to 9999, and the next press had turned every wheel at once, back to 0000. The counter did not complain. It did not stop. It just kept going from zero as if nothing had happened, and the first ten thousand people were gone.

Ravi, who is fourteen, was helping at the other gate. He had no clicker. He counted in his head, in groups of ten, and every hundred he said the running total out loud so his cousin could save it in her phone. His count that evening reached fourteen thousand six hundred and something. He could have gone to a million if the night had been long enough. There is no highest number in your head.

But Ravi was slower. Each person cost him a moment of attention. The clicker never had to think.

That night, the two of them compared. The clicker was fast and had a ceiling, and when it hit the ceiling it lied quietly. Ravi's head was slower and had no ceiling at all.

There was one more clicker that night, a cheap plastic one the sweet stall had borrowed. Nobody knew what it did past 9999. The stall owner said his old one used to jam. His son said the one before that had skipped straight to 5000. It had never been the same twice. "Do not trust it past the top," the stall owner said. "Past the top, it does whatever it likes."

## 3. The idea in plain English

A **variable** is a name attached to a value. In C++ you declare one with the type first: `int count = 213;`. The **type** says what kind of value the name holds; `int` is a whole number. Once declared, the type never changes. `count = "two hundred";` does not compile. That is **static typing**, and C++ and Go share it.

How wide is `int`? The honest answer is "it depends on the machine", and on every machine you will meet it is 32 **bits**, where a bit is one on-or-off switch. Thirty-two bits with one spent on the sign gives a range of −2 147 483 648 to 2 147 483 647. That is the clicker's 9999.

Because "it depends" is a bad answer when it matters, C++ gives you types whose width is in the name: `std::int8_t`, `std::int16_t`, `std::int32_t`, `std::int64_t`, and unsigned versions `std::uint32_t` and so on. They live in the header `<cstdint>`. When the width matters, you use these and you say the width out loud.

Now the part that makes C++ different. When a **signed** whole number goes past its top, the language says the result is **undefined behaviour**. That does not mean "it wraps". It means the language makes no promise, and the compiler is allowed to assume it never happens. In practice you usually see it wrap, `-294967296`, just as Go does. But you cannot rely on it, and a compiler with optimisation on may delete a check you wrote because "that overflow cannot happen". That is the sweet stall's plastic clicker: past the top, it does whatever it likes.

**Unsigned** whole numbers are different: their overflow is defined to wrap, like Go. `std::uint32_t` at zero, minus one, is 4 294 967 295, every time.

`auto` asks the compiler to work out the type from the value: `auto count = 213;` makes `count` an `int`. It is C++'s version of Go's `:=`, and it has the same trap: the type you get is the type of the value, which for `213` is `int`, 32 bits, whether or not that was what you wanted.

Decimal numbers are `double`, 64 bits, and `0.1 + 0.2` is `0.30000000000000004`, though `std::cout` will hide it from you at first. You will see how in section 5.

## 4. The picture

```
 std::int32_t                                 signed, 32 bits
 ┌───────────────────────────────────────────────────────────┐
 │ -2147483648  ............  0  ............  2147483647     │
 └───────────────────────────────────────────────────────────┘
   2000000000 + 2000000000 = 4000000000  ──►  past the top
                                              language says: no promise
                                              usually prints: -294967296

 std::uint32_t                                unsigned, 32 bits
 ┌───────────────────────────────────────────────────────────┐
 │ 0  ..................................  4294967295           │
 └───────────────────────────────────────────────────────────┘
   0 - 1  ──►  4294967295, defined, every time
```

*Notice that the two boxes hold the same number of values, but the promise is different. Signed past the edge is a promise the language refuses to make. Unsigned past the edge is a wrap it guarantees.*

## 5. The code, built step by step

Start `numbers.cpp` in a `day02` folder.

```cpp
#include <cstdint>
#include <iomanip>
#include <iostream>

int main() {
    int count = 213;
    count = count + 1;
    std::cout << "count is " << count << "\n";
}
```

Three headers. `<iostream>` for printing, `<cstdint>` for the fixed-width types, `<iomanip>` for one printing tool you will need in a moment. `int count = 213;` declares and initialises; `count = count + 1;` reads, adds, stores. Always give a variable a value when you declare it. An `int` declared without one holds whatever was in that spot before, and reading it is another undefined behaviour.

Now the width, said out loud.

```cpp
    std::int32_t a = 2'000'000'000;
    std::int32_t b = 2'000'000'000;
    std::cout << "int32: " << a + b << "\n";
```

```
int32: -294967296
```

The single quotes inside the number are digit separators, purely for reading; the compiler ignores them. The output is the wrap you expected, and it is undefined behaviour that happened to wrap. Do not learn `-294967296` as "the answer". Learn it as "what this compiler did today".

Now the width that fits.

```cpp
    std::int64_t c = 2'000'000'000;
    std::int64_t d = 2'000'000'000;
    std::cout << "int64: " << c + d << "\n";
```

```
int64: 4000000000
```

Now `auto`.

```cpp
    auto e = 2'000'000'000;
    std::cout << "auto gave " << sizeof(e) << " bytes\n";
```

```
auto gave 4 bytes
```

`sizeof` tells you how many **bytes** a value takes, a byte being eight bits. Four bytes is 32 bits. `auto` chose `int` because the literal fits in an `int`, not because you wanted 32 bits. If `e + e` follows, that is the same overflow as `a + b`.

And the float that hides.

```cpp
    double x = 0.1, y = 0.2;
    std::cout << "double: " << x + y << "\n";
    std::cout << std::setprecision(17) << "really: " << x + y << "\n";
    std::cout << std::boolalpha << "equal to 0.3? " << (x + y == 0.3) << "\n";
```

```
double: 0.3
really: 0.30000000000000004
equal to 0.3? false
```

By default `std::cout` prints six significant digits, so the first line looks correct. `std::setprecision(17)` from `<iomanip>` shows all of it. `std::boolalpha` makes `true` and `false` print as words instead of `1` and `0`. The comparison is `false` either way, whether you can see the reason or not.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra numbers.cpp -o numbers
./numbers
```

```
count is 214, 4 bytes wide
int32: -294967296
int64: 4000000000
auto gave 4 bytes
double: 0.3
really: 0.30000000000000004
equal to 0.3? false
20 / 3 = 6 remainder 2
20.0 / 3 = 6.666666666666667
```

And the complete file.

```cpp
// numbers.cpp — day 2, fixed widths, overflow, and auto
// Build: g++ -std=c++20 -Wall -Wextra numbers.cpp -o numbers
// Run:   ./numbers
#include <cstdint>
#include <iomanip>
#include <iostream>

int main() {
    int count = 213;
    count = count + 1;
    std::cout << "count is " << count << ", " << sizeof(count) << " bytes wide\n";

    std::int32_t a = 2'000'000'000;
    std::int32_t b = 2'000'000'000;
    std::cout << "int32: " << a + b << "\n";   // undefined behaviour; usually wraps

    std::int64_t c = 2'000'000'000;
    std::int64_t d = 2'000'000'000;
    std::cout << "int64: " << c + d << "\n";

    auto e = 2'000'000'000;
    std::cout << "auto gave " << sizeof(e) << " bytes\n";

    double x = 0.1, y = 0.2;
    std::cout << "double: " << x + y << "\n";
    std::cout << std::setprecision(17) << "really: " << x + y << "\n";
    std::cout << std::boolalpha << "equal to 0.3? " << (x + y == 0.3) << "\n";

    std::cout << "20 / 3 = " << 20 / 3 << " remainder " << 20 % 3 << "\n";
    std::cout << "20.0 / 3 = " << 20.0 / 3 << "\n";
    return 0;
}
```

The last two lines: `20 / 3` with two ints is whole-number division, `6`, and `%` gives the remainder. `20.0 / 3` involves a double, so the answer is a double. Same rule as Go.

## 6. How the other two languages do it

Python, no width, no overflow, name has no type:

```python
big = 2_000_000_000 + 2_000_000_000
print(big)            # 4000000000
big = "four billion"  # allowed
```

Go, width chosen like C++, but the overflow is a promise:

```go
var a int32 = 2_000_000_000
var b int32 = 2_000_000_000
fmt.Println(a + b)    // -294967296, defined, every machine
```

The one line of difference that matters: **Go promises the wrap; C++ refuses to promise anything for signed types.** Both print `-294967296` today. In Go that is the specified result. In C++ it is a coincidence the optimiser is allowed to break. The consequence at work: in C++ you check for overflow **before** the addition, by testing whether `a > INT32_MAX - b`, never after, because after the overflow the compiler may have already assumed it did not happen. In Go you can check after, `if a+b < a`. Python has nothing to check.

## 7. The traps

**The near-miss: the constant the compiler can see.** Write the overflow with literals instead of variables.

```cpp
    std::cout << 2'000'000'000 + 2'000'000'000 << "\n";
```

```
numbers.cpp: In function 'int main()':
numbers.cpp:6:33: warning: integer overflow in expression of type 'int' results in '-294967296' [-Woverflow]
    6 |     std::cout << 2'000'000'000 + 2'000'000'000 << "\n";
      |                  ~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~
```

A warning, not an error: the program is built and prints `-294967296`. This is why yesterday's `-Wall -Wextra` is not optional. Without those flags, the line above compiles in silence.

**The real error: the missing header.** Use `std::int32_t` without `<cstdint>`.

```
numbers.cpp: In function 'int main()':
numbers.cpp:5:10: error: 'int32_t' is not a member of 'std'
    5 |     std::int32_t a = 2'000'000'000;
      |          ^~~~~~~
numbers.cpp:2:1: note: 'std::int32_t' is defined in header '<cstdint>'; did you forget to '#include <cstdint>'?
```

As yesterday, read to the `note:` line. The compiler names the header.

**The near-miss: the uninitialised variable.** This compiles and runs.

```cpp
    int total;
    std::cout << total << "\n";
```

```
numbers.cpp:6:18: warning: 'total' is used uninitialized [-Wuninitialized]
```

And it prints some number. Maybe `0`. Maybe `32767`. Maybe a different number on the next run. Reading a variable you never gave a value is undefined behaviour, and the warning is the only thing standing between you and a bug that appears once a week. Go would have refused to compile a use of an undeclared name, and gives every declared variable a zero value. C++ gives you the garbage that was there and a warning if you asked for one.

## 8. Say it out loud

**How it gets asked**

- "What does signed integer overflow do in C++?"
- "Why use `int32_t` instead of `int`?"
- "What type does `auto x = 2000000000;` give you?"

**What to say out loud, the first ninety seconds**

"C++ is statically typed: every variable has a type fixed at declaration. `int` is 32 bits on every platform I work on, but the language only guarantees a minimum, so when the width matters I use the fixed-width types from `<cstdint>`, `int32_t`, `int64_t` and their unsigned versions, which say the width in the name.

Signed overflow is undefined behaviour. In practice it usually wraps, so two billion plus two billion in an `int32_t` prints minus 294 967 296, but the standard makes no promise, and the optimiser is allowed to assume it never happens, which means a check written after the addition can be deleted. So I check before: is `a` greater than the maximum minus `b`. Unsigned overflow, by contrast, is defined to wrap. `auto` deduces the type from the initialiser, so `auto x = 2000000000;` is an `int`, not a wide type, and I say the type explicitly whenever the width is the point."

**The follow-ups**

1. *"Why did the C++ designers leave it undefined?"* — Different hardware historically did different things, and leaving it undefined let the compiler generate the fastest code for each machine without inserting checks.
2. *"How do you detect overflow safely?"* — Check before the operation against the type's limits, or use the compiler builtins `__builtin_add_overflow`, which return whether it overflowed without triggering undefined behaviour.
3. *"Why does `std::cout << 0.1 + 0.2` print `0.3`?"* — The stream prints six significant digits by default. The stored value is `0.30000000000000004`; `std::setprecision(17)` shows it.

**A model answer**

"C++ has static types with platform-dependent widths for `int`, so for anything where the width matters I use `std::int32_t` or `std::int64_t` from `<cstdint>`. Signed overflow is undefined behaviour: it commonly wraps, giving `-294967296` for two billion plus two billion in 32 bits, but the compiler may assume it cannot happen and optimise accordingly, so overflow checks must run before the arithmetic. Unsigned overflow is defined modular wrap. `auto` deduces from the initialiser and gives `int` for an integer literal, so it is not a way to get a wide type. `double` is IEEE 64-bit, so `0.1 + 0.2 != 0.3`, and I always compile with `-Wall -Wextra` because both the constant-overflow and the uninitialised-read above are only warnings."

## 9. Recall card

- Type first, then name: `int count = 213;`; the type is fixed; always initialise.
- `int` is 32 bits in practice; say the width with `std::int32_t` and `std::int64_t` from `<cstdint>`.
- Signed overflow is undefined behaviour: usually `-294967296` for two billion plus two billion, never a promise; check before the operation. Unsigned wraps, guaranteed.
- `auto x = 2'000'000'000;` is an `int`; `sizeof(x)` is 4.
- `std::cout` hides `0.30000000000000004` behind six digits; `std::setprecision(17)` shows it, and the `==` is `false` either way.
