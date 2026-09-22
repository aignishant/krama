# Python — quick recall

Use this file to refresh language concepts you have already studied. No new lab, prediction
exercise, code execution, or practice is required in this reading mode. Read a card and return
to your work; open its lesson only when you need the detailed explanation.

Cards describe authored lessons. Your completion status remains in [track progress](TRACK_PROGRESS.csv):
use the latest `lang` event for each day. A missing event is not a completion claim. Day 001 is
the first available card; future taught days will extend this file in day order.

## Index

| Day | Topic | Jump |
| --- | --- | --- |
| 001 | Identity, equality, aliases, mutation, and rebinding | [Recall card](#day-001-identity-equality-and-aliasing) |

## Day 001: Identity, equality, and aliasing

**Core idea:** names refer to objects. Matching contents do not imply a shared object.

| Relationship or operation | Meaning |
| --- | --- |
| `a is b` | Both references identify the same object |
| `a == b` | Their values compare equal under the type's comparison rules |
| `b = a` | Another name is bound to the same object; no implicit copy |
| Mutation through `b` | The existing object changes; aliases observe that object |
| Rebinding `b` | The name refers to a different object; other names retain their references |

**Memory anchor:** two people can edit one shared shopping list, or keep two independent
sheets that initially list the same groceries. Editing the shared sheet is visible to both;
replacing one person's sheet does not replace the other person's sheet.

**Reasoning method:** draw names as arrows and objects as separate boxes. An assignment can
redirect an arrow; an item update changes a box. Keep these events separate when debugging.

**Production implication:** changing a shared configuration through a request-local name can
affect later requests. State whether a function reads, mutates, or retains a supplied object.
Test the ownership relationship you need, not just a coincidentally equal final value.

**Common mistakes:** using `is` for ordinary value comparison; assuming assignment copies;
relying on integer/string interning; believing equality is always a cheap scalar operation.
Use `is None` for the singleton. Identity does not inspect contents; equality can.

**Optional Day 2 bridge:** a shallow copy separates the outer container but may share mutable
contents. A copying policy must identify which objects need independent ownership.

[Full explanation](../days/day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md) ·
[Your Day 1 notes](../days/day-001-count-target-values/lang_identity-and-equality/NOTES.md)

---

[DSA recall](DSA_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
