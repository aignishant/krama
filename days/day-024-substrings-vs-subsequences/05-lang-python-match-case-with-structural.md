---
day: 24
track: lang-python
title: "match/case with structural patterns and guards"
theme: "Pattern matching"
phase: "Languages: advanced features"
status: written
---

# Day 024 · Python — match/case with structural patterns and guards

**Today's theme:** Pattern matching

**After today you can:** You can branch on the shape of data in each language.

**The interviewer asks it as:** *How do you handle a value that could be one of several types?*

## 1. What this is, and why it matters

Structural pattern matching selects a branch by a value’s shape and can bind pieces of that value to names. Guards add conditions after a match.

You use this when discussing pattern matching in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Dev sorts deliveries for a family gathering. A box of fruit goes to the kitchen. A bag of clothes goes to the spare room. A small envelope goes to his aunt. He could inspect everything in exactly the same way, but the outside of each delivery already tells him which questions to ask.

For fruit, he checks whether it needs to stay cool. For clothes, he checks whose name is on the bag. For an envelope, he checks whether his aunt is home. The first decision narrows the next decision. Asking whether an envelope needs washing would not help anyone.

One afternoon a box arrives with a picture of fruit on it, but inside are cups. Dev stops relying on the picture alone. He checks what is actually there before carrying it into the kitchen. The label is a useful clue, not a guarantee.

His sister adds another instruction: small fruit boxes can go on the shelf, but heavy ones must stay on the floor. Dev first recognises the kind of delivery, then checks its weight. Both facts matter. A heavy box must not take the small-box route merely because both contain fruit.

Finally, something arrives that neither of them recognises. They leave it beside the door and ask the person who ordered it. A deliberate place for the unknown delivery is better than quietly treating it as something familiar and sending it to the wrong room.

## 3. The idea in plain English

Dev recognises a delivery before reading the details that matter. A mapping pattern such as `{"kind": "move", "steps": int(steps)}` asks for named keys and an integer-shaped value. It binds steps only for that branch. Extra keys are allowed in a mapping pattern unless you inspect them explicitly.

A **guard** is the `if steps > 0` after the pattern. Cases are considered in order. The first matching pattern with a true guard wins. A bare name is a capture, not a comparison; `_` is the wildcard. Use literals or qualified names for constants. Pattern matching improves dispatch, but it is not a complete input schema validator.

## 4. The picture

```text
input -> recognise shape/type -> extract fields -> check condition -> action
                    unknown -------------------------------------> reject
```

Recognise the alternative before interpreting its fields.

## 5. The code, built step by step

First isolate the important operation:

```python
case {"kind": "move", "steps": int(steps)} if steps > 0:
    return f"move {steps}"
```

Extract fields only in the matching branch.

The complete example follows. Use Python 3.12+. Save as `main.py` and run `python main.py`.

```python
def describe(command: object) -> str:
    match command:
        case {"kind": "move", "steps": int(steps)} if steps > 0:
            return f"move {steps}"
        case {"kind": "stop"}:
            return "stop"
        case _:
            raise ValueError("invalid command")

print(describe({"kind": "move", "steps": 3}))
print(describe({"kind": "stop"}))
try:
    describe({"kind": "move", "steps": -2})
except ValueError as error:
    print(error)
```

**Check the result:** Prints `move 3`, `stop`, and `invalid command`.

## 6. How the other two languages do it

**Go**

```go
switch value := command.(type) {
case Move:
    return fmt.Sprintf("move %d", value.Steps)
}
```

A type switch inspects the dynamic type of an interface value. A value switch compares values and does not fall through by default.

**C++**

```cpp
if constexpr (std::is_same_v<T, Move>) {
    auto [steps] = value;
    return "move " + std::to_string(steps);
}
```

std::visit dispatches on a variant’s active alternative. if constexpr selects code at compile time for the alternative’s type.

Python matches runtime shapes, Go switches on a dynamic type or value, and C++ visits a declared variant alternative. A guard is an extra condition after a match.

## 7. The traps

**Near-miss:** `case expected:` binds expected and matches almost anything instead of comparing against a local constant. The fallback in this example raises `ValueError: invalid command`. Also bool is a subclass of int, so int(steps) accepts True; add `type(steps) is int` in the guard if the boundary must reject booleans.

## 8. Say it out loud

**How it gets asked:** “How do you handle a value that could be one of several types?” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I match the shape first, bind the fields I need, and then apply the domain condition as a guard. I put specific cases before general cases and reject unknown input deliberately. I do not treat match as a schema validator: extra mapping keys and Python’s bool-as-int relationship can matter. Qualified names compare known values; bare names capture new ones.

**Follow-ups**

1. **Are extra mapping keys rejected?** No. Check them separately when the boundary requires an exact schema.

2. **Does a guard run before the pattern?** No. It runs after a successful pattern match.

3. **Does a bare name compare a constant?** No. It captures the subject; use a qualified name or a literal.

**Model answer:** Structural pattern matching selects a branch by a value’s shape and can bind pieces of that value to names. Guards add conditions after a match. An explicit fallback makes unknown input visible.

## 9. Recall card

- Extract fields only in the matching branch.
- Guards check extra domain conditions.
- Cases are considered in order.
- An explicit fallback makes unknown input visible.

Further reading: [Official reference](https://docs.python.org/3.12/reference/compound_stmts.html#the-match-statement).
