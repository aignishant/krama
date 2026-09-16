---
day: 2
track: lang-go
title: "Static types, int64, and := versus var"
theme: "Variables, types, and numbers"
phase: "Languages: every language, every basic"
status: written
---

# Day 002 · Go — Static types, int64, and := versus var

**Today's theme:** Variables, types, and numbers

**After today you can:** You can declare a number in each language, say how wide it is, and predict what 2 000 000 000 + 2 000 000 000 prints.

**The interviewer asks it as:** *What is the difference between a statically and a dynamically typed language?*

---

## 1. What this is, and why it matters

In Go every variable has a type fixed at the moment it is declared, and the compiler refuses the program if you ever put a different kind of value into it. Whole numbers come in fixed widths, `int8` through `int64`, and when a sum does not fit the width, it wraps round silently. Today you learn the two ways to declare a variable, `var` and `:=`, and you watch a 32-bit integer roll over.

At work, Go's insistence on types is the reason large Go codebases can be changed with confidence: rename a field and the compiler lists every place that breaks. Interviewers ask "what is the difference between `var` and `:=`", "how wide is `int`", and "what happens on integer overflow in Go", and the last one has a surprising answer.

## 2. The story

Ravi's uncle has run the gate at the neighbourhood temple for eleven years, and every festival evening he counts the people coming in. He does it with a small metal clicker in his left hand. Press the button, the number goes up by one. It has four little wheels, so it shows numbers from 0000 up to 9999.

Last Diwali the crowd was bigger than anyone expected. At around eight in the evening, Ravi's uncle looked down and the clicker read 0213. He was sure he had clicked more than ten thousand times. He had. The wheels had gone all the way round to 9999, and the next press had turned every wheel at once, back to 0000. The counter did not complain. It did not stop. It just kept going from zero as if nothing had happened, and the first ten thousand people were gone.

Ravi, who is fourteen, was helping at the other gate. He had no clicker. He counted in his head, in groups of ten, and every hundred he said the running total out loud so his cousin could save it in her phone. His count that evening reached fourteen thousand six hundred and something. He could have gone to a million if the night had been long enough. There is no highest number in your head.

But Ravi was slower. Each person cost him a moment of attention. The clicker never had to think.

That night, the two of them compared. The clicker was fast and had a ceiling, and when it hit the ceiling it lied quietly. Ravi's head was slower and had no ceiling at all.

The next morning his uncle went to the shop and asked for a clicker with more wheels. The shopkeeper had one with six. Up to 999 999. "That will do for this temple," his uncle said. "But I am writing on the box how many wheels it has, so nobody forgets."

## 3. The idea in plain English

A **variable** is a name attached to a value. In Go you declare one with `var count int = 213`: the word `var`, the name, the **type**, and the starting value. The type says what kind of thing the variable holds, and here `int` means a whole number.

Once declared, the type is fixed. `count = "two hundred"` is a compile error. This is **static typing**: every name has a type, chosen when the name is created, checked by the compiler before the program runs. It is the uncle writing the number of wheels on the box.

Go has a shorter way to declare inside a function: `count := 213`. The `:=` means "declare a new variable and let the compiler work out its type from the value". `213` is an `int`, so `count` is an `int`. You will write `:=` far more often than `var`. `var` is for when you want to name the type explicitly, or declare a variable without a value yet, or declare one outside any function.

Now the widths. Go's whole numbers come in sizes: `int8`, `int16`, `int32`, `int64`, where the number is how many **bits** the value gets. A bit is one on-or-off switch. Eight bits hold 256 different values; 32 bits hold about four billion; 64 bits hold about eighteen billion billion. Plain `int` is 64 bits on every machine you are likely to use. Signed types spend one bit on the sign, so `int32` runs from −2 147 483 648 to 2 147 483 647.

That top number is the clicker's 9999. Add one more and the wheels roll: **overflow**. Go does not panic and does not warn. The value wraps round to the far negative end and carries on. `2 000 000 000 + 2 000 000 000` in an `int32` is `-294967296`. In an `int64` it is `4000000000`, because the wheels are bigger. Neither is a bug. The bug is picking too few wheels.

Decimal numbers are `float64`, 64 bits, and they have the same limits as Python's float: `0.1 + 0.2` is `0.30000000000000004`.

## 4. The picture

