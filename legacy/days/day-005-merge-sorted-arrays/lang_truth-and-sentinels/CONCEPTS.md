---
day: 5
part: "3.1"
title: "Distinguish an absent value from a false value"
ids: [PY-05]
level: working
prerequisites: ["Identity and equality", "Default argument lifetime"]
failure: true
---

# Distinguish an absent value from a false value

Core: trace the value states and the failure before implementing your own API experiment.
Serialization and custom truth methods are optional follow-ups within spare time or later review.

## One-line answer

Use truth testing for a truth question and an identity-tested sentinel for an absence question.

## The story

A parcel form asks how many reminder messages to send. Leaving the field blank means use the
default; entering zero means send none. Replacing both answers with the default sends unwanted
messages. A separate mark for “not supplied” preserves what the sender actually chose.

## The idea in plain language

Python treats `None`, numeric zero, and empty built-in containers as false in a condition.
They can still represent different valid API states. A **sentinel** is a distinguished object
used to represent a state such as omission. Compare it by identity, using
[Day 1's identity model](../../day-001-count-target-values/lang_identity-and-equality/CONCEPTS.md).

Recognize this issue when `value or default` unexpectedly replaces a valid zero, false flag,
empty list, or empty string. `or` returns an operand, not necessarily a Boolean: it returns
the first operand if truthy, otherwise the second. It does not specifically test for missing data.

## Why Krama needs it

[Day 3's None default](../../day-003-stable-compaction/lang_mutable-defaults/CONCEPTS.md) works
when `None` can mean absence. Some interfaces allow explicit `None` as meaningful data.
A separate sentinel lets omission, explicit null, and valid false values remain distinguishable.

## The source behind it

[Built-in Types — Truth Value Testing](https://docs.python.org/3.12/library/stdtypes.html#truth-value-testing)
and [6. Expressions — Identity comparisons](https://docs.python.org/3.12/reference/expressions.html#is)
were checked on 2026-09-22 (`spec:python-3.12-builtins`, `spec:python-3.12-expressions`).
They define the truth and identity operations used below. The parcel configuration is an
original example; its treatment of null and zero is an explicit product policy.

## The mechanism

### Worked trace

Suppose a configuration mapping may omit `reminders`. Decide meanings before writing conditions:

| Input state | Meaning in this example | Result |
| --- | --- | --- |
| Key omitted | Use the configured default | 3 |
| Explicit `None` | Defer policy to a later layer | None |
| Explicit `0` | Disable reminders | 0 |
| Explicit `2` | Request two reminders | 2 |

Create `MISSING = object()` once in the scope that owns the interface. Retrieve the value
with `mapping.get("reminders", MISSING)`. A missing key returns that exact object; a supplied
value, even a false one, comes back unchanged. Branch on `value is MISSING` and apply the
default only to that state. This preserves the information needed by later policy decisions.

Why it works: the absence representation is distinct from every supported ordinary value.
The identity test asks whether the reference is the designated marker; custom equality cannot
pretend to match it. Constructing a fresh `object()` inside the comparison would always compare
against the wrong marker. Sharing one sentinel intentionally is safe because it is a marker,
not a container that accumulates per-call data.

For a function parameter, bind its default to the same sentinel and apply the same identity
test. Do not use `None` as that default if explicit `None` must remain distinct from omission.
The sentinel branch handles presence only: range and type validation are separate decisions.
For example, `False` is a Boolean and also compares equal to zero; define whether your numeric
API accepts it instead of letting a casual equality check decide.

## When it breaks

```python
parcel = {"reminders": 0}
wrong = parcel.get("reminders") or 3
print("truth-based fallback:", wrong)
try:
    assert wrong == 0, "an explicit zero was replaced"
except AssertionError as error:
    print(f"AssertionError: {error}")

MISSING = object()
def configured_reminders(mapping):
    value = mapping.get("reminders", MISSING)
    if value is MISSING:
        return 3
    return value

observed = [configured_reminders(item) for item in
            ({}, {"reminders": None}, {"reminders": 0}, {"reminders": 2})]
assert observed == [3, None, 0, 2]
print("presence-based results:", observed)
```

**Line by line:** `.get()` without a distinct default can conflate omission with explicit
`None`; `or` additionally replaces zero. The assertion exposes the lost user choice. The repair
creates one marker, uses it as the lookup default, and branches only on its identity. The four
fixtures separately test omission, null, zero, and an ordinary supplied value. Your lab should
extend the state table to its own API's empty-value and false-flag cases.

Author verification on Python 3.12.10, 2026-09-22:

```text
truth-based fallback: 3
AssertionError: an explicit zero was replaced
presence-based results: [3, None, 0, 2]
```

### Optional depth: truth is a protocol

A custom object's truth test can call `__bool__`, or fall back to `__len__` when `__bool__` is
absent. Those methods can do work or raise. Therefore `if value` is not universally a free
presence check. Identity testing does not invoke these methods. For the ordinary dictionary
fixture, lookup is expected O(1) and the marker adds O(1) space; custom lookup or truth behavior
can change costs. No timing measurement is implied.

## In production

Use explicit state tables for configuration, partial updates, and cached values. In an update
API, omission may mean keep a field while null means clear it and an empty string means store
empty text. Those meanings require a contract; they are not universal Python rules.

A plain `object()` marker is process-local implementation state, not a portable wire value.
Do not expect identity to survive copying, serialization, or a process boundary. Convert absence
to an agreed representation at such boundaries. Where the only missing state really is `None`,
`is None` is simpler and sufficient. Extra sentinel states add documentation and validation work.

## Check yourself

### Readiness before practice

1. What values does `value or default` replace besides `None`?
2. Why must an absence marker be compared with `is`, and why create it once?
3. When is a `None` default sufficient, and when does it lose information?
4. Does preserving a supplied false value prove that the value is valid for the API?

Follow [the assignment](README.md#assignment) in [lab.py](lab.py). Define your own API meanings
for omitted, `None`, zero, false, and empty inputs before predicting behavior. Include a
distinguishing failure and regression assertions, then record actual output and the policy in
[NOTES.md](NOTES.md). Keep the experiment within the 15-minute track budget.

[Navigation](README.md) · [Quick recall](../../../docs/LANG_RECALL.md#day-005-truth-and-sentinels)
