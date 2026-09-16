---
day: 7
track: lang-python
title: "dict and set: hashing, ordering, and the in operator"
theme: "Key-value and membership"
phase: "Languages: every language, every basic"
status: written
---

# Day 007 · Python — dict and set: hashing, ordering, and the in operator

**Today's theme:** Key-value and membership

**After today you can:** You can count, group and deduplicate with a map in each language and explain what happens on a missing key.

**The interviewer asks it as:** *What does your language do when you read a key that is not there?*

---

## 1. What this is, and why it matters

A dict is a collection that stores values under keys, so you look things up by name instead of by position, and a set is a collection of keys with no values, good only for asking "is this in here". Both are built on hashing, which turns a key into a slot number so lookup takes the same time whether there are ten entries or ten million. When you read a key a Python dict does not have, it refuses loudly with a `KeyError`, and the two ways around that, `get` and `in`, are half of today.

At work, dicts are how you count, group, cache and index almost everything, and the `KeyError` on a missing key is the most common Python exception after `TypeError`. Interviewers ask "why is dict lookup O(1)", "what can be a dict key and why", and the question in the heading, which has three different answers across today's three languages.

## 2. The story

Devika is running the cloakroom at her cousin's wedding. Three hundred guests, one long counter, a wall of numbered hooks behind her, and a bowl of plastic tokens with the same numbers.

A guest hands over a shawl. Devika hangs it on hook 47, hands the guest token 47, and forgets about it. That is the whole system. When the guest comes back with token 47, Devika does not search three hundred hooks. She walks to 47 and lifts the shawl. It takes the same five seconds whether the wall has ten hooks in use or all three hundred.

Around eleven, a man hands her token 112. She goes to hook 112. It is empty. She is sure of it, because she never gave out 112; that batch of tokens is still in the sealed bag. So what does she do?

Devika, being Devika, comes back to the counter and says, "There is nothing under 112. This token was never issued." She refuses to hand over anything, and the man, embarrassed, finds his real token in the other pocket.

Her brother, who took over at midnight, handles it differently. A woman hands him token 200. He goes to the hook, finds nothing, comes back, and hands her an empty hanger with a straight face. No shawl, no explanation, just the empty hanger, as if that is what was always there.

And the hired boy at the far end of the counter does the third thing. Token 250, empty hook. He writes 250 on a fresh tag, hangs an empty hanger on hook 250, and gives the guest the hanger. Now hook 250 exists, with nothing on it, and at the end of the night the count of hooks in use is one higher than the number of things anyone ever left.

Meanwhile at the gate, Devika's aunt has the guest list on her phone, and her whole job is one question: is this name on it, yes or no. She does not care about order or how many times a name appears. Just in, or not in.

## 3. The idea in plain English

A **dict** stores **values** under **keys**. `cloakroom = {47: "shawl", 48: "bag"}` maps the key `47` to the value `"shawl"`. You read with `cloakroom[47]` and write with `cloakroom[49] = "coat"`. Hook number to item. Keys are unique; writing to a key that exists replaces its value.

How is the lookup fast? Python runs the key through a **hash function**, which turns any key into a number, and uses that number to pick a slot in a table. That is Devika walking straight to hook 47. No search. Lookup, insert and delete all take roughly constant time no matter how many entries there are.

For hashing to work, a key must never change while it is in the dict, because its slot was chosen from its value. So keys must be **immutable**: strings, numbers, tuples. A list cannot be a key, and Python tells you so with `TypeError: unhashable type: 'list'`.

When you read a key that is not there, `cloakroom[112]`, Python raises **`KeyError: 112`**. That is Devika refusing. It is the safest of the three behaviours, and it is also the one that crashes your program if you did not expect it. The alternatives: `cloakroom.get(112)` returns `None`, or `cloakroom.get(112, "nothing")` returns your chosen default, without adding anything; and `112 in cloakroom` asks first. `get` is the brother's empty hanger, but you had to ask for it.

