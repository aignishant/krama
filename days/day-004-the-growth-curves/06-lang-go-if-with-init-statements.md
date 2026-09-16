---
day: 4
track: lang-go
title: "if with init statements, the only loop is for, switch without fallthrough"
theme: "Conditions and loops"
phase: "Languages: every language, every basic"
status: written
---

# Day 004 · Go — if with init statements, the only loop is for, switch without fallthrough

**Today's theme:** Conditions and loops

**After today you can:** You can write every loop shape in each language and pick the one that reads cleanest for a given job.

**The interviewer asks it as:** *Write a loop that stops early. Now write it without break.*

---

## 1. What this is, and why it matters

Go has exactly one loop keyword, `for`, and it wears three costumes: the counted loop, the while-style loop, and the loop over a collection. Conditions are `if`/`else if`/`else`, with an optional short statement before the condition that lets you declare a variable that lives only inside the `if`. `switch` picks one of several branches and, unlike C++, does not fall through to the next one unless you say so.

At work you will read the phrase `if err != nil` more than any other three words in Go, and it is this `if` with this init statement. Interviewers ask "why does Go have no `while`", "what is the scope of a variable declared in an `if`", and "does Go's `switch` fall through", and all three are today.

## 2. The story

Sunil gets home at half past seven and cannot find his house key. His wife is out until ten. There are five jackets hanging on the hooks by the door, and the key is in one of them.

He starts at the left. The first jacket is his wife's red one. He does not check it; his key would not be in her jacket. He moves on. The second is his grey work jacket. He checks both pockets. Nothing. The third is his wife's again, the long black one. Skip. The fourth is his old brown jacket from last winter. Left pocket, nothing. Right pocket, keys. He stops. He does not check the fifth jacket, because there is no reason to. He has what he came for.

That is the whole search on a good day. Start at one end. Skip the ones that cannot be right. Stop the moment you find it.

On a bad day, it goes differently. He checks all five, skipping his wife's two, and gets to the end of the row with nothing in his hand. And now, only now, because he reached the end without finding it, he does the thing he was hoping not to do: he phones the locksmith.

His neighbour, watching from the stairs, asks why he did not just check all five and then decide. Sunil says that would be silly. Once the key is in his hand, checking more jackets is wasted time. And the locksmith call is not something he does after every search; it is only for the search that comes up empty.

There is one more version of the same evening. Sometimes Sunil does not think of it as "check jackets until I find the key". He thinks of it as "keep going as long as I have not found it and there are jackets left". Same jackets, same pockets, same moment of stopping. But the rule for stopping is said out loud at the start, instead of being a decision made halfway through. His wife prefers that version. She says it is easier to explain to the locksmith.

## 3. The idea in plain English

A **condition** is a yes-or-no question. In Go its answer is a **bool**, `true` or `false`, made with `==`, `!=`, `<`, `>`, `<=`, `>=`, and joined with `&&` (and), `||` (or), `!` (not).

`if cond { ... } else if cond { ... } else { ... }` picks one block. No round brackets around the condition, and the curly braces are compulsory even for one line. Go also lets you put a short statement before the condition: `if n := count(); n > 3 { ... }`. The variable `n` is created for this `if` and vanishes after it. That is the shape of `if err != nil`, which you meet on day 9.

A **loop** runs a block repeatedly, and Go has one keyword for it, `for`, in three shapes.

`for i := 0; i < 5; i++ { ... }` is the counted loop: a start, a condition checked before each go, and a step after each go. `i++` means add one to `i`.

`for !found && position < len(jackets) { ... }` is the while-style loop: only a condition. Go has no `while` keyword, because this is the same thing. This is Sunil's wife's version, the stopping rule said at the top.

`for i, jacket := range jackets { ... }` walks a collection, giving the index and the item each time. Yesterday you saw it on a string, where it gave runes. On a **slice**, a row of values written `[]string{"red", "grey"}` that day 6 covers properly, it gives each item. If you do not need the index, write `_` in its place, because Go refuses an unused variable.

`break` leaves the loop. `continue` skips to the next go. There is no `for-else`; the locksmith call is a flag checked after the loop.

`switch value { case "red": ... case "grey": ... default: ... }` picks one case and **stops there**. It does not run on into the next case the way C++ does. If you genuinely want that, the keyword `fallthrough` exists, and you will almost never write it.

## 4. The picture

```
 the one keyword, three shapes

 for i := 0; i < 5; i++ {     ┐ start ; check ; step
 }                            ┘ the counted loop

 for !found && i < n {        ┐ check only
 }                            ┘ what other languages call while

 for i, v := range items {    ┐ walk a collection
 }                            ┘ index and value each time

 for {                        ┐ no condition at all
 }                            ┘ runs until break
```

