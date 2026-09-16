---
day: 2
track: lang-python
title: "Dynamic names, int without limits, float with them"
theme: "Variables, types, and numbers"
phase: "Languages: every language, every basic"
status: written
---

# Day 002 · Python — Dynamic names, int without limits, float with them

**Today's theme:** Variables, types, and numbers

**After today you can:** You can declare a number in each language, say how wide it is, and predict what 2 000 000 000 + 2 000 000 000 prints.

**The interviewer asks it as:** *What is the difference between a statically and a dynamically typed language?*

---

## 1. What this is, and why it matters

A variable is a name you attach to a value so you can use it again later. In Python the name carries no type of its own: it can point at a whole number now and at a piece of text a line later, and the interpreter only checks what a value is when it actually uses it. Python's whole numbers have no upper limit, and its decimal numbers are stored in a fixed 64 bits and are therefore slightly wrong in ways that surprise everyone once.

At work this is the day you learn why `0.1 + 0.2` is not `0.3`, and why that matters for money. In interviews, "what is the difference between static and dynamic typing" is a standard opener, and "why does Python let you add a number to a string only at run time" is its follow-up.

## 2. The story

Ravi's uncle has run the gate at the neighbourhood temple for eleven years, and every festival evening he counts the people coming in. He does it with a small metal clicker in his left hand. Press the button, the number goes up by one. It has four little wheels, so it shows numbers from 0000 up to 9999.

Last Diwali the crowd was bigger than anyone expected. At around eight in the evening, Ravi's uncle looked down and the clicker read 0213. He was sure he had clicked more than ten thousand times. He had. The wheels had gone all the way round to 9999, and the next press had turned every wheel at once, back to 0000. The counter did not complain. It did not stop. It just kept going from zero as if nothing had happened, and the first ten thousand people were gone.

Ravi, who is fourteen, was helping at the other gate. He had no clicker. He counted in his head, in groups of ten, and every hundred he said the running total out loud so his cousin could save it in her phone. His count that evening reached fourteen thousand six hundred and something. He could have gone to a million if the night had been long enough. There is no highest number in your head.

But Ravi was slower. Each person cost him a moment of attention. The clicker never had to think.

That night, the two of them compared. The clicker was fast and had a ceiling, and when it hit the ceiling it lied quietly. Ravi's head was slower and had no ceiling at all.

His uncle also keeps a jar of coins for the parking. At the end of the night, he splits the coins between the three helpers. Twenty coins, three people. Six each, two left over. He never pretends it is six and two-thirds each. Coins do not split.

## 3. The idea in plain English

A **variable** is a name attached to a value. In Python you make one by writing the name, an equals sign, and the value: `count = 213`. From then on, `count` means 213 until you attach it to something else.

A **type** is what kind of thing a value is. `213` is an **int**, a whole number. `3.5` is a **float**, a number with a decimal point. `"Ravi"` is a **str**, a piece of text. Every value in Python has a type, and you can ask with `type(count)`.

In Python, the **name** has no type. Only the value does. You can write `count = 213` and then `count = "two hundred"` and nothing objects. This is called **dynamic typing**: the type is checked when the value is used, not when the name is created. Go and C++ do the opposite, and you will see that in section 6.

Python's ints are Ravi's head. They have no ceiling. `2_000_000_000 + 2_000_000_000` is `4000000000`, and `2 ** 100` is a thirty-one digit number, and Python is fine with both. It grows the number as needed. The underscores in `2_000_000_000` are allowed purely so humans can read the digits; Python ignores them.

Python's floats are the clicker. A float is stored in exactly **64 bits**, a bit being a single on-or-off switch, and 64 of them can hold a great many numbers but not all of them. `0.1` is one of the ones it cannot hold exactly, in the same way that one-third cannot be written exactly as a decimal. So `0.1 + 0.2` comes out as `0.30000000000000004`. That is not a bug in Python. Every language with 64-bit floats does it, and today you will see Go and C++ do it too.

And the coins: `20 // 3` is `6`, whole-number division, with `20 % 3` being the `2` left over. Plain `20 / 3` always gives a float, `6.666666666666667`, even when it would divide evenly.

## 4. The picture