Python dicts remember **insertion order**: walk one with `for key, value in cloakroom.items()` and you get entries in the order they were added.

A **set** is a dict with keys and no values: `guests = {"Asha", "Ravi"}`. `"Asha" in guests` is the aunt at the gate, constant time. `add` puts a name in, and adding one that is already there changes nothing. `set(some_list)` removes duplicates. Sets also do the operations from school: `&` for both, `|` for either, `-` for in-this-not-that. The one catch: `{}` is an empty dict, not an empty set. An empty set is `set()`.

## 4. The picture

```
 cloakroom = {47: "shawl", 48: "bag", 51: "coat"}

   key ──► hash(key) ──► slot            table
   47  ──►   ...     ──►  3      ┌────┬─────────────────┐
   48  ──►   ...     ──►  0      │ 0  │ 48 → "bag"      │
   51  ──►   ...     ──►  6      │ 1  │                 │
                                 │ 2  │                 │
   cloakroom[47]                 │ 3  │ 47 → "shawl"    │  ◄── straight here, no search
                                 │ 4  │                 │
   cloakroom[112]                │ 5  │                 │
     hash → slot 5 → empty       │ 6  │ 51 → "coat"     │
     → KeyError: 112             └────┴─────────────────┘
```

*Notice that the key is not stored in order and is not searched for; the hash says which slot to look in. Notice that the miss is also instant: slot 5 is empty, so the answer is "not here" without checking anything else.*

## 5. The code, built step by step

Start `cloakroom.py` in a `day07` folder.

```python
cloakroom: dict[int, str] = {47: "shawl", 48: "bag"}
cloakroom[51] = "coat"
print(cloakroom[47], len(cloakroom))
print(cloakroom)
```

```
shawl 3
{47: 'shawl', 48: 'bag', 51: 'coat'}
```

The hint `dict[int, str]` says int keys, str values. Order printed is order inserted.

The missing key, three ways.

```python
print(47 in cloakroom, 112 in cloakroom)
print(cloakroom.get(112))
print(cloakroom.get(112, "nothing under that token"))
print(len(cloakroom))
```

```
True False
None
nothing under that token
3
```

`in` asks. `get` returns `None` or your default. And `len` is still 3: `get` added nothing. Now the fourth way, which is what `[]` does.

```python
print(cloakroom[112])
```

```
Traceback (most recent call last):
  File "/home/you/day07/cloakroom.py", line 9, in <module>
    print(cloakroom[112])
          ~~~~~~~~~^^^^^
KeyError: 112
```

Devika refusing. Most of the time this is what you want: a missing key is a bug, and a crash at the right line is better than an empty hanger nobody notices.

Counting, which is the most common dict job there is.

```python
items = ["shawl", "bag", "shawl", "coat", "shawl", "bag"]
counts: dict[str, int] = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1
print(counts)
```

```
{'shawl': 3, 'bag': 2, 'coat': 1}
```

`get(item, 0)` is the trick: the first time an item is seen, it counts from zero instead of raising. The standard library packages this as `collections.Counter(items)`, which gives the same dict with `.most_common()` on top. In an interview, write the `get` version first, then say you would use `Counter`.

Grouping, the second most common job.

```python
by_hook: dict[str, list[int]] = {}
for hook, item in cloakroom.items():
    by_hook.setdefault(item, []).append(hook)
print(by_hook)
```

```
{'shawl': [47], 'bag': [48], 'coat': [51]}
```

`setdefault(key, [])` returns the existing list for that key, or stores and returns a new empty one. `.items()` walks key-value pairs together.

Sets.

```python
guests = {"Asha", "Ravi", "Meera"}
arrived = ["Ravi", "Asha", "Ravi", "Tom"]
print("Asha" in guests, "Tom" in guests)
print(set(arrived))
print(set(arrived) & guests, set(arrived) - guests)
```

```
True False
{'Ravi', 'Asha', 'Tom'}
{'Ravi', 'Asha'} {'Tom'}
```

