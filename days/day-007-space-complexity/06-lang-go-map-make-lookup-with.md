---
day: 7
track: lang-go
title: "map: make, lookup with the comma-ok idiom, delete, and no order"
theme: "Key-value and membership"
phase: "Languages: every language, every basic"
status: written
---

# Day 007 · Go — map: make, lookup with the comma-ok idiom, delete, and no order

**Today's theme:** Key-value and membership

**After today you can:** You can count, group and deduplicate with a map in each language and explain what happens on a missing key.

**The interviewer asks it as:** *What does your language do when you read a key that is not there?*

---

## 1. What this is, and why it matters

A Go map stores values under keys, looks them up by hashing in constant time, and, when you ask for a key that is not there, hands you the zero value of the value type with no complaint: `""` for strings, `0` for numbers, `false` for booleans. To tell a real zero from a missing key you use the comma-ok form, `v, ok := m[k]`. Go has no set; a map whose values are booleans, or empty structs, does the job. And a map has no order at all: walk it twice and you may get two different sequences.

At work, the zero-value-on-miss rule is why Go counting code is one line, `counts[word]++`, and also why a typo in a key silently gives you zero instead of an error. Interviewers ask "what is the comma-ok idiom", "why is map iteration order random", and "what happens when you write to a nil map", and the last one is a panic that every Go beginner meets in their first week.

## 2. The story

Devika is running the cloakroom at her cousin's wedding. Three hundred guests, one long counter, a wall of numbered hooks behind her, and a bowl of plastic tokens with the same numbers.

A guest hands over a shawl. Devika hangs it on hook 47, hands the guest token 47, and forgets about it. That is the whole system. When the guest comes back with token 47, Devika does not search three hundred hooks. She walks to 47 and lifts the shawl. It takes the same five seconds whether the wall has ten hooks in use or all three hundred.

Around eleven, a man hands her token 112. She goes to hook 112. It is empty. She is sure of it, because she never gave out 112; that batch of tokens is still in the sealed bag. So what does she do?

Devika, being Devika, comes back to the counter and says, "There is nothing under 112. This token was never issued." She refuses to hand over anything, and the man, embarrassed, finds his real token in the other pocket.

Her brother, who took over at midnight, handles it differently. A woman hands him token 200. He goes to the hook, finds nothing, comes back, and hands her an empty hanger with a straight face. No shawl, no explanation, just the empty hanger, as if that is what was always there.

And the hired boy at the far end of the counter does the third thing. Token 250, empty hook. He writes 250 on a fresh tag, hangs an empty hanger on hook 250, and gives the guest the hanger. Now hook 250 exists, with nothing on it, and at the end of the night the count of hooks in use is one higher than the number of things anyone ever left.

Meanwhile at the gate, Devika's aunt has the guest list on her phone, and her whole job is one question: is this name on it, yes or no. She does not care about order or how many times a name appears. Just in, or not in.

## 3. The idea in plain English

A **map** stores **values** under **keys**: `map[int]string` is a map from int keys to string values. You make one with a literal, `map[int]string{47: "shawl"}`, or empty with `make(map[int]string)`. Read with `cloakroom[47]`, write with `cloakroom[51] = "coat"`, remove with `delete(cloakroom, 47)`, count with `len`.

Lookup is by **hashing**: the key is turned into a number that picks a slot, so it takes the same time at ten entries or ten million. That is Devika walking straight to hook 47. Keys must be **comparable**, which in Go means anything you can use `==` on: strings, numbers, booleans, structs of those. A slice cannot be a key, and the compiler says so.

When the key is not there, `cloakroom[112]` returns the **zero value** of the value type. For `string` that is `""`. No error, no panic, nothing added to the map. That is the brother's empty hanger. It is convenient and it is dangerous, because an empty string that means "missing" looks exactly like an empty string that was stored on purpose.

So Go gives you a second answer on request. `item, ok := cloakroom[112]` sets `item` to the zero value and `ok` to `false`. If the key exists, `ok` is `true`, even when the stored value is itself `""`. This is the **comma-ok idiom**, and you will write it thousands of times. Combined with day 4's `if` init statement it becomes `if item, ok := cloakroom[112]; ok { ... }`.

