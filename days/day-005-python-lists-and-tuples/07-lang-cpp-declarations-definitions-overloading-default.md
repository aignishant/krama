---
day: 5
track: lang-cpp
title: "Declarations, definitions, overloading, default arguments"
theme: "Functions"
phase: "Languages: every language, every basic"
status: written
---

# Day 005 · C++ — Declarations, definitions, overloading, default arguments

**Today's theme:** Functions

**After today you can:** You can write a function with several inputs and outputs in each language and explain where each argument lives.

**The interviewer asks it as:** *How does each language return more than one value?*

---

## 1. What this is, and why it matters

A C++ function has a return type, a name, and typed parameters, and the compiler must have seen at least its signature before any line that calls it. Several functions may share one name if their parameters differ, which is overloading; parameters may carry default values; and a function returns exactly one thing, so returning two means packing them into a `std::pair` or `std::tuple` and unpacking with structured bindings. Every parameter is a copy.

At work, the declaration-before-use rule is why C++ projects have header files, and overloading is how the standard library gives you one name, `std::to_string`, that works for every number type. Interviewers ask "what is the difference between a declaration and a definition", "how do you return multiple values in C++", and "what happens if a non-void function has no return", and the last one is undefined behaviour with a warning.

## 2. The story

Farhan's father needs a new kurta for a wedding on the twentieth, and Farhan is sent to the tailor with the cloth.

The tailor is a small, quick man who has been on the same corner for thirty years. Farhan hands over the folded cloth and says the three numbers his mother told him: chest forty-two, length thirty-eight, sleeve twenty-four. The tailor writes nothing down. He nods.

"Collar?" the tailor asks. Farhan does not know. "Then the usual," the tailor says. "Band collar. Everybody who does not say wants the band collar." Farhan realises that if his mother had cared, she would have told him, and that the tailor has a standing answer for anyone who does not.

"Pockets?" Farhan's mother had said one on the left. "Left, then. If you had said nothing, I would have done none."

On Thursday Farhan comes back. The tailor hands him a kurta on a hanger, and then, separately, a folded square of the same cloth. "Leftover," he says. "Nearly half a metre. Your mother will want it." So Farhan walks home carrying two things from one visit: the thing he asked for and the thing that came out of making it. He had not thought of the leftover as a result. The tailor had.

The next week Farhan's uncle sends him back with four shirts that all need the sleeves taken up by the same amount. The tailor does not want to hear about them one at a time. "Put them all on the counter. Same job, however many there are." He counts them, does the same thing four times, and hands back four shirts.

And Farhan notices one more thing. While the tailor is measuring, he says numbers out loud to himself, chest, length, sleeve, and then forgets them completely the moment the kurta is done. Ask him a week later what Farhan's father's chest measurement was, and he will shrug. Those numbers existed for one job. When the job ended, so did they.

## 3. The idea in plain English

A **function** is a named block you run by name. In C++ the return type comes first: `std::string stitch(int chest, int length) { ... }`. The **parameters** each have a type. You **call** it with `stitch(42, 38)`, and each **argument** is copied into its parameter.

C++ splits a function into two ideas. A **declaration** is the signature alone, ending in a semicolon: `std::string stitch(int chest, int length);`. It tells the compiler "a function of this shape exists somewhere". A **definition** is the signature with the body. The compiler reads a file top to bottom, and a call to a function it has not yet seen at least a declaration of is an error. So either you define functions above the code that uses them, or you declare them at the top and define them below. Larger programs put declarations in **header files**, which day 11 covers; today everything sits in one file.

**Overloading**: several functions may share a name if their parameter lists differ. `stitch(int, int)` and `stitch(int, int, std::string)` can both exist, and the compiler picks by the arguments you pass. The standard library uses this everywhere. It also means an interview question about "which one gets called" is really about how the compiler ranks conversions, and the ambiguous case is in the traps.

**Default arguments**: a parameter can carry a standing answer, `std::string collar = "band"`. Defaults must be the last parameters, and they go on the declaration, not repeated on the definition. There are no keyword arguments; you cannot write `stitch(42, 38, collar = "mandarin")`. To pass the fourth argument you must pass the third.