`set(arrived)` removed the duplicate `Ravi`. `&` is who both arrived and was invited; `-` is who arrived uninvited. Sets print in no particular order; they do not promise one.

Here is the run and output for the complete program.

```bash
python3 cloakroom.py
```

```
hook 47 holds shawl; 3 hooks in use
{47: 'shawl', 48: 'bag', 51: 'coat'}
is 112 there? False; get says None; get with default says nothing under that token
still 3 hooks in use
counts: {'shawl': 3, 'bag': 2, 'coat': 1}
grouped: {'shawl': [47], 'bag': [48], 'coat': [51]}
Asha invited? True; Tom invited? False
unique arrivals: 3; gatecrashers: {'Tom'}
```

And the complete file.

```python
# cloakroom.py — day 7, dict and set
# Run:  python3 cloakroom.py

cloakroom: dict[int, str] = {47: "shawl", 48: "bag"}
cloakroom[51] = "coat"
print(f"hook 47 holds {cloakroom[47]}; {len(cloakroom)} hooks in use")
print(cloakroom)

print(
    f"is 112 there? {112 in cloakroom}; get says {cloakroom.get(112)}; "
    f"get with default says {cloakroom.get(112, 'nothing under that token')}"
)
print(f"still {len(cloakroom)} hooks in use")

items = ["shawl", "bag", "shawl", "coat", "shawl", "bag"]
counts: dict[str, int] = {}
for item in items:
    counts[item] = counts.get(item, 0) + 1
print(f"counts: {counts}")

by_hook: dict[str, list[int]] = {}
for hook, item in cloakroom.items():
    by_hook.setdefault(item, []).append(hook)
print(f"grouped: {by_hook}")

guests = {"Asha", "Ravi", "Meera"}
arrived = ["Ravi", "Asha", "Ravi", "Tom"]
print(f"Asha invited? {'Asha' in guests}; Tom invited? {'Tom' in guests}")
print(f"unique arrivals: {len(set(arrived))}; gatecrashers: {set(arrived) - guests}")
```

Two f-strings next to each other inside round brackets are joined into one; that is how you split a long print across lines.

## 6. How the other two languages do it

Go, where a missing key hands you the empty hanger and you ask separately whether it was real:

```go
cloakroom := map[int]string{47: "shawl", 48: "bag"}
fmt.Println(cloakroom[112])          // "" — the zero value, no error, nothing added
item, ok := cloakroom[112]           // ok is false: the comma-ok idiom
```

C++, where `[]` on a missing key hangs an empty hanger on a new hook:

```cpp
std::unordered_map<int, std::string> cloakroom = {{47, "shawl"}, {48, "bag"}};
std::cout << cloakroom[112] << "\n";  // "" — and now cloakroom.size() is 3
std::cout << cloakroom.at(112);        // throws std::out_of_range
```

The one line of difference that matters: **a missing key raises in Python, returns the zero value in Go, and inserts the zero value in C++.** Python is Devika: refuse. Go is the brother: empty hanger, and a second value `ok` if you want to know. C++ is the hired boy: `[]` creates the entry, and only `at()` refuses. A Python programmer moving to Go will forget to check `ok` and process empty strings. A Python programmer moving to C++ will read a key to check whether it exists and thereby create it.

## 7. The traps

**The real error: a list as a key.** Group guests by the tables they sat at.

```python
seating = {}
seating[["Asha", "Ravi"]] = "table 4"
```

```
Traceback (most recent call last):
  File "/home/you/day07/cloakroom.py", line 2, in <module>
    seating[["Asha", "Ravi"]] = "table 4"
    ~~~~~~~^^^^^^^^^^^^^^^^^^
TypeError: unhashable type: 'list'
```

A list can change after it is stored, so its hash would go stale. Use a tuple, `("Asha", "Ravi")`, which cannot change and therefore can be hashed.

**The real error: changing a dict while walking it.** Remove every empty hook.