*Notice that all four are the same keyword with parts removed. Go's designers judged that one loop with optional parts is easier to hold in your head than four keywords.*

## 5. The code, built step by step

Start `search.go` in a `day04` folder.

```go
package main

import "fmt"

func main() {
	jackets := []string{"red", "grey", "black", "brown", "green"}
	keyIn := "brown"
```

`[]string{...}` is a slice of strings, a row of values you can walk and index. `jackets[3]` is `"brown"` and `len(jackets)` is 5. Day 6 is all about slices; today you only walk them.

The `if` with an init statement.

```go
	if n := len(jackets); n > 3 {
		fmt.Println("more than three jackets:", n)
	}
```

```
more than three jackets: 5
```

`n` exists only inside this `if`. After the closing brace it is gone. This keeps the temporary out of the rest of the function.

The counted loop.

```go
	for i := 0; i < len(jackets); i++ {
		fmt.Println(i, jackets[i])
	}
```

```
0 red
1 grey
2 black
3 brown
4 green
```

The range loop, with `break` and `continue`.

```go
	hers := []string{"red", "black"}
	for _, jacket := range jackets {
		if jacket == hers[0] || jacket == hers[1] {
			continue
		}
		fmt.Println("checking", jacket)
		if jacket == keyIn {
			fmt.Println("found it")
			break
		}
	}
```

```
checking grey
checking brown
found it
```

`_` throws away the index. `||` is "or". Go has no `in` operator for slices, so the test spells out both of hers; day 7 gives you a better tool for membership.

The while-style loop, which is the interview answer.

```go
	position := 0
	found := false
	for !found && position < len(jackets) {
		if jackets[position] == keyIn {
			found = true
		} else {
			position++
		}
	}
	fmt.Println("found:", found, "at", position)
```

```
found: true at 3
```

No `break`. The loop stops because its condition becomes false. `!found` is "not found".

The locksmith, without `for-else`.

```go
	found = false
	for _, jacket := range jackets {
		if jacket == "nowhere" {
			found = true
			break
		}
	}
	if !found {
		fmt.Println("checked every jacket; phoning the locksmith")
	}
```

```
checked every jacket; phoning the locksmith
```

A flag before, a check after. This is the shape you write in Go and in C++.

`switch`, which does not fall through.

```go
	switch keyIn {
	case "red", "black":
		fmt.Println("that is hers")
	case "brown":
		fmt.Println("the old brown one")
	default:
		fmt.Println("some other jacket")
	}
```

```
the old brown one
```

One case runs, then the `switch` is over. A case can list several values with commas. No `break` is needed. `default` catches the rest.

Here is the run and output for the complete program.

```bash
go run search.go
```

```
more than three jackets: 5
with break:
  skip red
  checking grey
  skip black
  checking brown -> found it
with a for condition:
  found: true at position 3
searching for a key that is not there:
  checked every jacket; phoning the locksmith
switch: the old brown one
```

And the complete file.

```go
// search.go — day 4, if with init, the one loop, switch
// Run:  go run search.go
package main

import "fmt"

func main() {
	jackets := []string{"red", "grey", "black", "brown", "green"}
	hers := []string{"red", "black"}
	keyIn := "brown"

	if n := len(jackets); n > 3 {
		fmt.Println("more than three jackets:", n)
	}

	fmt.Println("with break:")
	for _, jacket := range jackets {
		if jacket == hers[0] || jacket == hers[1] {
			fmt.Println("  skip", jacket)
			continue
		}
		if jacket == keyIn {
			fmt.Println("  checking", jacket, "-> found it")
			break
		}
		fmt.Println("  checking", jacket)
	}

	fmt.Println("with a for condition:")
	position := 0
	found := false
	for !found && position < len(jackets) {
		if jackets[position] == keyIn {
			found = true
		} else {
			position++
		}
	}
	fmt.Println("  found:", found, "at position", position)

	fmt.Println("searching for a key that is not there:")
	found = false
	for _, jacket := range jackets {
		if jacket == "nowhere" {
			found = true
			break
		}
	}
	if !found {
		fmt.Println("  checked every jacket; phoning the locksmith")
	}

	switch keyIn {
	case "red", "black":
		fmt.Println("switch: that is hers")
	case "brown":
		fmt.Println("switch: the old brown one")
	default:
		fmt.Println("switch: some other jacket")
	}
}
```

## 6. How the other two languages do it

Python, with indentation instead of braces and a `for-else` that Go lacks:

```python
for jacket in jackets:
    if jacket == key_in:
        print("found it")
        break
else:
    print("phoning the locksmith")
```