**Returning two things**: a C++ function returns one value. To return the kurta and the leftover, you return a `std::pair<std::string, double>`, one object with two named halves, `.first` and `.second`, from `<utility>`. C++17 added **structured bindings**, `auto [kurta, leftover] = stitch_with_leftover(...)`, which unpack the pair into two named variables at the call site. For three or more, `std::tuple` from `<tuple>` works the same way. Day 8 gives you a better tool for this: a small struct with named fields.

Every variable declared inside a function is **local** and destroyed at `return`. The tailor's measurements. And a function declared to return a value that reaches its closing brace without a `return` is **undefined behaviour**, which the compiler warns about and then compiles anyway.

## 4. The picture

```
 what the compiler needs to see, in order

   std::string stitch(int chest, int length);        ← declaration: shape only
   ...
   int main() {
       std::cout << stitch(42, 38);                   ← call: allowed, shape is known
   }
   ...
   std::string stitch(int chest, int length) {       ← definition: shape plus body
       return std::format("kurta {}/{}", chest, length);
   }

 returning two things

   std::pair<std::string, double>   one object ───┐
   ┌──────────────────┬─────────┐                 │
   │ .first "kurta.." │ .second │                 │
   │                  │  0.5    │                 │
   └──────────────────┴─────────┘                 │
   auto [kurta, leftover] = ...;   ◄── unpacked ──┘
```

*Notice that the call sits above the definition and compiles only because the declaration sits above the call. Notice that the pair is one thing on the way back and becomes two only when the caller unpacks it.*

## 5. The code, built step by step

Start `tailor.cpp` in a `day05` folder. Declarations first.

```cpp
#include <format>
#include <iostream>
#include <string>
#include <utility>

std::string stitch(int chest, int length, std::string collar = "band", std::string pocket = "none");
std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth);
double take_up(double amount);
int take_up(int amount, int shirts);
```

Four declarations, each a signature with a semicolon. The defaults for `collar` and `pocket` live here, on the declaration, and nowhere else. The two `take_up` lines are an overload: same name, different parameters, and the compiler will pick between them.

Now `main`, above the definitions, which is allowed because the declarations came first.

```cpp
int main() {
    std::cout << stitch(42, 38) << "\n";
    std::cout << stitch(42, 38, "mandarin") << "\n";
    std::cout << stitch(42, 38, "band", "left") << "\n";
```

```
kurta 42/38, band collar, pocket none
kurta 42/38, mandarin collar, pocket none
kurta 42/38, band collar, pocket left
```

The third call is the price of having no keyword arguments: to set `pocket`, you must also spell out `collar`, even though you wanted the default.

Two results.

```cpp
    auto [kurta, leftover] = stitch_with_leftover(42, 38, 2.5);
    std::cout << kurta << " with " << leftover << " metres left\n";

    std::pair<std::string, double> result = stitch_with_leftover(42, 38, 2.5);
    std::cout << result.first << " / " << result.second << "\n";
```

```
kurta 42/38 with 0.5 metres left
kurta 42/38 / 0.5
```

The first form is what you write. The second shows what it unpacks: one object with `.first` and `.second`.

Overload resolution.

```cpp
    std::cout << take_up(2.5) << "\n";
    std::cout << take_up(2, 4) << "\n";
}
```

```
2.5
8
```

One argument that is a `double` picks the first `take_up`; two `int`s pick the second. The compiler decides at compile time from the argument types, and the two functions are entirely separate.

The definitions, below `main`. Note the defaults are not repeated.

```cpp
std::string stitch(int chest, int length, std::string collar, std::string pocket) {
    return std::format("kurta {}/{}, {} collar, pocket {}", chest, length, collar, pocket);
}

std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth) {
    double used = (chest + length) / 40.0;
    return {std::format("kurta {}/{}", chest, length), cloth - used};
}
```

`return {a, b};` builds the pair from the two values in braces. `(chest + length) / 40.0` divides by a double so the answer is `2.0`, not the whole-number `2`; `/ 40` would still give `2` here but would truncate for other inputs.