```
 int32: 32 wheels, one of them for the sign
 ┌──────────────────────────────────────────────┐
 │ min  -2147483648                              │
 │ ...                                           │
 │ max   2147483647   ◄── the clicker's 9999     │
 └──────────────────────────────────────────────┘
        2000000000
      + 2000000000
      = 4000000000  does not fit; the wheels roll
                    4000000000 - 4294967296 = -294967296

 int64: 64 wheels
 ┌──────────────────────────────────────────────┐
 │ max   9223372036854775807                     │
 └──────────────────────────────────────────────┘
        4000000000  fits easily
```

*Notice the subtraction. 4 294 967 296 is 2 to the 32, the total number of values 32 bits can hold. Overflow is not random: the answer is exactly what you would get from a clicker with that many positions.*

## 5. The code, built step by step

Start `numbers.go` in a `day02` folder.

```go
package main

import "fmt"

func main() {
	var count int = 213
	count = count + 1
	fmt.Println(count)
}
```

`var count int = 213` declares `count` as an `int` holding 213. The next line reads it, adds one, and stores 214 back. `=` alone means assign to an existing variable; `:=` means declare a new one.

```go
	total := 213
	fmt.Printf("total is %d and its type is %T\n", total, total)
```

```
total is 213 and its type is int
```

`:=` declared `total` and the compiler chose `int` from the value. `fmt.Printf` prints with holes: `%d` is filled by a whole number and `%T` by the type of whatever you pass. `\n` ends the line, because `Printf`, unlike `Println`, does not add one.

Now try to change its type, the way Python allowed.

```go
	total = "two hundred and thirteen"
```

```
./numbers.go:10:10: cannot use "two hundred and thirteen" (untyped string constant) as int value in assignment
```

The program does not compile. That is static typing: the mistake is found before anything runs. Delete that line and move on to widths.

```go
	var a int32 = 2_000_000_000
	var b int32 = 2_000_000_000
	fmt.Println("int32:", a+b)

	var c int64 = 2_000_000_000
	var d int64 = 2_000_000_000
	fmt.Println("int64:", c+d)
```

```
int32: -294967296
int64: 4000000000
```

The same arithmetic, two different answers, and the compiler said nothing, because at compile time it cannot know what `a` and `b` will hold. When the value is known at compile time, Go does catch it:

```go
	var e int32 = 4_000_000_000
```

```
./numbers.go:20:16: cannot use 4_000_000_000 (untyped int constant) as int32 value in variable declaration (overflows)
```

So the rule: constants that overflow are compile errors; arithmetic that overflows at run time wraps silently.

Two more lines for the float.

```go
	fmt.Println(0.1 + 0.2)
	x, y := 0.1, 0.2
	fmt.Println(x+y, x+y == 0.3)
```

```
0.3
0.30000000000000004 false
```

The first line is a trick. `0.1 + 0.2` written as literal constants is computed by the compiler with unlimited precision, so it prints `0.3`. The moment the values live in `float64` variables, you get the real 64-bit answer. Never compare floats with `==`.

Here is the run and output for the complete program.

```bash
go run numbers.go
```

```
count is 214 and its type is int
int32: -294967296
int64: 4000000000
float64: 0.30000000000000004 equal to 0.3? false
20 / 3 = 6 remainder 2
20.0 / 3 = 6.666666666666667
```

And the complete file.

```go
// numbers.go — day 2, static types and fixed widths
// Run:  go run numbers.go
package main

import "fmt"

func main() {
	var count int = 213
	count = count + 1
	fmt.Printf("count is %d and its type is %T\n", count, count)

	var a int32 = 2_000_000_000
	var b int32 = 2_000_000_000
	fmt.Println("int32:", a+b)

	var c int64 = 2_000_000_000
	var d int64 = 2_000_000_000
	fmt.Println("int64:", c+d)

	x, y := 0.1, 0.2
	fmt.Println("float64:", x+y, "equal to 0.3?", x+y == 0.3)

	fmt.Println("20 / 3 =", 20/3, "remainder", 20%3)
	fmt.Println("20.0 / 3 =", 20.0/3)
}
```

Notice the last two lines. `20/3` with two ints is whole-number division, `6`, with `%` giving the remainder. Go has no separate `//`; the types of the operands decide. `20.0/3` involves a float, so the answer is a float.

## 6. How the other two languages do it

Python, where the name has no type and the int has no width:

```python
count = 213
count = "two hundred"      # allowed
big = 2_000_000_000 + 2_000_000_000
print(big)                 # 4000000000
```

C++, where the width is chosen just as in Go, but overflow is worse than a wrap:

