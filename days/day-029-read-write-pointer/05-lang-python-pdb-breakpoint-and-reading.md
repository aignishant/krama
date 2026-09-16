---
day: 29
track: lang-python
title: "pdb, breakpoint(), and reading a traceback"
theme: "Debugging"
phase: "Languages: advanced features"
status: written
---

# Day 029 · Python — pdb, breakpoint(), and reading a traceback

**Today's theme:** Debugging

**After today you can:** You can set a breakpoint, step, and inspect a variable in each language.

**The interviewer asks it as:** *Your program crashes. Walk me through how you find the bug.*

## 1. What this is, and why it matters

A traceback shows the calls that led to an exception. pdb lets you stop at a line, inspect values, and step through the failing path.

You use this when discussing debugging in an interview. The useful answer includes both the working case and the boundary where its guarantee ends.

## 2. The story

Omar follows a recipe for a family dinner. The finished dish tastes far too salty. He could immediately add more water, but that would hide the reason and might ruin the texture. Instead, he asks everyone to stop changing it while he works out what happened.

He begins with the last step and walks backwards. His sister added a spoon of salt because the recipe said so. Before that, his brother added a ready-made sauce. The sauce already contained salt. The recipe had assumed an unsalted sauce, but nobody had noticed the difference.

Omar repeats a small portion in a separate pan. This time he pauses before the salt goes in and tastes what is already there. He checks the amount of sauce rather than guessing from the final flavour. The smaller portion gives him a way to repeat the problem without wasting another whole meal.

He changes one thing: he leaves out the extra salt. The portion tastes right. Then he tries the same change in another small portion to make sure the first result was not luck. He tells the family exactly which assumption failed.

For the next dinner, they add a check beside the recipe: taste the sauce before adding salt. They have not merely rescued tonight’s food. They have found a repeatable cause and a check that will catch the same mistake before it spoils another meal.

## 3. The idea in plain English

Omar’s small pan is the minimal reproducer. A **breakpoint** pauses before an operation, so you can compare actual values with the assumptions needed for it to work. In pdb, n steps over a call, s steps into it, c continues, and p evaluates an expression.

Read the final traceback line for the exception category, then inspect the innermost relevant frame. Work back toward the caller only when the bad value came from there. The program below intentionally fails; the repair is to reject empty input and use len(values) - 1 for the last valid position.

## 4. The picture

```text
reproduce -> stop before failure -> inspect values -> test one cause -> regression case
```

A debugger exposes the actual state; it does not choose the explanation for you.

## 5. The code, built step by step

First isolate the important operation:

```python
position = len(values)
return values[position]
```

Inspect the failing operation’s actual inputs.

The complete example follows. Save as `main.py`. Run `python main.py` to reproduce the failure. Then run `python -m pdb main.py`; use `b last`, `c`, `p position`, `p len(values)`, and `n`. You can also insert `breakpoint()` before the return.

```python
def last(values: list[int]) -> int:
    position = len(values)
    return values[position]

def main() -> None:
    values = [10, 20, 30]
    print(last(values))

if __name__ == "__main__":
    main()
```

**Check the result:** This intentional reproducer ends with `IndexError: list index out of range`. At the return, position is 3 and len(values) is 3, so valid positions 0, 1, and 2 exclude the requested position. Change the function to raise ValueError("empty input") for an empty list and return values[-1] otherwise; the repaired program prints 30.

After inspecting the failure, replace the file with this complete repair. Run the same ordinary build/run command; it prints `30`.

```python
def last(values: list[int]) -> int:
    if not values:
        raise ValueError("empty input")
    return values[-1]

def main() -> None:
    print(last([10, 20, 30]))
    assert last([7]) == 7
    try:
        last([])
    except ValueError as error:
        assert str(error) == "empty input"
    else:
        raise AssertionError("empty input was accepted")

if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

**Go**

```go
position := len(values)
return values[position]
```

A Go panic dump names the failing goroutine and call frames. Delve can pause that execution and inspect the values that violated an assumption.

**C++**

```cpp
auto position = values.size();
return values.at(position);
```

GDB exposes call frames and local values. Sanitizers instrument a program to detect selected memory errors and undefined behaviour during execution.

Python pdb, Go Delve, and C++ GDB all support breakpoints and inspection. Tracebacks identify the failing path; sanitizers add checks for C++ memory and undefined-behaviour defects.

## 7. The traps

**Near-miss:** catch IndexError and return 0, hiding both empty input and the off-by-one defect. The real failure is `IndexError: list index out of range`. Inspect the position before changing code. Do not print secrets merely because you are debugging; choose the specific state needed for the hypothesis.

## 8. Say it out loud

**How it gets asked:** “Your program crashes. Walk me through how you find the bug.” Another phrasing is “Show the smallest example that demonstrates the rule, then show an input that breaks the tempting alternative.”

**Your first ninety seconds:** I reproduce the failure with the smallest input, read the exception and relevant frame, and pause before the operation. I compare the observed index with the valid range rather than guessing from the final message. I change one cause, rerun the failing case, and add empty and one-element cases. I use breakpoint for interactive inspection and remove temporary stops from the final program.

**Follow-ups**

1. **Why minimise the input?** It removes unrelated state and makes the causal path easier to inspect.

2. **What is the difference between n and s?** n steps over calls; s enters the next call when possible.

3. **When is the repair complete?** When the original failure and neighbouring boundary cases meet the intended contract.

**Model answer:** A traceback shows the calls that led to an exception. pdb lets you stop at a line, inspect values, and step through the failing path. A regression case preserves the reason for the fix.

## 9. Recall card

- Inspect the failing operation’s actual inputs.
- Read the final exception and relevant stack frame.
- Change one hypothesis at a time.
- A regression case preserves the reason for the fix.

Further reading: [Official reference](https://docs.python.org/3.12/library/pdb.html).
