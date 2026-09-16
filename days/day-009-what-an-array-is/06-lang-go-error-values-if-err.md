---
day: 9
track: lang-go
title: "Error values: if err != nil, errors.New, fmt.Errorf"
theme: "Errors, three ways"
phase: "Languages: every language, every basic"
status: written
---

# Day 009 · Go — Error values: if err != nil, errors.New, fmt.Errorf

**Today's theme:** Errors, three ways

**After today you can:** You can make a function fail in each language and make the caller handle it, and say which style each language prefers.

**The interviewer asks it as:** *Should this function throw, or return an error?*

---

## 1. What this is, and why it matters

In Go, a failure is an ordinary value: a function that can fail returns an extra result of type `error`, which is `nil` when everything went well and holds a description when it did not. The caller checks it on the very next line, `if err != nil`, and either deals with it or hands it upward, usually with a note attached. Nothing climbs the stack on its own. There are no exceptions for ordinary failure; the closest thing, `panic`, is reserved for bugs.

At work, `if err != nil` is the most common three-line block in every Go codebase, and the discipline of wrapping errors with context as they pass upward is what makes a Go log line tell you the whole story in one read. Interviewers ask "why does Go not have exceptions", "what is the difference between `errors.New` and `fmt.Errorf`", and "what does `%w` do", and all three are today.

## 2. The story

Kabir sends a birthday parcel to his sister by courier, three days early, from the branch near his office.

On Tuesday the delivery boy reaches the building and the flat number does not exist. Flat 4B. The building stops at 3. He does not phone anyone. He puts the parcel back in the van, comes back to the branch, and hands it across the counter with a slip: "4B, building stops at 3, Tuesday 11:20." That is his whole job when a delivery fails. Come back, hand it over, say exactly what happened.

The branch clerk looks at the slip. She cannot fix the address either. So she does the same thing one level up: she adds her own line to the slip, "Andheri branch, returned by driver 7," and sends the parcel with the slip to the booking office where Kabir paid. The booking office adds a line, "booked by Kabir, phone ending 4471," and phones him.

By the time Kabir hears about it, the slip has three lines on it, and each one says who had the parcel and what they knew. Nobody in the chain was surprised. Nobody was interrupted mid-sentence. Each person received the parcel and the slip, looked at the slip, added what they knew, and passed both on. At every handover, both hands were used: one for the parcel and one for the slip, and the slip was empty on a good day and full on a bad one.

Kabir's sister, when she finally gets the parcel on Wednesday, asks why the delivery boy could not have just phoned someone. Kabir says that in this company, nobody phones anyone. Every handover has a slip, and you read the slip before you do anything else. It is slower per step, and nobody ever loses a parcel, and you can always tell from the slip exactly where it went wrong.

She says that sounds exhausting. He says it sounds exhausting until the day something goes wrong.

## 3. The idea in plain English

An **`error`** is a built-in type. Any value that has a method `Error() string` is an `error`; that is the whole definition, and day 16 explains the mechanism, called an interface. Today you only need to make them and check them.

A function that can fail returns an error as its **last result**: `func findFlat(flat string) (string, error)`. When the function succeeds, it returns the real result and `nil`, Go's word for "no value here", which for an error means "nothing went wrong". When it fails, it returns a zero result and a non-nil error. The slip is empty on a good day and full on a bad one.

The caller receives both and checks the slip first:

```go
receipt, err := findFlat("4B")
if err != nil {
	return "", err
}
```

This is the shape. Three lines, immediately after every call that can fail. If `err` is not `nil`, deal with it or return it. Only after that do you touch `receipt`. Go's compiler helps with day 5's rule: you cannot take one result from a function that returns two, so you cannot accidentally forget the error exists. You can deliberately ignore it with `_`, and that is on you.

Making an error: `errors.New("flat does not exist")` for a fixed message, or `fmt.Errorf("flat %s does not exist", flat)` when the message needs values in it. Both come from the standard library, `errors` and `fmt`.

