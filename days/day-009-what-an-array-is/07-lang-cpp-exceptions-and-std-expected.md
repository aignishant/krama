---
day: 9
track: lang-cpp
title: "Exceptions and std::expected: throw, catch, and returning failure"
theme: "Errors, three ways"
phase: "Languages: every language, every basic"
status: written
---

# Day 009 · C++ — Exceptions and std::expected: throw, catch, and returning failure

**Today's theme:** Errors, three ways

**After today you can:** You can make a function fail in each language and make the caller handle it, and say which style each language prefers.

**The interviewer asks it as:** *Should this function throw, or return an error?*

---

## 1. What this is, and why it matters

C++ has both of today's styles. `throw` sends an exception climbing up through the callers until a `catch` takes it, exactly as Python's `raise` does, and `std::expected<T, E>` returns a value that is either a result or an error, exactly as Go's second return value does. One honesty note first: `std::expected` arrived in C++23, not C++20, so today's complete program is compiled with `-std=c++23`, which GCC 13 and later accept. Everything else today is plain C++20.

At work, which style a C++ codebase uses is a project-wide decision, often written down, and you will be expected to work in either. Interviewers ask "when would you use exceptions versus error codes", "what happens when an exception is not caught", and "how do you clean up without `finally`", and the answer to the last one is the most important idea in the language, which day 13 names.

## 2. The story

Kabir sends a birthday parcel to his sister by courier, three days early, from the branch near his office.

On Tuesday the delivery boy reaches the building and the flat number does not exist. Flat 4B. The building stops at 3. This courier company runs two kinds of route, and the driver knows which one he is on.

On the first kind, the phone route, he stands in the lobby and calls his supervisor, who calls the branch manager, who calls Kabir. The problem climbs the chain until someone can fix it, and the people in between only pass the call along. If nobody can fix it, the parcel goes back to the depot with a sticker saying exactly what happened.

On the second kind, the slip route, he does not call anyone. He puts the parcel back in the van, returns to the branch, and hands it over with a slip: "4B, building stops at 3." The clerk reads the slip, adds her line, passes it up. Every handover is two hands, parcel and slip, and the slip is empty on a good day.

The company argued for years about which route was better. The phone people said the slip route made every handover slow, even the ninety-nine good ones. The slip people said the phone route meant you could not tell, looking at any one person's job, whether it could go wrong. In the end the company kept both. Fragile parcels and long chains go by phone. Short local runs, where the driver hands straight to the clerk, go by slip. Each depot picks one and writes it on the wall, and a driver never mixes them on a single run.

One thing is the same on both routes. Whatever happens, the van is locked and the keys go on the hook at six. Not because anyone remembers to do it, but because the van locks itself when the driver walks away from it. He could not leave it open if he tried.

## 3. The idea in plain English

**Throwing.** `throw std::runtime_error("flat 4B does not exist");` ends the current function immediately and sends the exception object climbing up through each caller, running their cleanup as it passes, until it reaches a matching `catch`. `try { ... } catch (const std::exception& error) { ... }` is where you catch it; `error.what()` is the message. Functions in between need no code at all. This is the phone route, and it is Python's `raise` in different clothes.

The standard library provides a family of exception kinds in `<stdexcept>`: `std::runtime_error` for things that went wrong at run time, `std::invalid_argument` and `std::out_of_range` for bad inputs, all descending from `std::exception`. Catch the specific kind when you can handle it, or `const std::exception&` to catch any of them. Always catch by `const` reference, `const std::exception&`; catching by value copies and, worse, slices away the specific kind, which is in the traps.

If no `catch` matches all the way up, the program calls `std::terminate` and prints the exception's message and `Aborted`. That is the depot sticker.

**Returning.** `std::expected<std::string, std::string>`, from `<expected>`, is a box that holds **either** a string result **or** a string error, never both. A function that returns one either returns the result, `return "delivered to " + flat;`, or returns `std::unexpected("flat does not exist")`. The caller checks `if (result)` or `result.has_value()`, reads the value with `*result` or `result.value()`, and reads the error with `result.error()`. Nothing climbs. This is the slip route, and it is Go's `(string, error)` in one object; the difference from Go is that the box makes it impossible to read the result and the error at the same time.

**No `finally`.** C++ does not have one, and it does not need one, because objects clean up after themselves when they go out of scope: a `std::string` frees its bytes, a file closes, a lock unlocks, whether the scope ended normally or by an exception flying through. The van locks itself. That mechanism is called **RAII**, and day 13 is entirely about it; today you only need to know it is why C++ programmers do not miss `finally`.

