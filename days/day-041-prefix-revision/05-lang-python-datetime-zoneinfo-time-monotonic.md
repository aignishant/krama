---
day: 41
track: lang-python
title: "datetime, zoneinfo, time.monotonic, and random versus secrets"
theme: "Dates, times, and randomness"
phase: "Languages: advanced features"
status: written
---

# Day 041 · Python — datetime, zoneinfo, time.monotonic, and random versus secrets

**Today's theme:** Dates, times, and randomness

**After today you can:** You can measure elapsed time correctly and generate a secure random token in each language.

**The interviewer asks it as:** *Why should you not use the wall clock to measure elapsed time?*

---

## 1. What this is, and why it matters

A **wall clock** names an instant, such as a meeting at 10:00 UTC. A
**monotonic clock** measures elapsed time without following wall-clock corrections.
Secure randomness makes a token hard to guess, even when someone knows how you
generated it. You meet all three when a service records an event, times a database
call, and creates a password-reset link.

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

Meera's kitchen clock is `datetime.now(UTC)`. UTC is the shared reference
used to describe instants across countries. A **time zone** supplies the local
clock rules for a place. `ZoneInfo("Asia/Kolkata")` turns an aware UTC value into
the local display of that same instant. An **aware** datetime carries enough zone
information to locate its instant; a **naive** one has no such information.

Her oven timer is `time.monotonic()`. Subtract two readings in the same running
environment. Do not save one as an event timestamp or send it to another machine.
The reading's origin is not a calendar date.

`random.Random(7)` gives a repeatable sequence for experiments. Repeatability is
useful when debugging a failed test. `secrets.token_hex(16)` instead requests 16
secure random bytes and represents them with 32 hexadecimal characters. Encoding
does not add randomness: 16 × 8 = 128 bits before and after encoding.

## 4. The picture

```text
Wall clock:     15:00 -------- correction --------> 15:30
Elapsed timer:      0 ----------------------------> 10 minutes
Meeting:        10:00 UTC = 15:30 Asia/Kolkata
```

Notice that an adjustment changes the displayed hour without adding baking time.
The two meeting labels describe one instant, not two meetings.

## 5. The code, built step by step

```python
meeting = datetime(2026, 1, 15, 10, tzinfo=UTC)
local = meeting.astimezone(ZoneInfo("Asia/Kolkata"))
```

Convert the instant; do not use `replace(tzinfo=...)` to convert its clock reading.
`replace` attaches a label without doing the conversion.

```python
start = time.monotonic()
total = sum(range(1000))
elapsed = time.monotonic() - start
```

The sum is 999 × 1000 / 2 = 499500. Elapsed seconds vary, so the complete example
prints whether the duration is nonnegative. It checks the secure token's length
without printing a secret. Run `python main.py` with Python 3.12+.
On a machine without an IANA zone database, install it with
`python -m pip install tzdata`; Windows commonly needs this package.

Successful output is exactly: `2026-01-15T15:30:00+05:30`, `499500`, `True`, `32`,
on four separate lines. Save this complete program as `main.py`:

```python
from datetime import UTC, datetime
from zoneinfo import ZoneInfo
import secrets
import time


def main() -> None:
    meeting = datetime(2026, 1, 15, 10, tzinfo=UTC)
    print(meeting.astimezone(ZoneInfo("Asia/Kolkata")).isoformat())
    start = time.monotonic()
    total = sum(range(1000))
    elapsed = time.monotonic() - start
    token = secrets.token_hex(16)
    print(total)
    print(elapsed >= 0)
    print(len(token))


if __name__ == "__main__":
    main()
```

## 6. How the other two languages do it

```go
start := time.Now()
elapsed := time.Since(start)
```

Go normally carries a monotonic reading inside values returned by `time.Now()`.

```cpp
auto start = std::chrono::steady_clock::now();
auto elapsed = std::chrono::steady_clock::now() - start;
```

C++ makes the clock part of the type. Python makes you choose separate calls:
`datetime.now(UTC)` for an instant and `time.monotonic()` for elapsed time.

## 7. The traps

**Attaching the wrong label.** At 10:00 UTC the example must display
15:30 in Kolkata. Replacing its `tzinfo` with Kolkata leaves 10:00 on the clock and
therefore names a different instant. This produces a wrong answer without raising.

**Mixing aware and naive dates.** Run this expression after importing `datetime`
and `UTC`: `datetime(2026, 1, 1) - datetime(2026, 1, 1, tzinfo=UTC)`.
Its final error line is:

```text
TypeError: can't subtract offset-naive and offset-aware datetimes
```

Choose the missing zone from the input contract; do not blindly assume local time.
For daylight-saving transitions, a local hour can occur twice or not occur at all.
Ask for a zone and an explicit rule for ambiguous input.

**Guessable tokens.** A seeded `random.Random` can replay exactly the same values.
That is desirable for a test, but disqualifies it for reset tokens. A timestamp
seed does not turn it into a secure generator.

## 8. Say it out loud

### How it gets asked

- Why should you not use the wall clock to measure elapsed time?
- How would you display the same event in two countries?
- Is a seeded random generator suitable for password-reset links?

### What to say out loud

"I separate an instant from a duration. An instant tells another person when an
event occurred; a duration tells me how long an operation took. If the system
corrects the wall clock halfway through a call, subtraction can report a negative
duration. I choose a monotonic clock for that measurement. In Python I use aware datetimes for events, `ZoneInfo` for local display, and `time.monotonic()` for elapsed seconds. I use `secrets`, not `random`, for reset tokens.
I keep a zone name when a future local appointment needs local calendar rules.
Finally, a repeatable random sequence helps tests, while an authentication token
must resist prediction. Those are different requirements."

### The follow-ups

1. **How would you time today's database work?** Use `time.monotonic()` around the complete operation, including time spent waiting for a connection. Its difference is seconds, so multiply by 1000 when reporting milliseconds.
2. **Does converting a timestamp change the event?** No. It changes the local
   representation. For 10:00 UTC on 15 January 2026, Kolkata displays 15:30.
3. **Does hexadecimal encoding make a token stronger?** No. Sixteen bytes carry
   128 bits; writing them as 32 hex characters preserves the same possibilities.

### A model answer

"Suppose a database call begins at wall time 10:00:05 and the clock is corrected
backward by ten seconds before it finishes. Wall subtraction gives a misleading
negative result. A monotonic duration avoids that correction. I still record an
aware wall timestamp for the event log so other services can understand it.
In Python I use aware datetimes for events, `ZoneInfo` for local display, and `time.monotonic()` for elapsed seconds. I use `secrets`, not `random`, for reset tokens. I verify units and check failures before using the result."

## 9. Recall card

- Use wall time for instants and a monotonic clock for durations.
- A time zone changes the display of an instant, not the instant.
- Keep duration units explicit; converting to whole units can truncate.
- Repeatable random engines serve tests, not security tokens.
- Generate 16 secure bytes for 128 bits; encoding adds no randomness.

Further reading: [Python clocks](https://docs.python.org/3.12/library/time.html), [time zones](https://docs.python.org/3.12/library/zoneinfo.html), and [secure tokens](https://docs.python.org/3.12/library/secrets.html).
