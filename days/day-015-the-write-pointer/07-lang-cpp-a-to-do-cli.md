---
day: 15
track: lang-cpp
title: "A to-do CLI in C++, saved as JSON"
theme: "Mini project 1: a to-do CLI"
phase: "Languages: every language, every basic"
status: written
---

# Day 015 · C++ — A to-do CLI in C++, saved as JSON

**Today's theme:** Mini project 1: a to-do CLI

**After today you can:** You can build the same small tool in all three languages, run it, and say which one felt right for the job.

**The interviewer asks it as:** *Walk me through a small program you wrote. Why did you structure it that way?*

---

## 1. What this is, and why it matters

A C++ CLI receives arguments through `argc` and `argv`. This program supports `add TITLE`, `list`, and `done ID`. The standard library has no general JSON parser, so the example declares a dependency on nlohmann/json rather than inventing a parser that fails on escaped text.

Today you use mini project 1: a to-do cli to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Dev forgets to buy milk twice in one week. He starts saving errands on his phone. At first he writes one sentence: buy milk, collect the parcel, and call the plumber. The sentence is easy to read, but awkward to update. After collecting the parcel he accidentally removes the milk reminder too.

He tries again with separate entries. Each errand has its own place and a clear indication of whether it is finished. In the morning he adds milk. At lunch he looks at the list. In the evening he marks the parcel as done. These are three distinct actions, and each should leave the other entries alone.

The next morning he closes and reopens the phone's notes. The errands must still be there. Remembering them only while the screen stays open would defeat the purpose. He checks that a completed errand remains completed after reopening it.

His sister borrows the phone and accidentally removes part of the saved text. Dev does not want the app to respond by silently replacing everything with an empty list. That would turn a visible problem into lost errands. He wants it to stop and explain what it could not read.

By Sunday, Dev's requirements are clear: add one errand, show all errands, mark one finished, and retain the result between visits. He leaves shared family editing for later. One person using one phone is enough to make the first version useful and to give every action an observable result.

## 3. The idea in plain English

A C++ CLI receives arguments through `argc` and `argv`. This program supports `add TITLE`, `list`, and `done ID`. The standard library has no general JSON parser, so the example declares a dependency on nlohmann/json rather than inventing a parser that fails on escaped text.

Dev's errands become JSON objects checked against the expected `text` and `done` fields. File streams use RAII for closing, while the code checks read and write failures explicitly. A missing file is the first-run case; malformed JSON or an unreadable existing file is an error.

The program uses one-based position IDs and keeps their meaning by never deleting or reordering tasks. It reads the complete small file, changes one task, then rewrites it. That makes the flow easy to inspect, but assumes one writer and is not crash-safe storage. Temporary-file replacement and writer coordination are separate extensions.

## 4. The picture

```text
arguments ---> load tasks.json ---> validate shape
                                      |
                       +--------------+-------------+
                       |                            |
                       v                            v
                    list                       add / done
                       |                            |
                       v                            v
                   print only                validate operation
                                                    |
                                                    v
                                             mutate ---> save

read / parse / validation failure ---> report error; no save
```

Only a valid mutation reaches save. In particular, a damaged existing store must not be silently replaced with an empty one.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```cpp
std::size_t consumed = 0;
int number = std::stoi(argument, &consumed);
```

stoi reports where parsing stopped as well as the parsed number. Check that consumed covers the whole argument, then check the one-based bounds. That rejects a numeric prefix such as 1oops instead of silently completing task 1.

Save the program as `main.cpp`. With CMake, a C++20 compiler, and network access for the first configuration, create this `CMakeLists.txt`:

```cmake
cmake_minimum_required(VERSION 3.20)
project(todo LANGUAGES CXX)
include(FetchContent)
FetchContent_Declare(json
  URL https://github.com/nlohmann/json/releases/download/v3.11.3/json.tar.xz)
FetchContent_MakeAvailable(json)
add_executable(todo main.cpp)
target_compile_features(todo PRIVATE cxx_std_20)
target_link_libraries(todo PRIVATE nlohmann_json::nlohmann_json)
```