The interview question, in C++: **throw** for failures that are rare and that the immediate caller cannot handle, so the phone route's silence in the middle is a feature. **Return `std::expected`** for failures that are ordinary and that the caller will handle right there, such as parsing input, so the cost of throwing is avoided and the signature says it can fail. Never mix the two in one function, and follow the codebase's wall.

## 4. The picture

```
 phone route: throw                          slip route: std::expected

 main()  try { send_parcel("4B") }           auto r = find_flat("4B");
   │  catch (const std::exception& e)        if (!r) { use r.error(); }
   │         ▲                               else    { use *r;        }
   ▼         │  climbs, running cleanup
 send_parcel()   no code about failure       std::expected<std::string, std::string>
   │         ▲                               ┌────────────────────────────────┐
   ▼         │                               │ has_value()  true  │ false     │
 find_flat()  throw std::runtime_error(...)  │ *r   "delivered.." │ ✗         │
                                             │ error()  ✗         │ "flat.."  │
                                             └────────────────────────────────┘
 uncaught → terminate called after throwing an instance of 'std::runtime_error'
```

*Notice that the middle function on the left has nothing to say about failure and the caller on the right must check before it can look inside. Notice that the box on the right can only ever be one of its two columns.*

## 5. The code, built step by step

Start `courier.cpp` in a `day09` folder. The throwing version first.

```cpp
#include <expected>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>

const std::set<std::string> flats = {"1A", "2A", "3A", "1B", "2B", "3B"};

std::string find_flat(const std::string& flat) {
    if (!flats.contains(flat)) {
        throw std::runtime_error("flat " + flat + " does not exist");
    }
    return "delivered to " + flat;
}
```

`throw` ends `find_flat` on the spot. `const std::string& flat` means "look at the caller's string without copying it", which day 12 explains; today it is the normal way to take a string parameter.

The function in the middle, with nothing to say.

```cpp
std::string send_parcel(const std::string& flat) {
    std::string receipt = find_flat(flat);
    return "receipt: " + receipt;
}
```

If `find_flat` throws, the exception passes straight through `send_parcel`. Its local `receipt` is never created, and the `return` never runs.

Catching.

```cpp
int main() {
    try {
        std::cout << send_parcel("2B") << "\n";
        std::cout << send_parcel("4B") << "\n";
        std::cout << "this line never runs\n";
    } catch (const std::exception& error) {
        std::cout << "could not deliver: " << error.what() << "\n";
    }
    std::cout << "van locked, keys on the hook\n";
```

```
receipt: delivered to 2B
could not deliver: flat 4B does not exist
van locked, keys on the hook
```

The second call threw two levels down and landed in the `catch`. The line after the `try` block runs either way, which is as close to `finally` as you need for printing; for real cleanup, RAII does it without a line of code.

The uncaught case.

```cpp
    std::cout << send_parcel("4B") << "\n";
```

```
terminate called after throwing an instance of 'std::runtime_error'
  what():  flat 4B does not exist
Aborted (core dumped)
```

No list of callers, unlike Python's traceback; you get the kind and the message. A debugger or a sanitiser gives you the rest.

Now the returning version, with `std::expected`.

```cpp
std::expected<std::string, std::string> find_flat_or_error(const std::string& flat) {
    if (!flats.contains(flat)) {
        return std::unexpected("flat " + flat + " does not exist");
    }
    return "delivered to " + flat;
}
```

The return type says it all: a string on success, a string describing the failure otherwise. `std::unexpected(...)` builds the failure side. Returning a plain string builds the success side.

Checking it.

```cpp
    for (const std::string& flat : {"2B", "4B"}) {
        auto result = find_flat_or_error(flat);
        if (!result) {
            std::cout << "could not deliver: " << result.error() << "\n";
            continue;
        }
        std::cout << *result << "\n";
    }
```

```
delivered to 2B
could not deliver: flat 4B does not exist
```

`!result` is "did it fail". `result.error()` is the slip. `*result` is the parcel. Reading `*result` when it failed is undefined behaviour, so the check comes first, exactly as Go's `if err != nil` comes first.

A standard-library throw, caught by kind.

