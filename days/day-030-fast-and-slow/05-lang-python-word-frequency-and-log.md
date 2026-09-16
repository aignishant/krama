---
day: 30
track: lang-python
title: "Word frequency and log summariser in Python"
theme: "Mini project 2: a text analyser"
phase: "Languages: advanced features"
status: written
---

# Day 030 · Python — Word frequency and log summariser in Python

**Today's theme:** Mini project 2: a text analyser

**After today you can:** You can build a tool that reads a large file, counts and reports, in all three, with tests.

**The interviewer asks it as:** *How would you find the top 10 words in a 2 GB file?*

## 1. What this is, and why it matters

A streaming text analyser reads incrementally, normalises according to an explicit policy, and stores one count per distinct word.

You use this when discussing mini project 2: a text analyser in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Priya helps count the food requests arriving for a family gathering. The messages come throughout the afternoon. She could wait until everyone has replied and then reread the whole conversation, but the list is long and she is likely to miss something.

Instead, she keeps a running count for each dish. When a new request arrives, she reads it once and updates that dish’s count. She does not need to keep another copy of every message merely to know how many people asked for rice.

Her brother sends Rice with a capital letter. Her aunt writes rice with a full stop. Priya decides that these should count together and tells everyone the rule. She also notices that sweet rice and plain rice are different dishes. Removing every difference would be just as misleading as keeping every spelling difference.

At the end, she sorts the dish names by how often they were requested. Two dishes have the same count, so she uses their names to decide which to display first. This gives the same answer each time someone opens the summary.

For a second view, she groups delivery messages by whether they say ready or delayed. She does not mix those labels into the dish counts. Both views read messages one at a time, but they answer different questions. Before sharing either summary, she tries a few small examples whose answers she can count aloud.

## 3. The idea in plain English

Priya’s running totals become Counter entries. The project policy is intentionally narrow: a word is a maximal run of ASCII letters A–Z or a–z, compared in lowercase. This makes the three versions directly comparable; it is not a universal definition of a human word.

For B input characters and U unique words, scanning is O(B). Sorting the U entries takes O(U log U) comparisons, with string-comparison cost depending on shared prefixes. Extra storage includes the dictionary’s distinct words, sorted entries, and the largest input line. A 2 GB file can still have too many distinct words for memory; streaming alone does not solve that.

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

```python
for line in stream:
    counts.update(word.lower() for word in re.findall(r"[A-Za-z]+", line))
```

Normalise according to a documented token policy.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from collections import Counter
from collections.abc import Iterable
import re
import sys

def analyse(stream: Iterable[str], mode: str = "words") -> list[tuple[str, int]]:
    counts: Counter[str] = Counter()
    if mode not in {"words", "logs"}:
        raise ValueError("mode must be words or logs")
    for line in stream:
        if mode == "words":
            counts.update(word.lower() for word in re.findall(r"[A-Za-z]+", line))
        else:
            fields = line.split(maxsplit=1)
            severity = fields[0] if fields else ""
            valid = len(fields) == 2 and fields[1].strip() and severity in {"INFO", "WARN", "ERROR"}
            counts[severity if valid else "MALFORMED"] += 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:10]

def self_test() -> None:
    assert analyse(["Tea tea, RICE!"]) == [("tea", 2), ("rice", 1)]
    assert analyse([]) == []
    assert analyse(["b a"]) == [("a", 1), ("b", 1)]
    assert analyse(["x" * 100000]) == [("x" * 100000, 1)]
    assert analyse(["INFO ready", "ERROR failed", "bad"], "logs") == [
        ("ERROR", 1), ("INFO", 1), ("MALFORMED", 1)
    ]

def main() -> None:
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        print("tests passed")
        return
    mode = sys.argv[1] if len(sys.argv) == 2 else "words"
    if len(sys.argv) > 2:
        raise ValueError("usage: main.py [words|logs|--self-test]")
    for name, count in analyse(sys.stdin, mode):
        print(name, count)

if __name__ == "__main__":
    main()
```

**Check the result:** The built-in checks pass. Feed `Tea tea, RICE!` on standard input, then end input (Ctrl+Z followed by Enter on Windows). Output is `tea 2` then `rice 1`. You can also redirect a UTF-8 text file to stdin in a shell that supports it.

Run `python main.py --self-test` to execute the included empty-input, tie, long-token, final-token, and log-mode checks; it prints `tests passed`. Run `python main.py logs` and enter `INFO ready`, `ERROR failed`, and `bad` on separate lines, then EOF. The report is `ERROR 1`, `INFO 1`, and `MALFORMED 1`. Run `python main.py words` for word mode. In PowerShell, use `.\demo.exe` instead of `./demo` for the C++ executable.

## 6. How the other two languages do it

**Go**

```go
line, err := reader.ReadString('\n')
// Process line before deciding whether err is io.EOF.
```

A Go text analyser can stream with bufio.Reader, maintain a map of counts, and sort an explicit result slice for deterministic output.

**C++**

```cpp
if (!word.empty()) {
    ++counts[word];
    word.clear();
}
```

A C++ text analyser can read one character at a time, count completed words, and sort results without retaining the whole input.

The three implementations use the same explicit ASCII-word policy and stable tie-break. Test identical input against all three before generalising to multilingual text.

## 7. The traps

**Near-miss:** sys.stdin.read() materialises the entire file before counting. Another is sorting only by count and getting unstable tie ordering across versions. Opening a missing path raises `FileNotFoundError`; stdin read errors must also be reported, not treated as a clean end. The ASCII policy splits accented words, so do not present it as Unicode-aware tokenisation.

## 8. Say it out loud

**How it gets asked:** “How would you find the top 10 words in a 2 GB file?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I state the token rule first, process one line at a time, and keep a count per distinct normalised word. I sort with an explicit tie-break so tests are repeatable. Streaming bounds the input buffer, not the vocabulary. If the distinct set is too large I partition counts onto disk or use an external aggregation stage. For log summaries I define a separate grammar and count rejected lines rather than silently accepting them.

**Follow-ups**

1. **Does streaming imply constant memory?** No. The number and lengths of distinct words still matter.

2. **How do you make ties deterministic?** Sort equal counts by a documented secondary key such as word.

3. **How would log mode differ?** Parse a stated severity field and count invalid records separately.

**Model answer:** A streaming text analyser reads incrementally, normalises according to an explicit policy, and stores one count per distinct word. Streaming input does not bound the size of the aggregation state.

## 9. Recall card

- Normalise according to a documented token policy.
- Count distinct words while reading incrementally.
- Use an explicit tie-break.
- Streaming input does not bound the size of the aggregation state.

Further reading: [Official reference](https://docs.python.org/3.12/library/collections.html#collections.Counter).
