---
day: 20
track: lang-python
title: "__iter__, __next__, yield, and generator expressions"
theme: "Iterators and generators"
phase: "Languages: advanced features"
status: written
---

# Day 020 · Python — __iter__, __next__, yield, and generator expressions

**Today's theme:** Iterators and generators

**After today you can:** You can produce values lazily in each language without building the whole list first.

**The interviewer asks it as:** *How do you loop over something that does not fit in memory?*

---

## 1. What this is, and why it matters

An **iterable** can provide an iterator through `iter(value)`. An **iterator** supplies successive values through `next` and signals completion with StopIteration. A **generator** is an iterator created by a function containing `yield`; it suspends execution between produced values.

Today you use iterators and generators to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Isha helps serve breakfast at a family gathering. There is space for only six plates beside the stove. She could try to cook every dosa before anyone starts eating, but the early ones would become cold and the kitchen would fill with trays. Instead, she cooks one when someone is ready to take it.

Her uncle stands nearby and asks for the next dosa. Isha makes it, hands it over, and waits for the next request. She remembers how much batter remains and whether the pan is hot. She does not restart the entire preparation each time someone asks.

After three servings, her uncle says he is full. Isha stops. There is no reason to cook the rest of the batter merely because it is available. The next person may begin another round later, but the first person's breakfast is finished.

Her cousin points out that the breakfast table and the serving process are different things. A tray holding six finished dosas can be visited repeatedly while the food remains there. The act of cooking the next dosa advances the meal. Asking again does not bring back the dosa that was already eaten.

Isha finds the arrangement useful for a large gathering. She keeps only the current work near the stove, serves each item when needed, and stops when the person eating stops asking. The total amount of food may be large, but she does not have to hold it all ready at once.

## 3. The idea in plain English

An **iterable** can provide an iterator through `iter(value)`. An **iterator** supplies successive values through `next` and signals completion with StopIteration. A **generator** is an iterator created by a function containing `yield`; it suspends execution between produced values.

Isha's pan state becomes the generator's saved local state. Calling a generator function creates the generator without executing its body. Each next resumes until another yield or completion. A for loop drives that protocol and handles normal exhaustion for you.

An iterator is often one-shot. Iterating the same exhausted generator again does not restart its function. Call the generator function again for a new traversal. A generator expression, `(value * value for value in range(10))`, is a compact lazy producer. A list comprehension eagerly stores its results. Laziness saves retained storage only while consumers avoid materialising everything.

## 4. The picture

```text
source/state ---> produce one ---> consumer
     ^                              |
     |                              | wants another
     +------------------------------+
                                    | stops
                                    v
                               no later work

retained results: current item + consumer's running state
materialise all:  item 0, item 1, item 2, ... item n-1
```

Lazy traversal avoids retaining all results. The producer must obey early termination, and any borrowed resources or storage must remain valid while traversal is active.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
def squares(limit: int) -> Iterator[int]:
    for value in range(limit):
        yield value * value
```

Each yield hands one square to the consumer and suspends the loop. One explicit next consumes zero; the following list consumes 1, 4, and 9. Reusing that exhausted generator produces no values, while a new generator expression can still sum a fresh traversal.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
from collections.abc import Iterator

def squares(limit: int) -> Iterator[int]:
    for value in range(limit):
        yield value * value

values = squares(4)
print(next(values))
print(list(values))
print(list(values))
print(sum(value * value for value in range(4)))
```

**Check the result:** Run `python main.py`. It prints `0`, `[1, 4, 9]`, `[]`, and `14`. The first list consumes the remaining generator values; the second sees exhaustion.

## 6. How the other two languages do it

- **Python** — An iterable supplies an iterator.
- **Go** — Go 1.23 supports range over iterator functions.
- **C++** — begin starts traversal; end marks its boundary.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** sum a generator, then try to list that same generator for debugging. The sum consumed it. Create a fresh generator or deliberately store results if repeated access is required.

**Failure to reproduce:** after both list calls, evaluate `next(values)`. The exception is `StopIteration`. Use `next(values, default)` when an explicit fallback is appropriate. A generator paused inside a resource-holding context may keep that resource until resumed or closed, so keep ownership clear when consumers stop early.

## 8. Say it out loud

**How it gets asked:** “How do you loop over something that does not fit in memory?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** I use an iterable to obtain an iterator, then consume values through the next protocol. A generator implements that protocol with suspended function state and yield. It can avoid storing the whole result, but is normally exhausted after one pass. I distinguish the source from one traversal and explain where resource cleanup happens if the consumer stops before exhaustion.

**Follow-ups**

1. **What do __iter__ and __next__ do?** They provide an iterator and its next value; a normal iterator returns itself from __iter__.

2. **Does lazy mean less total CPU work?** Not necessarily. Consuming everything still does the work; early stopping can avoid later work.

3. **What does list(generator) change?** It consumes the iterator and stores all produced values.

**Model answer:** Each yield hands one square to the consumer and suspends the loop. One explicit next consumes zero; the following list consumes 1, 4, and 9. Reusing that exhausted generator produces no values, while a new generator expression can still sum a fresh traversal. Streaming saves storage only if consumers avoid materialising everything.

## 9. Recall card

- An iterable supplies an iterator.
- An iterator advances with next until StopIteration.
- yield suspends a generator with its local state.
- Exhausted generators do not restart themselves.
- Streaming saves storage only if consumers avoid materialising everything.
