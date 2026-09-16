---
day: 41
track: lang-go
title: "time.Time, Duration, time.Now, and math/rand versus crypto/rand"
theme: "Dates, times, and randomness"
phase: "Languages: advanced features"
status: written
---

# Day 041 · Go — time.Time, Duration, time.Now, and math/rand versus crypto/rand

**Today's theme:** Dates, times, and randomness

**After today you can:** You can measure elapsed time correctly and generate a secure random token in each language.

**The interviewer asks it as:** *Why should you not use the wall clock to measure elapsed time?*

---

## 1. What this is, and why it matters

`time.Time` represents an instant, and `time.Duration` represents a
length of time. Values returned by `time.Now()` normally carry both a wall-clock
reading and a monotonic reading. That lets `time.Since(start)` measure an operation
without being fooled by a corrected wall clock. The choice matters when you time
the database calls from today's system design lesson.

## 2. The story

Meera is baking with her cousin when the kitchen clock stops. The cake went in when
it showed three o'clock. Ten minutes later, her cousin notices the clock is slow and
moves its hands forward by twenty minutes. Meera looks up and thinks the cake has
been in for half an hour. It has not. Changing the hands did not make the cake bake
any faster.

Her cousin has also started the little timer beside the oven. That still shows ten
minutes. They decide to trust it for the cake. The kitchen clock can tell them when
their guests expect tea, but it cannot now tell them how long the cake has been in.

One guest is Meera's aunt, who lives abroad. She calls to ask when they will eat.
Meera says four o'clock, then stops. Four where? They agree to name the city as well
as the hour. Her aunt can now work out when to call again without guessing.

While they wait, the cousins choose who gets the first piece by shaking a covered
cup with two coloured stones. For a game, taking turns would also have been fine.
But Meera would not choose the number for her front-door lock by taking the next
number after yesterday's. Something that looks different each time can still be
easy for another person to guess.

Three small choices have three different jobs: arrange tea, judge the cake, and
keep a stranger from guessing. Meera stops asking one thing to do all three.

## 3. The idea in plain English

Meera's clock and timer can travel together in a Go `time.Time`.
When both operands retain monotonic readings, `Sub` uses those readings.
`time.Since(start)` is the usual spelling for measuring from a saved start.
A **duration** is a signed number of nanoseconds; `250 * time.Millisecond`
expresses its unit instead of leaving the reader to guess what 250 means.

A **location** holds a place's clock rules. Load one with `time.LoadLocation`
and display an instant there with `In`. The instant stays the same. A location
name is more useful than a fixed offset when the local rules change seasonally.

`math/rand` is for simulations; `crypto/rand` is for values another person must
not predict. Read 16 bytes and hex-encode them to obtain 32 characters carrying
128 bits. Check the error on Go 1.23 rather than issuing a token after a failed read.

## 4. The picture

```text
Wall clock:     15:00 -------- correction --------> 15:30
Elapsed timer:      0 ----------------------------> 10 minutes
Meeting:        10:00 UTC = 15:30 Asia/Kolkata
```

Notice that an adjustment changes the displayed hour without adding baking time.
The two meeting labels describe one instant, not two meetings.

## 5. The code, built step by step

```go
start := time.Now()
elapsed := time.Since(start)
```

Keep the original value in this process for timing. Serialising it removes its
monotonic reading, so a saved timestamp cannot replace the start of a stopwatch.

```go
token := make([]byte, 16)
if _, err := rand.Read(token); err != nil {
	return err
}
```

This fragment belongs in a function returning `error`; import `crypto/rand`.
The complete program embeds zone data using `time/tzdata`, making Kolkata
available even on a host without zone files. Save as `main.go`, then run
`gofmt -w main.go` and `go run main.go` with Go 1.23+.

Successful output is exactly: `2026-01-15T15:30:00+05:30`, `499500`, `true`, `32`,
on four separate lines. The duration and token vary; only their properties print.