Adding a line to the slip: `fmt.Errorf("send parcel: %w", err)`. The `%w` verb **wraps** the inner error inside the new one, so the message reads `send parcel: flat 4B does not exist` and the original is still inside. Each function on the way up adds its own prefix, and by the time the error is printed it reads like the slip: `book: send parcel: flat 4B does not exist`.

Asking about the inside: `errors.Is(err, ErrNoFlat)` looks through the wrapping layers and answers whether a particular known error is in there. That needs a **sentinel error**, a package-level variable like `var ErrNoFlat = errors.New("flat does not exist")`, that callers can compare against. Never compare error message text; compare with `errors.Is`.

And `panic`: it exists, it unwinds the stack like an exception, and it is for bugs, an index out of range, a nil map write, a state that should be impossible. It is not for a missing flat. Go's answer to the interview question is: return.

## 4. The picture

```
 findFlat("4B")          returns  ("",  error{"flat 4B does not exist"})
        │
        ▼  slip read, line added
 sendParcel("4B")        returns  ("",  error{"send parcel: flat 4B does not exist"})
        │
        ▼  slip read, line added
 book("Kabir", "4B")     returns  (     error{"book for Kabir: send parcel: flat 4B does not exist"})
        │
        ▼  slip read, decision made
 main()                  prints it, or errors.Is(err, ErrNoFlat) → true

 Every arrow is two hands: the result and the error, together, checked at each step.
 Nothing moves up on its own. A function that forgets to return err drops the parcel.
```

*Notice that each layer adds its name to the front and keeps the original inside. Notice that the failure only climbs because every function chose to pass it up.*

## 5. The code, built step by step

Start `courier.go` in a `day09` folder. A sentinel, and the function that fails.

```go
package main

import (
	"errors"
	"fmt"
)

var ErrNoFlat = errors.New("flat does not exist")

var flats = map[string]bool{"1A": true, "2A": true, "3A": true, "1B": true, "2B": true, "3B": true}

func findFlat(flat string) (string, error) {
	if !flats[flat] {
		return "", fmt.Errorf("flat %s: %w", flat, ErrNoFlat)
	}
	return "delivered to " + flat, nil
}
```

`ErrNoFlat` is a package-level error that callers can compare against. `findFlat` wraps it with the specific flat using `%w`, and returns `nil` for the error on success. `ErrNoFlat` starts with `Err` by convention.

The function in the middle, which must pass it on by hand.

```go
func sendParcel(flat string) (string, error) {
	receipt, err := findFlat(flat)
	if err != nil {
		return "", fmt.Errorf("send parcel: %w", err)
	}
	return "receipt: " + receipt, nil
}
```

Compare this with Python's `send_parcel`, which had no error handling at all. Here the three lines are mandatory: without them, a failure in `findFlat` would be silently dropped, because `err` would go unused and the compiler would refuse, or be ignored with `_` and the parcel would vanish.

The caller.

```go
func main() {
	for _, flat := range []string{"2B", "4B"} {
		receipt, err := sendParcel(flat)
		if err != nil {
			fmt.Println("could not deliver:", err)
			continue
		}
		fmt.Println(receipt)
	}
}
```

```
receipt: delivered to 2B
could not deliver: send parcel: flat 4B: flat does not exist
```

The message reads as the slip: each layer's prefix, then the original. `continue` moves to the next flat; in a function you would `return` instead.

Looking inside the wrapping.

```go
	_, err := sendParcel("4B")
	fmt.Println(errors.Is(err, ErrNoFlat))
	fmt.Println(err.Error() == "flat does not exist")
```

```
true
false
```

`errors.Is` unwraps layer by layer and finds `ErrNoFlat` inside. Comparing the text fails, because the text has been prefixed twice. This is why you wrap with `%w` and check with `errors.Is`, never with string comparison.

A failure from the standard library, handled the same way.

```go
	for _, text := range []string{"3", "four"} {
		n, err := strconv.Atoi(text)
		if err != nil {
			fmt.Println("bad input:", err)
			continue
		}
		fmt.Println(n)
	}
```

