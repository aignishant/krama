---
day: 16
track: lang-python
title: "Duck typing, abstract base classes, and Protocol"
theme: "Interfaces"
phase: "Languages: advanced features"
status: written
---

# Day 016 · Python — Duck typing, abstract base classes, and Protocol

**Today's theme:** Interfaces

**After today you can:** You can define a behaviour without naming a type in each language, and say when the check happens.

**The interviewer asks it as:** *What is an interface, and when does the compiler check it?*

---

## 1. What this is, and why it matters

**Duck typing** means using an object according to the operations it supports rather than requiring a particular class. If a caller needs `greet()`, any suitable object can work. A `Protocol` describes that required shape for static type checkers without forcing implementations to inherit from it.

Today you use interfaces to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Priya runs a neighbourhood book exchange. At the entrance, every volunteer has one job: welcome a visitor and tell them where to leave a book. Priya does not care whether the volunteer is a teacher, a student, or a retired neighbour. She cares that the visitor receives a clear greeting and the right directions.

On the first morning, Priya asks each person to demonstrate. Arun says hello and points to the table. Leela does the same in another language for visitors who prefer it. Their words differ, but each fulfils the promise. Priya can send the next visitor to either of them without changing the rest of the event.

A new volunteer arrives and offers to carry chairs. That is useful, but it does not prove that he can greet visitors. Priya gives him the directions and asks him to practise before taking a place at the entrance. Being willing to help is not the same as being ready for this particular job.

Later, one visitor needs directions spoken slowly. Priya swaps the greeter without moving the book tables or stopping the exchange. The other volunteers do not need to know the new greeter's whole background. They need to know that the same small promise will still be kept.

By closing time, Priya has learned to describe jobs by what someone must do, rather than by who they are. A narrow promise makes it easier to welcome new helpers and easier to notice when an essential part of the job is missing.

## 3. The idea in plain English

**Duck typing** means using an object according to the operations it supports rather than requiring a particular class. If a caller needs `greet()`, any suitable object can work. A `Protocol` describes that required shape for static type checkers without forcing implementations to inherit from it.

Priya's greeting job becomes a protocol with one method. **Structural typing** means matching the required members, not belonging to a declared inheritance family. Python itself does not enforce ordinary annotations when the program runs. A static checker can reject an incompatible call before execution, while an unchecked call fails when it tries to use a missing operation.

An **abstract base class**, built with `ABC` and `abstractmethod`, is another option. A subclass with unimplemented abstract methods cannot be instantiated. Use that when an explicit shared family and runtime construction restriction are useful. It is different from simply describing the shape a caller accepts.

## 4. The picture

```text
                    welcome(greeter)
                            |
                            v
                     greet() -> text
                       /         \
                      v           v
                    Friend     Neighbour
                    hello       namaste
```

The caller needs one operation. Python Protocol and Go interfaces allow structural matching; the C++ example uses an explicitly inherited abstract base.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
class Greeter(Protocol):
    def greet(self) -> str: ...
```

The ellipsis marks a protocol method description rather than useful greeting behaviour. Friend and Neighbour provide real methods with that signature. welcome calls only greet, so it need not know which class produced the object.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
from typing import Protocol

class Greeter(Protocol):
    def greet(self) -> str: ...

class Friend:
    def greet(self) -> str:
        return "hello"

class Neighbour:
    def greet(self) -> str:
        return "namaste"

def welcome(greeter: Greeter) -> None:
    print(greeter.greet())

welcome(Friend())
welcome(Neighbour())
```

**Check the result:** Run `python main.py`. It prints `hello` and `namaste`. Neither class inherits from Greeter; their methods satisfy its shape for a static checker.

## 6. How the other two languages do it

- **Python** — Duck typing asks whether an object supports an operation.
- **Go** — An interface lists required methods.
- **C++** — A pure virtual operation defines required behaviour.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** assume writing `greeter: Greeter` validates incoming objects at runtime. It does not. Static checks must actually be run, and external data still needs runtime validation.

**Failure to reproduce:** add `welcome(object())` and run the program. The final line is `AttributeError: 'object' object has no attribute 'greet'`. A type checker should reject that call before execution. Runtime-checkable protocols can inspect member presence, but they do not fully validate method signatures or behaviour.

## 8. Say it out loud

**How it gets asked:** “What is an interface, and when does the compiler check it?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** Python can use an object by its supported operations, which is duck typing. I express the expected shape with Protocol when I want static checking without requiring inheritance. An abstract base class instead defines an explicit family and can block construction of incomplete subclasses. Neither approach proves the method's semantics; I still test what the caller expects it to do.

**Follow-ups**

1. **Must Friend inherit Greeter?** No; Protocol uses structural compatibility.

2. **Do annotations run validation?** No. Run a static checker separately.

3. **When use ABC?** When shared inheritance and required implementations at construction are part of the design.

**Model answer:** The ellipsis marks a protocol method description rather than useful greeting behaviour. Friend and Neighbour provide real methods with that signature. welcome calls only greet, so it need not know which class produced the object. A matching method name does not prove correct behaviour.

## 9. Recall card

- Duck typing asks whether an object supports an operation.
- Protocol describes that shape to static checkers.
- Ordinary annotations do not enforce it at runtime.
- ABC can prevent construction of incomplete subclasses.
- A matching method name does not prove correct behaviour.
