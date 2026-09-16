---
day: 12
track: lang-python
title: "Everything is a reference to an object; is versus =="
theme: "Pointers, references, and value semantics"
phase: "Languages: every language, every basic"
status: written
---

# Day 012 · Python — Everything is a reference to an object; is versus ==

**Today's theme:** Pointers, references, and value semantics

**After today you can:** You can say, for each language, whether a function receives a copy or the original, and prove it with a print.

**The interviewer asks it as:** *Is this passed by value or by reference?*

---

## 1. What this is, and why it matters

A Python name refers to an object. **Aliasing** means two names refer to the same object. Assignment binds a name; it does not copy the object. **Mutation** changes an existing object, while **rebinding** changes which object a name refers to.

Today you use pointers, references, and value semantics to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Ravi and his sister share a shopping basket at the market. Ravi puts two oranges in it. His sister adds a third. When Ravi looks down, he sees three oranges. They have two people talking about one basket, not two baskets that somehow stay in agreement.

At the next stall, the shopkeeper offers his sister a fresh basket. She takes it and puts a mango inside. Ravi's basket still contains three oranges. Changing which basket she carries has not moved the fruit in his basket. Earlier she changed the shared contents. Now she changed what she was holding.

Ravi then asks for a second basket with exactly the same three oranges. He can compare the contents and say the two baskets match. He cannot honestly say they are the very same basket. If one falls, the other remains upright. Equal contents and being the same thing answer different questions.

Before they leave, their mother asks them to carry the heavy shopping upstairs. She can hand Ravi the actual basket, or she can ask him to assemble another basket containing the same purchases. One choice lets him change what everyone will receive; the other gives him something separate to rearrange.

The family avoids confusion by asking two questions before anyone moves anything: which basket are you holding, and are you changing its contents or choosing a different basket? Those questions explain the whole disagreement without blaming anyone for remembering the oranges incorrectly.

## 3. The idea in plain English

A Python name refers to an object. **Aliasing** means two names refer to the same object. Assignment binds a name; it does not copy the object. **Mutation** changes an existing object, while **rebinding** changes which object a name refers to.

Ravi's shared basket is a list. `other = values` shares it; `other = values.copy()` makes a shallow copy. A shallow copy makes a new outer collection but still shares any nested objects. A function receives access to the same object through a new local parameter name. Rebinding that parameter does not rebind the caller's name.

`==` compares values according to the object's equality operation. `is` compares identity: whether both sides are the same object. Use `is None` for the singleton `None`, but do not use `is` to compare numbers or text. Implementation reuse of some objects can make a wrong identity test appear to work.

## 4. The picture

```text
caller --------------------> object A: [1, 2]
                                  ^
local parameter / alias -----------+

mutate A: both paths observe the change
rebind local: local -------------> object B: [99]
             caller still ------> object A
```

This is the shared-object case. In Go it requires a reference-bearing value such as a pointer or slice; a copied struct is different. In C++, compare a reference parameter with a plain value parameter.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
def mutate(values: list[int]) -> None:
    values.append(3)
```

The parameter is another name for the caller's list. Appending changes that one shared object. In the complete example, rebind instead selects a new local list; it does not change where the caller's name points.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
def mutate(values: list[int]) -> None:
    values.append(3)

def rebind(values: list[int]) -> None:
    values = [99]
    print("inside", values)

values = [1, 2]
alias = values
copy = values.copy()
mutate(values)
rebind(values)
print(values)
print(alias is values, copy is values)
print([1, 2] == [1, 2])
```

**Check the result:** Run `python main.py`. The lines are `inside [99]`, `[1, 2, 3]`, `True False`, and `True`.

## 6. How the other two languages do it

- **Python** — Assignment binds names to objects; it does not copy.
- **Go** — Every Go argument is passed by value.
- **C++** — A value parameter is independent of its caller's value.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** `rows = [[0]] * 3` repeats a reference to one inner list. After `rows[0][0] = 7`, all three rows show 7. Use a comprehension, `[[0] for _ in range(3)]`, to construct independent rows.

**Failure to reproduce:** `text = "cat"; text[0] = "b"` ends with `TypeError: 'str' object does not support item assignment`. Strings cannot be mutated. Build a new string and return it; callers decide whether to bind their name to that result.

## 8. Say it out loud

**How it gets asked:** “Is this passed by value or by reference?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Python passes an object reference by assignment to a local parameter. I can mutate a shared mutable object, but assigning a new object to the local name does not change the caller's binding. Equality asks whether values compare equal; identity asks whether they are one object. I draw two arrows to one list to explain aliasing.

**Follow-ups**

1. **Does copy() duplicate nested lists?** No. It is shallow.

2. **Can a function change an integer argument in place?** Integers are immutable; return a new result.

3. **When is is appropriate?** For identity questions such as whether a value is None.

**Model answer:** The parameter is another name for the caller's list. Appending changes that one shared object. In the complete example, rebind instead selects a new local list; it does not change where the caller's name points. A shallow copy still shares nested objects.

## 9. Recall card

- Assignment binds names to objects; it does not copy.
- Aliases observe mutation of the shared object.
- Rebinding a local parameter leaves the caller's name alone.
- == checks equality; is checks identity.
- A shallow copy still shares nested objects.