```cpp
double take_up(double amount) {
    return amount;
}

int take_up(int amount, int shirts) {
    return amount * shirts;
}
```

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra tailor.cpp -o tailor
./tailor
```

```
kurta 42/38, band collar, pocket none
kurta 42/38, mandarin collar, pocket none
kurta 42/38, band collar, pocket left
kurta 42/38 with 0.5 metres left
as a pair: kurta 42/38 / 0.5
take_up(2.5) -> 2.5
take_up(2, 4) -> 8
```

And the complete file.

```cpp
// tailor.cpp — day 5, declarations, definitions, overloading, defaults
// Build: g++ -std=c++20 -Wall -Wextra tailor.cpp -o tailor
// Run:   ./tailor
#include <format>
#include <iostream>
#include <string>
#include <utility>

// Declarations. Defaults live here and only here.
std::string stitch(int chest, int length, std::string collar = "band", std::string pocket = "none");
std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth);
double take_up(double amount);
int take_up(int amount, int shirts);

int main() {
    std::cout << stitch(42, 38) << "\n";
    std::cout << stitch(42, 38, "mandarin") << "\n";
    std::cout << stitch(42, 38, "band", "left") << "\n";

    auto [kurta, leftover] = stitch_with_leftover(42, 38, 2.5);
    std::cout << kurta << " with " << leftover << " metres left\n";

    std::pair<std::string, double> result = stitch_with_leftover(42, 38, 2.5);
    std::cout << "as a pair: " << result.first << " / " << result.second << "\n";

    std::cout << "take_up(2.5) -> " << take_up(2.5) << "\n";
    std::cout << "take_up(2, 4) -> " << take_up(2, 4) << "\n";
    return 0;
}

// Definitions. The compiler already knows their shapes from the declarations above.
std::string stitch(int chest, int length, std::string collar, std::string pocket) {
    return std::format("kurta {}/{}, {} collar, pocket {}", chest, length, collar, pocket);
}

std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth) {
    double used = (chest + length) / 40.0;
    return {std::format("kurta {}/{}", chest, length), cloth - used};
}

double take_up(double amount) {
    return amount;
}

int take_up(int amount, int shirts) {
    return amount * shirts;
}
```

## 6. How the other two languages do it

Python, where order in the file does not matter as long as the `def` runs before the call, and two results are a tuple:

```python
def stitch_with_leftover(chest: int, length: int, cloth: float) -> tuple[str, float]:
    return f"kurta {chest}/{length}", cloth - (chest + length) / 40

kurta, leftover = stitch_with_leftover(42, 38, 2.5)
print(stitch(42, 38, pocket="left"))    # by name, skipping collar
```

Go, where order never matters, two results are native, and overloading and defaults do not exist:

```go
func stitchWithLeftover(chest, length int, cloth float64) (string, float64) {
	return fmt.Sprintf("kurta %d/%d", chest, length), cloth - float64(chest+length)/40
}

kurta, leftover := stitchWithLeftover(42, 38, 2.5)
```

The one line of difference that matters: **C++ must see a declaration before a call; Python and Go do not care about order.** In Go you can call a function defined at the bottom of the file from the top. In Python a `def` just has to have run before the call reaches it, which in practice means the same freedom. In C++, a call above the definition with no declaration is a compile error, and that single rule is the reason header files exist. The second difference: C++ has overloading, one name for several functions chosen by argument types. Go forbids it outright, and Python fakes it with defaults and `isinstance` checks inside one function.

## 7. The traps

**The real error: calling before declaring.** Put the call above the definition and delete the declaration.

```cpp
int main() {
    std::cout << stitch(42, 38) << "\n";
}

std::string stitch(int chest, int length) {
    return std::format("kurta {}/{}", chest, length);
}
```

```
tailor.cpp: In function 'int main()':
tailor.cpp:6:18: error: 'stitch' was not declared in this scope
    6 |     std::cout << stitch(42, 38) << "\n";
      |                  ^~~~~~
```

The function exists, three lines down. The compiler had not seen it yet. Add the declaration above `main`, or move the definition above it.

**The real error: the default given twice.** Repeat the default on the definition.

```cpp
std::string stitch(int chest, int length, std::string collar = "band");
std::string stitch(int chest, int length, std::string collar = "band") { ... }
```

```
tailor.cpp:12:57: error: default argument given for parameter 3 of 'std::string stitch(int, int, std::string)' [-fpermissive]
   12 | std::string stitch(int chest, int length, std::string collar = "band") {
      |                                           ~~~~~~~~~~~~^~~~~~~~~~~~~~~
tailor.cpp:7:13: note: previous specification in 'std::string stitch(int, int, std::string)' here
```

Once. On the declaration.

**The near-miss: the missing return.** A non-void function that falls off the end.

```cpp
double cloth_needed(int chest, int length) {
    double needed = (chest + length) / 40.0;
}
```

```
tailor.cpp: In function 'double cloth_needed(int, int)':
tailor.cpp:10:1: warning: no return statement in function returning non-void [-Wreturn-type]
   10 | }
      | ^
