---
day: 5
track: lang-go
title: "func, multiple return values, named results, variadic"
theme: "Functions"
phase: "Languages: every language, every basic"
status: written
---

# Day 005 · Go — func, multiple return values, named results, variadic

**Today's theme:** Functions

**After today you can:** You can write a function with several inputs and outputs in each language and explain where each argument lives.

**The interviewer asks it as:** *How does each language return more than one value?*

---

## 1. What this is, and why it matters

A Go function is declared with `func`, names the type of every parameter and every result, and can return several results at once as a first-class feature of the language. It can name its results, accept any number of trailing arguments with `...`, and it cannot do two things Python does: give a parameter a default value, or be called with arguments by name. Every parameter is a copy, and every variable declared inside is local to that call.

At work, multiple returns are why Go code reads `value, err := doThing()` on every other line; the second result is how Go reports failure, and day 9 is built on it. Interviewers ask "how does Go return multiple values", "why does Go have no default arguments", and "what does `...` mean in a parameter list", and all three are today.

## 2. The story

Farhan's father needs a new kurta for a wedding on the twentieth, and Farhan is sent to the tailor with the cloth.

The tailor is a small, quick man who has been on the same corner for thirty years. Farhan hands over the folded cloth and says the three numbers his mother told him: chest forty-two, length thirty-eight, sleeve twenty-four. The tailor writes nothing down. He nods.

"Collar?" the tailor asks. Farhan does not know. "Then the usual," the tailor says. "Band collar. Everybody who does not say wants the band collar." Farhan realises that if his mother had cared, she would have told him, and that the tailor has a standing answer for anyone who does not.

"Pockets?" Farhan's mother had said one on the left. "Left, then. If you had said nothing, I would have done none."

On Thursday Farhan comes back. The tailor hands him a kurta on a hanger, and then, separately, a folded square of the same cloth. "Leftover," he says. "Nearly half a metre. Your mother will want it." So Farhan walks home carrying two things from one visit: the thing he asked for and the thing that came out of making it. He had not thought of the leftover as a result. The tailor had.

The next week Farhan's uncle sends him back with four shirts that all need the sleeves taken up by the same amount. The tailor does not want to hear about them one at a time. "Put them all on the counter. Same job, however many there are." He counts them, does the same thing four times, and hands back four shirts.

And Farhan notices one more thing. While the tailor is measuring, he says numbers out loud to himself, chest, length, sleeve, and then forgets them completely the moment the kurta is done. Ask him a week later what Farhan's father's chest measurement was, and he will shrug. Those numbers existed for one job. When the job ended, so did they.

## 3. The idea in plain English

A **function** is a named block you run by name. In Go: `func stitch(chest int, length int) string { ... }`. The word `func`, the name, the **parameters** each with a type, the type of the **result** after the closing bracket, and the body in braces. When several parameters in a row share a type, you may write it once: `chest, length int`.

You **call** it with `stitch(42, 38)`. The values passed are **arguments**, and every one of them is copied into the function's parameter. Change `chest` inside and the caller's variable does not move. Day 12 is about what that copying means for bigger things.

`return` hands results back. Go's distinctive feature: a function can have **several results**, declared in brackets after the parameters, `(string, float64)`, and returned together, `return kurta, leftover`. The caller writes `kurta, leftover := stitch(...)`. That is Farhan walking home with the kurta and the folded square. This is not a tuple wrapped up and unwrapped; it is two results, and the compiler insists you take both, or explicitly throw one away with `_`.

Results can be **named**: `func stitch(...) (kurta string, leftover float64)`. Named results are ordinary variables inside the function, start at their zero value, and a bare `return` sends back whatever they hold. Use names when they document what each result means; avoid the bare `return` in anything longer than a few lines.

A **variadic** parameter takes any number of arguments: `func takeUp(amount int, shirts ...string)`. Inside, `shirts` is a slice of strings, and callers write `takeUp(2, "white", "blue")` or `takeUp(2, pile...)` to spread an existing slice. That is the four shirts on the counter.

What Go does **not** have: default values, and calling by name. `stitch(42, 38, collar="band")` is not Go. If a function needs options, you pass them all, pass a struct (day 8), or write a second function. The designers thought defaults hide behaviour and named arguments make signatures fragile, and they left both out.

Every variable declared inside a function is **local**: it exists for this call and is gone at `return`. The tailor's measurements.

## 4. The picture

```
 the call:  kurta, leftover := stitchWithLeftover(42, 38, 2.5)

 inside, for this one call:
 ┌─ locals ──────────────────────────────┐
 │ chest  int     = 42   ← copied in     │
 │ length int     = 38   ← copied in     │
 │ cloth  float64 = 2.5  ← copied in     │
 │ used   float64 = 2.0  ← made inside   │
 └───────────────────────────────────────┘
      │ return "kurta 42/38", cloth - used
      ▼ two results, both must be received
 caller:  kurta = "kurta 42/38"    leftover = 0.5

 k := stitchWithLeftover(42, 38, 2.5)      ✗ compile error: 1 variable, 2 values
 k, _ := stitchWithLeftover(42, 38, 2.5)   ✓ second result thrown away on purpose
```

