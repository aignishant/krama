---
day: 13
track: lang-python
title: "Reference counting and the garbage collector"
theme: "Memory: who frees what"
phase: "Languages: every language, every basic"
status: written
---

# Day 013 · Python — Reference counting and the garbage collector

**Today's theme:** Memory: who frees what

**After today you can:** You can say where a value lives, who frees it, and when, in each language.

**The interviewer asks it as:** *How does memory get freed in your language?*

---

## 1. What this is, and why it matters

**Reference counting** tracks strong references to objects in CPython, the usual Python implementation. Releasing the last strong reference often makes an object eligible for immediate destruction there. Python as a language does not guarantee CPython's exact reclamation timing.

Today you use memory: who frees what to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Anika borrows a badminton racket at the sports centre. The attendant gives her a numbered tag and says to return the racket before leaving. Anika plays one game and hands both items back. The racket is ready for the next person, and nobody has to search the building for it.

Her brother borrows a second racket, then lends it to a friend while he gets water. When he returns, the friend is still playing. He cannot return that racket merely because he has stopped using it. Someone else still needs it. The attendant waits until the last person brings it back.

Two friends make a different mistake. Each believes the other will return a pair of spare rackets. Both leave. No one is playing with them, but the rackets remain beside a bench because the responsibility has gone round in a circle. At closing time, an attendant walks through the hall and finds the forgotten equipment.

Anika notices that the three arrangements have different costs. Returning her own racket promptly is simple because responsibility is clear. Shared borrowing needs everyone to keep track of who still needs the racket. The final walk through the building finds things that ordinary handovers miss, but it takes work and happens later.

Before borrowing again, she asks who is responsible for returning the equipment and when that must happen. Being finished with something and having actually returned it are related, but they are not the same event.

## 3. The idea in plain English

**Reference counting** tracks strong references to objects in CPython, the usual Python implementation. Releasing the last strong reference often makes an object eligible for immediate destruction there. Python as a language does not guarantee CPython's exact reclamation timing.

Shared rackets correspond to several names referring to one object. `del name` removes that binding; it does not command every alias to disappear. A **cycle** is a chain of references that reaches itself. CPython also has a cyclic garbage collector to find unreachable tracked groups that reference counting alone cannot release.

Memory management is not resource management. Close files with `with` rather than waiting for garbage collection. The example uses a **weak reference**, which can observe an object without keeping it alive. An explicit `gc.collect()` makes this demonstration observable; forcing collection repeatedly is not a routine performance fix.

## 4. The picture

```text
live owner / root ----> object A ----> object B
                          ^               |
                          +---------------+

Remove the outside path:
  tracing collector: A and B may become unreachable
  strong reference counts: the cycle can retain owners
  unique ownership: one responsible owner releases its object
```

Distinguish a live outside path from a cycle's internal links. Go traces reachability; CPython supplements reference counting with cyclic collection; C++ shared ownership needs cycles broken explicitly.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
box = Box()
box.self = box
reference = weakref.ref(box)
```

The self field makes a strong cycle, while reference observes without owning. Once the local strong name disappears, the cycle is unreachable. The complete program requests a collection and then checks that the weak reference no longer finds an object.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
import gc
import weakref

class Box:
    pass

def make_cycle() -> weakref.ReferenceType[Box]:
    box = Box()
    box.self = box
    return weakref.ref(box)

reference = make_cycle()
gc.collect()
print(reference() is None)
values = [1, 2]
alias = values
del values
print(alias)
```

**Check the result:** Run `python main.py` on CPython. It prints `True` and `[1, 2]`. Automatic collection could have occurred before the explicit collection too.

## 6. How the other two languages do it

- **Python** — CPython uses reference counting plus cyclic collection.
- **Go** — Go keeps reachable objects alive.
- **C++** — RAII ties release to an owning object's lifetime.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** use `__del__` as the main way to close a file. Destruction timing, shutdown, and exceptions complicate that design. A context manager gives cleanup a clear boundary even when work raises an exception.

**Failure to reproduce:** after `values = [1]; del values`, evaluate `values`. The final line is `NameError: name 'values' is not defined`. That says a binding is gone; it says nothing about whether another binding still keeps the list alive.

## 8. Say it out loud

**How it gets asked:** “How does memory get freed in your language?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** CPython combines reference counting with cyclic garbage collection. Dropping one name removes one reference, not necessarily the object. Unreachable cycles need the collector. I do not promise exact destruction timing across Python implementations, and I use context managers for resources that need prompt release, such as files. Memory reclamation and closing a file are separate responsibilities.

**Follow-ups**

1. **Does del force reclamation?** No; other strong references may remain.

2. **Does a weak reference keep its target alive?** No. Calling it returns the object if still alive, otherwise None.

3. **Should every request call gc.collect()?** No. Measure first; explicit collection itself costs work.

**Model answer:** The self field makes a strong cycle, while reference observes without owning. Once the local strong name disappears, the cycle is unreachable. The complete program requests a collection and then checks that the weak reference no longer finds an object. Do not depend on exact garbage-collection timing.

## 9. Recall card

- CPython uses reference counting plus cyclic collection.
- Removing one binding may leave other references.
- Unreachable cycles can be collected.
- Use with for prompt resource cleanup.
- Do not depend on exact garbage-collection timing.
