---
day: 19
track: lang-python
title: "Functions as values, lambda, and captured variables"
theme: "Closures"
phase: "Languages: advanced features"
status: written
---

# Day 019 · Python — Functions as values, lambda, and captured variables

**Today's theme:** Closures

**After today you can:** You can return a function from a function in each language and say what it captured.

**The interviewer asks it as:** *What is a closure, and what does it capture?*

---

## 1. What this is, and why it matters

A **closure** is a function together with access to variables from an enclosing scope. A function can be returned or stored like another value. A **lambda** is a compact expression that creates a function; it follows the same name-lookup rules as a def-created closure.

Today you use closures to make a small program predictable. In an interview, explain the rule and then trace an example; naming the feature alone does not show that you can use it.

## 2. The story

Tara helps three children practise multiplication. She gives the first child the instruction to add two to any number she says. The second child must add five. The third must add ten. All three follow the same kind of instruction, but each remembers a different extra amount.

Tara goes to the kitchen and calls out seven. The children answer nine, twelve, and seventeen. The instructions remain useful even after she has left the room. Each child needs the remembered amount as well as the number just announced.

Then Tara changes the game. She puts a bowl of counters on the table and tells all three children to add however many counters are currently in the bowl. There are initially two. Before the next round, she adds three more. Now all three answer twelve when she calls seven. They are consulting one shared, changing thing rather than remembering three separate amounts.

Neither game is wrong, but they answer different promises. A child told to remember two should not silently switch to five. A child told to consult the bowl should notice when its contents change. Tara repeats the rule before each round so the children can predict what the next answer will be.

When she explains the game to another parent, she includes both parts: what each child should do, and which information that child carries or consults later. The action alone is not enough to determine the answer.

## 3. The idea in plain English

A **closure** is a function together with access to variables from an enclosing scope. A function can be returned or stored like another value. A **lambda** is a compact expression that creates a function; it follows the same name-lookup rules as a def-created closure.

Tara's remembered amounts become enclosing bindings. `make_adder(2)` creates an invocation whose amount remains accessible to its returned function. Python closures generally look up the captured binding when called; they do not automatically freeze its current value. Separate factory invocations create separate enclosing bindings.

In a loop, several closures can share one changing loop binding and later all observe its final value. A default argument such as `lambda value, amount=amount: value + amount` evaluates that default when the function is created. To rebind an enclosing variable inside a closure, declare it `nonlocal`; mutation of an already shared list does not itself require rebinding.

## 4. The picture

```text
make_adder(2) ---> function + retained amount 2 ---> call(7) = 9
make_adder(5) ---> function + retained amount 5 ---> call(7) = 12

snapshot capture ---> private copied value
shared capture   ---> live binding / original object
                          |
                          v
                 later changes may be observed
```

A closure includes retained context as well as code. The second part distinguishes snapshots from shared state; use each language's precise capture rules.

## 5. The code, built step by step

First isolate the operation that controls today's behaviour:

```python
def make_adder(amount: int) -> Callable[[int], int]:
    def add(value: int) -> int:
        return value + amount
    return add
```

Return the function itself, not the result of calling it. Its enclosing amount remains accessible after the factory returns. The two factory calls below retain different enclosing bindings, producing 9 and 12 from the same input 7.


The complete example follows. Save each labelled file separately if the example contains more than one file. Otherwise save it as `main.py`.

```python
from collections.abc import Callable

def make_adder(amount: int) -> Callable[[int], int]:
    def add(value: int) -> int:
        return value + amount
    return add

add_two = make_adder(2)
add_five = make_adder(5)
print(add_two(7), add_five(7))

callbacks = [lambda amount=amount: amount for amount in range(3)]
print([callback() for callback in callbacks])
```

**Check the result:** Run `python main.py`. It prints `9 12` and `[0, 1, 2]`.

## 6. How the other two languages do it

- **Python** — Functions can be returned and stored as values.
- **Go** — A function value preserves its parameter and result types.
- **C++** — Lambdas are callable objects with captured state.

The syntax changes, so trace the same input in each version before assuming the behaviour carries across. Explain which rule the language enforces and which rule your program has to enforce.

## 7. The traps

**Near-miss:** remove `amount=amount` from the callback lambda, leaving `lambda: amount`. The three later calls return `[2, 2, 2]` because they consult the same enclosing binding after the comprehension finishes.

**Failure to reproduce:** inside make_adder.add insert `amount += 1` without nonlocal. Python treats amount as local and raises UnboundLocalError, commonly ending `cannot access local variable 'amount' where it is not associated with a value`. Declare nonlocal only if updating shared enclosing state is the intended operation.

## 8. Say it out loud

**How it gets asked:** “What is a closure, and what does it capture?” A follow-up phrasing is “Show me a small example, and explain where the tempting version goes wrong.”

**What to say out loud:** A closure retains access to its enclosing bindings after the outer call returns. That lets a factory return behaviour configured with a particular amount. I distinguish late lookup of a captured name from taking a creation-time snapshot through a default argument. If a callback unexpectedly sees the last loop value, I inspect which binding all callbacks share.

**Follow-ups**

1. **Does lambda freeze captured variables?** No. Its lookup rules are the same as an ordinary nested function.

2. **When do defaults get evaluated?** At function creation, not each call.

3. **When is nonlocal needed?** When assigning a new value to an existing enclosing function binding.

**Model answer:** Return the function itself, not the result of calling it. Its enclosing amount remains accessible after the factory returns. The two factory calls below retain different enclosing bindings, producing 9 and 12 from the same input 7. Use nonlocal for intentional enclosing rebinding.

## 9. Recall card

- Functions can be returned and stored as values.
- A closure retains access to enclosing bindings.
- Captured bindings can be looked up at call time.
- Default arguments can take creation-time values.
- Use nonlocal for intentional enclosing rebinding.