*Notice the last two lines. Go will not let you quietly drop a result. You take it or you write `_`, and either way a reader can see what you decided.*

## 5. The code, built step by step

Start `tailor.go` in a `day05` folder.

```go
package main

import "fmt"

func stitch(chest, length int) string {
	return fmt.Sprintf("kurta %d/%d", chest, length)
}
```

Functions are declared at the top level, outside `main`, in any order; Go does not care whether `stitch` is above or below the code that calls it. `chest, length int` declares two `int` parameters. The result type `string` comes after the brackets.

Two results.

```go
func stitchWithLeftover(chest, length int, cloth float64) (string, float64) {
	used := float64(chest+length) / 40
	kurta := fmt.Sprintf("kurta %d/%d", chest, length)
	return kurta, cloth - used
}
```

`(string, float64)` declares two results. `float64(chest+length)` converts the int sum to a float before dividing, because Go will not divide an int by a float. `used` and `kurta` are local and gone after `return`.

Named results.

```go
func measure(chest, length int) (cloth float64, seams int) {
	cloth = float64(chest+length) / 40
	seams = 4
	return
}
```

`cloth` and `seams` exist from the first line, starting at `0` and `0`. The bare `return` sends back whatever they hold. This reads well in a short function and badly in a long one, where a reader has to scroll to find out what is being returned.

Variadic.

```go
func takeUp(amount int, shirts ...string) string {
	return fmt.Sprintf("took up %d shirts by %d cm: %v", len(shirts), amount, shirts)
}
```

`shirts ...string` must be the last parameter. Inside, it is a `[]string`. `%v` prints any value in its default form, which for a slice is `[white blue check grey]`.

Calling all of them from `main`.

```go
func main() {
	fmt.Println(stitch(42, 38))

	kurta, leftover := stitchWithLeftover(42, 38, 2.5)
	fmt.Println(kurta, "with", leftover, "metres left")

	cloth, seams := measure(42, 38)
	fmt.Println("needs", cloth, "metres and", seams, "seams")

	fmt.Println(takeUp(2, "white", "blue", "check", "grey"))
	pile := []string{"grey", "check"}
	fmt.Println(takeUp(3, pile...))
}
```

```
kurta 42/38
kurta 42/38 with 0.5 metres left
needs 2 metres and 4 seams
took up 4 shirts by 2 cm: [white blue check grey]
took up 2 shirts by 3 cm: [grey check]
```

`pile...` spreads an existing slice into the variadic parameter. Without the three dots, the compiler refuses, and that is in the traps.

Here is the run and output for the complete program.

```bash
go run tailor.go
```

```
kurta 42/38
kurta 42/38 with 0.5 metres left
only the kurta: kurta 42/38
needs 2 metres and 4 seams
took up 4 shirts by 2 cm: [white blue check grey]
took up 2 shirts by 3 cm: [grey check]
```

And the complete file.

```go
// tailor.go — day 5, functions
// Run:  go run tailor.go
package main

import "fmt"

// stitch makes one kurta. No defaults: every caller says both numbers.
func stitch(chest, length int) string {
	return fmt.Sprintf("kurta %d/%d", chest, length)
}

// stitchWithLeftover returns the kurta and the cloth left over, together.
func stitchWithLeftover(chest, length int, cloth float64) (string, float64) {
	used := float64(chest+length) / 40
	kurta := fmt.Sprintf("kurta %d/%d", chest, length)
	return kurta, cloth - used
}

// measure uses named results; they start at zero and a bare return sends them back.
func measure(chest, length int) (cloth float64, seams int) {
	cloth = float64(chest+length) / 40
	seams = 4
	return
}

// takeUp does the same job to however many shirts are on the counter.
func takeUp(amount int, shirts ...string) string {
	return fmt.Sprintf("took up %d shirts by %d cm: %v", len(shirts), amount, shirts)
}

func main() {
	fmt.Println(stitch(42, 38))

	kurta, leftover := stitchWithLeftover(42, 38, 2.5)
	fmt.Println(kurta, "with", leftover, "metres left")

	onlyKurta, _ := stitchWithLeftover(42, 38, 2.5)
	fmt.Println("only the kurta:", onlyKurta)

	cloth, seams := measure(42, 38)
	fmt.Println("needs", cloth, "metres and", seams, "seams")

	fmt.Println(takeUp(2, "white", "blue", "check", "grey"))
	pile := []string{"grey", "check"}
	fmt.Println(takeUp(3, pile...))
}
```

The comment above each function starting with its name is the Go convention for documentation; tools read it. `onlyKurta, _ :=` shows the second result being thrown away on purpose, visibly.

## 6. How the other two languages do it

Python, with defaults, keyword arguments, and a tuple for the two results:

```python
def stitch(chest: int, length: int, collar: str = "band") -> str:
    return f"kurta {chest}/{length}, {collar} collar"

def stitch_with_leftover(chest: int, length: int, cloth: float) -> tuple[str, float]:
    return f"kurta {chest}/{length}", cloth - (chest + length) / 40

print(stitch(42, 38, collar="mandarin"))
kurta, leftover = stitch_with_leftover(42, 38, 2.5)
```