```python
for hook in cloakroom:
    if cloakroom[hook] == "":
        del cloakroom[hook]
```

```
Traceback (most recent call last):
  File "/home/you/day07/cloakroom.py", line 1, in <module>
    for hook in cloakroom:
RuntimeError: dictionary changed size during iteration
```

Yesterday's list trap, and this time Python catches it. Walk a copy of the keys, `for hook in list(cloakroom)`, or build a new dict of what to keep.

**The near-miss: the empty set that is a dict.** Start a set of arrivals.

```python
arrived = {}
arrived.add("Ravi")
```

```
AttributeError: 'dict' object has no attribute 'add'
```

`{}` is a dict. The empty set is `set()`. A set with items uses braces, `{"Ravi"}`, which is what makes the empty case confusing.

## 8. Say it out loud

**How it gets asked**

- "What does your language do when you read a key that is not there?"
- "Why is dictionary lookup O(1), and what can be a key?"
- "How would you count the occurrences of each word in a list?"

**What to say out loud, the first ninety seconds**

"A Python dict is a hash table. Each key is run through a hash function that gives a slot index, so lookup, insert and delete are average constant time regardless of size. Keys must be hashable, which in practice means immutable: strings, numbers, tuples of those. A list cannot be a key because it could change after insertion and its hash would no longer match its slot.

Reading a missing key with square brackets raises `KeyError`. That is deliberate: a missing key is usually a bug, and a loud failure at the right line beats a silent default. When a missing key is expected, I use `d.get(key, default)`, which returns the default without inserting, or test with `key in d` first. Go returns the zero value and a second boolean; C++'s `operator[]` inserts a default-constructed value, so the three languages disagree, and I say which one I am in.

Dicts preserve insertion order since Python 3.7. A set is a hash table of keys with no values; `in` is O(1), it deduplicates, and it supports intersection, union and difference. To count words I do `counts[w] = counts.get(w, 0) + 1`, or use `collections.Counter`."

**The follow-ups**

1. *"What happens when two keys hash to the same slot?"* — A collision. Python probes for another slot; lookup checks the key itself, not only the hash, so correctness is unaffected. Too many collisions degrade toward O(n), which is why the table grows before it gets crowded.
2. *"What is `defaultdict`?"* — A dict that creates a value on a missing key using a factory you give it: `defaultdict(list)` for grouping, `defaultdict(int)` for counting. It is C++'s `operator[]` behaviour, opted into.
3. *"Can a dict key be a tuple containing a list?"* — No. The tuple is immutable but its hash includes its contents, and the list inside is unhashable, so the whole tuple is unhashable.

**A model answer**

"`dict` is an insertion-ordered hash map: keys are hashed to slots, giving average O(1) get, set and delete; keys must be hashable and therefore effectively immutable, so lists and dicts cannot be keys but tuples of hashables can. Reading an absent key via `[]` raises `KeyError`; `get(k, default)` and `in` handle the expected-miss case without inserting; `setdefault` and `defaultdict` opt into insert-on-miss. `set` is the key-only counterpart with O(1) membership and the algebraic operations. Counting is `get(k, 0) + 1` or `Counter`; grouping is `setdefault(k, []).append(v)`. Mutating a dict during iteration raises `RuntimeError`, so I iterate over `list(d)` when deleting."

## 9. Recall card

- `d = {k: v}`; `d[k]` reads and raises `KeyError` on a miss; `d.get(k, default)` and `k in d` do not; `get` never inserts.
- Hashing makes lookup O(1); keys must be immutable: str, int, tuple; a list key is `TypeError: unhashable type`.
- Count with `d[k] = d.get(k, 0) + 1` or `Counter`; group with `d.setdefault(k, []).append(v)`; dicts keep insertion order.
- `set` is keys only: `in`, `add`, `set(list)` dedups, `&` `|` `-`; empty set is `set()`, because `{}` is a dict.
- Deleting while iterating is `RuntimeError: dictionary changed size during iteration`; iterate over `list(d)` instead.
