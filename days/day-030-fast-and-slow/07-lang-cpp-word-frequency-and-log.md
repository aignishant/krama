---
day: 30
track: lang-cpp
title: "Word frequency and log summariser in C++"
theme: "Mini project 2: a text analyser"
phase: "Languages: advanced features"
status: written
---

# Day 030 · C++ — Word frequency and log summariser in C++

**Today's theme:** Mini project 2: a text analyser

**After today you can:** You can build a tool that reads a large file, counts and reports, in all three, with tests.

**The interviewer asks it as:** *How would you find the top 10 words in a 2 GB file?*

## 1. What this is, and why it matters

A C++ text analyser can read one character at a time, count completed words, and sort results without retaining the whole input.

You use this when discussing mini project 2: a text analyser in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Priya helps count the food requests arriving for a family gathering. The messages come throughout the afternoon. She could wait until everyone has replied and then reread the whole conversation, but the list is long and she is likely to miss something.

Instead, she keeps a running count for each dish. When a new request arrives, she reads it once and updates that dish’s count. She does not need to keep another copy of every message merely to know how many people asked for rice.

Her brother sends Rice with a capital letter. Her aunt writes rice with a full stop. Priya decides that these should count together and tells everyone the rule. She also notices that sweet rice and plain rice are different dishes. Removing every difference would be just as misleading as keeping every spelling difference.

At the end, she sorts the dish names by how often they were requested. Two dishes have the same count, so she uses their names to decide which to display first. This gives the same answer each time someone opens the summary.

For a second view, she groups delivery messages by whether they say ready or delayed. She does not mix those labels into the dish counts. Both views read messages one at a time, but they answer different questions. Before sharing either summary, she tries a few small examples whose answers she can count aloud.

## 3. The idea in plain English

Priya’s current request becomes the current token. Letters extend that token; a separator commits it to the map. EOF must commit any last token too. The policy accepts ASCII letters only and converts A–Z manually, so locale-dependent character classification does not change the result.

The input buffer is one growing token rather than a full line. Distinct words still occupy the map. For B characters and U unique words, the ordered map adds O(log U) key comparisons per completed word; sorting the U report entries adds O(U log U) comparisons. String comparisons also depend on word length. A production tool needs an explicit maximum token length or another policy for a maliciously long uninterrupted word.

Log mode accepts one record per line: an uppercase severity INFO, WARN, or ERROR, followed by whitespace and a nonempty message. Unknown severity, missing message, and blank lines count as MALFORMED. The common cross-language log format uses ASCII whitespace. The report uses the same count-descending, name-ascending ordering as word mode.

## 4. The picture

```text
read one line -> normalise -> count -> discard line
                              |
                         distinct words -> sort report
```

Streaming input avoids retaining the whole file, but distinct-word counts still occupy memory.

## 5. The code, built step by step

First isolate the important operation:

```cpp
if (!word.empty()) {
    ++counts[word];
    word.clear();
}
```

Flush the final token at EOF.

The complete example follows. Use a C++20 compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra -pthread main.cpp -o demo`, then run `./demo` (`.\demo.exe` in PowerShell).

```cpp
#include <algorithm>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Report = std::vector<std::pair<std::string, long long>>;
Report analyse(std::istream& input, const std::string& mode) {
    if (mode != "words" && mode != "logs") throw std::invalid_argument("mode must be words or logs");
    std::map<std::string, long long> counts;
    if (mode == "words") {
        std::string word;
        auto finish = [&] { if (!word.empty()) { ++counts[word]; word.clear(); } };
        char ch;
        while (input.get(ch)) {
            if (ch >= 'A' && ch <= 'Z') ch = static_cast<char>(ch - 'A' + 'a');
            if (ch >= 'a' && ch <= 'z') word.push_back(ch);
            else finish();
        }
        finish();
    } else {
        std::string line;
        while (std::getline(input, line)) {
            std::istringstream fields(line);
            std::string severity, message;
            bool valid = static_cast<bool>(fields >> severity >> message);
            valid = valid && (severity == "INFO" || severity == "WARN" || severity == "ERROR");
            ++counts[valid ? severity : "MALFORMED"];
        }
    }
    if (input.bad() || !input.eof()) throw std::runtime_error("input read failed");
    Report entries(counts.begin(), counts.end());
    std::sort(entries.begin(), entries.end(), [](const auto& left, const auto& right) {
        if (left.second != right.second) return left.second > right.second;
        return left.first < right.first;
    });
    if (entries.size() > 10) entries.resize(10);
    return entries;
}

