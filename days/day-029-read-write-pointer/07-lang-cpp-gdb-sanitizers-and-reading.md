---
day: 29
track: lang-cpp
title: "gdb, sanitizers, and reading a segfault"
theme: "Debugging"
phase: "Languages: advanced features"
status: written
---

# Day 029 · C++ — gdb, sanitizers, and reading a segfault

**Today's theme:** Debugging

**After today you can:** You can set a breakpoint, step, and inspect a variable in each language.

**The interviewer asks it as:** *Your program crashes. Walk me through how you find the bug.*

## 1. What this is, and why it matters

GDB exposes call frames and local values. Sanitizers instrument a program to detect selected memory errors and undefined behaviour during execution.

You use this when discussing debugging in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Omar follows a recipe for a family dinner. The finished dish tastes far too salty. He could immediately add more water, but that would hide the reason and might ruin the texture. Instead, he asks everyone to stop changing it while he works out what happened.

He begins with the last step and walks backwards. His sister added a spoon of salt because the recipe said so. Before that, his brother added a ready-made sauce. The sauce already contained salt. The recipe had assumed an unsalted sauce, but nobody had noticed the difference.

Omar repeats a small portion in a separate pan. This time he pauses before the salt goes in and tastes what is already there. He checks the amount of sauce rather than guessing from the final flavour. The smaller portion gives him a way to repeat the problem without wasting another whole meal.

He changes one thing: he leaves out the extra salt. The portion tastes right. Then he tries the same change in another small portion to make sure the first result was not luck. He tells the family exactly which assumption failed.

For the next dinner, they add a check beside the recipe: taste the sauce before adding salt. They have not merely rescued tonight’s food. They have found a repeatable cause and a check that will catch the same mistake before it spoils another meal.

## 3. The idea in plain English

Omar pauses before adding salt; you pause before an invalid access. Debug symbols connect machine instructions to source names. AddressSanitizer detects many out-of-bounds and use-after-free accesses; UndefinedBehaviorSanitizer catches selected undefined operations. Neither proves the absence of every defect.

The reproducer uses vector::at so the bad index produces a defined exception. Replacing at with unchecked operator[] can make the same defect undefined behaviour, perhaps a crash, perhaps apparently normal output. A segmentation fault indicates an invalid memory access, not a complete explanation of its cause.

## 4. The picture

```text
reproduce -> stop before failure -> inspect values -> test one cause -> regression case
```

A debugger exposes the actual state; it does not choose the explanation for you.

## 5. The code, built step by step

First isolate the important operation:

```cpp
auto position = values.size();
return values.at(position);
```

Keep debug symbols when investigating a failure.

The complete example follows. Save as `main.cpp`. Build a debug executable with `g++ -std=c++20 -g -O0 main.cpp -o demo`. Run `gdb ./demo`, then `break last`, `run`, `next`, `print position`, `print values.size()`, and `backtrace`. A compatible GCC/Clang installation can additionally build with `-fsanitize=address,undefined -fno-omit-frame-pointer`.

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>

int last(const std::vector<int>& values) {
    auto position = values.size();
    return values.at(position);
}
int main() {
    try {
        std::cout << last({10, 20, 30}) << '\n';
    } catch (const std::out_of_range&) {
        std::cerr << "index outside vector\n";
        return 1;
    }
}
```

**Check the result:** The intentional failure prints `index outside vector` and exits with status 1. Inspect position = 3 and size = 3. Repair last by rejecting empty input and returning values.back(); the repaired program prints 30.

After inspecting the failure, replace the file with this complete repair. Run the same ordinary build/run command; it prints `30` and `empty input`.

```cpp
#include <iostream>
#include <stdexcept>
#include <vector>

int last(const std::vector<int>& values) {
    if (values.empty()) throw std::invalid_argument("empty input");
    return values.back();
}

int main() {
    std::cout << last({10, 20, 30}) << '\n';
    try { last({}); }
    catch (const std::invalid_argument& error) {
        std::cout << error.what() << '\n';
    }
}
```

## 6. How the other two languages do it

**Python**

```python
position = len(values)
return values[position]
```

A traceback shows the calls that led to an exception. pdb lets you stop at a line, inspect values, and step through the failing path.

**Go**

```go
position := len(values)
return values[position]
```

A Go panic dump names the failing goroutine and call frames. Delve can pause that execution and inspect the values that violated an assumption.

Python pdb, Go Delve, and C++ GDB all support breakpoints and inspection. Tracebacks identify the failing path; sanitizers add checks for C++ memory and undefined-behaviour defects.

## 7. The traps

**Near-miss:** replace at with [] to make the exception disappear. The access remains invalid and now has undefined behaviour. The example’s stable diagnostic is `index outside vector`; library what() messages vary. Sanitizers only report executed failures, so exercise the failing input rather than merely compiling with the flags.

## 8. Say it out loud

**How it gets asked:** “Your program crashes. Walk me through how you find the bug.” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I build with symbols, reproduce the input, and stop at the invalid operation. I use backtrace and inspect sizes and lifetimes. If memory corruption is suspected, I run a sanitizer build to locate an executed invalid access. I do not treat a missing crash as correctness. After repair I rerun the original input and nearby boundary cases, then remove temporary debugging changes.

**Follow-ups**

1. **Does a sanitizer prove memory safety?** No. It checks selected operations on paths that execute.

2. **Why use at in a reproducer?** It gives a defined out_of_range failure for a bad index.

3. **What does a segmentation fault tell you?** An access failed; the invalid pointer may have been created much earlier.

**Model answer:** GDB exposes call frames and local values. Sanitizers instrument a program to detect selected memory errors and undefined behaviour during execution. An unchecked access is not a fix for a bounds error.

## 9. Recall card

- Keep debug symbols when investigating a failure.
- Inspect sizes and lifetimes at the failing access.
- Sanitizers need the relevant input to execute.
- An unchecked access is not a fix for a bounds error.

Further reading: [Official reference](https://clang.llvm.org/docs/AddressSanitizer.html).
