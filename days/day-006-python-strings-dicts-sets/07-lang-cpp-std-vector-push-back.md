---
day: 6
track: lang-cpp
title: "std::vector: push_back, size, capacity, and reallocation"
theme: "Growable sequences"
phase: "Languages: every language, every basic"
status: written
---

# Day 006 · C++ — std::vector: push_back, size, capacity, and reallocation

**Today's theme:** Growable sequences

**After today you can:** You can grow, shrink, index and copy a sequence in each language and say when a copy really happens.

**The interviewer asks it as:** *What happens under the hood when you append to a full sequence?*

---

## 1. What this is, and why it matters

`std::vector` is C++'s growable row of values: one continuous block with some spare slots, `push_back` to add at the end, `size()` for how many you have and `capacity()` for how many will fit before the next move. When the block fills, the vector gets a bigger block and copies everything across, and at that moment anything that was pointing into the old block is pointing at nothing. Assigning one vector to another copies every element, which is the opposite of what Python and Go do.

At work, `std::vector` is the default container for everything, and the two bugs it produces are the unchecked `v[i]` that reads past the end without complaint and the reference that outlives a reallocation. Interviewers ask "what is the difference between `size` and `capacity`", "what happens to references when a vector grows", and "why is `v[i]` faster than `v.at(i)` and when should you care".

## 2. The story

Nandini is having twenty people over for her mother's sixtieth, and everyone leaves their shoes at the door. She has a shoe rack in the hallway with eight slots.

The first guests arrive and slide their shoes into slot one, slot two, slot three. Easy. Nobody has to think. Each new pair goes in the next empty slot at the end.

At around seven the ninth pair arrives, and the rack is full. Nandini drags out the bigger rack from the storeroom, the one with sixteen slots, and moves all eight pairs across in the same order, then slides the ninth pair into slot nine. It takes her two minutes. The guests after that go straight into slots ten, eleven, twelve, and nobody has to move anything again for a while.

Her uncle, who arrived third, comes out later for a cigarette and reaches for slot three on the old rack. Empty. The rack he remembered is not the rack anymore. His shoes are in slot three of the new one, but he had remembered the place, not the shoes.

Then her mother's oldest friend arrives, and her mother insists, absolutely insists, that this woman's shoes go in slot one. So Nandini takes every single pair out, shifts each one along by one slot, and puts the new pair at the front. Eleven pairs moved for one arrival. Nobody enjoys it.

At the end of the night, people leave in reverse order, roughly. The last pair in is the first pair out, and taking a pair from the end of the rack costs nothing: lift, go. But when her uncle leaves early, from slot three, everyone after him shuffles down a slot to close the gap, because Nandini does not like gaps.

Two rules she has learned by midnight. Adding at the end is free until the rack is full, and then it costs a whole move, but only once in a while. Adding or removing anywhere else costs a shuffle of everyone behind it, every time.

## 3. The idea in plain English

A **`std::vector<T>`**, from the header `<vector>`, is a row of values of type `T` in one continuous block, with spare slots at the end. `std::vector<std::string> shoes = {"red", "blue", "black"};` makes one holding three strings. `shoes[0]` reads the first, `shoes[0] = "grey"` changes it, `shoes.size()` is how many there are.

`capacity()` is how many slots the block has, spare ones included. `push_back(x)` writes `x` into the next spare slot. When `size() == capacity()`, the rack is full: the vector gets a new block, usually twice the size, copies or moves every element across, and frees the old block. That is the two minutes with the bigger rack, and it is why `push_back` is **amortised constant time**: the copy is rare and gets rarer.

`reserve(n)` asks for a block of at least `n` slots up front. If you know you will push twenty items, `reserve(20)` first means no copies at all.

Here is the thing the other two languages do not make you think about as hard. When the vector moves to a new block, **anything that referred to a slot in the old block is now invalid**. A **reference**, written `std::string& first = shoes[0];`, is another name for that exact slot, and day 12 covers it properly; today, know that after a reallocation `first` names a slot in a freed block, and reading it is undefined behaviour. The uncle at the old rack. This is called **iterator invalidation**, and it is the classic `std::vector` bug.

