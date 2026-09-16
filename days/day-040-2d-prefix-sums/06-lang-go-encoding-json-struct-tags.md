---
day: 40
track: lang-go
title: "encoding/json, struct tags, and omitempty"
theme: "JSON in and out"
phase: "Languages: advanced features"
status: written
---

# Day 040 · Go — encoding/json, struct tags, and omitempty

**Today's theme:** JSON in and out

**After today you can:** You can round-trip a struct through JSON in each language and handle a bad document.

**The interviewer asks it as:** *How do you turn a JSON document into an object?*

## 1. What this is, and why it matters

encoding/json maps JSON to exported struct fields. Struct tags choose names and omitempty behaviour; decoding still needs presence and domain validation.

You use this when discussing json in and out in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sana asks relatives to send their meal choices through a simple form on their phones. Each reply needs a name and a number of meals. At first, she accepts anything that looks readable. One person writes two where she expects a number, another leaves the name blank, and another asks for minus three meals.

The replies all arrived successfully, but they are not all useful. Sana separates two checks. First, can she read the reply at all? Second, does what it says make sense for a meal order? A readable request for minus three meals still needs to be rejected.

She sends a reply back to each person showing the accepted name and count. They can check that nothing changed during the handover. She does not expect the order of the fields on their screens to matter. The meaning matters more than the arrangement.

One relative leaves out a special-note field. Another writes an empty note. Sana asks whether those should mean the same thing. For the meal order they do, but for a later form an omitted answer might mean that somebody has not yet been asked. She wants the rule chosen deliberately.

Before collecting more replies, she tries the form with a valid request, a missing name, a word where a number belongs, and a negative count. A form is useful only when its accepted answers are well defined and its rejected answers explain what needs to change.

## 3. The idea in plain English

Sana’s form becomes a struct. A **struct tag** supplies metadata such as `json:"count"`. Unexported fields are not populated by ordinary encoding/json decoding. omitempty affects encoding: it omits selected empty values, not invalid input.

The incoming struct uses pointers so a present zero can be distinguished from missing or null. This example rejects both missing and null required fields; distinguishing those two from each other needs a richer presence representation. DisallowUnknownFields rejects unexpected keys. A second decode must reach EOF, otherwise trailing documents can be accepted accidentally. Duplicate object keys are not rejected by this decoder and need an additional policy if that matters.

## 4. The picture

```text
bytes/text -> parse JSON -> validate shape/types -> validate domain -> object
object -> serialise JSON -> parse -> equivalent accepted value
```

Parsing checks representation. Validation checks whether the resulting value belongs in the application.

## 5. The code, built step by step

First isolate the important operation:

```go
decoder.DisallowUnknownFields()
if err := decoder.Decode(&input); err != nil { return Meal{}, err }
```

Decode into exported fields and explicit tags.

The complete example follows. Use Go 1.23+. Save as `main.go` and run `go run main.go`.

```go
package main

import (
    "encoding/json"
    "fmt"
    "io"
    "strings"
)
type Meal struct {
    Name string `json:"name"`
    Count int `json:"count"`
    Note string `json:"note,omitempty"`
}
func parse(text string) (Meal, error) {
    var input struct {
        Name *string `json:"name"`
        Count *int `json:"count"`
        Note string `json:"note,omitempty"`
    }
    decoder := json.NewDecoder(strings.NewReader(text))
    decoder.DisallowUnknownFields()
    if err := decoder.Decode(&input); err != nil { return Meal{}, err }
    var extra any
    if err := decoder.Decode(&extra); err != io.EOF { return Meal{}, fmt.Errorf("trailing data") }
    if input.Name == nil || strings.TrimSpace(*input.Name) == "" || input.Count == nil || *input.Count < 0 {
        return Meal{}, fmt.Errorf("invalid meal")
    }
    return Meal{*input.Name, *input.Count, input.Note}, nil
}
func main() {
    meal, err := parse(`{"name":"Sana","count":2}`)
    if err != nil { panic(err) }
    encoded, err := json.Marshal(meal)
    if err != nil { panic(err) }
    fmt.Println(string(encoded))
    restored, err := parse(string(encoded))
    fmt.Println(err == nil && restored == meal)
    _, err = parse(`{"name":"Sana","count":-1}`)
    fmt.Println(err)
}
```

**Check the result:** Prints `{"name":"Sana","count":2}`, `true`, and `invalid meal`. The empty optional note is omitted, while a required zero count would remain present.

## 6. How the other two languages do it

**Python**

```python
data = json.loads(text)
if type(data.get("count")) is not int:
    raise ValueError("count must be an integer")
```

json.loads parses JSON into Python values and json.dumps serialises them. A dataclass models accepted data but does not validate external input by itself.

**C++**

```cpp
Meal meal = json::parse(text).get<Meal>();
```

nlohmann/json parses and serialises JSON values. to_json and from_json in a type’s namespace define explicit conversions for that type.

Python json creates ordinary containers and needs explicit validation, Go decodes into typed structs with configurable strictness, and nlohmann/json uses conversion functions for C++ types. Defaults and omitted fields need a documented policy.

## 7. The traps

**Near-miss:** decode directly into int and treat zero as proof the field was supplied. Both missing and explicit zero then look the same. With strict decoding an extra key produces a diagnostic such as `json: unknown field "extra"`. omitempty does not validate anything and can remove a meaningful zero if applied to the wrong field.

## 8. Say it out loud

**How it gets asked:** “How do you turn a JSON document into an object?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I decode into exported fields with explicit tags and preserve presence where zero is a valid value. I reject unknown fields when the endpoint contract calls for it, check for trailing input, and then validate domain conditions. I use omitempty only for fields whose empty value may genuinely be omitted. I document how null and duplicates behave rather than assuming the standard decoder enforces an entire schema.

**Follow-ups**

1. **Does omitempty validate input?** No. It is an encoding rule.

2. **How do you distinguish missing from present zero?** Use a pointer or an explicit presence-bearing type at the input boundary.

3. **Does DisallowUnknownFields reject duplicate keys?** No. Duplicate-key handling requires a separate policy or parser layer.

**Model answer:** encoding/json maps JSON to exported struct fields. Struct tags choose names and omitempty behaviour; decoding still needs presence and domain validation. omitempty is a serialisation choice, not a validation rule.

## 9. Recall card

- Decode into exported fields and explicit tags.
- Preserve presence when zero is meaningful.
- Check trailing data and domain conditions.
- omitempty is a serialisation choice, not a validation rule.

Further reading: [Official reference](https://pkg.go.dev/encoding/json).
