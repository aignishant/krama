---
day: 40
track: lang-python
title: "json.loads, json.dumps, dataclasses, and pydantic"
theme: "JSON in and out"
phase: "Languages: advanced features"
status: written
---

# Day 040 · Python — json.loads, json.dumps, dataclasses, and pydantic

**Today's theme:** JSON in and out

**After today you can:** You can round-trip a struct through JSON in each language and handle a bad document.

**The interviewer asks it as:** *How do you turn a JSON document into an object?*

## 1. What this is, and why it matters

json.loads parses JSON into Python values and json.dumps serialises them. A dataclass models accepted data but does not validate external input by itself.

You use this when discussing json in and out in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sana asks relatives to send their meal choices through a simple form on their phones. Each reply needs a name and a number of meals. At first, she accepts anything that looks readable. One person writes two where she expects a number, another leaves the name blank, and another asks for minus three meals.

The replies all arrived successfully, but they are not all useful. Sana separates two checks. First, can she read the reply at all? Second, does what it says make sense for a meal order? A readable request for minus three meals still needs to be rejected.

She sends a reply back to each person showing the accepted name and count. They can check that nothing changed during the handover. She does not expect the order of the fields on their screens to matter. The meaning matters more than the arrangement.

One relative leaves out a special-note field. Another writes an empty note. Sana asks whether those should mean the same thing. For the meal order they do, but for a later form an omitted answer might mean that somebody has not yet been asked. She wants the rule chosen deliberately.

Before collecting more replies, she tries the form with a valid request, a missing name, a word where a number belongs, and a negative count. A form is useful only when its accepted answers are well defined and its rejected answers explain what needs to change.

## 3. The idea in plain English

Sana’s readable reply is only the first check. A **schema** specifies required fields and their allowed types. The explicit validator below rejects unknown fields, requires a nonblank name, and accepts only a non-negative integer count. `type(count) is int` deliberately rejects booleans, which otherwise satisfy isinstance(True, int).

Pydantic is an optional external validation library. A model with strict=True and extra="forbid" can enforce type and unknown-field policies, while field constraints or validators enforce domain rules. Its defaults can coerce values, so do not assume strictness without configuring it. JSON null becomes None; absence is a missing key and may mean something different.

## 4. The picture

```text
bytes/text -> parse JSON -> validate shape/types -> validate domain -> object
object -> serialise JSON -> parse -> equivalent accepted value
```

Parsing checks representation. Validation checks whether the resulting value belongs in the application.

## 5. The code, built step by step

First isolate the important operation:

```python
data = json.loads(text)
if type(data.get("count")) is not int:
    raise ValueError("count must be an integer")
```

Validate after parsing and before constructing accepted data.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
from dataclasses import asdict, dataclass
import json

@dataclass(frozen=True)
class Meal:
    name: str
    count: int

def parse(text: str) -> Meal:
    data = json.loads(text)
    if not isinstance(data, dict) or set(data) != {"name", "count"}:
        raise ValueError("expected name and count")
    if not isinstance(data["name"], str) or not data["name"].strip():
        raise ValueError("name must be nonblank")
    if type(data["count"]) is not int or data["count"] < 0:
        raise ValueError("count must be a non-negative integer")
    return Meal(data["name"], data["count"])

meal = parse('{"name":"Sana","count":2}')
encoded = json.dumps(asdict(meal), sort_keys=True)
print(encoded)
print(parse(encoded) == meal)
try:
    parse('{"name":"Sana","count":-1}')
except ValueError as error:
    print(error)
```

**Check the result:** Prints `{"count": 2, "name": "Sana"}`, `True`, and `count must be a non-negative integer`. The accepted value round-trips even when field order changes.

## 6. How the other two languages do it

**Go**

```go
decoder.DisallowUnknownFields()
if err := decoder.Decode(&input); err != nil { return Meal{}, err }
```

encoding/json maps JSON to exported struct fields. Struct tags choose names and omitempty behaviour; decoding still needs presence and domain validation.

**C++**

```cpp
Meal meal = json::parse(text).get<Meal>();
```

nlohmann/json parses and serialises JSON values. to_json and from_json in a type’s namespace define explicit conversions for that type.

Python json creates ordinary containers and needs explicit validation, Go decodes into typed structs with configurable strictness, and nlohmann/json uses conversion functions for C++ types. Defaults and omitted fields need a documented policy.

## 7. The traps

**Near-miss:** call Meal(**json.loads(text)) and assume annotations validated the types. They did not. A malformed document such as `{` raises `json.decoder.JSONDecodeError` with a line and column; a negative count reaches the separate domain diagnostic `count must be a non-negative integer`. If duplicate-key rejection is required, configure object_pairs_hook rather than silently accepting the default last value.

## 8. Say it out loud

**How it gets asked:** “How do you turn a JSON document into an object?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I separate JSON syntax from schema and domain validation. I reject wrong shapes and types before creating the dataclass, then enforce conditions such as a non-negative count. I decide how unknown fields, null, missing fields, and duplicates behave. For larger models I can use Pydantic with explicitly chosen strictness. I test a value round-trip rather than comparing serialized key order, which is not the business meaning.

**Follow-ups**

1. **Does a dataclass validate annotations at runtime?** No. Construction alone does not enforce the annotated field types.

2. **Are null and missing the same?** No. One is a present null value; the other is absence of a key.

3. **Why compare decoded values rather than JSON text?** Whitespace and object-key order can differ without changing the accepted value.

**Model answer:** json.loads parses JSON into Python values and json.dumps serialises them. A dataclass models accepted data but does not validate external input by itself. A successful parse does not prove a valid application request.

## 9. Recall card

- Validate after parsing and before constructing accepted data.
- Dataclass annotations are not runtime validation.
- Choose strictness and unknown-field policy explicitly.
- A successful parse does not prove a valid application request.

Further reading: [Official reference](https://docs.python.org/3.12/library/json.html).