`shoes[i]` does **no bounds checking**. `shoes[3]` on a three-element vector reads whatever bytes sit past the end and tells you nothing. `shoes.at(3)` checks and stops the program with a message. `[]` is faster; `at()` is safer; interviewers want you to know both exist and when you would pick each.

Insert at the front, `shoes.insert(shoes.begin(), "sandal")`, shifts every element: the mother's oldest friend. `pop_back()` removes the last for free. `erase(shoes.begin() + 1)` removes the second and shifts the rest down. `begin()` is a marker for the first slot, and `begin() + i` for the slot at index `i`.

And copying. `std::vector<std::string> b = shoes;` makes a **complete copy**, every element, into a new block. Python and Go would have made `b` a second name for the same block. In C++, `=` copies, always, unless you ask otherwise.

## 4. The picture

```
 std::vector<std::string> shoes = {"red", "blue", "black"};     size 3, capacity 3

   index:   0       1        2
          ┌───────┬────────┬────────┐
  shoes ─►│ "red" │ "blue" │"black" │
          └───────┴────────┴────────┘
             ▲
  first ─────┘   std::string& first = shoes[0];

 shoes.push_back("white");     full → new block of 6, copy 3, write 1, free the old

          ┌───────┬────────┬────────┬────────┬──────┬──────┐
  shoes ─►│ "red" │ "blue" │"black" │"white" │  --  │  --  │
          └───────┴────────┴────────┴────────┴──────┴──────┘
  first ─────► (the old block, freed)   ✗ dangling: reading it is undefined behaviour

 std::vector<std::string> b = shoes;     a SECOND block, every element copied
```

*Notice that `first` still points where the old block was. Nothing updates it. Notice that `b` is a whole new block, which is what `=` means in C++ and not in the other two languages.*

## 5. The code, built step by step

Start `rack.cpp` in a `day06` folder.

```cpp
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> shoes = {"red", "blue", "black"};
    std::cout << shoes.size() << " " << shoes.capacity() << "\n";
    shoes.push_back("white");
    std::cout << shoes.size() << " " << shoes.capacity() << "\n";
```

```
3 3
4 6
```

Full at three, so the fourth `push_back` moved to a block of six. Two more pushes are free.

Watch it grow, and then watch `reserve` stop it growing.

```cpp
    std::vector<int> rack;
    std::size_t last_cap = 0;
    for (int i = 0; i < 20; ++i) {
        rack.push_back(i);
        if (rack.capacity() != last_cap) {
            last_cap = rack.capacity();
            std::cout << "after " << rack.size() << " items: capacity " << last_cap << "\n";
        }
    }
```

```
after 1 items: capacity 1
after 2 items: capacity 2
after 3 items: capacity 4
after 5 items: capacity 8
after 9 items: capacity 16
after 17 items: capacity 32
```

Same doubling as Go, and for the same reason. Now with `reserve`:

```cpp
    std::vector<int> planned;
    planned.reserve(20);
    for (int i = 0; i < 20; ++i) {
        planned.push_back(i);
    }
    std::cout << planned.size() << " items, capacity " << planned.capacity() << ", zero copies\n";
```

```
20 items, capacity 20, zero copies
```

Index, change in place, and the two ways to read a slot.

```cpp
    shoes[0] = "grey";
    std::cout << shoes[0] << " " << shoes.at(1) << " " << shoes.back() << "\n";
```

```
grey blue white
```

`[]` and `at()` read the same slot; `at()` checks the index first. `back()` is the last element, `front()` the first.

Front and middle, and what they cost.

```cpp
    shoes.insert(shoes.begin(), "sandal");
    shoes.pop_back();
    shoes.erase(shoes.begin() + 1);
    for (std::string shoe : shoes) {
        std::cout << shoe << " ";
    }
    std::cout << "\n";
```

```
sandal blue black
```

`insert` at `begin()` shifted four. `pop_back` removed `white` for free. `erase` at index 1 removed `grey` and shifted two down. There is no built-in way to print a vector, so a loop does it.

Copying, which is what `=` does.

```cpp
    std::vector<std::string> b = shoes;
    b.push_back("brown");
    std::cout << shoes.size() << " " << b.size() << "\n";
```