```
3
bad input: strconv.Atoi: parsing "four": invalid syntax
```

`strconv.Atoi` turns text into a number, and its second result is the same `error` type you have been writing yourself. Every failing function in the standard library follows this shape, and so should yours. Add `"strconv"` to the imports.

Here is the run and output for the complete program.

```bash
go run courier.go
```

```
receipt: delivered to 2B
could not deliver: send parcel: flat 4B: flat does not exist
is it the no-flat error? true
is the text equal? false
3
bad input: strconv.Atoi: parsing "four": invalid syntax
```

And the complete file.

```go
// courier.go — day 9, error values
// Run:  go run courier.go
package main

import (
	"errors"
	"fmt"
	"strconv"
)

// ErrNoFlat is a sentinel: callers compare against it with errors.Is.
var ErrNoFlat = errors.New("flat does not exist")

var flats = map[string]bool{"1A": true, "2A": true, "3A": true, "1B": true, "2B": true, "3B": true}

func findFlat(flat string) (string, error) {
	if !flats[flat] {
		return "", fmt.Errorf("flat %s: %w", flat, ErrNoFlat)
	}
	return "delivered to " + flat, nil
}

// sendParcel adds its own line to the slip and passes the parcel up.
func sendParcel(flat string) (string, error) {
	receipt, err := findFlat(flat)
	if err != nil {
		return "", fmt.Errorf("send parcel: %w", err)
	}
	return "receipt: " + receipt, nil
}

func main() {
	for _, flat := range []string{"2B", "4B"} {
		receipt, err := sendParcel(flat)
		if err != nil {
			fmt.Println("could not deliver:", err)
			continue
		}
		fmt.Println(receipt)
	}

	_, err := sendParcel("4B")
	fmt.Println("is it the no-flat error?", errors.Is(err, ErrNoFlat))
	fmt.Println("is the text equal?", err.Error() == "flat does not exist")

	for _, text := range []string{"3", "four"} {
		n, err := strconv.Atoi(text)
		if err != nil {
			fmt.Println("bad input:", err)
			continue
		}
		fmt.Println(n)
	}
}
```

## 6. How the other two languages do it

Python, where the failure climbs on its own and the function in the middle says nothing:

```python
def find_flat(flat: str) -> str:
    if flat not in FLATS:
        raise AddressError(f"flat {flat} does not exist")
    return f"delivered to {flat}"

def send_parcel(flat: str) -> str:
    return f"receipt: {find_flat(flat)}"      # no handling; the exception passes through

try:
    print(send_parcel("4B"))
except AddressError as error:
    print(f"could not deliver: {error}")
```

C++, where you can throw like Python, or return a value that is either a result or an error, like Go:

```cpp
std::expected<std::string, std::string> find_flat(const std::string& flat) {
    if (!flats.contains(flat)) {
        return std::unexpected("flat " + flat + " does not exist");
    }
    return "delivered to " + flat;
}

auto result = find_flat("4B");
if (!result) {
    std::cout << "could not deliver: " << result.error() << "\n";
}
```

The one line of difference that matters: **in Go, a function's signature tells you it can fail; in Python it does not.** `func sendParcel(flat string) (string, error)` announces the failure. `def send_parcel(flat: str) -> str` hides it, and you find out by reading the body of every function it calls. Go pays for that honesty with three lines after every call. C++'s `std::expected` is Go's idea in C++ clothing, and its `throw` is Python's; C++ lets each project choose, and most large ones have a rule about which.

## 7. The traps

**The near-miss: the shadowed `err`.** Declare `err` outside, then use `:=` inside a block.

```go
	var receipt string
	var err error
	if flats["2B"] {
		receipt, err := findFlat("4B")
		_ = receipt
		_ = err
	}
	fmt.Println(receipt, err)
```

```
 <nil>
```

