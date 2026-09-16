# Day 039 — Difference arrays: range updates, cheaply

| Track | Today |
|---|---|
| **DSA** | Difference arrays: range updates, cheaply |
| **System design** | Wide-column and time-series stores |
| **Languages** | Text versus bytes |
| &nbsp;&nbsp;Python | str versus bytes, encode, decode, and UnicodeDecodeError |
| &nbsp;&nbsp;Go | []byte, rune, the utf8 package, and strings.Builder |
| &nbsp;&nbsp;C++ | char, char8_t, std::string_view, and UTF-8 by hand |

## What you can do by tonight

- **DSA** — You can apply a thousand range updates in O(1) each and rebuild the array at the end.
- **System design** — You can say what Cassandra's data model really is and when a time-series store is right.
- **Languages** — You can explain what a byte is, what a character is, and where each language draws the line.

## The questions today answers

- *Apply many range increments and then report the final array.*
- *Which database would you pick for storing metrics, and why?*
- *What is the difference between a byte and a character?*

## Read in this order

1. [01-dsa-difference-arrays-range-updates-cheaply.md](01-dsa-difference-arrays-range-updates-cheaply.md) — the DSA lesson
2. [02-system-design-wide-column-and-time-series-stores.md](02-system-design-wide-column-and-time-series-stores.md) — the system design lesson
3. [03-practice.md](03-practice.md) — code it, then say it out loud
4. [05-lang-python-str-versus-bytes-encode.md](05-lang-python-str-versus-bytes-encode.md) — the Python lesson
5. [06-lang-go-byte-rune-the-utf8.md](06-lang-go-byte-rune-the-utf8.md) — the Go lesson
6. [07-lang-cpp-char-char8-t-std.md](07-lang-cpp-char-char8-t-std.md) — the C++ lesson
7. [08-lang-practice.md](08-lang-practice.md) — build it three times, then say it out loud

## Where this sits

- DSA phase: **Prefix sums**
- System design phase: **Databases from zero**
- Languages phase: **Languages: advanced features**

---

[← Day 038](../day-038-subarray-sum-k/README.md) · [All days](../README.md) · [Day 040 →](../day-040-2d-prefix-sums/README.md)