```
3 4
```

`b` got its own block. Pushing to it left `shoes` at three. In Python and Go this would have printed `4 4`.

Here is the build, run, and output for the complete program.

```bash
g++ -std=c++20 -Wall -Wextra rack.cpp -o rack
./rack
```

```
start: size 3 capacity 3
after push_back: size 4 capacity 6
after 1 items: capacity 1
after 2 items: capacity 2
after 3 items: capacity 4
after 5 items: capacity 8
after 9 items: capacity 16
after 17 items: capacity 32
reserved: 20 items, capacity 20, zero copies
read: grey blue white
after insert, pop_back, erase: sandal blue black
copy: shoes has 3, b has 4
```

And the complete file.

```cpp
// rack.cpp — day 6, std::vector, capacity, reallocation, and copies
// Build: g++ -std=c++20 -Wall -Wextra rack.cpp -o rack
// Run:   ./rack
#include <iostream>
#include <string>
#include <vector>

int main() {
    std::vector<std::string> shoes = {"red", "blue", "black"};
    std::cout << "start: size " << shoes.size() << " capacity " << shoes.capacity() << "\n";
    shoes.push_back("white");
    std::cout << "after push_back: size " << shoes.size() << " capacity " << shoes.capacity() << "\n";

    std::vector<int> rack;
    std::size_t last_cap = 0;
    for (int i = 0; i < 20; ++i) {
        rack.push_back(i);
        if (rack.capacity() != last_cap) {
            last_cap = rack.capacity();
            std::cout << "after " << rack.size() << " items: capacity " << last_cap << "\n";
        }
    }

    std::vector<int> planned;
    planned.reserve(20);
    for (int i = 0; i < 20; ++i) {
        planned.push_back(i);
    }
    std::cout << "reserved: " << planned.size() << " items, capacity " << planned.capacity()
              << ", zero copies\n";

    shoes[0] = "grey";
    std::cout << "read: " << shoes[0] << " " << shoes.at(1) << " " << shoes.back() << "\n";

    shoes.insert(shoes.begin(), "sandal");
    shoes.pop_back();
    shoes.erase(shoes.begin() + 1);
    std::cout << "after insert, pop_back, erase: ";
    for (std::string shoe : shoes) {
        std::cout << shoe << " ";
    }
    std::cout << "\n";

    std::vector<std::string> b = shoes;
    b.push_back("brown");
    std::cout << "copy: shoes has " << shoes.size() << ", b has " << b.size() << "\n";
    return 0;
}
```

## 6. How the other two languages do it

Python, where `=` shares and the capacity is hidden:

```python
shoes = ["red", "blue", "black"]
shoes.append("white")
b = shoes                 # same list
b.append("brown")         # shoes now has 5 too
print(shoes[10])          # IndexError: list index out of range
```

Go, where `=` shares the backing array and `cap` is visible like `capacity()`:

```go
shoes := []string{"red", "blue", "black"}
shoes = append(shoes, "white")
b := shoes                // same backing array
b = append(b, "brown")    // may or may not be visible through shoes
fmt.Println(shoes[10])    // panic: index out of range [10] with length 4
```

The one line of difference that matters: **C++ `=` copies every element; Python and Go `=` share.** And **C++ `[]` checks nothing; Python and Go check every index.** A Python programmer writing C++ will copy a large vector by accident and wonder why the function is slow, and will index past the end and wonder why the program prints nonsense instead of failing. The Go line to notice is the middle one: Go's sharing is conditional on capacity, which is its own kind of surprise, where C++ simply copies and Python simply shares.

## 7. The traps

**The near-miss: reading past the end with `[]`.** Three shoes, ask for the fourth.

```cpp
    std::vector<std::string> three = {"red", "blue", "black"};
    std::cout << three[3] << "\n";
```

No compiler warning. At run time it prints an empty line, or garbage, or crashes, depending on what happened to be in the memory after the block. Undefined behaviour with no message is the worst kind, because the program looks like it worked. Python raised `IndexError`, Go panicked; C++ said nothing.

**The real error: reading past the end with `at()`.** The same line with the checked version.

