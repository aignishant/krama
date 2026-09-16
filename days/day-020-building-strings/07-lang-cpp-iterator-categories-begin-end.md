---
day: 20
track: lang-cpp
title: "Iterator categories, begin/end, and C++20 ranges"
theme: "Iterators and generators"
phase: "Languages: advanced features"
status: written
---

# Day 020 · C++ — Iterator categories, begin/end, and C++20 ranges

**Today's theme:** Iterators and generators

**After today you can:** You can produce values lazily in each language without building the whole list first.

**The interviewer asks it as:** *How do you loop over something that does not fit in memory?*

---

## 1. What this is, and why it matters

An **iterator** represents a position in a sequence and supports operations for reading or advancing it. `begin` identifies the first position and `end` identifies the boundary after the last element. Never dereference that boundary. A **range** groups traversal access; a **view** is a range designed for inexpensive composition, often with lazy operations.

Today you use iterators and generators to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Isha helps serve breakfast at a family gathering. There is space for only six plates beside the stove. She could try to cook every dosa before anyone starts eating, but the early ones would become cold and the kitchen would fill with trays. Instead, she cooks one when someone is ready to take it.

Her uncle stands nearby and asks for the next dosa. Isha makes it, hands it over, and waits for the next request. She remembers how much batter remains and whether the pan is hot. She does not restart the entire preparation each time someone asks.

After three servings, her uncle says he is full. Isha stops. There is no reason to cook the rest of the batter merely because it is available. The next person may begin another round later, but the first person's breakfast is finished.

Her cousin points out that the breakfast table and the serving process are different things. A tray holding six finished dosas can be visited repeatedly while the food remains there. The act of cooking the next dosa advances the meal. Asking again does not bring back the dosa that was already eaten.

Isha finds the arrangement useful for a large gathering. She keeps only the current work near the stove, serves each item when needed, and stops when the person eating stops asking. The total amount of food may be large, but she does not have to hold it all ready at once.

## 3. The idea in plain English

An **iterator** represents a position in a sequence and supports operations for reading or advancing it. `begin` identifies the first position and `end` identifies the boundary after the last element. Never dereference that boundary. A **range** groups traversal access; a **view** is a range designed for inexpensive composition, often with lazy operations.

Isha's on-demand servings resemble a transform view: the next result is produced when traversal needs it. C++20 ranges can compose a source, a transformation, and a limit without allocating a vector of all intermediate values. Such a view may refer to existing storage, so that storage must remain alive.

Iterator categories describe supported operations. Input iterators support single-pass reading; forward iterators support repeated passes, bidirectional iterators also move backwards, and random-access iterators support jumps and distance arithmetic. Contiguous iterators additionally describe adjacent element storage. Do not assume every iterator supports `+ 5` just because vector's iterator does.

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

```cpp
auto squares = std::views::iota(0, 10)
    | std::views::transform([](int value) { return value * value; });
```

iota provides successive integers and transform computes a square when accessed. take limits the consumer to the requested prefix. The second loop traverses a new prefix of the same repeatable view; it does not depend on a stored vector of squares.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.cpp`.

```cpp
#include <iostream>
#include <ranges>

int main() {
    auto squares = std::views::iota(0, 10)
        | std::views::transform([](int value) { return value * value; });
    for (int value : squares | std::views::take(3)) {
        std::cout << value << '\n';
    }
    int total = 0;
    for (int value : squares | std::views::take(4)) {
        total += value;
    }
    std::cout << "sum " << total << '\n';
}
```

**Check the result:** Compile with a compiler and standard library supporting C++20 ranges, using `g++ -std=c++20 -Wall -Wextra main.cpp -o demo`. It prints `0`, `1`, `4`, and `sum 14`.

## 6. How the other two languages do it

- **Python** — An iterable supplies an iterator.
- **Go** — Go 1.23 supports range over iterator functions.
- **C++** — begin starts traversal; end marks its boundary.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** return a view referring to a local vector. The vector dies when the function returns, leaving dangling access. Return owned data or keep the source alive for the view's whole use.

**Failure to reproduce:** with `std::list<int> values{1, 2};`, try `auto position = values.begin() + 1;` after including `<list>`. GCC reports a diagnostic containing `no match for 'operator+'`. A list iterator is bidirectional, not random-access. Advance it with `++position` or an appropriate iterator utility. Dereferencing end is a separate undefined-behaviour bug, not a guaranteed exception.

## 8. Say it out loud

**How it gets asked:** “How do you loop over something that does not fit in memory?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** C++ iterators describe traversal positions, and their categories determine which operations are available. Ranges and views compose traversal, often lazily, without requiring intermediate containers. I check source lifetime and invalidation rules as carefully as the transformation. The pipeline saves retained results, but repeated traversal can recompute them, so laziness is a trade-off rather than automatic caching.

**Follow-ups**

1. **Is end an element?** No. It is the boundary after the last element.

2. **Does a view always own its source?** No. Many views borrow storage whose lifetime must cover traversal.

3. **Can this squares view be read again?** Yes. This iota-based source is repeatable and recomputes values.

**Model answer:** iota provides successive integers and transform computes a square when accessed. take limits the consumer to the requested prefix. The second loop traverses a new prefix of the same repeatable view; it does not depend on a stored vector of squares. Laziness is not caching and does not guarantee less total work.

## 9. Recall card

- begin starts traversal; end marks its boundary.
- Iterator categories determine supported operations.
- Views compose lazy traversal without intermediate vectors.
- Borrowed sources must outlive their views.
- Laziness is not caching and does not guarantee less total work.