```
 Python int: grows as needed          Python float: always 64 bits
 ───────────────────────────          ────────────────────────────
 213          [ 213 ]                 0.1  →  [0.1000000000000000055511151231257827…]
 4000000000   [ 4000000000 ]                   ▲ stored as the nearest 64-bit value
 2**100       [ 1267650600228229401496703205376 ]
              no ceiling              0.1 + 0.2  →  0.30000000000000004
```

*Notice that the int box stretches to fit and the float box does not. The float is not wrong by much, about one part in ten million billion, but it is wrong, and two small wrongs added together become a visible one.*

## 5. The code, built step by step

Start a new file, `numbers.py`, in a `day02` folder. First, names and values.

```python
count = 213
print(count)
count = count + 1
print(count)
```

The first line attaches the name `count` to `213`. The third line reads the current value, adds one, and attaches the name to the new value `214`. The `=` is not a claim that the two sides are equal; it is an instruction: "make the left name mean the right value from now on".

```python
print(type(count))
count = "two hundred and fourteen"
print(type(count))
```

```
<class 'int'>
<class 'str'>
```

The same name, two types, no complaint. That is dynamic typing in two lines. It is convenient, and it is also how a number silently becomes text in a large program and nobody finds out until much later.

Now the ceiling that is not there.

```python
big = 2_000_000_000 + 2_000_000_000
print(big)
print(2 ** 100)
```

```
4000000000
1267650600228229401496703205376
```

Keep `4000000000` in mind. You will see what Go and C++ print for the same sum later today, and it is not this.

Now the ceiling that is there.

```python
print(0.1 + 0.2)
print(0.1 + 0.2 == 0.3)
```

```
0.30000000000000004
False
```

The second line is the one that costs people money. Never compare floats with `==`. If you need to know whether two floats are close, decide how close is close enough and check the difference: `abs(a - b) < 0.000001`. If you are handling money, do not use floats at all; count in whole paise or cents as ints.

And the coins.

```python
print(20 / 3)
print(20 // 3)
print(20 % 3)
print(6 / 3)
```

```
6.666666666666667
6
2
2.0
```

`/` always produces a float, even for `6 / 3`. `//` is whole-number division, rounding down. `%` is the remainder. Read `%` as "what is left over".

Here is the run and output for the complete program.

```bash
python3 numbers.py
```

```
count is 214 and its type is <class 'int'>
now count is a <class 'str'>
2 000 000 000 + 2 000 000 000 = 4000000000
2 to the 100 = 1267650600228229401496703205376
0.1 + 0.2 = 0.30000000000000004
is 0.1 + 0.2 == 0.3? False
20 / 3 = 6.666666666666667
20 // 3 = 6, remainder 2
```

And the complete file. `f"..."` is an **f-string**: text with `{}` holes that Python fills in with the value of whatever is inside the braces. You will learn it properly tomorrow; today just read it as "print this with the values filled in".

```python
# numbers.py — day 2, names, ints, and floats
# Run:  python3 numbers.py

count = 213
count = count + 1
print(f"count is {count} and its type is {type(count)}")

count = "two hundred and fourteen"
print(f"now count is a {type(count)}")

big = 2_000_000_000 + 2_000_000_000
print(f"2 000 000 000 + 2 000 000 000 = {big}")
print(f"2 to the 100 = {2 ** 100}")

print(f"0.1 + 0.2 = {0.1 + 0.2}")
print(f"is 0.1 + 0.2 == 0.3? {0.1 + 0.2 == 0.3}")

print(f"20 / 3 = {20 / 3}")
print(f"20 // 3 = {20 // 3}, remainder {20 % 3}")
```

## 6. How the other two languages do it

The same sum in Go:

```go
package main

import "fmt"

func main() {
	var a int32 = 2_000_000_000
	var b int32 = 2_000_000_000
	fmt.Println(a + b)
}
```

```
-294967296
```

And in C++:

```cpp
#include <cstdint>
#include <iostream>

int main() {
    std::int32_t a = 2'000'000'000;
    std::int32_t b = 2'000'000'000;
    std::cout << a + b << "\n";
}
```

```
-294967296
```

