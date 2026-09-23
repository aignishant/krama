---
day: 2
part: "3.1"
title: "Choose which layer of an object graph to copy"
ids: [PY-02]
level: working
prerequisites: ["Day 1 identity and aliasing"]
failure: true
---

# Choose which layer of an object graph to copy

Core: trace the ownership diagram, predict the demo, and check readiness. The graph-sharing
follow-up is optional depth for a later sitting; retain the 15-minute experiment budget.

## One-line answer

A new outer container does not guarantee independent mutable objects inside it.

## The story

You duplicate a folder of shortcuts to shared documents. Renaming your folder does not rename
the original folder. Editing a document through either shortcut still changes the same document.
To work independently, decide which documents need separate copies, not just which folder.

## The idea in plain language

Recall [identity, mutation, and rebinding](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md).
Draw an object graph: objects are boxes and references are arrows. A shallow copy duplicates
one container's reference slots. A deep copy follows the graph to copy supported nested objects.
Use this model when a supposedly local edit changes a template or another request's state.

## Why Krama needs it

Copying is an ownership decision. Tests must identify the boundary that should be independent,
rather than merely verifying equal initial contents.

## The source behind it

[copy — Shallow and deep copy operations](https://docs.python.org/3.12/library/copy.html),
checked 2026-09-22 (`spec:python-3.12-copy`), defines `copy` and `deepcopy`. Deep copying uses
a memo and supports custom behavior; it is not a promise to clone every external resource.
The example below is an original configuration fixture.

## The mechanism

### Worked trace

For a configuration dictionary with one nested list:

```text
config  -> dictionary A --"labels"--> list L
shallow -> dictionary B --"labels"--> list L
deep    -> dictionary C --"labels"--> list M

A and B differ; their child L is shared. M starts equal to L but is independent.
```

Adding a new outer key to B affects only B. Appending through B's `labels` arrow changes L,
so A observes it too. Replacing B's `labels` arrow with a new list would instead leave L alone.
The operation's depth determines which owners see a change.

```python
from copy import copy, deepcopy

config = {"labels": ["ready"]}
shallow = copy(config)
deep = deepcopy(config)
print("outer shared:", shallow is config)
print("child shared:", shallow["labels"] is config["labels"])
shallow["labels"].append("sent")
print("original:", config["labels"])
print("deep:", deep["labels"])
assert deep["labels"] == ["ready"]
assert deep["labels"] is not config["labels"]
```

**Line by line:** imports name the two copy policies. `config` creates an outer dictionary
and a nested list. Each copy creates a distinct outer dictionary. The identity prints inspect
the graph directly. Appending through the shallow copy changes the shared child. The deep copy
was taken before that edit, so its child retains the old value; both value and identity are checked.

Author verification on Python 3.12.10, 2026-09-22:

```text
outer shared: False
child shared: True
original: ['ready', 'sent']
deep: ['ready']
```

For a built-in container with n direct references, a shallow copy needs O(n) time and space.
A deep copy of ordinary containers traverses the reachable graph, costing roughly O(V+E)
time and space for V objects and E references, plus payload-copy costs. Custom hooks can do
arbitrary work. These are model bounds, not timing measurements.

Optional depth: if two source fields point to the same child, `deepcopy` normally preserves
that sharing **inside the new graph** through its memo. It does not create an independent child
for every arrow. Cycles also make a tree-only mental model inadequate.

## When it breaks

This independent fixture exposes the mistaken claim that an outer copy isolates child edits.

```python
template = {"labels": ["ready"]}
request = template.copy()
request["labels"].append("private")
try:
    assert template["labels"] == ["ready"], "shallow copy leaked a child edit"
except AssertionError as error:
    print(f"AssertionError: {error}")

template = {"labels": ["ready"]}
request = {**template, "labels": list(template["labels"])}
request["labels"].append("private")
assert template["labels"] == ["ready"]
print("explicit child copy: PASS")
```

**Line by line:** `.copy()` duplicates only the outer dictionary. The append reaches its
shared child. The repaired fixture copies just the list whose ownership must change; `**template`
retains other fields and the later `labels` entry replaces that one reference. This policy is
sufficient for a list of immutable strings, not arbitrary nested mutable values.

Observed output:

```text
AssertionError: shallow copy leaked a child edit
explicit child copy: PASS
```

## In production

Prefer a documented ownership policy: immutable configuration, explicit copies of editable
fields, or a deep copy when the supported object graph justifies it. Blindly deep-copying a large
request graph increases memory and can duplicate state intended to remain shared. File handles
and network resources need lifecycle decisions, not a copying slogan. Review question: which
objects may this request mutate, and which aliases must stay unaffected?

## Check yourself

### Readiness before practice

Explain which boxes change when you append to a nested list, replace the nested list, or add
an outer key. Why can `a == b` pass before a mutation despite an incorrect ownership relationship?
What does a shallow copy of a flat list of immutable integers buy you?

Then use [the assignment](README.md#assignment) to construct your own nested-list experiment
in [lab.py](lab.py). Predict first, run it, and assert both intended sharing and intended isolation.
Keep actual results in [NOTES.md](NOTES.md); copying this dictionary demo is not the assigned lab.

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-002-shallow-and-deep-copies)