void self_test() {
    auto check = [](const std::string& text, const std::string& mode, const Report& expected) {
        std::istringstream input(text);
        if (analyse(input, mode) != expected) throw std::runtime_error("test failed");
    };
    check("Tea tea, RICE!", "words", {{"tea", 2}, {"rice", 1}});
    check("", "words", {});
    check("b a", "words", {{"a", 1}, {"b", 1}});
    check(std::string(100000, 'x'), "words", {{std::string(100000, 'x'), 1}});
    check("INFO ready\nERROR failed\nbad", "logs", {{"ERROR", 1}, {"INFO", 1}, {"MALFORMED", 1}});
}

int main(int argc, char** argv) {
    try {
        if (argc == 2 && std::string(argv[1]) == "--self-test") {
            self_test(); std::cout << "tests passed\n"; return 0;
        }
        if (argc > 2) throw std::invalid_argument("usage: demo [words|logs|--self-test]");
        for (const auto& [name, count] : analyse(std::cin, argc == 2 ? argv[1] : "words"))
            std::cout << name << ' ' << count << '\n';
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n'; return 1;
    }
}
```

**Check the result:** Input `Tea tea, RICE!` produces `tea 2` and `rice 1`. Verify empty input, `b a` producing a before b, and a final word without a newline.

Run `./demo --self-test` to execute the included empty-input, tie, long-token, final-token, and log-mode checks; it prints `tests passed`. Run `./demo logs` and enter `INFO ready`, `ERROR failed`, and `bad` on separate lines, then EOF. The report is `ERROR 1`, `INFO 1`, and `MALFORMED 1`. Run `./demo words` for word mode. In PowerShell, use `.\demo.exe` instead of `./demo` for the C++ executable.

## 6. How the other two languages do it

**Python**

```python
for line in stream:
    counts.update(word.lower() for word in re.findall(r"[A-Za-z]+", line))
```

A streaming text analyser reads incrementally, normalises according to an explicit policy, and stores one count per distinct word.

**Go**

```go
line, err := reader.ReadString('\n')
// Process line before deciding whether err is io.EOF.
```

A Go text analyser can stream with bufio.Reader, maintain a map of counts, and sort an explicit result slice for deterministic output.

The three implementations use the same explicit ASCII-word policy and stable tie-break. Test identical input against all three before generalising to multilingual text.

## 7. The traps

**Near-miss:** omit finish after EOF and lose the final word. Another is passing a negative signed char to std::tolower, which is undefined outside the permitted unsigned-char/EOF values. This ASCII implementation avoids that API. An input failure prints the explicit diagnostic `input read failed` and returns status 1.

## 8. Say it out loud

**How it gets asked:** “How would you find the top 10 words in a 2 GB file?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I scan characters incrementally and flush the current token on separators and EOF. I make the ASCII policy explicit instead of promising full linguistic tokenisation. The ordered map stores counts and a sorted vector produces deterministic output. I check stream state to distinguish EOF from failure. If distinct tokens exceed memory, I need partitioned or external counting; replacing a full-file read with a loop alone is not enough.

**Follow-ups**

1. **Does streaming imply constant memory?** No. The current token and all distinct words still occupy storage.

2. **Why flush at EOF?** The final word may not be followed by a separator.

3. **How would log mode differ?** Read and validate records under a severity grammar rather than count every word.

**Model answer:** A C++ text analyser can read one character at a time, count completed words, and sort results without retaining the whole input. Bounded input buffering does not bound the dictionary of unique words.

## 9. Recall card

- Flush the final token at EOF.
- State the exact normalisation policy.
- Sort equal counts by word.
- Bounded input buffering does not bound the dictionary of unique words.

Further reading: [Official reference](https://eel.is/c++draft/istream.unformatted).
