---
day: 5
track: lang-python
title: "def, default arguments, *args, **kwargs, and returning anything"
theme: "Functions"
phase: "Languages: every language, every basic"
status: written
---

# Day 005 · Python — def, default arguments, *args, **kwargs, and returning anything

**Today's theme:** Functions

**After today you can:** You can write a function with several inputs and outputs in each language and explain where each argument lives.

**The interviewer asks it as:** *How does each language return more than one value?*

---

## 1. What this is, and why it matters

A function is a named block of lines that takes some inputs, does something, and hands back a result, so that you write the lines once and use them from anywhere. Python functions are declared with `def`, take arguments by position or by name, can give arguments default values, can accept any number of extras with `*args` and `**kwargs`, and can return anything at all, including several values at once. Every name created inside a function lives only inside it and is gone when it returns.

At work, a program is a few hundred functions calling each other, and the shape of each one, what goes in and what comes out, is most of what design means. Interviewers ask "how do you return multiple values", "what is the mutable default argument bug", and "what is the difference between `*args` and `**kwargs`", and all three are today.

## 2. The story

Farhan's father needs a new kurta for a wedding on the twentieth, and Farhan is sent to the tailor with the cloth.

The tailor is a small, quick man who has been on the same corner for thirty years. Farhan hands over the folded cloth and says the three numbers his mother told him: chest forty-two, length thirty-eight, sleeve twenty-four. The tailor writes nothing down. He nods.

"Collar?" the tailor asks. Farhan does not know. "Then the usual," the tailor says. "Band collar. Everybody who does not say wants the band collar." Farhan realises that if his mother had cared, she would have told him, and that the tailor has a standing answer for anyone who does not.

"Pockets?" Farhan's mother had said one on the left. "Left, then. If you had said nothing, I would have done none."

On Thursday Farhan comes back. The tailor hands him a kurta on a hanger, and then, separately, a folded square of the same cloth. "Leftover," he says. "Nearly half a metre. Your mother will want it." So Farhan walks home carrying two things from one visit: the thing he asked for and the thing that came out of making it. He had not thought of the leftover as a result. The tailor had.

The next week Farhan's uncle sends him back with four shirts that all need the sleeves taken up by the same amount. The tailor does not want to hear about them one at a time. "Put them all on the counter. Same job, however many there are." He counts them, does the same thing four times, and hands back four shirts.

And Farhan notices one more thing. While the tailor is measuring, he says numbers out loud to himself, chest, length, sleeve, and then forgets them completely the moment the kurta is done. Ask him a week later what Farhan's father's chest measurement was, and he will shrug. Those numbers existed for one job. When the job ended, so did they.

## 3. The idea in plain English

A **function** is a named block of lines that you can run by name. You define it once with `def stitch(chest, length):` and a colon, and indent its lines underneath. You **call** it by writing its name with round brackets: `stitch(42, 38)`.

The names inside the round brackets of the `def` are **parameters**: `chest`, `length`. The values you pass when calling are **arguments**: `42`, `38`. The tailor's parameters are chest, length, sleeve; Farhan's arguments were 42, 38, 24. The distinction matters only when someone asks; most people say "arguments" for both.

`return` hands a value back to whoever called. A function with no `return` hands back `None`, Python's word for "nothing". To return several values, write `return kurta, leftover`; Python bundles them into a **tuple**, an unchangeable row of values, and the caller unpacks it with `kurta, leftover = stitch(...)`. That is the kurta and the folded square in one visit.

A **default argument** is a parameter with a standing answer: `def stitch(chest, length, collar="band"):`. Callers who do not mention the collar get the band collar. Callers who care pass `collar="mandarin"`, by name, which is called a **keyword argument**. You can pass any argument by name, in any order, as long as you name it.

`*args` collects any number of extra positional arguments into a tuple: the four shirts on the counter. `**kwargs` collects any number of extra keyword arguments into a **dict**, a set of name-to-value pairs that day 7 covers. You will read these in other people's code long before you need to write them.

**Type hints** say what kind of value each parameter and the return should be: `def stitch(chest: int, length: int) -> str:`. Python does not enforce them; they are documentation that tools can check, and this course always writes them.

Every name you create inside a function is **local**: it exists from the moment it is assigned until the function returns, and then it is gone. The tailor's measurements. A name created outside all functions is **global**, and functions can read it but cannot quietly change it.

## 4. The picture

```
 the call:   kurta, leftover = stitch(42, 38, collar="mandarin")

 inside stitch, for the length of this one call:
 ┌─ local names ─────────────────────────────┐
 │ chest   = 42       ← positional, 1st      │
 │ length  = 38       ← positional, 2nd      │
 │ collar  = "mandarin"  ← by name; "band" if omitted
 │ sleeve  = 24       ← default, nobody said │
 │ kurta   = "..."    ← made inside          │
 └───────────────────────────────────────────┘
        │ return kurta, leftover  → ("kurta 42/38 mandarin", 0.45)
        ▼ the box is thrown away; only the returned tuple survives
 caller: kurta = "kurta 42/38 mandarin"    leftover = 0.45
```

