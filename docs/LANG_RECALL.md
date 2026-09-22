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
| 006 | Mutation contracts | [Recall card](#day-006-mutation-contracts) |
| 007 | Week 1 Python review | [Recall card](#day-007-week-1-python-review) |
| 008 | Argument binding | [Recall card](#day-008-argument-binding) |
| 009 | Closure binding | [Recall card](#day-009-closure-binding) |
| 010 | Nonlocal state | [Recall card](#day-010-nonlocal-state) |
| 011 | Decorator metadata | [Recall card](#day-011-decorator-metadata) |
| 012 | Decorator arguments | [Recall card](#day-012-decorator-arguments) |
| 013 | Partial application | [Recall card](#day-013-partial-application) |
| 014 | Week 2 Python review | [Recall card](#day-014-week-2-python-review) |
| 015 | Iterator protocol | [Recall card](#day-015-iterator-protocol) |
| 016 | Generator laziness | [Recall card](#day-016-generator-laziness) |

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

## Day 006: Mutation contracts

**Cue and mechanism:** if an edit leaks between callers, name the ownership promise: permitted
input mutation, fresh output, shared children, and retained references. Test value and identity
separately. Binding a parameter does not copy the object it receives.

**Why it works:** aliases observe changes to one object; a fresh outer container separates
outer edits only. Copying n references costs O(n) space and time. Avoiding allocation through
mutation shifts responsibility to callers that share the input.

**Memory anchor:** `items.sort()` reorders the caller's list and returns `None`; `sorted(items)`
returns a fresh outer list. Nested mutable children may still be shared. Equality alone cannot
prove independent ownership, and an exception need not roll back changes already made.

[Full lesson](../days/day-006-best-single-trade/lang_mutation-contracts/CONCEPTS.md) ·
[Your notes](../days/day-006-best-single-trade/lang_mutation-contracts/NOTES.md)

## Day 007: Week 1 Python review

**Cue and mechanism:** a remembered surprise needs an explicit contract and object graph.
Identify the shared object, the mutation, and the observer. A regression assertion should fail
on the original mistake and pass after its repair.

**Why it works:** checking the affected layer distinguishes equal contents, independent
containers, default lifetime, key equality, and absence semantics. Copy only the layer the
contract requires; copying more costs extra references and may change intended sharing.

**Memory anchor:** a shallow copy of `[[2]]` has a new outer list and the same child. Appending
through the copy changes the original child. An outer identity assertion can pass while the
ownership promise fails. A one-call test can similarly miss shared defaults across calls.
This reading card does not substitute for the cold reproduction, repair, and explanation.

[Repair lesson](../days/day-007-week-1-review/lang_week-1-python-review/CONCEPTS.md) ·
[Your notes](../days/day-007-week-1-review/lang_week-1-python-review/NOTES.md)

## Day 008: Argument binding

**Cue and mechanism:** use signature slots to reason about ambiguous options and forwarding
errors. Parameters before `/` are positional-only; those after `*` are keyword-only; middle
slots permit either route. Reject duplicates and missing required slots; defaults fill omissions.

**Why it works:** valid binding establishes which supplied reference each parameter denotes
before the body executes. It neither copies mutable inputs nor performs business validation.
Named options improve clarity but their names become part of the public calling contract.

**Memory anchor:** `label(parcel, /, copies=1, *, urgent=False)` accepts
`label("P7", 2, urgent=True)`. Supplying `parcel=` or a third positional argument fails.
Argument expressions can run even when binding fails. Fixed small signatures have bounded
binding work; large unpacked collections have separate costs. Error wording can vary by version.

[Full lesson](../days/day-008-first-repeated-value/lang_argument-binding/CONCEPTS.md) ·
[Your notes](../days/day-008-first-repeated-value/lang_argument-binding/NOTES.md)

## Day 009: Closure binding

**Cue and mechanism:** Delayed callbacks read retained bindings at call time. Capture a creation-time object with a default parameter or a fresh factory scope when that is the intended policy.

**Why it works and cost:** Loop-created closures can share one changing binding. A default is evaluated at function creation. O(m) function storage for m callbacks; captured objects may keep much larger graphs alive.

**Memory anchor and trap:** Late callbacks for 4, 7, 9 all see 9; defaults retain 4, 7, 9. Capturing a list does not copy its contents. A default parameter can also be overridden by the caller.

[Full lesson](../days/day-009-frequency-ranking/lang_closure-binding/CONCEPTS.md) ·
[Your notes](../days/day-009-frequency-ranking/lang_closure-binding/NOTES.md)

## Day 010: Nonlocal state

**Cue and mechanism:** A stateful closure needs an explicit owner. nonlocal rebinds an existing enclosing function name; each factory call owns separate state.

**Why it works and cost:** Assignment normally makes the name local, so reading it first can fail. An instance with __call__ can expose the same ownership through attributes. Constant state here; neither form supplies durability or thread safety.

**Memory anchor and trap:** Independent running totals produce [5, 7, 2], not one global sequence. An alias to one returned callable shares its state. Mutating an outer list differs from rebinding its name.

[Full lesson](../days/day-010-pair-sum-indices/lang_nonlocal-state/CONCEPTS.md) ·
[Your notes](../days/day-010-pair-sum-indices/lang_nonlocal-state/NOTES.md)

## Day 011: Decorator metadata

**Cue and mechanism:** A forwarding decorator replaces the public callable. functools.wraps preserves metadata and the __wrapped__ link while behavior still runs through the wrapper.

**Why it works and cost:** Tools can follow the link back to the wrapped callable. Metadata work occurs at decoration time; forwarding and tracing add per-call overhead.

**Memory anchor and trap:** A plain wrapper is named wrapper; the preserved wrapper reports receipt. inspect.signature normally follows __wrapped__, but actual wrapper arguments can remain *args and **kwargs. wraps cannot fix a missing return or async awaiting.

[Full lesson](../days/day-011-group-anagrams/lang_decorator-metadata/CONCEPTS.md) ·
[Your notes](../days/day-011-group-anagrams/lang_decorator-metadata/NOTES.md)

## Day 012: Decorator arguments

**Cue and mechanism:** Separate factory configuration, function decoration, and wrapper invocation. Validate policy once and call arguments each time; let business exceptions propagate.

**Why it works and cost:** Distinct closures retain configuration and the function at the right lifetime. A fixed integer guard adds O(1) work and state here; general binding and wrapped execution have separate costs.

**Memory anchor and trap:** bounded(20) captures 20 before receipt(12) executes. An invalid amount is a validation error; a broken printer must remain a RuntimeError. A catch-all returning None hides that failure.

[Full lesson](../days/day-012-range-sums/lang_decorator-arguments/CONCEPTS.md) ·
[Your notes](../days/day-012-range-sums/lang_decorator-arguments/NOTES.md)

## Day 013: Partial application

**Cue and mechanism:** Use partial when a callback needs some arguments supplied in advance.

**Why it works and cost:** Stored positional arguments precede later ones; later keywords override stored keywords before ordinary binding. Retains references, not deep copies.

**Memory anchor and trap:** partial(f, prefix="x")(7) can bind prefix twice. Mutating a retained list is visible; rebinding its old name is not.

[Full lesson](../days/day-013-count-target-subarrays/lang_partial-application/CONCEPTS.md) ·
[Your notes](../days/day-013-count-target-subarrays/lang_partial-application/NOTES.md)

## Day 014: Week 2 Python review

**Cue and mechanism:** Diagnose a function surprise by when the object is selected: definition, decoration, lookup, or invocation.

**Why it works and cost:** A regression rejects the original behavior and accepts the intended repair. Capturing n callbacks costs O(n) references plus retained objects.

**Memory anchor and trap:** Loop closures share a binding; default parameters store each creation-time object. Mutable objects are still shared. Cold attempt first.

[Full lesson](../days/day-014-week-2-review/lang_week-2-python-review/CONCEPTS.md) ·
[Your notes](../days/day-014-week-2-review/lang_week-2-python-review/NOTES.md)

## Day 015: Iterator protocol

**Cue and mechanism:** Distinguish a reusable iterable from one consumable iterator.

**Why it works and cost:** iter(iterator) returns itself; next advances state and exhaustion remains exhausted. Cursor state may be O(1) while retaining a large collection.

**Memory anchor and trap:** list(cursor) consumes it. Calling iter(cursor) does not rewind; create a new iterator from the source.

[Full lesson](../days/day-015-sorted-pair-existence/lang_iterator-protocol/CONCEPTS.md) ·
[Your notes](../days/day-015-sorted-pair-existence/lang_iterator-protocol/NOTES.md)

## Day 016: Generator laziness

**Cue and mechanism:** Use generator laziness to perform body work only when consumers request values.

**Why it works and cost:** next runs to yield, preserving local state for resumption. Total work follows consumption; retained locals determine memory.

**Memory anchor and trap:** Creation is not first execution. Body errors may appear on next, while argument expressions already ran at the call site.

[Full lesson](../days/day-016-unique-triples/lang_generator-laziness/CONCEPTS.md) ·
[Your notes](../days/day-016-unique-triples/lang_generator-laziness/NOTES.md)


---

[DSA recall](DSA_RECALL.md) · [System design recall](SD_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
