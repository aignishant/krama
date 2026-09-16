---
day: 30
track: lang-go
title: "Word frequency and log summariser in Go"
theme: "Mini project 2: a text analyser"
phase: "Languages: advanced features"
status: written
---

# Day 030 · Go — Word frequency and log summariser in Go

**Today's theme:** Mini project 2: a text analyser

**After today you can:** You can build a tool that reads a large file, counts and reports, in all three, with tests.

**The interviewer asks it as:** *How would you find the top 10 words in a 2 GB file?*

## 1. What this is, and why it matters

A Go text analyser can stream with bufio.Reader, maintain a map of counts, and sort an explicit result slice for deterministic output.

You use this when discussing mini project 2: a text analyser in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Priya helps count the food requests arriving for a family gathering. The messages come throughout the afternoon. She could wait until everyone has replied and then reread the whole conversation, but the list is long and she is likely to miss something.

Instead, she keeps a running count for each dish. When a new request arrives, she reads it once and updates that dish’s count. She does not need to keep another copy of every message merely to know how many people asked for rice.

Her brother sends Rice with a capital letter. Her aunt writes rice with a full stop. Priya decides that these should count together and tells everyone the rule. She also notices that sweet rice and plain rice are different dishes. Removing every difference would be just as misleading as keeping every spelling difference.

At the end, she sorts the dish names by how often they were requested. Two dishes have the same count, so she uses their names to decide which to display first. This gives the same answer each time someone opens the summary.

For a second view, she groups delivery messages by whether they say ready or delayed. She does not mix those labels into the dish counts. Both views read messages one at a time, but they answer different questions. Before sharing either summary, she tries a few small examples whose answers she can count aloud.

## 3. The idea in plain English

Priya’s totals become a map[string]int. The reader handles one line at a time and processes any bytes returned before io.EOF. That detail matters for a final line without a newline.

Scanner is convenient but has a token-size limit unless configured. Reader.ReadString avoids that fixed scanner limit but still retains a whole line, so an enormous line consumes enormous memory. The regular expression uses the same ASCII-word policy as Python. Map iteration order is unspecified; sorting by count and then word is required for a stable report. The counting state grows with distinct words, not merely the buffer size.

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

```go
line, err := reader.ReadString('\n')
// Process line before deciding whether err is io.EOF.
```

Process returned data before handling EOF.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "bufio"
    "fmt"
    "io"
    "os"
    "reflect"
    "regexp"
    "sort"
    "strings"
)

type Entry struct {
    Word string
    Count int
}

func analyse(input io.Reader, mode string) ([]Entry, error) {
    if mode != "words" && mode != "logs" {
        return nil, fmt.Errorf("mode must be words or logs")
    }
    reader := bufio.NewReader(input)
    words := regexp.MustCompile(`[A-Za-z]+`)
    counts := make(map[string]int)
    for {
        line, err := reader.ReadString('\n')
        if len(line) > 0 {
            if mode == "words" {
                for _, word := range words.FindAllString(line, -1) {
                    counts[strings.ToLower(word)]++
                }
            } else {
                fields := strings.Fields(line)
                severity := "MALFORMED"
                if len(fields) >= 2 && (fields[0] == "INFO" || fields[0] == "WARN" || fields[0] == "ERROR") {
                    severity = fields[0]
                }
                counts[severity]++
            }
        }
        if err == io.EOF { break }
        if err != nil { return nil, err }
    }
    result := make([]Entry, 0, len(counts))
    for word, count := range counts { result = append(result, Entry{word, count}) }
    sort.Slice(result, func(i, j int) bool {
        if result[i].Count != result[j].Count { return result[i].Count > result[j].Count }
        return result[i].Word < result[j].Word
    })
    if len(result) > 10 { result = result[:10] }
    return result, nil
}

func selfTest() error {
    cases := []struct {
        input, mode string
        want []Entry
    }{
        {"Tea tea, RICE!", "words", []Entry{{"tea", 2}, {"rice", 1}}},
        {"", "words", []Entry{}},
        {"b a", "words", []Entry{{"a", 1}, {"b", 1}}},
        {strings.Repeat("x", 100000), "words", []Entry{{strings.Repeat("x", 100000), 1}}},
        {"INFO ready\nERROR failed\nbad", "logs", []Entry{{"ERROR", 1}, {"INFO", 1}, {"MALFORMED", 1}}},
    }
    for _, test := range cases {
        got, err := analyse(strings.NewReader(test.input), test.mode)
        if err != nil { return err }
        if !reflect.DeepEqual(got, test.want) { return fmt.Errorf("unexpected result: %v", got) }
    }
    return nil
}

func run() error {
    if len(os.Args) == 2 && os.Args[1] == "--self-test" {
        if err := selfTest(); err != nil { return err }
        fmt.Println("tests passed")
        return nil
    }
    mode := "words"
    if len(os.Args) == 2 { mode = os.Args[1] }
    if len(os.Args) > 2 { return fmt.Errorf("usage: main [words|logs|--self-test]") }
    result, err := analyse(os.Stdin, mode)
    if err != nil { return err }
    for _, item := range result { fmt.Println(item.Word, item.Count) }
    return nil
}

func main() {
    if err := run(); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

**Check the result:** Input `Tea tea, RICE!` followed by EOF prints `tea 2` and `rice 1`. Empty input prints nothing; `b a` prints `a 1` then `b 1`. Test the same input with and without a trailing newline.

Run `go run main.go --self-test` to execute the included empty-input, tie, long-token, final-token, and log-mode checks; it prints `tests passed`. Run `go run main.go logs` and enter `INFO ready`, `ERROR failed`, and `bad` on separate lines, then EOF. The report is `ERROR 1`, `INFO 1`, and `MALFORMED 1`. Run `go run main.go words` for word mode. In PowerShell, use `.\demo.exe` instead of `./demo` for the C++ executable.

## 6. How the other two languages do it

**Python**

```python
for line in stream:
    counts.update(word.lower() for word in re.findall(r"[A-Za-z]+", line))
```

A streaming text analyser reads incrementally, normalises according to an explicit policy, and stores one count per distinct word.

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

**Near-miss:** break on any err before processing line and lose the final non-newline-terminated text. A Scanner-based alternative must inspect scanner.Err(); oversized tokens otherwise look like early completion. Its diagnostic is `bufio.Scanner: token too long`. This Reader version has no fixed scanner token limit but does allocate for long lines.

## 8. Say it out loud

**How it gets asked:** “How would you find the top 10 words in a 2 GB file?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate reading, token policy, counting, and reporting. I process partial data returned with EOF, propagate other read errors, and sort the map’s entries before printing. With B bytes and U unique words, scanning and counting are roughly O(B) expected work, followed by O(U log U) comparisons. Storage grows with vocabulary and line length. For strict memory limits I need chunked tokenisation and possibly external aggregation.

**Follow-ups**

1. **Does streaming imply constant memory?** No. A map of unique words and a long line can both grow.

2. **Why process data before EOF?** A read may return the final data together with EOF.

3. **How would log mode differ?** Parse each line’s severity under an explicit grammar and count malformed records.

**Model answer:** A Go text analyser can stream with bufio.Reader, maintain a map of counts, and sort an explicit result slice for deterministic output. Read errors must not masquerade as a successful partial report.

## 9. Recall card

- Process returned data before handling EOF.
- Map iteration does not define report order.
- Account for the largest line and vocabulary.
- Read errors must not masquerade as a successful partial report.

Further reading: [Official reference](https://pkg.go.dev/bufio#Reader.ReadString).
