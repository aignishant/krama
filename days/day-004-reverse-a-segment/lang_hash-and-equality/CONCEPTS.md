---
day: 4
part: "3.1"
title: "Keep dictionary key equality and hashing consistent"
ids: [PY-04]
level: working
prerequisites: ["Identity and equality", "Classes and dictionaries"]
failure: true
---

# Keep dictionary key equality and hashing consistent

Core: understand the two key obligations and trace the failure. Implement your own value
object afterwards. Runtime hash values and collision performance are optional deeper reading.

## One-line answer

Equal keys must have equal hashes, and a stored key's hash and equality meaning must remain stable.

## The story

A storeroom files parcels under a label. If a parcel's label changes after filing, the next
lookup may search another shelf. If two equivalent labels send staff to different shelves,
the same logical parcel may be treated as two different entries.

## The idea in plain language

Recall [equality versus identity](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md).
A dictionary uses a hash to narrow its search and equality to distinguish candidate keys.
Different keys may share a hash: a **collision** is allowed. Equal keys with different hashes
break the contract. Hashable does not simply mean “has no mutable attributes”: the relevant
question is whether the fields determining hash and equality can change.

## Why Krama needs it

Domain objects used as cache or lookup keys need a coherent value model. Making a class
syntactically hashable is insufficient if equivalent instances cannot retrieve the same entry.

## The source behind it

[3. Data model — object.__hash__](https://docs.python.org/3.12/reference/datamodel.html#object.__hash__),
checked 2026-09-22 (`spec:python-3.12-data-model`), states the equal-hash requirement and the
behavior of classes overriding equality without hashing. It also warns against mutable value
keys. The following failures use an original parcel-label fixture.

## The mechanism

### Worked trace

Imagine a key represented by the immutable pair `("west", 7)`.

| Operation | What must happen conceptually |
| --- | --- |
| Insert the key | Compute its hash and retain the key/value association |
| Look up a separately created equal pair | Equal content gives a compatible hash and equality match |
| Look up `("west", 8)` | Equality distinguishes it, even if a collision occurs |
| Change equality-relevant state in a custom stored key | The dictionary's prior placement can no longer be trusted |

For a custom value object, define which fields constitute equality, then hash the same
immutable representation, often a tuple of those fields. Return `NotImplemented` for unsupported
comparison types so Python can use its comparison protocol. Keep those fields stable for the
key's lifetime. A tuple containing a list is not hashable merely because its outer shell is immutable.

Expected dictionary lookup is O(1) with ordinary hash distribution, excluding the cost of
hashing and comparing the key. Long composite keys cost work proportional to their inspected
content; heavy collisions can make a lookup O(n). Constant-time lookup is not an unconditional
guarantee. Correctness comes from equality checks after candidate selection, not collision absence.

## When it breaks

```python
class Label:
    def __init__(self, code):
        self.code = code

    def __eq__(self, other):
        if not isinstance(other, Label):
            return NotImplemented
        return self.code == other.code

try:
    mapping = {Label("A"): "parcel"}
except TypeError as error:
    print(f"TypeError: {error}")

class MutableLabel(Label):
    def __hash__(self):
        return self.code

key = MutableLabel(1)
old_hash = hash(key)
key.code = 2
print("hash changed:", hash(key) != old_hash)
try:
    assert hash(key) == old_hash, "key hash changed during its lifetime"
except AssertionError as error:
    print(f"AssertionError: {error}")

mapping = {("west", 7): "parcel"}
query = tuple(["west", 7])
assert mapping[query] == "parcel"
print("immutable value key: PASS")
```

**Line by line:** `Label` defines value equality but no compatible hash, so dictionary insertion
raises a useful error. The subclass adds an integer-valued hash for the numeric fixture, but
leaves the field mutable. Comparing hashes before and after the edit directly detects the
violated obligation without relying on a particular dictionary table layout. The final tuple
example demonstrates a safe value representation, leaving your custom-class implementation to you.

Author verification on Python 3.12.10, 2026-09-22:

```text
TypeError: unhashable type: 'Label'
hash changed: True
AssertionError: key hash changed during its lifetime
immutable value key: PASS
```

Restoring `object.__hash__` to a value-equality class is not a repair: identity-based hashing
can give equal instances different hashes. Nor does one successful lookup after mutation prove
safety; that observation can depend on table placement.

## In production

Prefer immutable key fields or an immutable key extracted from a mutable entity. Validate
lookup with a separately constructed equal key. If mutability is required, leaving the object
unhashable may be the correct API. Python string hashes can vary between processes; do not use
`hash()` as a persistent identifier, checksum, or portable partition assignment.

## Check yourself

### Readiness before practice

Explain why equal values need equal hashes but equal hashes do not prove equality. Which
fields may safely change in a key? Why is a lookup using the identical instance a weak test?
What should happen if your object compares with an unrelated type?

Use [the assignment](README.md#assignment) to implement your own key in [lab.py](lab.py).
Check equal-instance lookup, inequality, equal hashes for equal objects, and your policy for
field changes. Preserve actual observations in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-004-hash-and-equality)
