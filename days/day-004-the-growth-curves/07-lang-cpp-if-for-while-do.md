---
day: 4
track: lang-cpp
title: "if, for, while, do-while, range-for, switch with fallthrough"
theme: "Conditions and loops"
phase: "Languages: every language, every basic"
status: written
---

# Day 004 · C++ — if, for, while, do-while, range-for, switch with fallthrough

**Today's theme:** Conditions and loops

**After today you can:** You can write every loop shape in each language and pick the one that reads cleanest for a given job.

**The interviewer asks it as:** *Write a loop that stops early. Now write it without break.*

---

## 1. What this is, and why it matters

C++ has the most loop keywords of the three: `for` with three parts, `while` that checks first, `do-while` that checks after, and the range-`for` that walks a collection. Conditions are `if`/`else if`/`else` with the condition in round brackets, and `switch`, which picks a case and then, unless you say `break`, keeps running into the next case. That last behaviour is called fallthrough, and it is the single most famous trap in the language.

At work, C++ conditions are where `=` gets written for `==` and the compiler lets it through with a warning, and `switch` is where a missing `break` runs two cases at once in production. Interviewers ask "what is the difference between `while` and `do-while`", "what does `switch` do without `break`", and the question in the heading, which in C++ you answer with a `while`.

## 2. The story

Sunil gets home at half past seven and cannot find his house key. His wife is out until ten. There are five jackets hanging on the hooks by the door, and the key is in one of them.

He starts at the left. The first jacket is his wife's red one. He does not check it; his key would not be in her jacket. He moves on. The second is his grey work jacket. He checks both pockets. Nothing. The third is his wife's again, the long black one. Skip. The fourth is his old brown jacket from last winter. Left pocket, nothing. Right pocket, keys. He stops. He does not check the fifth jacket, because there is no reason to. He has what he came for.

That is the whole search on a good day. Start at one end. Skip the ones that cannot be right. Stop the moment you find it.

On a bad day, it goes differently. He checks all five, skipping his wife's two, and gets to the end of the row with nothing in his hand. And now, only now, because he reached the end without finding it, he does the thing he was hoping not to do: he phones the locksmith.

His neighbour, watching from the stairs, asks why he did not just check all five and then decide. Sunil says that would be silly. Once the key is in his hand, checking more jackets is wasted time. And the locksmith call is not something he does after every search; it is only for the search that comes up empty.

There is one more version of the same evening. Sometimes Sunil does not think of it as "check jackets until I find the key". He thinks of it as "keep going as long as I have not found it and there are jackets left". Same jackets, same pockets, same moment of stopping. But the rule for stopping is said out loud at the start, instead of being a decision made halfway through. His wife prefers that version. She says it is easier to explain to the locksmith.

## 3. The idea in plain English

A **condition** is a yes-or-no question whose answer is a **bool**, `true` or `false`, built from `==`, `!=`, `<`, `>`, `<=`, `>=` and joined with `&&` (and), `||` (or), `!` (not).

`if (cond) { ... } else if (cond) { ... } else { ... }` picks one block. The condition sits in round brackets. The braces are optional for a single statement, and leaving them out is the source of enough bugs that this course always writes them.

A **loop** runs a block repeatedly. C++ has four.

`for (int i = 0; i < 5; ++i) { ... }` is the counted loop: start, condition checked before each go, step after each go. `++i` adds one.

`while (cond) { ... }` checks the condition first and runs the block while it holds. This is Sunil's wife's version, and it is the answer to the interview question.

`do { ... } while (cond);` runs the block **once, then** checks. Use it when the body must happen at least once, such as asking for input until it is valid. Note the semicolon at the end; it is required.

`for (std::string jacket : jackets) { ... }` is the range-`for`, and walks each item in a collection. A **`std::vector<std::string>`** is a growable row of strings, written `{"red", "grey"}`, from the header `<vector>`; day 6 covers it properly. Today you walk it and index it with `jackets[3]`, and `jackets.size()` is how many it holds.

