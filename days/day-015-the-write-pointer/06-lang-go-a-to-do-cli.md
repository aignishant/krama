---
day: 15
track: lang-go
title: "A to-do CLI in Go, saved as JSON"
theme: "Mini project 1: a to-do CLI"
phase: "Languages: every language, every basic"
status: written
---

# Day 015 · Go — A to-do CLI in Go, saved as JSON

**Today's theme:** Mini project 1: a to-do CLI

**After today you can:** You can build the same small tool in all three languages, run it, and say which one felt right for the job.

**The interviewer asks it as:** *Walk me through a small program you wrote. Why did you structure it that way?*

---

## 1. What this is, and why it matters

A command-line program reads arguments from `os.Args`. This tool implements `add TITLE`, `list`, and `done ID`, persisting a JSON list in `tasks.json`. **Struct tags** such as `json:"text"` tell the JSON encoder which field names to use.

Today you use mini project 1: a to-do cli to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Dev forgets to buy milk twice in one week. He starts saving errands on his phone. At first he writes one sentence: buy milk, collect the parcel, and call the plumber. The sentence is easy to read, but awkward to update. After collecting the parcel he accidentally removes the milk reminder too.

He tries again with separate entries. Each errand has its own place and a clear indication of whether it is finished. In the morning he adds milk. At lunch he looks at the list. In the evening he marks the parcel as done. These are three distinct actions, and each should leave the other entries alone.

The next morning he closes and reopens the phone's notes. The errands must still be there. Remembering them only while the screen stays open would defeat the purpose. He checks that a completed errand remains completed after reopening it.

His sister borrows the phone and accidentally removes part of the saved text. Dev does not want the app to respond by silently replacing everything with an empty list. That would turn a visible problem into lost errands. He wants it to stop and explain what it could not read.

By Sunday, Dev's requirements are clear: add one errand, show all errands, mark one finished, and retain the result between visits. He leaves shared family editing for later. One person using one phone is enough to make the first version useful and to give every action an observable result.

## 3. The idea in plain English

A command-line program reads arguments from `os.Args`. This tool implements `add TITLE`, `list`, and `done ID`, persisting a JSON list in `tasks.json`. **Struct tags** such as `json:"text"` tell the JSON encoder which field names to use.

Dev's errands become Task structs. Loading and saving return errors rather than pretending every failure is an empty task list. The decode struct uses pointer fields so a missing or null field can be distinguished from a legitimate empty string or false boolean. We then copy validated values into ordinary Task objects.

The list position is the ID, starting at one. That stays meaningful because this version does not delete or reorder tasks. It rewrites the whole small file after a valid mutation and assumes one writer. Direct rewriting can be interrupted; temporary-file replacement and coordination between writers belong in a stronger persistence design.

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

```go
number, err := strconv.Atoi(args[1])
if err != nil { return err }
if number < 1 || number > len(tasks) {
    return errors.New("task ID out of range")
}
tasks[number-1].Done = true
```

Conversion and bounds checks are separate failure points. Return either failure before changing the task. The run function returns save's error too, so main cannot report success when persistence failed.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.go`.

```go
package main

import (
    "bytes"
    "encoding/json"
    "errors"
    "fmt"
    "os"
    "strconv"
    "strings"
)

type Task struct {
    Text string `json:"text"`
    Done bool `json:"done"`
}

func load() ([]Task, error) {
    data, err := os.ReadFile("tasks.json")
    if errors.Is(err, os.ErrNotExist) { return []Task{}, nil }
    if err != nil { return nil, err }
    if bytes.Equal(bytes.TrimSpace(data), []byte("null")) {
        return nil, errors.New("invalid task store")
    }
    var raw []struct {
        Text *string `json:"text"`
        Done *bool `json:"done"`
    }
    if err := json.Unmarshal(data, &raw); err != nil { return nil, err }
    tasks := make([]Task, 0, len(raw))
    for _, item := range raw {
        if item.Text == nil || item.Done == nil {
            return nil, errors.New("invalid task store")
        }
        tasks = append(tasks, Task{Text: *item.Text, Done: *item.Done})
    }
    return tasks, nil
}

func save(tasks []Task) error {
    data, err := json.MarshalIndent(tasks, "", "  ")
    if err != nil { return err }
    return os.WriteFile("tasks.json", data, 0600)
}

func run(args []string) error {
    tasks, err := load()
    if err != nil { return err }
    if len(args) == 1 && args[0] == "list" {
        for number, task := range tasks {
            mark := " "
            if task.Done { mark = "x" }
            fmt.Printf("%d [%s] %s\n", number+1, mark, task.Text)
        }
        return nil
    }
    if len(args) == 2 && args[0] == "add" && strings.TrimSpace(args[1]) != "" {
        tasks = append(tasks, Task{Text: args[1]})
    } else if len(args) == 2 && args[0] == "done" {
        number, err := strconv.Atoi(args[1])
        if err != nil { return err }
        if number < 1 || number > len(tasks) { return errors.New("task ID out of range") }
        tasks[number-1].Done = true
    } else {
        return errors.New("usage: add TITLE | list | done ID")
    }
    return save(tasks)
}

func main() {
    if err := run(os.Args[1:]); err != nil {
        fmt.Fprintln(os.Stderr, "error:", err)
        os.Exit(1)
    }
}
```

**Check the result:** Run `go run main.go add "buy milk"`, `go run main.go list`, `go run main.go done 1`, and `go run main.go list` in a fresh directory. The final list is `1 [x] buy milk`.

## 6. How the other two languages do it

- **Python** — Read command arguments and validate the requested operation.
- **Go** — Parse command arguments before applying a mutation.
- **C++** — Use a real JSON parser and serializer.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** ignore the error returned by WriteFile and report success. The next process then loads stale data. Return each error to main, which prints it and exits unsuccessfully.

**Failure to reproduce:** run `go run main.go done 0` after adding a task. The application prints `error: task ID out of range`; the go run wrapper may add an exit-status line. The saved file is unchanged. Also try a store containing `[{}]`: the explicit shape check reports `invalid task store` rather than silently constructing an empty task.

## 8. Say it out loud

**How it gets asked:** “Walk me through a small program you wrote. Why did you structure it that way?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I separate loading, saving, and command handling. Every fallible operation returns an error to one boundary in main. I validate both JSON syntax and required fields, then check the ID before changing a task. Listing is read-only. The file format is simple and portable, but whole-file direct writes do not solve crash durability or simultaneous writers.

**Follow-ups**

1. **Why export Task fields?** encoding/json accesses exported struct fields.

2. **Why pointer fields while decoding?** They distinguish absent or null data from ordinary zero values.

3. **Why not os.Exit inside load?** Returning an error keeps the helper reusable and lets callers control cleanup and reporting.

**Model answer:** Conversion and bounds checks are separate failure points. Return either failure before changing the task. The run function returns save's error too, so main cannot report success when persistence failed. One small file still needs an explicit concurrency policy.

## 9. Recall card

- Parse command arguments before applying a mutation.
- Validate JSON fields, not just JSON syntax.
- Return read, decode, encode, and write errors.
- Persist a valid mutation; listing does not save.
- One small file still needs an explicit concurrency policy.