The one line of difference that matters: **in Go and C++ you choose how many bits a whole number gets, and when it does not fit, the clicker rolls over.** A 32-bit signed integer tops out at 2 147 483 647. Add past that and the wheels turn back round, into negative numbers. Python's int has no wheels; it grows. Go and C++ also make you declare the type on the name itself, `int32`, and refuse to attach a string to it later. That is **static typing**: the name has a type, fixed when it is created, checked before the program runs.

The bite for a Python programmer moving over: you have never once thought about how big a number might get. In the other two, that is the first question.

## 7. The traps

**The near-miss: text that looks like a number.** Input from a person always arrives as text. This looks like it adds 5 and 3.

```python
age = "5"
print(age + 3)
```

```
Traceback (most recent call last):
  File "/home/you/day02/numbers.py", line 2, in <module>
    print(age + 3)
          ~~~~^~~
TypeError: can only concatenate str (not "int") to str
```

Python does not guess. `"5"` is text, `3` is a number, and it will not add them. The fix is `int(age) + 3`. And notice when this error appears: at run time, on that line, not before. In Go and C++ it would not have compiled.

**The near-miss: float equality.** This looks like it should print `equal`.

```python
total = 0.1 + 0.1 + 0.1
if total == 0.3:
    print("equal")
else:
    print(f"not equal: {total}")
```

```
not equal: 0.30000000000000004
```

No error, no warning, just the wrong branch. Compare with a tolerance, or use ints.

**The real error: a name before its value.** Using a name that has not been given a value yet.

```python
print(total)
total = 10
```

```
Traceback (most recent call last):
  File "/home/you/day02/numbers.py", line 1, in <module>
    print(total)
          ^^^^^
NameError: name 'total' is not defined
```

The name only exists from the line that first assigns it. Python reads top to bottom; on line 1, `total` does not exist yet.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a statically and a dynamically typed language?"
- "Why is `0.1 + 0.2` not `0.3`, and what do you do about it?"
- "What is the largest int in Python?"

**What to say out loud, the first ninety seconds**

"In a dynamically typed language like Python, the type belongs to the value, not to the name. I can attach the name `x` to an integer and then to a string, and nothing checks that until a line actually tries to use `x` as a number. In a statically typed language like Go or C++, the name has a type fixed when it is declared, and the compiler refuses the program if I ever try to put the wrong kind of value in it. So Python finds type mistakes at run time, on the line where they happen; Go and C++ find them before the program exists.

For numbers specifically: Python's int has no upper limit, it grows as needed, so two billion plus two billion is four billion. Its float is a 64-bit IEEE value, the same as Go's `float64` and C++'s `double`, and some decimals like 0.1 cannot be stored exactly in 64 bits, so `0.1 + 0.2` is `0.30000000000000004`. I never compare floats with `==`, and for money I count in whole paise as integers."

**The follow-ups**

1. *"Is dynamic typing slower?"* — Usually, yes. Every operation has to check the type of its operands at run time. That is part of why Python is slower than Go or C++ on number-heavy work.
2. *"What does Python do when an int gets huge?"* — It switches to a representation that uses as many digits as needed. It is slower than a fixed 64-bit number but it never overflows.
3. *"How would you compare two floats?"* — Check that their difference is smaller than a tolerance I choose for the problem, or avoid floats: use `decimal.Decimal` for money, or integers in the smallest unit.

**A model answer**

"Static typing means each name has a type fixed at declaration and checked by the compiler; dynamic typing means only values have types and the check happens when a value is used. Python is dynamic, so `x = 5` then `x = 'five'` is legal, and `'5' + 3` is a `TypeError` at run time rather than a compile error. Python's `int` is arbitrary-precision, so it cannot overflow; its `float` is a 64-bit IEEE double, which is why `0.1 + 0.2 == 0.3` is `False`. The practical rules are: convert text to numbers explicitly, never compare floats for equality, and keep money in integers."

## 9. Recall card

- `name = value` attaches a name to a value; the name has no type, the value does, and `type(x)` tells you which.
- Python `int` has no ceiling: `2_000_000_000 + 2_000_000_000` is `4000000000`. Go and C++ 32-bit ints print `-294967296`.
- `float` is 64 bits; `0.1 + 0.2` is `0.30000000000000004`; never `==` two floats; money goes in ints.
- `/` always gives a float, `//` is whole-number division, `%` is the remainder.
- `"5" + 3` is a `TypeError` at run time; convert with `int("5")` first.