```cpp
    std::cout << three.at(3) << "\n";
```

```
terminate called after throwing an instance of 'std::out_of_range'
  what():  vector::_M_range_check: __n (which is 3) >= this->size() (which is 3)
Aborted (core dumped)
```

Now it stops and says why. `at()` throws an **exception**, which day 9 teaches you to catch; today, the point is that it stops the program with a message instead of continuing with garbage. In code where an index comes from outside, from a user or a file, `at()` earns its small cost.

**The near-miss: the reference that outlives the block.** Name a slot, then grow the vector.

```cpp
    std::vector<std::string> v = {"red", "blue", "black"};
    std::string& first = v[0];
    v.push_back("white");
    std::cout << first << "\n";
```

The `push_back` reallocated, so `first` names a slot in a block that no longer exists. Sometimes this prints `red`, because the freed memory has not been reused yet. Sometimes it prints garbage. Sometimes it crashes next Tuesday. Compile with `-fsanitize=address` and the sanitiser catches it and reports `heap-use-after-free`, with the line that freed the block and the line that read it. Rule: after any `push_back`, `insert` or `erase`, every reference, pointer and iterator into that vector is suspect. Take them fresh.

## 8. Say it out loud

**How it gets asked**

- "What is the difference between `size()` and `capacity()`?"
- "What happens to a reference into a vector when the vector grows?"
- "Why does `v[i]` not check bounds, and when do you use `at()`?"

**What to say out loud, the first ninety seconds**

"`std::vector` is a contiguous dynamic array. `size()` is the number of elements; `capacity()` is the number of slots allocated. `push_back` writes into spare capacity in constant time; when size equals capacity it allocates a new block, typically double, moves or copies the elements, frees the old block, and continues. That geometric growth makes `push_back` amortised O(1), and `reserve(n)` lets me pay for the block once up front when I know the count.

Reallocation invalidates every pointer, reference and iterator into the old block, so a reference taken before a `push_back` may dangle after it; that is the classic vector bug, and AddressSanitizer catches it as heap-use-after-free. `operator[]` does no bounds check, for speed, and reading past the end is undefined behaviour with no diagnostic; `at()` checks and throws `std::out_of_range`. I use `[]` in hot loops where the index is provably valid and `at()` when the index comes from outside. Assignment copies the whole vector element by element, unlike Python and Go where it aliases."

**The follow-ups**

1. *"What is the complexity of `insert` at the front?"* — O(n): every element shifts. For frequent front insertion use `std::deque`, which is O(1) at both ends.
2. *"Does `pop_back` shrink the capacity?"* — No. Capacity never shrinks on its own. `shrink_to_fit()` requests it, and even that is a request the implementation may ignore.
3. *"How do you pass a vector to a function without copying it?"* — By `const` reference, `const std::vector<T>&`, which is the subject of day 12. Passing by value copies every element.

**A model answer**

"`std::vector` stores elements contiguously with a size and a larger-or-equal capacity. `push_back` is amortised O(1) through geometric reallocation: when full, it allocates roughly double, moves the elements, and frees the old storage. That reallocation invalidates all references, pointers and iterators into the vector, so any held reference must be re-taken after a growing operation; `reserve` avoids reallocation when the final size is known. `operator[]` is unchecked and out-of-range access is undefined behaviour; `at()` throws `std::out_of_range`. `insert` and `erase` away from the end are O(n) shifts. Copy assignment deep-copies the elements, which distinguishes C++ from the aliasing semantics of Python lists and Go slices."

## 9. Recall card

- `push_back` fills spare capacity; when `size() == capacity()` the vector allocates about double, copies, frees; capacity goes 1, 2, 4, 8, 16, 32; `reserve(n)` skips it.
- Reallocation invalidates every reference, pointer and iterator into the old block; re-take them after any `push_back`, `insert`, `erase`.
- `v[i]` checks nothing, reads garbage past the end; `v.at(i)` throws `std::out_of_range` with a message.
- `insert(begin(), x)` and `erase(begin() + i)` shift everything after, O(n); `pop_back()` is free.
- `std::vector b = a;` copies every element, unlike Python and Go where `b = a` shares.