```cpp
    for (const std::string& text : {"3", "four"}) {
        try {
            std::cout << std::stoi(text) << "\n";
        } catch (const std::invalid_argument& error) {
            std::cout << "bad input: " << error.what() << "\n";
        }
    }
```

```
3
bad input: stoi
```

`std::stoi` turns text into a number and throws `std::invalid_argument` when it cannot. Its message is famously unhelpful, which is why real code wraps it.

Here is the build, run, and output for the complete program. Note `-std=c++23`, for `<expected>`.

```bash
g++ -std=c++23 -Wall -Wextra courier.cpp -o courier
./courier
```

```
receipt: delivered to 2B
could not deliver: flat 4B does not exist
van locked, keys on the hook
delivered to 2B
could not deliver: flat 4B does not exist
3
bad input: stoi
```

And the complete file.

```cpp
// courier.cpp — day 9, throw/catch and std::expected
// Build: g++ -std=c++23 -Wall -Wextra courier.cpp -o courier   (C++23 for <expected>)
// Run:   ./courier
#include <expected>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>

const std::set<std::string> flats = {"1A", "2A", "3A", "1B", "2B", "3B"};

// The phone route: throw, and let it climb.
std::string find_flat(const std::string& flat) {
    if (!flats.contains(flat)) {
        throw std::runtime_error("flat " + flat + " does not exist");
    }
    return "delivered to " + flat;
}

// Nothing to say about failure; the exception passes through.
std::string send_parcel(const std::string& flat) {
    std::string receipt = find_flat(flat);
    return "receipt: " + receipt;
}

// The slip route: return either a result or an error.
std::expected<std::string, std::string> find_flat_or_error(const std::string& flat) {
    if (!flats.contains(flat)) {
        return std::unexpected("flat " + flat + " does not exist");
    }
    return "delivered to " + flat;
}

int main() {
    try {
        std::cout << send_parcel("2B") << "\n";
        std::cout << send_parcel("4B") << "\n";
        std::cout << "this line never runs\n";
    } catch (const std::exception& error) {
        std::cout << "could not deliver: " << error.what() << "\n";
    }
    std::cout << "van locked, keys on the hook\n";

    for (const std::string& flat : {"2B", "4B"}) {
        auto result = find_flat_or_error(flat);
        if (!result) {
            std::cout << "could not deliver: " << result.error() << "\n";
            continue;
        }
        std::cout << *result << "\n";
    }

    for (const std::string& text : {"3", "four"}) {
        try {
            std::cout << std::stoi(text) << "\n";
        } catch (const std::invalid_argument& error) {
            std::cout << "bad input: " << error.what() << "\n";
        }
    }
    return 0;
}
```

## 6. How the other two languages do it

Python, which has only the phone route and a `finally` for cleanup:

```python
def find_flat(flat: str) -> str:
    if flat not in FLATS:
        raise AddressError(f"flat {flat} does not exist")
    return f"delivered to {flat}"

try:
    print(send_parcel("4B"))
except AddressError as error:
    print(f"could not deliver: {error}")
finally:
    print("van keys returned")
```

Go, which has only the slip route, as two return values instead of one box:

```go
func findFlat(flat string) (string, error) {
	if !flats[flat] {
		return "", fmt.Errorf("flat %s does not exist", flat)
	}
	return "delivered to " + flat, nil
}

receipt, err := findFlat("4B")
if err != nil {
	fmt.Println("could not deliver:", err)
}
```

The one line of difference that matters: **Python chose throwing, Go chose returning, and C++ makes you choose per project.** Python's `finally` and Go's explicit passing both exist because those languages lack what C++ has instead: destructors that run automatically when an exception passes through a scope, so cleanup needs no keyword. The second difference is between the two returning styles: Go's `(string, error)` lets you read the string even when the error is set, which is a bug waiting to happen; C++'s `std::expected` holds one or the other, and reading the wrong side is on you but at least not silent in a debug build.

## 7. The traps

**The near-miss: catching by value.** Drop the `&`.

```cpp
    } catch (std::exception error) {
        std::cout << error.what() << "\n";
    }
```

```
courier.cpp: In function 'int main()':
courier.cpp:38:29: warning: catching polymorphic type 'class std::exception' by value [-Wcatch-value=]
   38 |     } catch (std::exception error) {
      |                             ^~~~~
```

It compiles and runs. But `error` is now a copy of only the `std::exception` part of what was thrown, and the specific kind, along with its message in some cases, is sliced off. Always `catch (const std::exception& error)`. The warning is in `-Wall`; read it.

