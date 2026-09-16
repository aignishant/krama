---
day: 41
track: lang-cpp
title: "std::chrono, time zones, and <random>"
theme: "Dates, times, and randomness"
phase: "Languages: advanced features"
status: written
---

# Day 041 · C++ — std::chrono, time zones, and <random>

**Today's theme:** Dates, times, and randomness

**After today you can:** You can measure elapsed time correctly and generate a secure random token in each language.

**The interviewer asks it as:** *Why should you not use the wall clock to measure elapsed time?*

---

## 1. What this is, and why it matters

`std::chrono` gives times and durations explicit types. Use
`system_clock` for event timestamps and `steady_clock` for elapsed time.
The generators in `<random>` help simulations; they do not give a portable promise
of cryptographic security. A service needs that distinction before it uses a
random-looking value as permission to reset an account.

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

Meera's oven timer is `std::chrono::steady_clock`. A **time point**
is a reading from a clock. Subtract two time points from the same clock to obtain
a **duration**, which holds a count and a unit. `duration_cast<milliseconds>`
converts that duration and truncates fractional milliseconds for an integer result.

`system_clock` supplies calendar instants. C++20 adds calendar types and time-zone
facilities: `locate_zone` looks up a place, and `zoned_time` associates its rules
with an instant. These need library support and an available time-zone database;
selecting `-std=c++20` alone does not install either.

`std::mt19937` is a repeatable engine. A distribution maps its output into a desired
range. Neither a clock seed nor a `std::random_device` seed makes that engine
cryptographically secure. The complete example uses OpenSSL for secure bytes:
16 × 8 = 128 bits, displayed as 32 hexadecimal characters if encoded.

## 4. The picture

```text
Wall clock:     15:00 -------- correction --------> 15:30
Elapsed timer:      0 ----------------------------> 10 minutes
Meeting:        10:00 UTC = 15:30 Asia/Kolkata
```

Notice that an adjustment changes the displayed hour without adding baking time.
The two meeting labels describe one instant, not two meetings.

## 5. The code, built step by step

```cpp
auto start = std::chrono::steady_clock::now();
auto elapsed = std::chrono::steady_clock::now() - start;
auto milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed);
```

The unit is part of the expression. Do not treat `.count()` as seconds without
checking its duration type.

```cpp
auto meeting = std::chrono::sys_days{std::chrono::year{2026}/1/15}
             + std::chrono::hours{10};
auto local = std::chrono::zoned_time{
    std::chrono::locate_zone("Asia/Kolkata"), meeting};
```

On a library implementing C++20 time zones, `local.get_local_time()` represents
15:30 that day. Converting from an instant is unambiguous; converting an ambiguous
local hour back requires a choice of occurrence. This optional fragment needs
the zone database. The complete program below uses only the widely available
clock facilities and OpenSSL 3's development headers and library.

Save as `main.cpp`. With g++ and OpenSSL installed in its include/library search
paths, compile with `g++ -std=c++20 -Wall -Wextra main.cpp -lcrypto -o main` and
run `./main` (`.\main.exe` in PowerShell). Successful output is exactly `499500`,
`true`, `32`, on separate lines. We print the token length, not the secret.

```cpp
#include <array>
#include <chrono>
#include <iostream>
#include <openssl/rand.h>
#include <string>

int main() {
    const auto start = std::chrono::steady_clock::now();
    int total = 0;
    for (int number = 0; number < 1000; ++number) {
        total += number;
    }
    const auto elapsed = std::chrono::steady_clock::now() - start;
    std::array<unsigned char, 16> bytes{};
    if (RAND_bytes(bytes.data(), static_cast<int>(bytes.size())) != 1) {
        std::cerr << "secure random generation failed\n";
        return 1;
    }
    constexpr char digits[] = "0123456789abcdef";
    std::string token;
    token.reserve(bytes.size() * 2);
    for (unsigned char value : bytes) {
        token.push_back(digits[value >> 4]);
        token.push_back(digits[value & 15]);
    }
    std::cout << total << '\n' << std::boolalpha
              << (elapsed >= std::chrono::steady_clock::duration::zero())
              << '\n' << token.size() << '\n';
}
```