The zero-value rule is what makes counting one line: `counts[item]++` works on the first sighting because the missing key reads as `0`, and writing `1` back creates the entry.

A map has **no order**. `for key, value := range cloakroom` visits every entry, but in an order that Go deliberately randomises from run to run, so that nobody accidentally depends on it. If you need order, collect the keys into a slice and sort them.

Go has **no set** type. A set is `map[string]bool`, where `guests["Asha"]` reads `true` if present and the zero value `false` if not, which is exactly the aunt's question. When memory matters, `map[string]struct{}` uses a zero-byte value; today, `bool` is clearer.

One more rule. A map variable declared without `make` or a literal is **nil**. Reading from a nil map gives zero values, harmlessly. Writing to one **panics**.

## 4. The picture

```
 cloakroom := map[int]string{47: "shawl", 48: "bag", 51: "coat"}

   key ──► hash ──► slot          buckets
                                  ┌────┬────────────────┐
   cloakroom[47]   → "shawl"      │    │ 48 → "bag"     │
                                  │    │ 47 → "shawl"   │  ◄── straight here
   cloakroom[112]  → ""           │    │                │
                     (nothing added, len still 3)
                                  │    │ 51 → "coat"    │
   item, ok := cloakroom[112]     └────┴────────────────┘
        ""    false

   item, ok := cloakroom[47]
      "shawl" true

 var empty map[int]string         nil: reads give "", writes panic
 empty[1] = "x"                   panic: assignment to entry in nil map
```

*Notice that the miss and the hit look identical if you only take one value. Notice the last two lines: a nil map is readable and not writable, which is why `make` matters.*

## 5. The code, built step by step

Start `cloakroom.go` in a `day07` folder.

```go
package main

import (
	"fmt"
	"maps"
	"slices"
)

func main() {
	cloakroom := map[int]string{47: "shawl", 48: "bag"}
	cloakroom[51] = "coat"
	fmt.Println(cloakroom[47], len(cloakroom))
	fmt.Println(cloakroom)
```

```
shawl 3
map[47:shawl 48:bag 51:coat]
```

`fmt.Println` sorts the keys when it prints a map, purely to make output readable; that is not the map's own order.

The missing key, and the comma-ok idiom.

```go
	fmt.Printf("%q\n", cloakroom[112])
	item, ok := cloakroom[112]
	fmt.Printf("%q %v\n", item, ok)
	item, ok = cloakroom[47]
	fmt.Printf("%q %v\n", item, ok)
	fmt.Println(len(cloakroom))
```

```
""
"" false
"shawl" true
3
```

`%q` prints the string in quotes so an empty one is visible. The first line is the empty hanger. The second tells you it was empty because the hook was never used. And `len` is still 3: nothing was added.

The idiom in its natural habitat.

```go
	if item, ok := cloakroom[112]; ok {
		fmt.Println("hook 112 holds", item)
	} else {
		fmt.Println("token 112 was never issued")
	}
```

```
token 112 was never issued
```

`item` and `ok` exist only inside this `if` and its `else`.

Counting, one line per item.

```go
	items := []string{"shawl", "bag", "shawl", "coat", "shawl", "bag"}
	counts := make(map[string]int)
	for _, item := range items {
		counts[item]++
	}
	fmt.Println(counts)
```

```
map[bag:2 coat:1 shawl:3]
```

`counts[item]++` reads `0` for an unseen key, adds one, writes `1`. No `get`, no default, no check. This is the zero value earning its keep.

Grouping.

```go
	byItem := make(map[string][]int)
	for hook, item := range cloakroom {
		byItem[item] = append(byItem[item], hook)
	}
	fmt.Println(byItem)
```

```
map[bag:[48] coat:[51] shawl:[47]]
```

`byItem[item]` on a new key is a nil slice, and `append` to a nil slice works, so the first hook for each item starts a fresh slice. Two zero-value rules cooperating.

Order, and the lack of it.

```go
	for hook := range cloakroom {
		fmt.Print(hook, " ")
	}
	fmt.Println()
	for _, hook := range slices.Sorted(maps.Keys(cloakroom)) {
		fmt.Print(hook, " ")
	}
	fmt.Println()
```

```
51 47 48 
47 48 51 
```