`break` leaves the loop. `continue` skips to the next go. There is no `for-else`; the locksmith call is a flag checked after the loop, exactly as in Go.

`switch (value) { case 1: ... break; case 2: ... break; default: ... }` picks the matching case and runs from there **until it meets a `break`**. Without one, it runs on into the next case. That is **fallthrough**. It is occasionally useful and usually a bug, and C++17 added `[[fallthrough]];` so you can mark the times you mean it.

## 4. The picture

```
 while (cond) { body }            do { body } while (cond);

   ┌──► cond? ──no──► exit          ┌──► body
   │      │yes                      │      │
   │    body                        │    cond? ──no──► exit
   └──────┘                         └──yes─┘

 switch (n) {
     case 1:  A;            ← n == 1 runs A, B, C   (no breaks)
     case 2:  B;            ← n == 2 runs B, C
     case 3:  C; break;     ← n == 3 runs C
     default: D;
 }
```

*Notice that `do-while` runs the body before it ever looks at the condition. Notice that in the `switch`, control enters at the matching case and keeps going downward until a `break`; the case labels are entry points, not walls.*

## 5. The code, built step by step

Start `search.cpp` in a `day04` folder.

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> jackets = {"red", "grey", "black", "brown", "green"};
    std::string key_in = "brown";
```

A vector of strings, five of them. `jackets[0]` is `"red"`, `jackets.size()` is 5.

The counted loop.

```cpp
    for (std::size_t i = 0; i < jackets.size(); ++i) {
        std::cout << i << " " << jackets[i] << "\n";
    }
```

```
0 red
1 grey
2 black
3 brown
4 green
```

`std::size_t` is the unsigned whole-number type that sizes and indices use. Writing `int i` here would work but the compiler would warn, and the warning is in the traps.

The range-`for`, with `continue` and `break`.

```cpp
    for (std::string jacket : jackets) {
        if (jacket == "red" || jacket == "black") {
            continue;
        }
        std::cout << "checking " << jacket << "\n";
        if (jacket == key_in) {
            std::cout << "found it\n";
            break;
        }
    }
```

```
checking grey
checking brown
found it
```

`std::string jacket` makes a copy of each item as the loop reaches it. That copy is wasteful and day 12 shows the fix; today the copy is fine.

The `while`, which is the interview answer.

```cpp
    std::size_t position = 0;
    bool found = false;
    while (!found && position < jackets.size()) {
        if (jackets[position] == key_in) {
            found = true;
        } else {
            ++position;
        }
    }
    std::cout << std::boolalpha << "found: " << found << " at " << position << "\n";
```

```
found: true at 3
```

No `break`. The condition at the top says when to stop.

The `do-while`, which runs first and asks afterwards.

```cpp
    int attempts = 0;
    do {
        ++attempts;
        std::cout << "attempt " << attempts << "\n";
    } while (attempts < 1);
```

```
attempt 1
```

The condition `attempts < 1` is already false after the first go, but the first go happened anyway. That is the entire difference from `while`.

The locksmith, with a flag.

```cpp
    found = false;
    for (std::string jacket : jackets) {
        if (jacket == "nowhere") {
            found = true;
            break;
        }
    }
    if (!found) {
        std::cout << "checked every jacket; phoning the locksmith\n";
    }
```

And `switch`, with its `break`s where they belong.

```cpp
    int hook = 4;
    switch (hook) {
        case 1:
        case 3:
            std::cout << "that is hers\n";
            break;
        case 4:
            std::cout << "the old brown one\n";
            break;
        default:
            std::cout << "some other jacket\n";
    }
```

```
the old brown one
```

`case 1:` with nothing under it falls straight into `case 3:`, which is the one place fallthrough is idiomatic: several labels sharing one body. Every other case ends in `break`. `switch` works on whole numbers and single characters, not on `std::string`; for strings you use an `if` chain.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra search.cpp -o search
./search
```

```
with break:
  skip red
  checking grey
  skip black
  checking brown -> found it
with a while condition:
  found: true at position 3
do-while ran: 1 time
searching for a key that is not there:
  checked every jacket; phoning the locksmith
switch: the old brown one
```