**The real error: reading the wrong side of `std::expected`.** Skip the check.

```cpp
    auto result = find_flat_or_error("4B");
    std::cout << *result << "\n";
```

No compiler warning. `*result` on a failed `expected` is undefined behaviour: garbage, a crash, or an empty line, depending on the day. `result.value()` instead of `*result` throws `std::bad_expected_access` on failure, which at least stops the program with a message. Check `if (result)` first, always.

**The near-miss: handlers in the wrong order.** Catch the general kind before the specific one.

```cpp
    try {
        std::stoi("four");
    } catch (const std::exception& error) {
        std::cout << "something failed\n";
    } catch (const std::invalid_argument& error) {
        std::cout << "bad number\n";
    }
```

```
courier.cpp:45:7: warning: exception of type 'std::invalid_argument' will be caught by earlier handler [-Wexceptions]
   45 |     } catch (const std::invalid_argument& error) {
      |       ^~~~~
courier.cpp:43:7: note: for type 'std::exception'
```

Handlers are tried top to bottom and `std::invalid_argument` is a kind of `std::exception`, so the first handler always wins and the second can never run. Specific kinds first, general last.

## 8. Say it out loud

**How it gets asked**

- "Should this function throw, or return an error?"
- "What happens when a C++ exception is not caught?"
- "C++ has no `finally`. How do you clean up when an exception is thrown?"

**What to say out loud, the first ninety seconds**

"C++ supports both styles. Exceptions, `throw` and `catch`, unwind the stack through intermediate functions that need no handling code, and are the right tool for failures that are rare and cannot be handled by the immediate caller: out of memory, a broken invariant, a resource that should have been there. `std::expected<T, E>`, from C++23, returns either a value or an error in one object, checked at the call site with `if (result)` and read with `*result` or `result.error()`; it is the right tool for expected, frequent failures like parsing or validation, where the signature should advertise failure and the cost of unwinding is unwanted.

An uncaught exception calls `std::terminate`, which aborts the program printing the exception's `what()`. Cleanup does not need `finally` because of RAII: objects with destructors, strings, vectors, file handles, locks, release their resources when their scope ends, and stack unwinding runs those destructors, so resources are freed on the exceptional path without any extra code. I catch by `const` reference to avoid slicing, order handlers specific to general, and follow the codebase's convention rather than mixing styles in one function."

**The follow-ups**

1. *"What does `noexcept` mean?"* — A promise that the function will not throw. If it does anyway, `std::terminate` is called immediately, with no unwinding. It lets the compiler and the standard library optimise, and it is required on move operations for containers to use them.
2. *"What is the cost of an exception?"* — Almost zero on the path where nothing is thrown, and comparatively expensive when one is thrown, because unwinding walks tables and runs destructors. That asymmetry is why exceptions suit rare failures and `std::expected` suits common ones.
3. *"What is `std::error_code`?"* — An older returning style: a small integer plus a category, used by the filesystem and networking parts of the standard library, and often paired with `std::expected` as the error type.

**A model answer**

"C++ offers exceptions for rare, non-local failures and value-based error returns for expected ones. `throw` transfers control to the nearest matching `catch`, running destructors for every scope it leaves; an uncaught exception terminates the program via `std::terminate`. There is no `finally` because RAII destructors perform cleanup on both normal and exceptional exits. `std::expected<T, E>` in C++23 models a result-or-error return, inspected with `has_value`, `operator*`, `value` and `error`, and mirrors Go's convention with the added guarantee that only one side exists. Best practice is to catch by `const` reference, order handlers from most to least specific, mark non-throwing functions `noexcept`, and choose one style per module rather than mixing them."

## 9. Recall card

- `throw std::runtime_error("...")` climbs until `catch (const std::exception& e)`; `e.what()` is the message; uncaught means `terminate called after throwing ...` and `Aborted`.
- Catch by `const&` or `-Wcatch-value` warns and the kind is sliced; specific handlers before general ones or `-Wexceptions` warns the second can never run.
- No `finally`: destructors run as the exception passes through each scope. That is RAII, day 13.
- `std::expected<T, E>` (C++23, `-std=c++23`): `return value;` or `return std::unexpected(err);`; check `if (r)` before `*r` or `r.error()`.
- Throw for rare failures the caller cannot handle; return `std::expected` for ordinary ones the caller handles on the spot; one style per module.
