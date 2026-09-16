---
day: 17
track: lang-python
title: "Inheritance, super(), and the MRO"
theme: "Composition versus inheritance"
phase: "Languages: advanced features"
status: written
---

# Day 017 · Python — Inheritance, super(), and the MRO

**Today's theme:** Composition versus inheritance

**After today you can:** You can extend a type in each language and say why composition is the usual answer.

**The interviewer asks it as:** *Why is composition preferred over inheritance?*

---

## 1. What this is, and why it matters

**Inheritance** lets a class derive behaviour from another class. **Composition** means an object contains a collaborator and delegates work to it. Inheritance should preserve the expectations of a caller using the base class; composition is often easier when a component should be replaceable.

Today you use composition versus inheritance to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Nikhil buys a bicycle for his commute. After a wet journey, he adds a removable rain cover to his bag. The bag has not become a different kind of bicycle, and the bicycle has not become a kind of rain cover. Each item has one job, and they work together when he needs them.

His friend buys a delivery bicycle with a large rear box fixed to it. That is still a bicycle: it can be steered, pedalled, and parked in the same way. The added box changes how much it carries, but it must not invalidate the ordinary expectations of someone borrowing a bicycle.

They test both arrangements on Saturday. Nikhil can lend the bag to his sister while keeping the bicycle. His friend cannot remove the rear box without tools. That is acceptable if the box always belongs there, but inconvenient if every trip needs a different arrangement.

Later, a shop offers Nikhil a complicated vehicle that looks like a bicycle but cannot be pedalled. Calling it a special bicycle does not make it suitable for the same job. His route includes a narrow path where he must pedal slowly, so he declines it.

He now asks two different questions when buying equipment. Is this genuinely a kind of thing I already know how to use? Or is it a separate thing that should work alongside it? Keeping those questions separate helps him choose equipment he can change without replacing everything at once.

## 3. The idea in plain English

**Inheritance** lets a class derive behaviour from another class. **Composition** means an object contains a collaborator and delegates work to it. Inheritance should preserve the expectations of a caller using the base class; composition is often easier when a component should be replaceable.

The delivery bicycle is a possible subtype; the removable bag is a collaborator. Python's **method resolution order**, or MRO, is the ordered search path used to find inherited attributes. `super()` continues that search after the current class, using the actual object's MRO. It does not simply mean 'call my named parent' in every design.

In single inheritance, super often reaches the one direct base, as below. In multiple inheritance, cooperative methods need compatible calling conventions and consistent super usage. Do not inherit only to reuse three lines when containing a helper would avoid exposing an inappropriate base contract.

## 4. The picture

```text
INHERITANCE                       COMPOSITION
base contract                     outer object
      ^                                | contains
      | must preserve promises         v
derived implementation            collaborator
                                       |
                                       v
                                  delegated work

Go embedding: containment plus promoted selectors, not inheritance.
```

Ask whether the new object can fulfil the base contract, or whether it merely needs another component to do part of its job.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
class WarmGreeter(Greeter):
    def greet(self) -> str:
        return super().greet() + ", friend"
```

The override extends the greeting found next in the MRO. The desk then demonstrates composition by storing a greeter and forwarding its welcome operation. It can receive a basic or warm greeter without changing its own implementation.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
class Greeter:
    def greet(self) -> str:
        return "hello"

class WarmGreeter(Greeter):
    def greet(self) -> str:
        return super().greet() + ", friend"

class WelcomeDesk:
    def __init__(self, greeter: Greeter) -> None:
        self.greeter = greeter

    def welcome(self) -> str:
        return self.greeter.greet()

desk = WelcomeDesk(WarmGreeter())
print(desk.welcome())
print([kind.__name__ for kind in WarmGreeter.__mro__])
```

**Check the result:** Run `python main.py`. It prints `hello, friend` and `['WarmGreeter', 'Greeter', 'object']`.

## 6. How the other two languages do it

- **Python** — Inheritance should preserve the base contract.
- **Go** — Go composition stores another value in a struct.
- **C++** — Public inheritance commits to the base's contract.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** assume a base __init__ always runs automatically when a subclass defines its own. If required fields are missing, later methods fail. Call super().__init__ with the appropriate arguments when the base initialisation is part of the contract.

**Failure to reproduce:** change `super().greet()` to `super().missing()`. The final line is `AttributeError: 'super' object has no attribute 'missing'`. super changes where lookup starts; it does not create an operation absent from the remaining MRO.

## 8. Say it out loud

**How it gets asked:** “Why is composition preferred over inheritance?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I inherit when the new class can fulfil the base class's promises. I compose when I want to swap a collaborator independently. Python resolves inherited methods using the MRO, and super continues along that order. I check initialisation and cooperative calls explicitly rather than assuming a family diagram alone guarantees correct behaviour.

**Follow-ups**

1. **What does super mean in multiple inheritance?** Continue lookup along the actual object's MRO after this class.

2. **Why prefer composition for a sender?** Changing the sender need not change the outer object's inheritance family.

3. **Does inheritance prove substitutability?** No. Overrides can still violate behavioural expectations.

**Model answer:** The override extends the greeting found next in the MRO. The desk then demonstrates composition by storing a greeter and forwarding its welcome operation. It can receive a basic or warm greeter without changing its own implementation. Choose reuse that preserves behaviour, not just fewer lines.

## 9. Recall card

- Inheritance should preserve the base contract.
- Composition stores a collaborator with a separate job.
- Python resolves inherited attributes using the MRO.
- super continues lookup along that order.
- Choose reuse that preserves behaviour, not just fewer lines.
