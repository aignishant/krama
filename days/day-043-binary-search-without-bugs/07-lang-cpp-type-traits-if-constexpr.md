---
day: 43
track: lang-cpp
title: "Type traits, if constexpr, and templates as compile-time code"
theme: "Reflection and metaprogramming"
phase: "Languages: advanced features"
status: written
---

# Day 043 · C++ — Type traits, if constexpr, and templates as compile-time code

**Today's theme:** Reflection and metaprogramming

**After today you can:** You can inspect a type at run time in each language and say what it costs.

**The interviewer asks it as:** *How does a JSON library know your struct's field names?*

---

## 1. What this is, and why it matters

C++20 type traits answer compile-time questions about types.
`if constexpr` chooses a branch during template instantiation, allowing the
other branch to use operations that the chosen type does not support.
This is compile-time metaprogramming, not general runtime member reflection.

## 2. The story

Ravi is helping his family prepare for a weekend away. His sister sends him
a photograph of each packed bag. He opens the first photograph and names what
he can see: a blue coat, a pair of shoes, and a small pouch. He can describe the
contents even though he did not pack the bag himself.

His mother asks him to put a spare key into the pouch. Ravi cannot do that by
touching the photograph. He needs the actual bag. Once his sister brings it to
him, he opens the pouch, adds the key, and closes it again. Seeing what something
contains and being able to change it are different kinds of access.

The family has three identical grey bags. Their father once sewed a small name
inside each one so that the children could tell them apart. Those names are
extra information about the bags; they do not change what the bags can carry.
Ravi reads the names before deciding which bag belongs by which bedroom door.

For his own bag he needs none of this checking. He knows exactly where he put
the coat and the pouch. Opening every pocket just to discover them again would
be wasted effort. But the photographs are helpful for bags other people packed.
He decides to ask for that extra information only when he needs it, and to ask
for the real bag whenever the job involves changing what is inside.

## 3. The idea in plain English

Reflection means inspecting a program's values and types while it runs.
Names, tags, and annotations are metadata: information describing the data.
Reading metadata is different from having permission to modify a value.
Python can look up a named attribute; Go can inspect an exported struct field.
C++20 does not provide general runtime enumeration of a struct's field names:
templates and type traits answer compile-time questions instead.

A JSON library may use runtime inspection, generated code, or explicit field
registration. It does not magically know every representation. Use ordinary
field access when the shape is already known; reserve general inspection for
boundaries that genuinely accept several shapes.

## 4. The picture

```text
known object ---- direct field access
unknown supported shape ---- metadata ---- checked access
C++20 template ---- compile-time condition ---- chosen code
```

Notice where the decision happens and what information it needs.

## 5. The code, built step by step

```cpp
template <typename T>
std::string describe(const T& value) {
    if constexpr (std::is_integral_v<T>) {
        return std::to_string(value);
    } else {
        return value;
    }
}
```

For an integer instantiation only the numeric branch is used. A normal if would still require both branches to be well-formed for that T.

Save as `main.cpp`; run `g++ -Wall -Wextra -std=c++20 main.cpp -o main`, then `./main`.

Expected application output (framework access logs are omitted):

    42
    Anya
    invalid: unknown field: balance

Complete program:

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>

template <typename T>
std::string describe(const T& value) {
    if constexpr (std::is_integral_v<T>) {
        return std::to_string(value);
    } else {
        static_assert(std::is_same_v<T, std::string>, "unsupported type");
        return value;
    }
}

int main() {
    std::cout << describe(42) << '\n';
    std::cout << describe(std::string("Anya")) << '\n';
    try {
        throw std::invalid_argument("unknown field: balance");
    } catch (const std::invalid_argument& exc) {
        std::cout << "invalid: " << exc.what() << '\n';
    }
}
```

## 6. How the other two languages do it

**Python**

```python
name = getattr(person, "name", "unknown")
```

The third argument supplies a default for a missing attribute; without it, absence raises AttributeError.

**Go**

```go
t := reflect.TypeOf(person)
field := t.Field(0)
fmt.Println(field.Tag.Get("json"))
```

Field metadata supplies the exported Go name and its optional external tag.

**The difference that matters:** Reflection inspects running values; templates operate during compilation.

## 7. The traps

**Near-miss:** replace `if constexpr` with `if`. Instantiating the template
with `std::string` now tries to compile `std::to_string(value)` too. Runtime
branch selection cannot make that expression valid.

**Real error:** the deliberately rejected field in the complete program prints
`invalid: unknown field: balance`. It demonstrates an adapter's explicit failure
path. Separately, `describe(3.5)` fails the `static_assert` with the diagnostic
message `unsupported type` (the surrounding compiler text varies).

`typeid(T).name()` is implementation-defined text, not a stable schema and not
a list of member names. For a C++20 Person serializer, explicitly map `name` to
`person.name` or use a library's documented registration facility. Do not claim
that this template discovers that mapping on its own.

Reference: [C++ working draft: constexpr if](https://eel.is/c++draft/stmt.if).

## 8. Say it out loud

**How it gets asked**

- How does a JSON library know your struct's field names?
- Why can inspecting a value succeed while modifying it fails?
- What can C++20 type traits tell you that runtime field-name reflection cannot?

**What to say out loud**

I ask what metadata the language makes available. In Python I can look up
attributes by name, although that lookup may execute a property. In Go I can
walk exported struct fields and read their tags using reflect. Updating a field
requires a settable value of the right kind. In C++20 I cannot enumerate arbitrary
member names at runtime; a serializer needs explicit mappings, generated code,
or another supported mechanism. Compile-time traits help select implementations,
but are not the same as runtime reflection. For a known application type I
prefer explicit code because its failures are easier to find and its accepted
fields are easier to review.

**The follow-ups**

- **Is reflection free?** No. Runtime lookup and checks add work and move some mistakes out of compile-time checking.

- **Should a request choose any field to set?** No. Validate against an allowlist and preserve the object's invariants.

- **What replaces reflection for a fixed schema?** Explicit adapters or generated code can make the mapping visible and checked.

**A model answer**

A serializer learns names from metadata or from mappings supplied by its
author. I would not build a general serializer just to avoid writing three
field assignments. If the input chooses a field, I first restrict the allowed
names and validate its value. Inspection can tell me a member exists; it cannot
tell me that changing it is a valid business operation. That is why I keep
domain updates behind methods even when the language permits dynamic access.

## 9. Recall card

- Reflection inspects running values; templates operate during compilation.
- Metadata describes data, not permission to edit it.
- Check existence, kind, and mutability before dynamic writes.
- C++20 needs explicit mappings to enumerate member names.
- Prefer direct access for known shapes.
