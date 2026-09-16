---
day: 15
track: lang-python
title: "A to-do CLI in Python, saved as JSON"
theme: "Mini project 1: a to-do CLI"
phase: "Languages: every language, every basic"
status: written
---

# Day 015 · Python — A to-do CLI in Python, saved as JSON

**Today's theme:** Mini project 1: a to-do CLI

**After today you can:** You can build the same small tool in all three languages, run it, and say which one felt right for the job.

**The interviewer asks it as:** *Walk me through a small program you wrote. Why did you structure it that way?*

---

## 1. What this is, and why it matters

A **CLI**, or command-line interface, reads an operation and arguments from the terminal. This program supports `add TITLE`, `list`, and `done ID`. **JSON** is a text format for values such as lists, objects, strings, numbers, and booleans. Here the saved value is a list of objects containing `text` and `done`.

Today you use mini project 1: a to-do cli to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Dev forgets to buy milk twice in one week. He starts saving errands on his phone. At first he writes one sentence: buy milk, collect the parcel, and call the plumber. The sentence is easy to read, but awkward to update. After collecting the parcel he accidentally removes the milk reminder too.

He tries again with separate entries. Each errand has its own place and a clear indication of whether it is finished. In the morning he adds milk. At lunch he looks at the list. In the evening he marks the parcel as done. These are three distinct actions, and each should leave the other entries alone.

The next morning he closes and reopens the phone's notes. The errands must still be there. Remembering them only while the screen stays open would defeat the purpose. He checks that a completed errand remains completed after reopening it.

His sister borrows the phone and accidentally removes part of the saved text. Dev does not want the app to respond by silently replacing everything with an empty list. That would turn a visible problem into lost errands. He wants it to stop and explain what it could not read.

By Sunday, Dev's requirements are clear: add one errand, show all errands, mark one finished, and retain the result between visits. He leaves shared family editing for later. One person using one phone is enough to make the first version useful and to give every action an observable result.

## 3. The idea in plain English

A **CLI**, or command-line interface, reads an operation and arguments from the terminal. This program supports `add TITLE`, `list`, and `done ID`. **JSON** is a text format for values such as lists, objects, strings, numbers, and booleans. Here the saved value is a list of objects containing `text` and `done`.

Dev's independent errands become dictionaries in a list. Separate loading, saving, and command dispatch so failures have clear boundaries. A missing store means this is the first run; malformed data is an error, not an empty list. Validate the saved shape because valid JSON can still be the wrong data for this application.

IDs are one-based positions, safe for this small version because it never deletes or reorders tasks. Save only after a valid mutating command. Direct rewriting is a teaching simplification: a crash during writing can damage the file. A temporary file plus replacement is an improvement, while concurrent writers require further coordination.

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

```python
if not 1 <= number <= len(tasks):
    raise ValueError("task ID out of range")
tasks[number - 1]["done"] = True
```

Validate the one-based ID before converting it to the list's zero-based position. ID 0 must not become Python's -1 and accidentally select the last task. Only after command validation does main call save.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
import json
import sys
from pathlib import Path
from typing import TypedDict, cast

class Task(TypedDict):
    text: str
    done: bool

STORE = Path("tasks.json")

def load() -> list[Task]:
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    if not isinstance(data, list) or any(
        not isinstance(item, dict)
        or not isinstance(item.get("text"), str)
        or not isinstance(item.get("done"), bool)
        for item in data
    ):
        raise ValueError("invalid task store")
    return cast(list[Task], data)

def save(tasks: list[Task]) -> None:
    STORE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")

def main(args: list[str]) -> None:
    tasks = load()
    if len(args) == 1 and args[0] == "list":
        for number, task in enumerate(tasks, 1):
            mark = "x" if task["done"] else " "
            print(f"{number} [{mark}] {task['text']}")
        return
    if len(args) == 2 and args[0] == "add" and args[1].strip():
        tasks.append({"text": args[1], "done": False})
    elif len(args) == 2 and args[0] == "done":
        number = int(args[1])
        if not 1 <= number <= len(tasks):
            raise ValueError("task ID out of range")
        tasks[number - 1]["done"] = True
    else:
        raise ValueError("usage: add TITLE | list | done ID")
    save(tasks)

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        sys.exit(1)
```

**Check the result:** In a fresh directory run `python main.py add "buy milk"`, `python main.py list`, `python main.py done 1`, then `python main.py list`. The list changes from `1 [ ] buy milk` to `1 [x] buy milk`. The file is relative to your working directory.

## 6. How the other two languages do it

- **Python** — Read command arguments and validate the requested operation.
- **Go** — Parse command arguments before applying a mutation.
- **C++** — Use a real JSON parser and serializer.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** catch every loading error and return an empty list. A subsequent add overwrites an unreadable or malformed store. Catch only FileNotFoundError for the first-run case; let other failures reach the error boundary.

**Failure to reproduce:** after adding one task, run `python main.py done 0`. The exact application message is `error: task ID out of range`, and the process exits unsuccessfully without saving. JSON syntax errors are ValueError subclasses and are also reported rather than erased.

## 8. Say it out loud

**How it gets asked:** “Walk me through a small program you wrote. Why did you structure it that way?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I use one JSON list, load it at the beginning of each command, validate before modifying it, and save after a successful add or done operation. Listing never writes. I distinguish a missing file from a damaged file. The prototype assumes one writer and stable list positions; durable replacement and concurrent editing are separate improvements.

**Follow-ups**

1. **Why not save after list?** It changes nothing and should not risk a write failure.

2. **What if someone deletes tasks later?** Position IDs become unstable; introduce persistent IDs.

3. **Is JSON parsing enough validation?** No. Check the application schema too.

**Model answer:** Validate the one-based ID before converting it to the list's zero-based position. ID 0 must not become Python's -1 and accidentally select the last task. Only after command validation does main call save. State the single-writer and direct-write limitations.

## 9. Recall card

- Read command arguments and validate the requested operation.
- Load and validate the persisted task list.
- Save only a successful mutation.
- Missing data and corrupt data are different cases.
- State the single-writer and direct-write limitations.