This pins a known release rather than following a moving branch. The library documents its imported target and [CMake integration](https://json.nlohmann.me/integration/cmake/).

The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <cctype>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <iterator>
#include <stdexcept>
#include <string>
#include <nlohmann/json.hpp>

using Json = nlohmann::json;

Json load() {
    if (!std::filesystem::exists("tasks.json")) return Json::array();
    std::ifstream input("tasks.json");
    if (!input) throw std::runtime_error("cannot read task store");
    std::string text((std::istreambuf_iterator<char>(input)), {});
    if (input.bad()) throw std::runtime_error("cannot read task store");
    auto tasks = Json::parse(text);
    if (!tasks.is_array()) throw std::runtime_error("invalid task store");
    for (const auto& task : tasks) {
        if (!task.is_object() || !task.contains("text") || !task.contains("done")
            || !task.at("text").is_string() || !task.at("done").is_boolean())
            throw std::runtime_error("invalid task store");
    }
    return tasks;
}

void save(const Json& tasks) {
    const auto text = tasks.dump(2);
    std::ofstream output("tasks.json");
    if (!output) throw std::runtime_error("cannot write task store");
    output << text << '\n';
    output.close();
    if (!output) throw std::runtime_error("cannot write task store");
}

void run(int argc, char* argv[]) {
    auto tasks = load();
    std::string command = argc > 1 ? argv[1] : "";
    if (argc == 2 && command == "list") {
        for (std::size_t i = 0; i < tasks.size(); ++i) {
            const auto& task = tasks.at(i);
            std::cout << i + 1 << " [" << (task.at("done").get<bool>() ? "x" : " ")
                      << "] " << task.at("text").get<std::string>() << '\n';
        }
        return;
    }
    if (argc == 3 && command == "add") {
        std::string title = argv[2];
        bool has_text = false;
        for (unsigned char ch : title) if (!std::isspace(ch)) has_text = true;
        if (!has_text) throw std::runtime_error("title must not be blank");
        tasks.push_back({{"text", title}, {"done", false}});
    } else if (argc == 3 && command == "done") {
        std::string argument = argv[2];
        std::size_t consumed = 0;
        int number = std::stoi(argument, &consumed);
        if (consumed != argument.size() || number < 1
            || static_cast<std::size_t>(number) > tasks.size())
            throw std::runtime_error("task ID out of range");
        tasks.at(number - 1)["done"] = true;
    } else {
        throw std::runtime_error("usage: add TITLE | list | done ID");
    }
    save(tasks);
}

int main(int argc, char* argv[]) {
    try { run(argc, argv); }
    catch (const std::exception& error) {
        std::cerr << "error: " << error.what() << '\n';
        return 1;
    }
}
```

**Check the result:** Build with the CMake commands from day 014. Run the resulting `todo` executable with `add "buy milk"`, `list`, `done 1`, and `list`. The last invocation prints `1 [x] buy milk`. Use a fresh working directory for this language's store.

## 6. How the other two languages do it

- **Python** — Read command arguments and validate the requested operation.
- **Go** — Parse command arguments before applying a mutation.
- **C++** — Use a real JSON parser and serializer.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** concatenate quotation marks around a title to produce JSON yourself. A title containing a quote or backslash breaks that approach. Let the JSON library encode and decode strings.

**Failure to reproduce:** with one task saved, run `todo done 0` using your executable's path. The application prints `error: task ID out of range` and exits with status 1 without saving. A store containing `{}` instead of a list reports `error: invalid task store`. Never treat either failure as permission to discard the file.

## 8. Say it out loud

**How it gets asked:** “Walk me through a small program you wrote. Why did you structure it that way?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I use a declared JSON dependency, validate the saved shape, and keep load, command handling, and save separate. RAII manages stream lifetimes, but I still check operation failures. I validate the whole ID rather than accepting a numeric prefix. The prototype is a single-writer local tool; it makes no claim that rewriting one file is a durable concurrent database.

**Follow-ups**

1. **Why check consumed after stoi?** stoi can parse a numeric prefix such as 1 in 1oops.

2. **Does RAII guarantee the write succeeded?** No. It manages lifetime; the stream state still needs checking.

3. **Why declare the JSON dependency?** A fresh build must know where the header comes from and which version is intended.

**Model answer:** stoi reports where parsing stopped as well as the parsed number. Check that consumed covers the whole argument, then check the one-based bounds. That rejects a numeric prefix such as 1oops instead of silently completing task 1. Direct whole-file rewriting assumes one writer and can be interrupted.

## 9. Recall card

- Use a real JSON parser and serializer.
- Check the task-list schema after parsing.
- Validate IDs and commands before saving.
- RAII closes streams; check their failure state too.
- Direct whole-file rewriting assumes one writer and can be interrupted.