And the complete file.

```cpp
// search.cpp — day 4, every loop shape and a switch
// Build: g++ -std=c++20 -Wall -Wextra search.cpp -o search
// Run:   ./search
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> jackets = {"red", "grey", "black", "brown", "green"};
    std::string key_in = "brown";

    std::cout << "with break:\n";
    for (std::string jacket : jackets) {
        if (jacket == "red" || jacket == "black") {
            std::cout << "  skip " << jacket << "\n";
            continue;
        }
        if (jacket == key_in) {
            std::cout << "  checking " << jacket << " -> found it\n";
            break;
        }
        std::cout << "  checking " << jacket << "\n";
    }

    std::cout << "with a while condition:\n";
    std::size_t position = 0;
    bool found = false;
    while (!found && position < jackets.size()) {
        if (jackets[position] == key_in) {
            found = true;
        } else {
            ++position;
        }
    }
    std::cout << std::boolalpha << "  found: " << found << " at position " << position << "\n";

    int attempts = 0;
    do {
        ++attempts;
    } while (attempts < 1);
    std::cout << "do-while ran: " << attempts << " time\n";

    std::cout << "searching for a key that is not there:\n";
    found = false;
    for (std::string jacket : jackets) {
        if (jacket == "nowhere") {
            found = true;
            break;
        }
    }
    if (!found) {
        std::cout << "  checked every jacket; phoning the locksmith\n";
    }

    int hook = 4;
    switch (hook) {
        case 1:
        case 3:
            std::cout << "switch: that is hers\n";
            break;
        case 4:
            std::cout << "switch: the old brown one\n";
            break;
        default:
            std::cout << "switch: some other jacket\n";
    }
    return 0;
}
```

## 6. How the other two languages do it

Python, with two loop keywords and an `else` on the loop:

```python
for jacket in jackets:
    if jacket == key_in:
        print("found it")
        break
else:
    print("phoning the locksmith")
```

Go, with one loop keyword and a `switch` that stops on its own:

```go
switch hook {
case 1, 3:
	fmt.Println("that is hers")
case 4:
	fmt.Println("the old brown one")
}
```

The one line of difference that matters: **C++'s `switch` falls through by default; Go's and Python's equivalents do not.** In Go, `case 4:` runs and the switch ends. In C++, `case 4:` runs and then `default:` runs too, unless there is a `break` in between. Python has `match`, which also stops after one arm. So the C++ habit is: every case ends in `break`, and the rare deliberate fallthrough is marked `[[fallthrough]];` so the compiler and the next reader know it was meant. The smaller difference: C++ is the only one of the three with `do-while`, and the only one where the `if` condition needs round brackets.

## 7. The traps

**The near-miss: the assignment in the condition.** One `=` where two were meant.

```cpp
    int hook = 4;
    if (hook = 3) {
        std::cout << "hook is three\n";
    }
```

```
search.cpp: In function 'int main()':
search.cpp:7:14: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
    7 |     if (hook = 3) {
      |         ~~~~~^~~
```

```
hook is three
```

It compiles, prints the warning, and runs. `hook = 3` assigns 3 to `hook` and the value of that expression is 3, which is not zero, which counts as `true`. So the branch always runs and `hook` is now 3. Python refused this line outright. C++ warns and continues, which is why `-Wall` is not optional. Some programmers write `if (3 == hook)` so that a slip becomes an error; more rely on reading their warnings.

**The real error: the missing `break`.** Forget one in the switch.

```cpp
    switch (hook) {
        case 4:
            std::cout << "the old brown one\n";
        default:
            std::cout << "some other jacket\n";
    }
```

```
search.cpp:9:23: warning: this statement may fall through [-Wimplicit-fallthrough=]
    9 |             std::cout << "the old brown one\n";
      |             ~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~
search.cpp:10:9: note: here
   10 |         default:
      |         ^~~~~~~
```

```
the old brown one
some other jacket
```