The first line differs from run to run. The second is the fix: `maps.Keys` gives the keys, `slices.Sorted` sorts them into a new slice, and you walk that.

A set.

```go
	guests := map[string]bool{"Asha": true, "Ravi": true, "Meera": true}
	arrived := []string{"Ravi", "Asha", "Ravi", "Tom"}
	unique := make(map[string]bool)
	for _, name := range arrived {
		unique[name] = true
		if !guests[name] {
			fmt.Println("gatecrasher:", name)
		}
	}
	fmt.Println("unique arrivals:", len(unique))
```

```
gatecrasher: Tom
unique arrivals: 3
```

`guests[name]` reads `false` for Tom because he is not there, which is exactly the answer wanted, so here the zero value needs no `ok`. Setting `unique[name] = true` twice for Ravi is harmless; the map keeps one key.

Here is the run and output for the complete program.

```bash
go run cloakroom.go
```

```
hook 47 holds shawl; 3 hooks in use
map[47:shawl 48:bag 51:coat]
missing key reads "" and ok is false; still 3 hooks in use
token 112 was never issued
counts: map[bag:2 coat:1 shawl:3]
grouped: map[bag:[48] coat:[51] shawl:[47]]
sorted hooks: [47 48 51]
gatecrasher: Tom
unique arrivals: 3
```

And the complete file.

```go
// cloakroom.go — day 7, maps, comma-ok, counting, and no order
// Run:  go run cloakroom.go
package main

import (
	"fmt"
	"maps"
	"slices"
)

func main() {
	cloakroom := map[int]string{47: "shawl", 48: "bag"}
	cloakroom[51] = "coat"
	fmt.Printf("hook 47 holds %s; %d hooks in use\n", cloakroom[47], len(cloakroom))
	fmt.Println(cloakroom)

	item, ok := cloakroom[112]
	fmt.Printf("missing key reads %q and ok is %v; still %d hooks in use\n", item, ok, len(cloakroom))

	if item, ok := cloakroom[112]; ok {
		fmt.Println("hook 112 holds", item)
	} else {
		fmt.Println("token 112 was never issued")
	}

	items := []string{"shawl", "bag", "shawl", "coat", "shawl", "bag"}
	counts := make(map[string]int)
	for _, it := range items {
		counts[it]++
	}
	fmt.Println("counts:", counts)

	byItem := make(map[string][]int)
	for hook, it := range cloakroom {
		byItem[it] = append(byItem[it], hook)
	}
	fmt.Println("grouped:", byItem)

	fmt.Println("sorted hooks:", slices.Sorted(maps.Keys(cloakroom)))

	guests := map[string]bool{"Asha": true, "Ravi": true, "Meera": true}
	arrived := []string{"Ravi", "Asha", "Ravi", "Tom"}
	unique := make(map[string]bool)
	for _, name := range arrived {
		unique[name] = true
		if !guests[name] {
			fmt.Println("gatecrasher:", name)
		}
	}
	fmt.Println("unique arrivals:", len(unique))
}
```

## 6. How the other two languages do it

Python, where a missing key is refused and a set is its own type:

```python
cloakroom = {47: "shawl", 48: "bag"}
print(cloakroom[112])                 # KeyError: 112
print(cloakroom.get(112, "nothing"))  # "nothing", nothing added
guests = {"Asha", "Ravi"}             # a real set
```

C++, where a missing key is inserted by `[]` and refused by `at()`:

```cpp
std::unordered_map<int, std::string> cloakroom = {{47, "shawl"}, {48, "bag"}};
std::cout << cloakroom[112];          // "" — and the map now has 3 entries
std::cout << cloakroom.at(112);       // throws std::out_of_range
std::set<std::string> guests = {"Asha", "Ravi"};
```

The one line of difference that matters: **Python refuses, Go returns zero, C++ inserts zero.** Go's `m[k]` and C++'s `m[k]` both print `""` for a missing key and look identical on the page, but the C++ one changed the map and the Go one did not. And Go is the only one of the three where the same expression gives you two results, `v, ok`, so that you can tell "stored empty" from "never stored" without a second lookup. Python needs `in` then `[]`, or `get`; C++ needs `find` or `contains`.

## 7. The traps