*Notice that the box exists only for one call. Call `stitch` again and you get a fresh box. Notice also that the two returned values travel together as one tuple and are split apart on the caller's side.*

## 5. The code, built step by step

Start `tailor.py` in a `day05` folder. The simplest function first.

```python
def stitch(chest: int, length: int) -> str:
    return f"kurta {chest}/{length}"

print(stitch(42, 38))
```

```
kurta 42/38
```

`def`, the name, the parameters with their type hints, `-> str` saying it returns a string, a colon, an indented body. The `print` line is outside the function, at the left margin, and it runs the function by calling it.

Defaults and keyword arguments.

```python
def stitch(chest: int, length: int, collar: str = "band", pocket: str = "none") -> str:
    return f"kurta {chest}/{length}, {collar} collar, pocket {pocket}"

print(stitch(42, 38))
print(stitch(42, 38, pocket="left"))
print(stitch(length=38, chest=42, collar="mandarin"))
```

```
kurta 42/38, band collar, pocket none
kurta 42/38, band collar, pocket left
kurta 42/38, mandarin collar, pocket none
```

Parameters with defaults must come after those without. Once you name an argument, every argument after it must be named too. The third call shows that named arguments can come in any order.

Returning more than one thing.

```python
def stitch_with_leftover(chest: int, length: int, cloth: float) -> tuple[str, float]:
    used = (chest + length) / 40
    kurta = f"kurta {chest}/{length}"
    return kurta, cloth - used

kurta, leftover = stitch_with_leftover(42, 38, 2.5)
print(kurta, "with", leftover, "metres left")
```

```
kurta 42/38 with 0.5 metres left
```

`return kurta, cloth - used` returns a tuple of two. The hint `tuple[str, float]` says so. The caller unpacks it into two names in one line. `used` is a local name; try to print it after the call and you get a `NameError`, because it is gone.

Any number of arguments.

```python
def take_up(amount: int, *shirts: str) -> str:
    return f"took up {len(shirts)} shirts by {amount} cm: {', '.join(shirts)}"

print(take_up(2, "white", "blue", "check", "grey"))
```

```
took up 4 shirts by 2 cm: white, blue, check, grey
```

`*shirts` gathers every positional argument after `amount` into a tuple called `shirts`. Four this time; it could be none or forty.

And `**kwargs`, which you will mostly read rather than write.

```python
def order(**details: str) -> None:
    for name, value in details.items():
        print(f"  {name}: {value}")

order(collar="band", pocket="left", thread="white")
```

```
  collar: band
  pocket: left
  thread: white
```

`**details` gathers every named argument into a dict, and `.items()` walks its name-value pairs. `-> None` says this function returns nothing useful; it only prints.

Here is the run and output for the complete program.

```bash
python3 tailor.py
```

```
kurta 42/38, band collar, pocket none
kurta 42/38, band collar, pocket left
kurta 42/38, mandarin collar, pocket none
kurta 42/38 with 0.5 metres left
took up 4 shirts by 2 cm: white, blue, check, grey
order details:
  collar: band
  pocket: left
  thread: white
```

And the complete file.

```python
# tailor.py — day 5, functions
# Run:  python3 tailor.py


def stitch(chest: int, length: int, collar: str = "band", pocket: str = "none") -> str:
    """One kurta, with a standing answer for collar and pocket."""
    return f"kurta {chest}/{length}, {collar} collar, pocket {pocket}"


def stitch_with_leftover(chest: int, length: int, cloth: float) -> tuple[str, float]:
    """The kurta and the leftover cloth, together."""
    used = (chest + length) / 40
    kurta = f"kurta {chest}/{length}"
    return kurta, cloth - used


def take_up(amount: int, *shirts: str) -> str:
    """Same job, however many shirts are on the counter."""
    return f"took up {len(shirts)} shirts by {amount} cm: {', '.join(shirts)}"


def order(**details: str) -> None:
    """Whatever named details the caller wants to mention."""
    for name, value in details.items():
        print(f"  {name}: {value}")


print(stitch(42, 38))
print(stitch(42, 38, pocket="left"))
print(stitch(length=38, chest=42, collar="mandarin"))

kurta, leftover = stitch_with_leftover(42, 38, 2.5)
print(kurta, "with", leftover, "metres left")

print(take_up(2, "white", "blue", "check", "grey"))

print("order details:")
order(collar="band", pocket="left", thread="white")
```

The text in triple quotes under each `def` is a **docstring**, a description that tools and other programmers read. Two blank lines between top-level functions is the convention.

## 6. How the other two languages do it

Go, where multiple returns are built into the language and defaults do not exist:

```go
func stitchWithLeftover(chest, length int, cloth float64) (string, float64) {
	used := float64(chest+length) / 40
	return fmt.Sprintf("kurta %d/%d", chest, length), cloth - used
}

kurta, leftover := stitchWithLeftover(42, 38, 2.5)
```

C++, where you must declare before you use, and multiple returns go through a pair:

