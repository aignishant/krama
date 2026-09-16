---
day: 14
track: lang-cpp
title: "CMake, clang-format, and a src/include layout"
theme: "Formatters, linters, and a real project layout"
phase: "Languages: every language, every basic"
status: written
---

# Day 014 · C++ — CMake, clang-format, and a src/include layout

**Today's theme:** Formatters, linters, and a real project layout

**After today you can:** You can start a new project in each language from an empty folder, with formatting and dependencies working.

**The interviewer asks it as:** *How do you set up a new project so a teammate can build it on day one?*

---

## 1. What this is, and why it matters

CMake describes build targets and generates instructions for a chosen build system. A **target** is something to build, such as an executable or library. `clang-format` standardises C++ source layout. Neither tool installs a C++ compiler automatically.

Today you use formatters, linters, and a real project layout to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Farah invites her cousin to help bake a cake. She sends a photo of the finished cake and says it is easy. Her cousin arrives with flour, but the recipe needs a different kind. The measuring cup has no markings. The oven dial has a worn patch where the temperature should be. Farah knows what all these things mean because she uses them every week. Her cousin does not.

The following Saturday, Farah prepares differently. She saves a shopping list on her phone, including the exact sizes of the packets. She puts the bowls together and checks that the scales turn on. She explains which oven setting she uses and where the cake goes after baking. Her cousin can now repeat the work without asking a question at every step.

They also agree on a few small habits. Wash a spoon before using it for another ingredient. Put lids back immediately. Wipe the counter before measuring the next thing. These habits do not guarantee a good cake. They remove preventable confusion so both people can pay attention to the mixture.

At the end, Farah keeps the recipe and shopping list, but throws away the used packaging. Next week she wants the instructions and ingredients, not yesterday's mess. She asks her cousin to try again without help. If the cake only works when Farah stands beside the oven, the instructions are still missing something important.

## 3. The idea in plain English

CMake describes build targets and generates instructions for a chosen build system. A **target** is something to build, such as an executable or library. `clang-format` standardises C++ source layout. Neither tool installs a C++ compiler automatically.

Farah's recipe becomes a CMake file that lists the source files and language requirement. Keep generated build files in a separate `build` directory. An `include` directory can hold public headers while `src` holds implementations, but a single source file does not need unnecessary scaffolding.

The configure step, `cmake -S . -B build`, prepares the build directory. The build step, `cmake --build build --config Debug`, compiles and links. Multi-configuration generators commonly place the executable under `build/Debug`; single-configuration generators commonly place it directly under `build`. State that difference when documenting how to run it.

## 4. The picture

```text
source + declared requirements + tool settings
                       |
                       v
              fresh project environment
                /       |         \
               v        v          v
           format     checks     build/run
                       |            |
                       v            v
                  diagnostics   observed result
```

A fresh environment should reproduce the workflow from committed inputs. Formatting, diagnostics, and running the program answer different questions.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
int add(int left, int right) {
    return left + right;
}
```

Save this behaviour in the source file listed by the CMake target. The full program calls it from main, while the build configuration separately declares which source and language standard are required.

Create `src/main.cpp` with the complete program below, and this `CMakeLists.txt` at the project root:

```cmake
cmake_minimum_required(VERSION 3.20)
project(krama_tool LANGUAGES CXX)
add_executable(krama_tool src/main.cpp)
target_compile_features(krama_tool PRIVATE cxx_std_20)
```

Run `cmake -S . -B build`, then `cmake --build build --config Debug`. Run `./build/krama_tool` or the generated `.exe`, possibly under `build/Debug`. The [CMake tutorial](https://cmake.org/cmake/help/latest/guide/tutorial/index.html) describes the target-based build workflow.

The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>

int add(int left, int right) {
    return left + right;
}

int main() {
    const int total = add(2, 3);
    std::cout << total << '\n';
}
```

**Check the result:** The built executable prints `5`. Run `clang-format -i src/main.cpp` to format it, or `clang-format --dry-run --Werror src/main.cpp` to check its formatting.

## 6. How the other two languages do it

- **Python** — Declare project metadata and dependencies in pyproject.toml.
- **Go** — go.mod identifies a module and its requirements.
- **C++** — CMake describes targets and their requirements.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** create a new source file but omit it from the target. CMake does not infer that every file in your editor belongs in the executable. List the sources or add them with target_sources.

**Failure to reproduce:** declare `add` in a header but remove its definition from the built sources. A GNU linker reports `undefined reference to 'add(int, int)'`. This is a link problem, not a formatting problem. Read the command that failed before choosing which tool setting to change.

## 8. Say it out loud

**How it gets asked:** “How do you set up a new project so a teammate can build it on day one?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I declare an executable target and its C++ standard in CMake, keep generated output outside src, and document configure, build, and run commands. I use clang-format for consistent layout and compiler warnings for a different set of problems. I make build prerequisites explicit so a teammate does not need to reconstruct my machine's setup.

**Follow-ups**

1. **Is CMake the compiler?** No. It configures build rules that invoke a compiler and linker.

2. **Should build be committed?** Normally no; recreate it from source and build configuration.

3. **Where do public headers go?** Often include, with include paths attached to the target that publishes them.

**Model answer:** Save this behaviour in the source file listed by the CMake target. The full program calls it from main, while the build configuration separately declares which source and language standard are required. Document compiler prerequisites and the executable location.

## 9. Recall card

- CMake describes targets and their requirements.
- Configure into a separate build directory.
- Build invokes the selected compiler and linker.
- clang-format controls layout, not correctness.
- Document compiler prerequisites and the executable location.