**The real error: writing to a nil map.** Declare a map without making it.

```go
	var counts map[string]int
	counts["shawl"]++
```

```
panic: assignment to entry in nil map

goroutine 1 [main]:
main.main()
	/home/you/day07/cloakroom.go:10 +0x2c
exit status 2
```

`var m map[K]V` gives you nil, which reads fine and writes never. Always `make` it or use a literal. This is the first panic most Go programmers ever see.

**The near-miss: trusting the zero value.** Look up a price and charge it.

```go
	prices := map[string]int{"shawl": 200, "bag": 150}
	fmt.Println("coat costs", prices["coat"])
```

```
coat costs 0
```

No error. The coat is free now. When zero is a plausible stored value, you must use comma-ok: `price, ok := prices["coat"]; if !ok { ... }`. The rule of thumb: if you would be embarrassed to act on the zero value, check `ok`.

**The real error: a slice as a key.** Group by a pair of names.

```go
	seating := map[[]string]string{}
```

```
./cloakroom.go:8:17: invalid map key type []string
```

Slices are not comparable, so they cannot be keys. Use an array, `[2]string`, or a struct, both of which are comparable when their contents are. Caught at compile time, where Python caught it at run time.

## 8. Say it out loud

**How it gets asked**

- "What does a Go map return for a missing key, and how do you tell?"
- "Why is map iteration order random in Go?"
- "What happens if you write to a nil map?"

**What to say out loud, the first ninety seconds**

"A Go map is a hash table with comparable keys and constant-time average lookup. Reading a key that is absent returns the zero value of the value type, with no error and no insertion, so `m["missing"]` on a `map[string]int` is `0`. That makes counting a one-liner, `counts[k]++`, but it also hides misses, so when the zero value is ambiguous I use the comma-ok form: `v, ok := m[k]`, where `ok` is `false` for an absent key even if `v` is a legitimate zero. In practice it is written `if v, ok := m[k]; ok { ... }`.

Iteration order is deliberately randomised so that code cannot accidentally rely on it; when order matters I sort the keys, `slices.Sorted(maps.Keys(m))`. There is no set type; `map[T]bool` or `map[T]struct{}` is the idiom. A map declared with `var` and never made is nil: reads return zero values, but a write panics with `assignment to entry in nil map`, so I always `make` or use a literal."

**The follow-ups**

1. *"Why `map[T]struct{}` rather than `map[T]bool` for a set?"* — `struct{}` occupies zero bytes, so the map stores only keys. `bool` costs a byte per entry and reads more clearly; for small sets clarity wins.
2. *"Is a Go map safe to use from multiple goroutines?"* — No. Concurrent writes, or a write concurrent with a read, cause a fatal error. You guard it with a mutex or use `sync.Map`, which day 33 covers.
3. *"Does `delete` on a missing key fail?"* — No. It is a no-op, and so is deleting from a nil map. Only writing to a nil map panics.

**A model answer**

"Go maps are hash tables keyed by comparable types. Absent-key reads return the value type's zero value without inserting, and the two-value form `v, ok := m[k]` distinguishes absence from a stored zero; with an `if` init statement this is the standard lookup idiom. The zero-value behaviour makes `counts[k]++` and `groups[k] = append(groups[k], v)` correct without initialisation. Iteration order is randomised by design; sorting `maps.Keys` gives determinism. Sets are maps to `bool` or `struct{}`. A nil map, from `var m map[K]V`, supports reads and `delete` but panics on write, so maps are created with `make` or a literal. Slices, maps and functions are not comparable and cannot be keys; arrays and structs of comparables can."

## 9. Recall card

- `m := map[K]V{}` or `make(map[K]V)`; `m[k]` on a miss returns the zero value and adds nothing; `v, ok := m[k]` tells you which.
- `if v, ok := m[k]; ok { ... }` is the lookup idiom; `counts[k]++` and `append(groups[k], v)` work from nothing because of zero values.
- `var m map[K]V` is nil: reads give zeros, writes `panic: assignment to entry in nil map`; always `make`.
- No order: `range` is randomised; sort with `slices.Sorted(maps.Keys(m))`; no set type: use `map[T]bool`.
- Keys must be comparable: slices are `invalid map key type`; arrays and structs are fine.