The `:=` inside the `if` made a **new** `receipt` and a **new** `err` that died at the closing brace. The outer ones were never set. Day 4's shadowing, in the one place it does the most damage. Inside a block, assign to existing variables with `=`, not `:=`.

**The real error: returning only the error.** Forget the first result.

```go
func sendParcel(flat string) (string, error) {
	receipt, err := findFlat(flat)
	if err != nil {
		return err
	}
	return "receipt: " + receipt, nil
}
```

```
./courier.go:22:10: not enough return values
	have (error)
	want (string, error)
```

Every return must supply every result. Write `return "", err`.

**The near-miss: the ignored error.** Throw the slip away.

```go
	receipt, _ := findFlat("4B")
	fmt.Println(receipt)
```

```

```

An empty line. The parcel is gone and nothing said so. The compiler allowed it because you wrote `_` on purpose. The only time `_` for an error is acceptable is when you have written a comment explaining why the failure genuinely cannot matter, and even then someone will ask.

## 8. Say it out loud

**How it gets asked**

- "Why does Go use error values instead of exceptions?"
- "What is the difference between `errors.New` and `fmt.Errorf`, and what does `%w` do?"
- "Should this function throw, or return an error?"

**What to say out loud, the first ninety seconds**

"Go treats errors as values. A function that can fail returns an `error` as its last result, `nil` on success. The caller checks it immediately, `if err != nil`, and either handles it or returns it, usually wrapped with context: `fmt.Errorf("send parcel: %w", err)`. `%w` keeps the original error inside the new one, so `errors.Is` can later check for a specific sentinel like `ErrNoFlat` through any number of wrapping layers, and the printed message reads as a chain of context from the outermost call to the root cause.

The reason is visibility. Because the error is in the signature, a reader knows which calls can fail and sees the handling at the call site; nothing propagates invisibly. The cost is repetition: the three-line check after every fallible call. `errors.New` makes a fixed error, typically a package-level sentinel; `fmt.Errorf` formats a message and, with `%w`, wraps. `panic` exists for programmer errors and impossible states, not for expected failures like a bad address or a missing file. So in Go the answer to 'throw or return' is always return."

**The follow-ups**

1. *"When is `panic` appropriate?"* — For bugs: a violated invariant, an index that cannot be out of range but is, initialisation that cannot proceed. Not for input errors, network failures or missing files. Libraries should almost never panic on behalf of their callers.
2. *"What is `errors.As`?"* — Like `errors.Is`, but for extracting an error of a specific type from the chain so you can read its fields, for example a path out of a `*fs.PathError`. Day 27 covers custom error types.
3. *"Does wrapping have a cost?"* — A small allocation per layer. It is worth it: the alternative is a log line that says "flat does not exist" with no idea which flat, which caller or which request.

**A model answer**

"Go returns errors as the last result of a function, `nil` meaning success, and idiomatic code checks `if err != nil` immediately after each call, returning early. Errors are created with `errors.New` for sentinels or `fmt.Errorf` for formatted messages, and wrapped with `%w` so context accumulates while the original remains inspectable via `errors.Is` and `errors.As`; message text is never compared directly. Failure is therefore part of every signature and every call site, at the cost of verbosity, in exchange for control flow that is visible on the page. `panic` and `recover` exist but are reserved for bugs and unrecoverable states. The classic mistakes are shadowing `err` with `:=` in an inner scope, discarding it with `_`, and comparing strings instead of using `errors.Is`."

## 9. Recall card

- Fallible functions return `(T, error)`; `nil` error means success; check with `if err != nil { return zero, err }` on the very next line.
- `errors.New("fixed message")` for sentinels, `var ErrNoFlat = ...`; `fmt.Errorf("context: %w", err)` to wrap and add a line to the slip.
- `errors.Is(err, ErrNoFlat)` looks through wrapping; never compare `err.Error()` text.
- `:=` inside a block shadows the outer `err` silently; `_` for an error throws the parcel away silently; `return err` alone is `not enough return values`.
- Go's answer to throw or return: return. `panic` is for bugs only.