C++, with `while` and `do-while` as separate keywords and a `switch` that falls through:

```cpp
while (!found && position < jackets.size()) {
    if (jackets[position] == key_in) found = true;
    else ++position;
}
switch (code) {
    case 1: std::cout << "one\n";      // no break: falls into case 2
    case 2: std::cout << "two\n"; break;
}
```

The one line of difference that matters: **Go's `switch` stops after the matching case; C++'s runs on into the next case unless you write `break`.** A C++ programmer writing Go will sprinkle `break` at the end of every case out of habit, which is harmless. A Go programmer writing C++ will leave them out, and the program will run two cases where one was meant, silently. The second difference is the loop keyword count: Python two, C++ four, Go one. Go's `for` with only a condition is exactly the other languages' `while`, so nothing is missing, just renamed.

## 7. The traps

**The near-miss: the shadowed variable.** This looks like it updates `count`.

```go
	count := 0
	if true {
		count := 5
		fmt.Println("inside:", count)
	}
	fmt.Println("outside:", count)
```

```
inside: 5
outside: 0
```

No error. The `:=` inside the braces declared a **new** `count` that lives only inside the `if`, and the outer one never changed. This is called **shadowing**, and it is Go's most common silent bug. Inside a block, use `=` to assign to an existing variable; `:=` always makes a fresh one.

**The real error: the unused loop index.** Ask for the index and not use it.

```go
	for i, jacket := range jackets {
		fmt.Println(jacket)
	}
```

```
./search.go:9:6: declared and not used: i
```

Replace `i` with `_`. Same rule as day 2: nothing declared may go unused.

**The near-miss: `while`.** Write the loop the way you would in another language.

```go
	while position < 5 {
```

```
./search.go:12:8: syntax error: unexpected name position at end of statement
```

Go has never heard of `while`; it reads it as a name and gets confused by the next word. Write `for position < 5 {`.

## 8. Say it out loud

**How it gets asked**

- "Why does Go only have `for`?"
- "What is the scope of a variable declared in an `if` init statement?"
- "Does Go's `switch` fall through?"

**What to say out loud, the first ninety seconds**

"Go has one loop keyword, `for`, with optional parts. With all three parts it is a counted loop; with only a condition it is what other languages call `while`; with `range` it walks a slice, map, string or channel; and with nothing at all it runs until `break`. So there is no `while` keyword because `for cond` already is one.

`if` takes an optional init statement: `if n := f(); n > 0 { }` declares `n` for the duration of the `if` and its `else` branches only, which is how `if err != nil` keeps the error out of the enclosing scope. The trap is that `:=` inside any block declares a new variable, so writing `x := ...` inside an `if` when you meant to update the outer `x` shadows it silently.

`switch` evaluates cases top to bottom and runs only the first match, with no fallthrough by default; a case can list multiple values, and `fallthrough` exists if you really want the C behaviour. Stopping a loop early is `break`; without `break`, I put the exit condition in the `for` header with a flag."

**The follow-ups**

1. *"What happens to the loop variable across iterations?"* — Since Go 1.22, each iteration gets its own copy, so capturing it in a closure or goroutine is safe. Before 1.22 there was one shared variable, and that was a famous bug.
2. *"How do you break out of a nested loop?"* — With a label: `outer:` before the outer `for`, then `break outer` from the inner one. Or a flag, or a function with `return`.
3. *"What can you `switch` on?"* — Any comparable value, or nothing at all: `switch { case x > 5: ... }` is a clean way to write an `if`/`else if` chain.

**A model answer**

"Go's single `for` covers counted loops, condition-only loops, `range` loops and infinite loops by omitting parts of the header, so `while` is unnecessary. `if` and `switch` accept an init statement whose variables are scoped to that statement, which is the basis of the `if err != nil` idiom. Shadowing via `:=` inside a block is the classic mistake, because it compiles and silently leaves the outer variable unchanged. `switch` has no implicit fallthrough, matches the first case only, allows comma-separated values and a tagless form, and `fallthrough` is explicit. To stop early without `break`, I encode the exit in the loop condition: `for !found && i < len(xs)`."

## 9. Recall card

- One keyword: `for init; cond; step {}`, `for cond {}` (while), `for i, v := range xs {}`, `for {}` (until break).
- `if n := f(); n > 3 {}` declares `n` for the `if` only; braces are compulsory; no round brackets.
- `:=` inside a block makes a new variable and shadows the outer one silently; use `=` to update.
- `switch` runs one case and stops; commas list several values; `fallthrough` is explicit and rare.
- No `for-else`: flag before the loop, `break` inside, check the flag after; unused `i` in `range` is a compile error, so write `_`.
