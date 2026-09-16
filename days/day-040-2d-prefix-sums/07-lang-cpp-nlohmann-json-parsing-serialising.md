---
day: 40
track: lang-cpp
title: "nlohmann/json: parsing, serialising, and from_json"
theme: "JSON in and out"
phase: "Languages: advanced features"
status: written
---

# Day 040 · C++ — nlohmann/json: parsing, serialising, and from_json

**Today's theme:** JSON in and out

**After today you can:** You can round-trip a struct through JSON in each language and handle a bad document.

**The interviewer asks it as:** *How do you turn a JSON document into an object?*

## 1. What this is, and why it matters

nlohmann/json parses and serialises JSON values. to_json and from_json in a type’s namespace define explicit conversions for that type.

You use this when discussing json in and out in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Sana asks relatives to send their meal choices through a simple form on their phones. Each reply needs a name and a number of meals. At first, she accepts anything that looks readable. One person writes two where she expects a number, another leaves the name blank, and another asks for minus three meals.

The replies all arrived successfully, but they are not all useful. Sana separates two checks. First, can she read the reply at all? Second, does what it says make sense for a meal order? A readable request for minus three meals still needs to be rejected.

She sends a reply back to each person showing the accepted name and count. They can check that nothing changed during the handover. She does not expect the order of the fields on their screens to matter. The meaning matters more than the arrangement.

One relative leaves out a special-note field. Another writes an empty note. Sana asks whether those should mean the same thing. For the meal order they do, but for a later form an omitted answer might mean that somebody has not yet been asked. She wants the rule chosen deliberately.

Before collecting more replies, she tries the form with a valid request, a missing name, a word where a number belongs, and a negative count. A form is useful only when its accepted answers are well defined and its rejected answers explain what needs to change.

## 3. The idea in plain English

Sana’s accepted reply becomes a Meal object. **Serialisation** produces a transport representation; deserialisation reconstructs data from it. The conversion functions are found through argument-dependent lookup, so place them with the type they convert.

Parsing creates a JSON value, not automatically a valid Meal. The validator checks the object shape, exact fields, text type, integer category, and count range before assignment. Numeric conversions can otherwise truncate or narrow, so range checks must precede get<int>. JSON object-key order is irrelevant to value equality. This header-only dependency is external to the C++ standard library.

## 4. The picture

```text
bytes/text -> parse JSON -> validate shape/types -> validate domain -> object
object -> serialise JSON -> parse -> equivalent accepted value
```

Parsing checks representation. Validation checks whether the resulting value belongs in the application.

## 5. The code, built step by step

First isolate the important operation:

```cpp
Meal meal = json::parse(text).get<Meal>();
```

Validate types and numeric ranges before conversion.

The complete example follows. Install the nlohmann/json header library and make its include directory available to the compiler. Save as `main.cpp`; build with `g++ -std=c++20 -Wall -Wextra main.cpp -o demo` (add `-I` with the header installation path if needed), then run the executable.

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <nlohmann/json.hpp>

using nlohmann::json;
struct Meal {
    std::string name;
    int count;
    bool operator==(const Meal&) const = default;
};
void to_json(json& output, const Meal& value) {
    output = json{{"name", value.name}, {"count", value.count}};
}
void from_json(const json& input, Meal& value) {
    if (!input.is_object() || input.size() != 2 || !input.contains("name") || !input.contains("count"))
        throw std::invalid_argument("expected name and count");
    const auto& name = input.at("name");
    const auto& count = input.at("count");
    if (!name.is_string() || !count.is_number_integer() || count < 0 || count > 1000)
        throw std::invalid_argument("invalid meal");
    auto text = name.get<std::string>();
    if (text.find_first_not_of(" \t\r\n") == std::string::npos)
        throw std::invalid_argument("name must be nonblank");
    value = Meal{text, count.get<int>()};
}
int main() {
    try {
        Meal meal = json::parse(R"({"name":"Sana","count":2})").get<Meal>();
        json encoded = meal;
        std::cout << encoded.dump() << '\n';
        std::cout << std::boolalpha << (encoded.get<Meal>() == meal) << '\n';
        json::parse(R"({"name":"Sana","count":-1})").get<Meal>();
    } catch (const std::exception& error) {
        std::cout << error.what() << '\n';
    }
}
```

**Check the result:** Prints `{"count":2,"name":"Sana"}`, `true`, and `invalid meal`. This version deliberately limits count to 0–1000 before narrowing it to int; choose and document the actual domain limit for a real endpoint.

## 6. How the other two languages do it

**Python**

```python
data = json.loads(text)
if type(data.get("count")) is not int:
    raise ValueError("count must be an integer")
```

json.loads parses JSON into Python values and json.dumps serialises them. A dataclass models accepted data but does not validate external input by itself.

**Go**

```go
decoder.DisallowUnknownFields()
if err := decoder.Decode(&input); err != nil { return Meal{}, err }
```

encoding/json maps JSON to exported struct fields. Struct tags choose names and omitempty behaviour; decoding still needs presence and domain validation.

Python json creates ordinary containers and needs explicit validation, Go decodes into typed structs with configurable strictness, and nlohmann/json uses conversion functions for C++ types. Defaults and omitted fields need a documented policy.

## 7. The traps

**Near-miss:** use get<int> on arbitrary numeric JSON and assume out-of-range or fractional values are automatically rejected. Validate category and range first. Malformed syntax raises json::parse_error; wrong JSON value operations can raise json::type_error. The example’s negative-count path throws invalid_argument with the exact text `invalid meal`. Duplicate keys need a separate rejection policy if required.

## 8. Say it out loud

**How it gets asked:** “How do you turn a JSON document into an object?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I give the type explicit conversion functions and validate every boundary before constructing the accepted value. Parsing and typed conversion are separate steps. I check numeric categories and bounds before narrowing, define required and unknown fields, and compare values after a round-trip. I keep the external library’s setup visible and do not imply that C++ itself includes JSON parsing. Error categories distinguish broken syntax from invalid application data.

**Follow-ups**

1. **Does parsing prove a valid Meal?** No. Shape, types, bounds, and domain conditions still need validation.

2. **Why validate before get<int>?** Numeric conversion can narrow or truncate unless the input is constrained first.

3. **Why compare values after round-trip?** Whitespace and object-key order do not define the business meaning.

**Model answer:** nlohmann/json parses and serialises JSON values. to_json and from_json in a type’s namespace define explicit conversions for that type. A round-trip checks accepted meaning, not a particular formatting style.

## 9. Recall card

- Validate types and numeric ranges before conversion.
- Keep to_json and from_json with the converted type.
- Treat JSON as an external representation.
- A round-trip checks accepted meaning, not a particular formatting style.

Further reading: [Official reference](https://json.nlohmann.me/features/arbitrary_types/).
