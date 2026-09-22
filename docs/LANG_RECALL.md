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
| 002 | Shallow and deep copies | [Recall card](#day-002-shallow-and-deep-copies) |
| 003 | Mutable defaults | [Recall card](#day-003-mutable-defaults) |
| 004 | Hash and equality | [Recall card](#day-004-hash-and-equality) |
| 005 | Truth and sentinels | [Recall card](#day-005-truth-and-sentinels) |

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

## Day 002: Shallow and deep copies

**Idea and cue:** when a local edit leaks into a template, inspect the object graph. A shallow
copy separates the outer container but shares its referenced children. Deep copying follows
supported nested objects; it does not blindly duplicate every resource.

**Why it works:** mutations affect a shared object, while replacing a reference changes only
that slot. Independence must exist at the layer being mutated. Deep-copy memoization normally
preserves repeated-child sharing within the new graph and handles cycles.

**Memory anchor:** two folders can contain shortcuts to one document. Copying the folder
does not make editing the document private.

**Cost and trap:** copying n outer references costs O(n); copying an ordinary graph scales
with its reachable objects, references, and payloads. Custom hooks can change those costs.
An explicit copy of the editable child may be enough. Equal initial values do not prove
independent ownership; inspect identities and the effects of mutation.

[Full lesson](../days/day-002-find-the-first-maximum/lang_shallow-and-deep-copies/CONCEPTS.md) ·
[Your notes](../days/day-002-find-the-first-maximum/lang_shallow-and-deep-copies/NOTES.md)

## Day 003: Mutable defaults

**Idea and cue:** repeated calls accumulating unexpected state suggest a shared mutable
default. A default expression runs when `def` executes, and omitted calls reuse that object.

**Why it works:** using `None` as an absence marker and allocating inside an `is None` branch
creates a fresh object for each omitted call. Explicit caller-supplied containers retain their
documented ownership. Rebinding a local parameter never resets the stored default.

**Memory anchor:** one blank order form reused for every customer carries earlier orders forward.

**Cost and trap:** allocating an empty container is small, but retained content grows. A hidden
shared cache needs lifecycle and concurrency decisions. `arg or []` discards a supplied empty
list; use an absence check. If `None` itself is meaningful input, use a distinct sentinel.
Tests need two calls in the same process and an explicit empty-container case.

[Full lesson](../days/day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md) ·
[Your notes](../days/day-003-stable-compaction/lang_mutable-defaults/NOTES.md)

## Day 004: Hash and equality

**Idea and cue:** value objects used as dictionary or set keys need compatible equality and
hashing. Equal objects must hash equally; collisions between unequal objects are allowed.
Keep hash- and equality-relevant state stable throughout the key's lifetime.

**Why it works:** a hash narrows lookup candidates, and equality distinguishes them. Changing
the lookup-relevant state after insertion can invalidate earlier placement. A value-equality
class without an explicit compatible hash is normally unhashable.

**Memory anchor:** changing a parcel's filing label after shelving it makes later lookup unreliable.

**Cost and trap:** lookup is expected O(1) under ordinary distribution, plus key hashing and
comparison costs; collisions can worsen it. Identity-based hashing does not repair value
equality. Test with a separate equal instance, not only the inserted object. Prefer immutable
key fields or extract an immutable tuple. A tuple containing a list is still unhashable.
Do not treat Python's process-dependent string hash as a persistent identifier.

[Full lesson](../days/day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md) ·
[Your notes](../days/day-004-reverse-a-segment/lang_hash-and-equality/NOTES.md)

---

## Day 005: Truth and sentinels

**Idea and cue:** omission, `None`, zero, false, and empty values can mean different things.
A truth-based fallback such as `value or default` replaces every falsey value, not just absence.
Use this distinction when a configuration or update API unexpectedly discards an explicit choice.

**Mechanism and reason:** create one `MISSING = object()` marker, use it as the lookup or
parameter default, and test `value is MISSING`. Only omission supplies that exact object.
Identity avoids custom equality and truth behavior. Preserve other values, then validate them
against the API's separate type and range policy.

**Memory anchor:** an omitted reminder count can mean use 3, while zero means send none.
`0 or 3` loses that decision. If explicit `None` means defer to another policy, it also needs
to remain distinct from omission.

**Tradeoff and trap:** `is None` suffices when null really means missing. A separate sentinel
adds a state to document; it is not a wire format or an identity guaranteed across copying
and serialization. Recreating `object()` for the comparison never matches the saved marker.
The marker and identity branch use constant extra space; custom truth methods may perform
work or raise. `False == 0` does not decide whether an API should accept Boolean counts.

[Full lesson](../days/day-005-merge-sorted-arrays/lang_truth-and-sentinels/CONCEPTS.md) ·
[Your notes](../days/day-005-merge-sorted-arrays/lang_truth-and-sentinels/NOTES.md)

---

[DSA recall](DSA_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