```cpp
std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth) {
    double used = (chest + length) / 40.0;
    return {std::format("kurta {}/{}", chest, length), cloth - used};
}

auto [kurta, leftover] = stitch_with_leftover(42, 38, 2.5);
```

The one line of difference that matters: **Python and Go return several values as a first-class idea; C++ packs them into one object and unpacks it on the other side.** Python's tuple and Go's `(string, float64)` both read as "this function gives back two things". C++'s `std::pair` reads as "this function gives back one thing that happens to have two parts", and until C++17's `auto [a, b]` syntax you had to pull them out by hand. The second thing to notice is what only Python has: default values and arguments passed by name. Go has neither and says so proudly. C++ has defaults but not names.

## 7. The traps

**The near-miss: the mutable default.** This looks like it starts each order with an empty list.

```python
def add_shirt(shirt: str, pile: list[str] = []) -> list[str]:
    pile.append(shirt)
    return pile

print(add_shirt("white"))
print(add_shirt("blue"))
```

```
['white']
['white', 'blue']
```

The second call was supposed to give `['blue']`. The default list is created **once**, when the `def` line runs, and every call that omits `pile` shares that same list. This is the most famous Python bug there is. The fix is `pile: list[str] | None = None`, then `if pile is None: pile = []` inside. Never use a list or a dict as a default value.

**The real error: forgetting to return.** Compute a value and forget the `return`.

```python
def cloth_needed(chest: int, length: int) -> float:
    needed = (chest + length) / 40

total = cloth_needed(42, 38) + 0.5
```

```
Traceback (most recent call last):
  File "/home/you/day05/tailor.py", line 4, in <module>
    total = cloth_needed(42, 38) + 0.5
            ~~~~~~~~~~~~~~~~~~~~~^~~~~
TypeError: unsupported operand type(s) for +: 'NoneType' and 'int'
```

A function without `return` returns `None`, and `None + 0.5` fails. The error points at the line that did the adding, not the function that forgot. When you see `NoneType` in an error, look for a missing `return`.

**The near-miss: positional after keyword.** Name one argument and then go back to positions.

```python
print(stitch(chest=42, 38))
```

```
  File "/home/you/day05/tailor.py", line 1
    print(stitch(chest=42, 38))
                             ^
SyntaxError: positional argument follows keyword argument
```

Once you start naming, you keep naming. Python catches this before running anything.

## 8. Say it out loud

**How it gets asked**

- "How do you return multiple values from a function?"
- "What is the mutable default argument problem?"
- "What is the difference between `*args` and `**kwargs`?"

**What to say out loud, the first ninety seconds**

"A Python function is defined with `def`, takes parameters by position or by keyword, and can give any parameter a default value. To return more than one thing, I write `return a, b`, which builds a tuple, and the caller unpacks it with `a, b = f()`. Go does the same natively; C++ uses `std::pair` or `std::tuple` with structured bindings.

`*args` collects extra positional arguments into a tuple and `**kwargs` collects extra keyword arguments into a dict; they let a function accept whatever the caller sends, and they are how wrappers forward arguments to another function.

Default values are evaluated once, when the `def` runs, not on each call. So a mutable default like an empty list is shared across every call that omits it, and appending to it accumulates. The fix is a default of `None` and creating the list inside the function. Every name assigned inside a function is local and disappears when the function returns."

**The follow-ups**

1. *"Can a function change a variable defined outside it?"* — It can read it. Assigning to the same name creates a local instead, unless you declare `global name`, which is almost always a design smell; pass it in and return it instead.
2. *"What does a function return if it has no `return` statement?"* — `None`. Adding or indexing `None` produces a `TypeError` mentioning `NoneType`, which is the tell.
3. *"What is a keyword-only argument?"* — A parameter after a bare `*` in the signature, `def f(a, *, verbose=False)`, which callers must pass by name. Used to stop long argument lists being called positionally by mistake.

**A model answer**

"`def name(params) -> return_type:` defines a function; arguments bind by position, then by keyword, and parameters may carry defaults evaluated once at definition time. `return a, b` returns a tuple, unpacked at the call site, which is the idiomatic multi-value return. `*args` and `**kwargs` gather variadic positional and keyword arguments respectively. The mutable-default trap comes directly from single evaluation: `def f(x, acc=[])` shares one list across calls, so the idiom is `acc=None` with an in-body check. Locals live in the call's frame and vanish on return, and a missing `return` yields `None`, which surfaces later as a `TypeError` mentioning `NoneType`."

## 9. Recall card

- `def f(a: int, b: int = 0) -> str:`; defaults after non-defaults; call by position or by name, and once named, stay named.
- `return a, b` returns a tuple; `a, b = f()` unpacks it; no `return` means `None`, and `NoneType` in an error means a missing `return`.
- `*args` gathers extra positionals into a tuple; `**kwargs` gathers extra keywords into a dict.
- Defaults are evaluated once: never `=[]` or `={}`; use `=None` and create inside.
- Names assigned inside a function are local and vanish when it returns.