```cpp
#include <cstdint>
#include <iostream>

int main() {
    std::int32_t a = 2'000'000'000;
    std::int32_t b = 2'000'000'000;
    std::cout << a + b << "\n";   // prints -294967296 on most machines
}
```

The one line of difference that matters: **Go defines what overflow does; C++ does not.** In Go, signed overflow wraps, always, on every machine, and you can rely on it. In C++, signed overflow is **undefined behaviour**, which means the language makes no promise at all: it usually wraps, but the compiler is allowed to assume it never happens and rearrange your program on that assumption. Python sidesteps the whole question by having no fixed width. Three languages, three answers to "what happens past the top": grow, wrap, or no promise.

## 7. The traps

**The near-miss: mixing widths.** This looks like it adds two numbers.

```go
	var small int32 = 5
	var large int64 = 10
	fmt.Println(small + large)
```

```
./numbers.go:9:14: invalid operation: small + large (mismatched types int32 and int64)
```

Go will not add an `int32` to an `int64`, even though the answer is obvious to you. You must convert one: `int64(small) + large`. This feels pedantic until the day a silent conversion would have thrown away the top 32 bits.

**The real error: declared and not used.** Declare a variable and forget to use it.

```go
	unused := 42
```

```
./numbers.go:8:2: declared and not used: unused
```

A compile error, not a warning. Same philosophy as the unused import from yesterday.

**The near-miss: `:=` when you meant `=`.** Inside a function, this looks like it updates `count`.

```go
	count := 213
	count := 214
```

```
./numbers.go:9:8: no new variables on left side of :=
```

`:=` always declares. Using it twice on the same name in the same block is an error. The subtler version, where the second `:=` is inside an inner block and creates a new variable that shadows the first, compiles fine and is one of Go's classic bugs. You will meet it properly on day 4 with `if` and `for`.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between `var` and `:=`?"
- "What happens when an `int32` overflows in Go?"
- "How wide is `int` in Go, and should I use it or `int64`?"

**What to say out loud, the first ninety seconds**

"Go is statically typed: every variable has a type fixed at declaration, and the compiler rejects any assignment of a different type. There are two ways to declare. `var name type = value` is the explicit form, and it is the only form allowed outside a function. `name := value` is the short form inside functions, where the compiler infers the type from the value; it is what I use most of the time.

Whole numbers have explicit widths, `int8` to `int64`, and plain `int` is 64 bits on modern machines. Overflow in Go is defined: signed integers wrap round, so two billion plus two billion in an `int32` is minus 294 967 296, with no panic and no warning. Constants that overflow are caught at compile time; arithmetic on variables is not. So I pick the width from the largest value I can imagine, and I use `int` unless I have a reason to be specific, such as matching a wire format."

**The follow-ups**

1. *"Why does `fmt.Println(0.1 + 0.2)` print `0.3` but the same in variables prints `0.30000000000000004`?"* — Untyped constants are evaluated by the compiler with arbitrary precision. Once the values are in `float64` variables, you get the 64-bit result.
2. *"Can I add an `int32` and an `int64`?"* — Not without an explicit conversion. Go has no implicit numeric conversions, which prevents silent truncation.
3. *"When would you use `int32` over `int`?"* — When the size matters for storage or a protocol: a struct with millions of instances, a file format, or a field in a message where the width is part of the contract.

**A model answer**

"Go is statically typed with explicit integer widths. `var x int = 5` and `x := 5` both declare an `int`; the second infers the type and only works inside functions. `int` is 64 bits on 64-bit platforms. Signed overflow is defined to wrap: `int32(2e9) + int32(2e9)` gives `-294967296` silently at run time, while a constant that overflows its type is a compile error. There are no implicit conversions between numeric types, so `int32 + int64` does not compile. `float64` is IEEE double, so `0.1 + 0.2 != 0.3` once the values are in variables, and I compare floats with a tolerance."

## 9. Recall card

- `var count int = 213` explicit; `count := 213` inferred and only inside functions; `=` alone assigns to an existing variable.
- Static typing: the type is fixed at declaration and the compiler rejects `count = "text"` before anything runs.
- `int` is 64 bits; `int32` overflows past 2 147 483 647 and wraps to `-294967296` for two billion plus two billion, silently.
- Constants that overflow are compile errors; variable arithmetic that overflows is not.
- No implicit conversions: `int32 + int64` is a compile error; declared-and-not-used is too.