```go
package main

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"os"
	"time"
	_ "time/tzdata"
)

func run() error {
	location, err := time.LoadLocation("Asia/Kolkata")
	if err != nil {
		return err
	}
	meeting := time.Date(2026, 1, 15, 10, 0, 0, 0, time.UTC)
	fmt.Println(meeting.In(location).Format(time.RFC3339))
	start := time.Now()
	total := 0
	for number := 0; number < 1000; number++ {
		total += number
	}
	elapsed := time.Since(start)
	token := make([]byte, 16)
	if _, err := rand.Read(token); err != nil {
		return err
	}
	fmt.Println(total)
	fmt.Println(elapsed >= 0)
	fmt.Println(len(hex.EncodeToString(token)))
	return nil
}

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

## 6. How the other two languages do it

```python
start = time.monotonic()
elapsed = time.monotonic() - start
```

Python returns seconds as a number; that number is not a calendar date.

```cpp
auto start = std::chrono::steady_clock::now();
auto elapsed = std::chrono::steady_clock::now() - start;
```

C++ uses a separate clock type. Go puts both readings into `time.Now()` values,
but saving and loading those values does not preserve the monotonic reading.

## 7. The traps

**Losing the stopwatch.** A `time.Time` read from JSON has no monotonic
reading. Subtracting it from another wall time cannot protect you from clock
corrections. `UTC()`, `In`, and calendar operations can also strip that reading;
keep the original start from `time.Now()` for `time.Since`.

**Missing units.** `time.Duration(250)` means 250 nanoseconds, not milliseconds.
Write `250 * time.Millisecond`. The wrong value may cause immediate timeouts
without any error message.

**Unchecked parsing.** Inside `main`, run:

```go
_, err := time.ParseDuration("250")
fmt.Println(err)
```

The error text is:

```text
time: missing unit in duration "250"
```

Handle the error; using the zero result would hide invalid configuration.
For equal instants use `Equal`: `==` also compares representation details,
including location and monotonic information.

## 8. Say it out loud

### How it gets asked

- Why should you not use the wall clock to measure elapsed time?
- How would you display the same event in two countries?
- Is a seeded random generator suitable for password-reset links?

### What to say out loud

"I separate an instant from a duration. An instant tells another person when an
event occurred; a duration tells me how long an operation took. If the system
corrects the wall clock halfway through a call, subtraction can report a negative
duration. I choose a monotonic clock for that measurement. In Go I preserve the original `time.Now()` result for `time.Since`. I store wall timestamps separately, display them with a location, and use `crypto/rand` for tokens.
I keep a zone name when a future local appointment needs local calendar rules.
Finally, a repeatable random sequence helps tests, while an authentication token
must resist prediction. Those are different requirements."

### The follow-ups

1. **How would you time today's database work?** A saved timestamp has no monotonic component. Use a new in-process start for measuring a call, and retain the saved timestamp only to describe when the event occurred.
2. **Does converting a timestamp change the event?** No. It changes the local
   representation. For 10:00 UTC on 15 January 2026, Kolkata displays 15:30.
3. **Does hexadecimal encoding make a token stronger?** No. Sixteen bytes carry
   128 bits; writing them as 32 hex characters preserves the same possibilities.

### A model answer

"Suppose a database call begins at wall time 10:00:05 and the clock is corrected
backward by ten seconds before it finishes. Wall subtraction gives a misleading
negative result. A monotonic duration avoids that correction. I still record an
aware wall timestamp for the event log so other services can understand it.
In Go I preserve the original `time.Now()` result for `time.Since`. I store wall timestamps separately, display them with a location, and use `crypto/rand` for tokens. I verify units and check failures before using the result."

## 9. Recall card

- Use wall time for instants and a monotonic clock for durations.
- A time zone changes the display of an instant, not the instant.
- Keep duration units explicit; converting to whole units can truncate.
- Repeatable random engines serve tests, not security tokens.
- Generate 16 secure bytes for 128 bits; encoding adds no randomness.

Further reading: [Go time](https://pkg.go.dev/time) and [Go cryptographic randomness](https://pkg.go.dev/crypto/rand).