```

It compiles. Calling it and using the result is undefined behaviour; you might get `2`, or `0`, or something that looks like a valid number and is not. Python gave you `None` and a `TypeError` at the point of use. C++ gives you a warning and whatever was in the register. Read your warnings.

**The near-miss: the ambiguous overload.** Two overloads that both need a conversion.

```cpp
void show(int n);
void show(long n);

show(2.5);
```

```
tailor.cpp:9:9: error: call of overloaded 'show(double)' is ambiguous
    9 |     show(2.5);
      |     ~~~~^~~~~
tailor.cpp:5:6: note: candidate: 'void show(int)'
tailor.cpp:6:6: note: candidate: 'void show(long int)'
```

A `double` converts equally well to `int` and to `long`, so the compiler refuses to guess. At least it is an error and not a silent pick. The fix is to add a `show(double)` overload or to cast the argument.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between a declaration and a definition?"
- "How do you return multiple values from a C++ function?"
- "What happens if a non-void function has no return statement?"

**What to say out loud, the first ninety seconds**

"A declaration is the function's signature followed by a semicolon; it tells the compiler the name, parameter types and return type. A definition adds the body. The compiler needs to have seen a declaration before any call, which is why declarations go in headers and are included at the top of each file, and why a call above a definition without a declaration is an error. A function may be declared many times but defined only once.

C++ returns one value. For two, I return a `std::pair`, or `std::tuple` for more, and unpack at the call site with structured bindings, `auto [a, b] = f()`; for anything that will be read more than once I prefer a small struct with named fields. Overloading lets one name have several definitions chosen by argument types at compile time; when two candidates need equal conversions the call is ambiguous and fails to compile. Default arguments go on the declaration only, must be trailing, and there are no keyword arguments, so skipping one default to set the next is impossible. Falling off the end of a non-void function is undefined behaviour with a `-Wreturn-type` warning."

**The follow-ups**

1. *"Why not just return a struct instead of a pair?"* — For anything non-trivial you should. `.first` and `.second` carry no meaning; a struct with `kurta` and `leftover` fields does. `std::pair` is for quick internal returns and for library functions that predate structured bindings.
2. *"Are arguments passed by value or by reference?"* — By value unless the parameter type says otherwise. `std::string collar` copies the whole string on every call; `const std::string&` would not. Day 12 is about that choice.
3. *"Can you overload on return type?"* — No. Overloads must differ in their parameters. `int f()` and `double f()` together is an error.

**A model answer**

"A C++ declaration states a function's signature; a definition provides its body; the one-definition rule allows many declarations but one definition. Because the compiler works top to bottom, a call needs a prior declaration, which motivates headers. Functions return a single value, so multiple results use `std::pair`, `std::tuple`, or preferably a named struct, unpacked with C++17 structured bindings. Overloading selects among same-named functions by parameter types at compile time; equal-rank conversions make the call ambiguous and it fails to compile. Default arguments are trailing, specified once on the declaration, and there are no keyword arguments. Reaching the end of a non-void function without `return` is undefined behaviour that `-Wall` reports as `-Wreturn-type`."

## 9. Recall card

- `ret_type name(type a, type b);` declares; the same with a body defines; a call needs a declaration above it or `'name' was not declared in this scope`.
- Two results: return `std::pair<A, B>` with `return {a, b};` and unpack with `auto [a, b] = f();`; a struct is better once it is read twice.
- Overloading: same name, different parameters, chosen at compile time; equal conversions make it `ambiguous`; no overloading on return type.
- Defaults are trailing, written once on the declaration; no keyword arguments, so to set the fourth you spell out the third.
- No `return` in a non-void function compiles with `-Wreturn-type` and is undefined behaviour.