## 6. How the other two languages do it

```python
start = time.monotonic()
elapsed = time.monotonic() - start
token = secrets.token_hex(16)
```

Python provides elapsed time and secure tokens in its standard library.

```go
start := time.Now()
elapsed := time.Since(start)
token := make([]byte, 16)
if _, err := rand.Read(token); err != nil { return err }
```

Here `rand` means `crypto/rand`, inside a function returning an error. C++ has
standard clock types but needs an OS facility or cryptographic library for a
portable security-oriented token implementation.

## 7. The traps

**The clock with the impressive name.** `high_resolution_clock` is not
guaranteed to be steady. Choosing it because its name sounds precise can reintroduce
wall-clock corrections. Ask whether the clock is steady before using it for timeouts.

**Truncating a short operation.** Casting 900 microseconds to whole milliseconds
gives 0. That is a unit conversion, not evidence that the operation took no time.

**A repeatable secret.** These two engines produce equal first values:

```cpp
std::mt19937 first{7};
std::mt19937 second{7};
std::cout << std::boolalpha << (first() == second()) << '\n';
```

Include `<random>` and `<iostream>`; the fragment prints `true`. Use it for replaying
tests, never for security tokens.

**Dependency failures.** If the OpenSSL header is missing, GCC's diagnostic includes:

```text
fatal error: openssl/rand.h: No such file or directory
```

Install the development headers and link the matching library. If random generation
itself fails, the complete program emits `secure random generation failed` and
returns 1. Never fall back to a predictable generator after this failure.

## 8. Say it out loud

### How it gets asked

- Why should you not use the wall clock to measure elapsed time?
- How would you display the same event in two countries?
- Is a seeded random generator suitable for password-reset links?

### What to say out loud

"I separate an instant from a duration. An instant tells another person when an
event occurred; a duration tells me how long an operation took. If the system
corrects the wall clock halfway through a call, subtraction can report a negative
duration. I choose a monotonic clock for that measurement. In C++ I choose `steady_clock` for intervals and retain explicit duration units. I use `system_clock` plus zone rules for display, and a cryptographic library for tokens.
I keep a zone name when a future local appointment needs local calendar rules.
Finally, a repeatable random sequence helps tests, while an authentication token
must resist prediction. Those are different requirements."

### The follow-ups

1. **How would you time today's database work?** The standard random engines are intended for statistical generation. I use a cryptographic facility such as OpenSSL RAND_bytes and require its success return before using any bytes.
2. **Does converting a timestamp change the event?** No. It changes the local
   representation. For 10:00 UTC on 15 January 2026, Kolkata displays 15:30.
3. **Does hexadecimal encoding make a token stronger?** No. Sixteen bytes carry
   128 bits; writing them as 32 hex characters preserves the same possibilities.

### A model answer

"Suppose a database call begins at wall time 10:00:05 and the clock is corrected
backward by ten seconds before it finishes. Wall subtraction gives a misleading
negative result. A monotonic duration avoids that correction. I still record an
aware wall timestamp for the event log so other services can understand it.
In C++ I choose `steady_clock` for intervals and retain explicit duration units. I use `system_clock` plus zone rules for display, and a cryptographic library for tokens. I verify units and check failures before using the result."

## 9. Recall card

- Use wall time for instants and a monotonic clock for durations.
- A time zone changes the display of an instant, not the instant.
- Keep duration units explicit; converting to whole units can truncate.
- Repeatable random engines serve tests, not security tokens.
- Generate 16 secure bytes for 128 bits; encoding adds no randomness.

Further reading: [C++ clocks and zones](https://learn.microsoft.com/en-us/cpp/standard-library/chrono?view=msvc-170) and [OpenSSL RAND_bytes](https://docs.openssl.org/3.0/man3/RAND_bytes/).