Both lines print. That warning comes from `-Wextra`; without it, silence. If the fallthrough is intended, write `[[fallthrough]];` as the last line of the case and the warning goes away.

**The near-miss: the semicolon after the `if`.** A stray `;`.

```cpp
    if (found);
    {
        std::cout << "found\n";
    }
```

```
search.cpp:7:14: warning: suggest braces around empty body in an 'if' statement [-Wempty-body]
```

The `if` governs the empty statement `;` and nothing else. The braces after it are just a block that always runs. `found` printed whether or not it was found. Again: a warning, not an error, and only with `-Wextra`.

**The near-miss: the signed index.** Write the counted loop with `int`.

```cpp
    for (int i = 0; i < jackets.size(); ++i) {
```

```
search.cpp:8:23: warning: comparison of integer expressions of different signedness: 'int' and 'std::vector<std::__cxx11::basic_string<char> >::size_type' {aka 'long unsigned int'} [-Wsign-compare]
```

`size()` returns an unsigned number and `i` is signed. It works here, and it stops working the day `i` is negative and the comparison converts it to a huge unsigned value. Use `std::size_t` for indices.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between `while` and `do-while`?"
- "What does a `switch` do without `break`?"
- "Write a loop that stops early. Now write it without `break`."

**What to say out loud, the first ninety seconds**

"C++ has four loops. `for` with init, condition and step; `while`, which tests before each iteration; `do-while`, which runs the body once and then tests, for cases like reading input until it is valid; and the range-`for`, which walks any container. `break` exits, `continue` skips ahead.

To stop early with `break`, I test inside a range-`for` and break. Without `break`, I write a `while` whose condition carries the exit rule: `while (!found && i < items.size())`, setting `found` inside. The `while` version puts the termination condition where a reader looks first.

`switch` selects a case label and then executes downward until a `break`, so a missing `break` runs the next case too. I end every case with `break` and mark intentional fallthrough with `[[fallthrough]]`, and I compile with `-Wall -Wextra` because the missing `break`, `if (x = 3)`, and a stray semicolon after an `if` are all warnings, not errors."

**The follow-ups**

1. *"Why does `if (x = 3)` compile at all?"* — Because assignment is an expression whose value is the assigned value, and any non-zero number converts to `true`. The language inherited this from C; the compiler warns because it is almost never intended.
2. *"What can you `switch` on?"* — Integers, characters and enumerations. Not `std::string`; for strings you use an `if`/`else if` chain or a map lookup.
3. *"When is fallthrough useful?"* — Stacked labels sharing one body, `case 1: case 3:`, and occasionally a case that does extra work then continues into the general case. Mark the second kind with `[[fallthrough]];`.

**A model answer**

"C++ offers `for`, `while`, `do-while` and range-`for`. `while` checks before the body and may run zero times; `do-while` checks after and runs at least once. Early exit is `break`; the same loop without `break` moves the exit condition into a `while` header with a flag. `switch` transfers control to the matching label and continues through subsequent labels until `break`, so every case should end in `break` unless fallthrough is intended and marked `[[fallthrough]]`. Three classic warnings, all real bugs, come from this material: `-Wparentheses` for `if (x = 3)`, `-Wimplicit-fallthrough` for a missing `break`, and `-Wsign-compare` for an `int` index against `size()`. I use `std::size_t` for indices and treat all three warnings as errors."

## 9. Recall card

- `if (cond) {}` with round brackets; `for (init; cond; step) {}`; `while (cond) {}` checks first; `do {} while (cond);` runs once first; `for (auto x : xs) {}` walks a container.
- Stop early without `break`: `while (!found && i < xs.size())` with a flag set inside.
- `switch` falls through: end every case with `break`, stack labels for shared bodies, mark intent with `[[fallthrough]];`.
- `if (x = 3)` compiles, warns, and is always true; missing `break` and a stray `;` after `if` are warnings too; `-Wall -Wextra` always.
- Index with `std::size_t`, not `int`, or `-Wsign-compare` tells you why.