C++, with defaults but no names, and a `std::pair` for the two results:

```cpp
std::string stitch(int chest, int length, std::string collar = "band");

std::pair<std::string, double> stitch_with_leftover(int chest, int length, double cloth) {
    return {std::format("kurta {}/{}", chest, length), cloth - (chest + length) / 40.0};
}

auto [kurta, leftover] = stitch_with_leftover(42, 38, 2.5);
```

The one line of difference that matters: **Go has multiple results built in and nothing else; Python has everything; C++ has defaults and overloading but packs multiple results into one object.** A Python programmer coming to Go reaches for `collar="band"` and finds it does not exist, and reaches for a single return value with `_` and finds the compiler asking about the second one. A C++ programmer coming to Go looks for overloading, two functions with the same name and different parameters, and finds Go has none of that either: one name, one function. Go's answer to all of it is the same: write another function, or pass a struct.

## 7. The traps

**The real error: taking one result from a function that gives two.** This looks like it grabs the kurta.

```go
	kurta := stitchWithLeftover(42, 38, 2.5)
```

```
./tailor.go:33:11: assignment mismatch: 1 variable but stitchWithLeftover returns 2 values
```

Write `kurta, _ :=`. The compiler makes you say what happens to the second result.

**The real error: passing a slice to a variadic without the dots.** This looks right.

```go
	pile := []string{"grey", "check"}
	fmt.Println(takeUp(3, pile))
```

```
./tailor.go:37:25: cannot use pile (variable of type []string) as string value in argument to takeUp
```

Without `...`, Go thinks you are passing one shirt whose name is a whole slice. `takeUp(3, pile...)` spreads it.

**The near-miss: shadowing a named result.** Named results plus `:=` inside.

```go
func measure(chest, length int) (cloth float64, seams int) {
	if chest > 40 {
		cloth := float64(chest+length) / 40
		seams = 4
		_ = cloth
	}
	return
}
```

No error, and `cloth` comes back as `0`. The `:=` inside the `if` declared a new `cloth` that died at the closing brace, and the named result was never touched. This is day 4's shadowing bug wearing a new coat, and named results make it easier to fall into. Use `=` to assign to a named result, and prefer explicit `return cloth, seams` in anything but the shortest functions.

## 8. Say it out loud

**How it gets asked**

- "How does Go return multiple values?"
- "Why does Go have no default arguments or function overloading?"
- "What does `...` mean in a Go function signature?"

**What to say out loud, the first ninety seconds**

"A Go function declares a type for every parameter and every result, and it can have more than one result, declared in brackets: `func f() (string, error)`. The caller receives them all with `a, b := f()`, and the compiler refuses a call that takes the wrong number, so a result can only be ignored by writing `_` explicitly. This is the basis of Go's error handling: the last result is conventionally an `error`.

Results can be named, which documents them and lets a bare `return` send back their current values; I use the names for documentation but write the explicit `return` in anything non-trivial, because a bare return plus an inner `:=` silently shadows the result.

Go has no default arguments, no keyword arguments, and no overloading. The philosophy is that a call site should show everything being passed, and one name should mean one function. When a function needs options, I pass a struct or add a second function. Variadic parameters, `shirts ...string`, accept any number of trailing arguments as a slice, and an existing slice is spread with `pile...`."

**The follow-ups**

1. *"Are arguments passed by value or by reference?"* — Always by value: the parameter is a copy. For slices, maps and pointers, the copy is a small header that refers to shared data, so changes through it are visible to the caller. Day 12 covers this precisely.
2. *"Can a function be a value?"* — Yes. Functions are first-class: you can store one in a variable, pass it as an argument, and return one. Day 19 is about that.
3. *"What is the cost of returning two values compared with one?"* — Negligible. Results are returned in registers or on the stack like parameters; there is no allocation for a multi-value return.

**A model answer**

"Go functions are typed on every parameter and result and support multiple results natively, `func f(x int) (string, float64)`, received as `a, b := f(x)`; the compiler enforces arity, so discarding a result requires `_`. Named results are pre-declared zero-valued locals returned by a bare `return`. Variadic functions take `args ...T` as the final parameter, seen internally as `[]T`, with an existing slice spread via `s...`. Go deliberately omits default arguments, keyword arguments and overloading, favouring explicit call sites and one function per name; options travel in a struct. All arguments are passed by value, and locals live only for the duration of the call."

## 9. Recall card

- `func name(a, b int, c float64) (string, float64) { return x, y }`; types on everything; declared at top level in any order.
- Multiple results are native: `a, b := f()`; taking one is `assignment mismatch`; discard with `_` on purpose.
- Named results `(cloth float64, seams int)` start at zero and a bare `return` sends them; `:=` inside shadows them silently, so assign with `=`.
- Variadic `shirts ...string` is a `[]string` inside; spread an existing slice with `pile...` or the compiler refuses.
- No defaults, no keyword arguments, no overloading: pass everything, or pass a struct, or write another function.
