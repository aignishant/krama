---
day: 78
track: cpp
title: "structs, pointers, and building your own nodes"
phase: "C++ and competitive programming"
status: written
---

# Day 078 · C++ — structs, pointers, and building your own nodes

**After today you can:** You can define a node, link nodes together, and say what a pointer holds and what happens when it dangles.

**The interviewer asks it as:** *What is the difference between a pointer and a reference?*

---

> Eighth of the twelve C++ days. Today's DSA lesson calls it "pointers without pointers", because
> Python does not make you look at them. C++ does, and this is the day the language stops being
> a nicer Python and becomes its own thing.

---

## 1. What this is, and why they ask it

Every structure from here to the end of the course — linked lists, trees, tries, graphs — is
built the same way. You define a small bundle of data, and inside it you keep the **address** of
another bundle of the same kind. Follow the addresses and you have a chain, a tree, or a network.

In Python that address is invisible. You write `node.next = other` and Python quietly stores a
reference for you. In C++ you write `node->next = other`, and `next` is a **pointer**: a variable
whose value is a memory address. You can print it. You can compare it. You can set it to
`nullptr`, meaning "this points at nothing". And you can get it wrong in ways Python will not let
you — leaving it pointing at memory that has been given back, which is the bug that made C++ a
byword for crashes.

Interviewers ask "pointer or reference" more often than any other C++ question except parameter
passing, and it is really a question about ownership: who is responsible for this memory, and who
is allowed to change where it points. Getting that answer right is also the foundation of the
low-level design rounds later in the course.

---

## 2. The story

The school Vidya's daughter goes to, in Dombivli, closes sometimes without warning — heavy rain,
a strike, once because a transformer went. When that happens somebody has to tell two hundred and
forty families before seven in the morning.

The teacher who used to do it stopped in 2018, because it took her over an hour and she had a
newborn. What replaced her is a chain.

The head teacher rings one parent. That parent rings one other. That one rings the next. Nobody
holds the full list. Each family knows exactly one thing: whose turn comes after theirs. Vidya
knows she rings the Kambles at 22B. The Kambles know they ring somebody in the next building. She
has no idea who that is and does not need to.

It works well. Two hundred and forty families in about twenty-five minutes, and the head teacher
makes one call.

The last family in the chain was told, very clearly, that they are the last. They ring nobody.
That was worth saying out loud, because the first year somebody at the end assumed they had been
forgotten and started ringing people at random.

Where it went wrong was March.

The Kambles moved to Kalyan. They gave up the old number, and the phone company gave that number
to somebody else about six weeks later — a man who works nights and had nothing to do with the
school.

The next time the school shut, at ten past six on a Tuesday, Vidya rang the number she had. It
rang. Somebody answered. It sounded like a man half asleep, which is exactly what a parent at ten
past six sounds like. She said the school was closed, he said something, and she hung up and went
back to bed satisfied that she had done her part.

Everyone after the Kambles in that chain — sixty-one families — sent their children out to a
locked school.

What Vidya said afterwards, and what the head teacher repeated at the next meeting, was that the
number had not stopped working. If it had stopped working she would have known in three seconds.
It worked perfectly. It just reached somebody who was not the Kambles, and there was no way to
tell from the ringing.

---

## 3. The idea in plain English

### A `struct` is a bundle with names

```cpp
struct Node {
    int value;
    Node* next;
};
```

That says: a `Node` is an `int` called `value`, and an address called `next` which points at
another `Node`. It is one family in the chain: the thing they know, and whose turn is next.

You make one and reach into it with a dot:

```cpp
Node a;
a.value = 5;
a.next = nullptr;
```

A `struct` in C++ is a **class whose members are public by default**, and that is the only
difference between `struct` and `class`. Use `struct` for plain data bundles, `class` when there
is behaviour and things to hide — [day 044](../day-044-first-and-last-occurrence/README.md) starts that
properly.

Giving it a constructor saves a lot of typing:

```cpp
struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}     // an initialiser list
};

Node* n = new Node(5);      // value = 5, next = nullptr
```

The `: value(v), next(nullptr)` part is an **initialiser list**. It sets the members as they are
created rather than assigning to them afterwards, which is both faster and the only way to
initialise things that cannot be reassigned.

### A pointer holds an address

```cpp
int x = 42;
int* p = &x;      // p holds the ADDRESS of x
```

- `int*` is the type: "address of an int".
- `&x` means "the address of x". Read `&` here as "address of".
- `*p` means "the thing at that address". Read `*` as "the thing at".

```cpp
std::cout << x;    // 42       — the value
std::cout << p;    // 0x7ffd…  — an address, a number
std::cout << *p;   // 42       — follow the address, get the value
*p = 99;           // change x through the address
std::cout << x;    // 99
```

That last pair of lines is the whole point of a pointer. It lets you reach a variable you were not
given directly.

`&` is doing two different jobs in C++ and this is a genuine source of confusion. In a *type* —
`int& r` — it means reference. In an *expression* — `&x` — it means address-of. The position tells
you which.

### `->` is a dot through a pointer

When you have a pointer to a struct, `p.value` is wrong, because `p` is an address and addresses
have no members. You must follow it first:

```cpp
(*p).value      // follow the pointer, then take the member. Correct but ugly.
p->value        // exactly the same thing. Always write this.
```

**Dot when you have the thing. Arrow when you have its address.** That one sentence resolves
ninety per cent of beginner confusion.

### `nullptr` is "points at nothing"

```cpp
Node* p = nullptr;
if (p == nullptr) { /* nothing there */ }
if (!p)           { /* the same test, shorter */ }
```

`nullptr` is the last family in the chain being told they ring nobody. It is a real value, it is
testable, and **following it crashes your program**:

```cpp
Node* p = nullptr;
std::cout << p->value;      // Segmentation fault
```

Use `nullptr`, not `NULL` and not `0`. `NULL` is inherited from C, is really just `0`, and can
pick the wrong function when overloading. `nullptr` has its own type and cannot be mistaken for a
number.

### Where the memory comes from: stack and heap

This is the part with no Python equivalent at all.

**The stack** is where local variables live. It is fast — allocating is one instruction — and it
is automatic: when the function returns, everything it declared is destroyed. It is also small,
typically 1 to 8 megabytes.

```cpp
void f() {
    Node a;          // on the stack
}                    // a is destroyed here, automatically
```

**The heap** is a large pool you ask for memory from explicitly. It survives until you give it
back. It is slower to allocate — hundreds of nanoseconds rather than one instruction — and it is
big, limited only by the machine.

```cpp
Node* p = new Node(5);   // on the heap
delete p;                // you must give it back. Nobody does it for you.
```

**Every `new` needs exactly one `delete`.** Not zero — that is a **memory leak**, memory you can
never use again. Not two — that is a **double free**, which corrupts the allocator and crashes.

Why does a linked list need the heap at all? Because the nodes have to outlive the function that
created them. A `Node` on the stack dies when the function returns, and returning a pointer to it
is a dangling pointer. So chains, trees and graphs live on the heap.

### The dangling pointer is the Kambles' number

```cpp
Node* p = new Node(5);
delete p;                  // the memory goes back to the pool
std::cout << p->value;     // p still holds the same address
```

`delete` does not change `p`. `p` still holds the number it held before. The memory at that
address has been returned to the allocator, and may already have been given to something else.

**It usually still prints 5.** That is what makes it lethal. The freed memory has not been reused
yet, so the old value is still sitting there, and your test passes. Then in a bigger program
something else takes that memory, and now you are reading somebody else's data — which is Vidya
ringing a number that answers, in a voice that sounds right, and telling a night-shift worker that
school is closed.

The habit that costs nothing:

```cpp
delete p;
p = nullptr;      // now using it crashes immediately instead of lying
```

A crash you get every time beats a wrong answer you get sometimes.

### Pointer versus reference — the interview question

| | Pointer `T*` | Reference `T&` |
|---|---|---|
| can be null | **yes** | no |
| can be reassigned to another object | **yes** | no, bound for life |
| must be initialised | no | **yes** |
| needs `*` or `->` to use | yes | no, used like the object |
| can do arithmetic (`p + 1`) | yes | no |
| can point into an array and walk it | **yes** | no |

**Use a reference by default. Use a pointer when you need one of the things only a pointer can
do** — most often, when "nothing" is a legitimate value. A `Node*` that is `nullptr` means "end of
the chain", and a reference cannot express that, which is exactly why every linked list in C++ is
built from pointers.

### Smart pointers, which is what you would actually write

Raw `new` and `delete` are how it works underneath, and you must know them, because interviewers
ask and because LeetCode hands you raw `ListNode*`. But in code that ships, C++ has owned the
problem since 2011:

```cpp
#include <memory>

std::unique_ptr<Node> p = std::make_unique<Node>(5);
// no delete. When p goes out of scope, the Node is freed. Automatically.
```

`unique_ptr` is a pointer that frees what it points at when it is destroyed. There is exactly one
owner — you cannot copy it, only move it — so there is no question of who calls `delete`. That
pattern is called **RAII**: the lifetime of the memory is tied to the lifetime of a variable, so
the compiler does the bookkeeping.

`std::shared_ptr` is the version with a count, for when several things own something and the last
one out frees it. It costs more, and needs `std::weak_ptr` to break cycles.

**In an interview:** write raw pointers for a linked-list problem, because that is what they asked
for and what the harness gives you. Mention that in production you would use `unique_ptr`. That
one sentence tells them you know both worlds.

---

## 4. The picture

What a pointer actually contains:

```
  int x = 42;
  int* p = &x;

  memory
  address       0x7ffd4a20         0x7ffd4a28
              +--------------+   +--------------------+
              |      42      |   |     0x7ffd4a20     |
              +--------------+   +--------------------+
                     x                     p
                the value              the ADDRESS of x

   x   ->  42
   p   ->  0x7ffd4a20        (a number, 8 bytes)
  *p   ->  42                (go to 0x7ffd4a20 and look)
```

**What to notice:** `p` is an ordinary variable holding an ordinary number. There is nothing
magical about it. `*` is the instruction "treat this number as an address and go there".

Now the chain:

```
  head
   |
   v
  +-------+------+     +-------+------+     +-------+---------+
  |  10   |  o---+---> |  20   |  o---+---> |  30   | nullptr |
  +-------+------+     +-------+------+     +-------+---------+
   value   next         value   next         value    next
                                                        ^
                                                the last family:
                                                "you ring nobody"

  walking it:
    Node* cur = head;
    while (cur != nullptr) { use(cur->value); cur = cur->next; }
```

**What to notice:** nothing knows the whole chain. Each bundle knows one value and one address.
`head` is not the chain — it is a pointer to the front of it, and losing `head` loses everything.

And the dangling pointer:

```
  BEFORE delete

  p ------> +--------------------+
            |  Node { 5, null }  |   heap memory you own
            +--------------------+

  AFTER  delete p;

  p ------> +--------------------+
            |  (returned to the  |   the address in p has NOT changed
            |   allocator)       |   the memory is no longer yours
            +--------------------+

  LATER, something else allocates

  p ------> +--------------------+
            |  someone else's    |   p->value now reads THEIR data
            |  data              |   no crash. no warning. wrong answer.
            +--------------------+
            ^
            some other variable also points here, legitimately
```

**What to notice:** the middle picture is the dangerous one, because reading it usually still
gives 5. The bug does not announce itself until the third picture, in a different part of the
program, weeks later.

---

## 5. The code, built step by step

### The node, and a chain by hand

```cpp
struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};

Node* head = new Node(10);
head->next = new Node(20);
head->next->next = new Node(30);
```

Three allocations, three links, and the last `next` is `nullptr` because the constructor set it.
That is the diagram above, in code.

### Walking it

```cpp
void print(Node* head) {
    for (Node* cur = head; cur != nullptr; cur = cur->next)
        std::cout << cur->value << " -> ";
    std::cout << "null\n";
}
```

`cur = cur->next` is the whole idea of a linked list. Note the loop condition is `cur != nullptr`
and not `cur->next != nullptr` — the difference is whether you process the last element, and it is
the most common off-by-one in list code.

### Pushing at the front

```cpp
Node* push_front(Node* head, int value) {
    Node* fresh = new Node(value);
    fresh->next = head;      // the new one points at the old front
    return fresh;            // and becomes the new front
}
```

O(1), and it is why a linked list beats a vector for front insertion. **Set `fresh->next` before
you move `head`** — do it the other way round and you have lost the address of everything after
it, permanently. That is the single most common linked-list bug and it is why
[day 080](../day-080-dummy-head/README.md) teaches the dummy-head trick.

### Reversing, which is the interview problem

[Day 081](../day-081-reversing-a-list/README.md) does the reasoning. Here is the C++:

```cpp
Node* reverse(Node* head) {
    Node* prev = nullptr;
    Node* cur = head;
    while (cur != nullptr) {
        Node* nxt = cur->next;   // save it BEFORE overwriting
        cur->next = prev;        // turn the arrow round
        prev = cur;              // step both markers forward
        cur = nxt;
    }
    return prev;                 // cur is null; prev is the new head
}
```

Four lines in the loop and every one is necessary. Saving `nxt` first is the step people drop, and
without it `cur = cur->next` walks into the arrow you just redirected and loops forever.

### Freeing it, which Python never makes you do

```cpp
void destroy(Node* head) {
    while (head != nullptr) {
        Node* nxt = head->next;   // save the address BEFORE deleting
        delete head;
        head = nxt;
    }
}
```

Same trick, same reason. `delete head` first and then `head->next` reads freed memory.

### The same thing with `unique_ptr`

```cpp
struct SafeNode {
    int value;
    std::unique_ptr<SafeNode> next;      // owns whatever comes after it
    SafeNode(int v) : value(v), next(nullptr) {}
};

auto head = std::make_unique<SafeNode>(10);
head->next = std::make_unique<SafeNode>(20);
// no destroy() needed. head goes out of scope, and the whole chain frees itself.
```

Each node owns the next one, so destroying the head cascades down the chain. No `delete`
anywhere. One caveat worth knowing: on a chain of a hundred thousand nodes this cascade is
recursive and can overflow the stack, which is a real and slightly notorious problem — for very
long lists you unlink iteratively before letting it go.

### The complete program

```cpp
// nodes.cpp — a linked list by hand, and the pointer rules that keep it alive.
//   g++ -std=c++20 -g -fsanitize=address -Wall -Wextra -o nodes nodes.cpp && ./nodes

#include <bits/stdc++.h>
using namespace std;

struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};

void print(Node* head) {
    for (Node* cur = head; cur != nullptr; cur = cur->next)
        cout << cur->value << " -> ";
    cout << "null\n";
}

Node* push_front(Node* head, int value) {
    Node* fresh = new Node(value);
    fresh->next = head;        // link BEFORE moving head, or the tail is lost
    return fresh;
}

Node* reverse(Node* head) {
    Node* prev = nullptr;
    Node* cur = head;
    while (cur != nullptr) {
        Node* nxt = cur->next; // save before overwriting
        cur->next = prev;
        prev = cur;
        cur = nxt;
    }
    return prev;
}

// Floyd's cycle detection — day 083. Two markers, one twice as fast.
bool has_cycle(Node* head) {
    Node* slow = head;
    Node* fast = head;
    while (fast != nullptr && fast->next != nullptr) {
        slow = slow->next;
        fast = fast->next->next;
        if (slow == fast) return true;      // comparing ADDRESSES, not values
    }
    return false;
}

void destroy(Node* head) {
    while (head != nullptr) {
        Node* nxt = head->next;
        delete head;
        head = nxt;
    }
}

int main() {
    ios::sync_with_stdio(false);

    // ---- what a pointer holds ----
    int x = 42;
    int* p = &x;
    cout << "x  = " << x  << "\n";
    cout << "*p = " << *p << "   (follow the address)\n";
    *p = 99;
    cout << "x  = " << x  << "   (changed through the pointer)\n\n";

    // ---- build a chain ----
    Node* head = new Node(30);
    head = push_front(head, 20);
    head = push_front(head, 10);
    cout << "built:    "; print(head);

    head = reverse(head);
    cout << "reversed: "; print(head);

    cout << "has cycle: " << (has_cycle(head) ? "yes" : "no") << "\n";

    // ---- dot versus arrow ----
    Node stack_node(7);                 // on the stack, no new, no delete
    cout << "stack_node.value = " << stack_node.value << "   (dot: I have the thing)\n";
    cout << "head->value      = " << head->value      << "   (arrow: I have its address)\n";

    destroy(head);                      // every new needs exactly one delete
    head = nullptr;                     // so a later use crashes instead of lying

    // ---- the same chain, owning itself ----
    struct SafeNode {
        int value;
        unique_ptr<SafeNode> next;
        SafeNode(int v) : value(v), next(nullptr) {}
    };
    auto owned = make_unique<SafeNode>(1);
    owned->next = make_unique<SafeNode>(2);
    cout << "unique_ptr chain: " << owned->value << " -> " << owned->next->value
         << " -> null   (freed automatically)\n";

    return 0;
}
```

Expected output:

```
x  = 42
*p = 42   (follow the address)
x  = 99   (changed through the pointer)

built:    10 -> 20 -> 30 -> null
reversed: 30 -> 20 -> 10 -> null
has cycle: no
stack_node.value = 7   (dot: I have the thing)
head->value      = 30   (arrow: I have its address)
unique_ptr chain: 1 -> 2 -> null   (freed automatically)
```

Compile it with `-fsanitize=address` as the comment says. If you have got the memory right it
prints nothing extra. Remove the `destroy(head)` line and it will tell you exactly what you
leaked.

---

## 6. What it costs

### Space

```
  a pointer                     8 bytes   (on any 64-bit machine)

  struct Node { int value; Node* next; }
    int      4 bytes
    padding  4 bytes    <- the pointer must sit on an 8-byte boundary
    pointer  8 bytes
    -------------------
    total   16 bytes    for 4 bytes of actual data
```

**Four times overhead**, and that is before the allocator's own bookkeeping, which is typically
another 8 to 16 bytes per `new`. So a linked list of 10^6 integers:

```
  linked list:  10^6 x (16 + ~16 allocator overhead)  =  ~32 MB
  vector<int>:  10^6 x 4                              =    4 MB
```

**Eight times the memory for the same data.** Worth saying in an interview, because most people
only talk about time.

### Time, and the number that actually decides it

The complexity table says both are O(n) to walk. The measured reality does not agree:

```
  summing 10^6 values

  vector<int>            ~0.4 ms
  linked list            ~8.0 ms         about 20x slower
```

Same operation count. The difference is entirely memory layout:

```
  vector:  elements are adjacent.  One cache line (64 bytes) holds 16 ints.
           the processor also PREFETCHES the next line, so it is already there.
           cost per element: about 0.4 nanoseconds.

  list:    each node was allocated separately and could be anywhere.
           every "cur = cur->next" is likely a cache miss: ~100 nanoseconds
           of waiting, and the prefetcher cannot help because it cannot know
           the next address until it has loaded the current node.
           cost per element: dominated by that miss.
```

That last clause is the deep reason. In a vector, the address of element `i+1` is arithmetic — the
hardware can fetch it in advance. In a list, the address of the next node **is stored in the
current node**, so nothing can be fetched until the current one has arrived. It is inherently
serial.

**This is why real code uses a `vector` almost always**, and why "insertion is O(1)" is a much
weaker argument than it looks: you still had to walk to the insertion point, and the walking is
what costs.

### Allocation

```
  new Node(x)     ~50-100 ns    a heap allocation
  v.push_back(x)  ~2 ns         amortised, into memory already owned

  building a 10^6 list:    10^6 x ~80 ns  =  ~80 ms
  building a 10^6 vector:  10^6 x  ~2 ns  =   ~2 ms
```

Forty times, and that is before you have read a single value.

---

## 7. The traps

### The real error: following `nullptr`

```cpp
Node* p = nullptr;
std::cout << p->value;
```

```
Segmentation fault (core dumped)
```

That is all you get from a plain build, with no line number and no clue. Compile with the address
sanitiser and it tells you where:

```
AddressSanitizer:DEADLYSIGNAL
=================================================================
==23315==ERROR: AddressSanitizer: SEGV on unknown address 0x0000000000000000 (pc 0x00000040123f)
==23315==The signal is caused by a READ memory access.
==23315==Hint: address points to the zero page.
    #0 0x40123e in main nodes.cpp:14
```

`Hint: address points to the zero page` is the sanitiser saying "you followed a null pointer".
That phrase is worth recognising; it is the most common crash in C++.

**Every `p->` needs to be reachable only when `p` is not null.** In a loop, the condition does it.
In a function, check at the top and return early.

### The real error: the leak

Forget one `delete`:

```cpp
Node* p = new Node(5);
// ... and never delete it
```

Nothing happens. The program runs correctly and exits cleanly. Then:

```
=================================================================
==24118==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 16 byte(s) in 1 object(s) allocated from:
    #0 0x7f2c1e2b1357 in operator new(unsigned long)
    #1 0x401286 in main nodes.cpp:9

SUMMARY: AddressSanitizer: 16 byte(s) leaked in 1 allocation(s).
```

It names the line that allocated the memory nobody freed. In a contest a leak is harmless — the
program exits and the operating system reclaims everything. In a service that runs for a month it
is the reason the machine falls over on a Sunday.

### The real error: deleting twice

```cpp
delete p;
delete p;
```

```
free(): double free detected in tcache 2
Aborted (core dumped)
```

The allocator keeps its bookkeeping in the freed memory itself, so freeing twice corrupts it. The
crash often happens later, in an unrelated allocation, which makes it miserable to track down.

`delete p; p = nullptr;` prevents it entirely, because `delete nullptr` is defined to do nothing.

### The one that lies to you: use after free

```cpp
Node* p = new Node(5);
delete p;
std::cout << p->value;      // often prints 5
```

No crash. The right answer. The bug ships. This is the Kambles' number, and it is why C++ has the
reputation it has.

```
==25011==ERROR: AddressSanitizer: heap-use-after-free on address 0x602000000010
READ of size 4 at 0x602000000010 thread T0
    #0 0x4013c7 in main nodes.cpp:12

0x602000000010 is located 0 bytes inside of 16-byte region [0x602000000010,0x602000000020)
freed by thread T0 here:
    #0 0x7f4a1b2b16c8 in operator delete(void*)
    #1 0x4013b2 in main nodes.cpp:11
previously allocated by thread T0 here:
    #1 0x401396 in main nodes.cpp:10
```

Read that output: it gives you the line that read it, the line that freed it, and the line that
allocated it. Three line numbers, and the bug is solved. **This is why you compile locally with
`-fsanitize=address`.** It is the difference between an hour and a minute.

### The near-miss: losing the tail

```cpp
Node* push_front(Node* head, int value) {
    Node* fresh = new Node(value);
    head = fresh;               // WRONG ORDER
    fresh->next = head;         // fresh now points at ITSELF
    return fresh;
}
```

`fresh->next = fresh` makes a one-element loop, and everything that was in the chain is now
unreachable — leaked, and gone. Printing it never terminates.

**Link the new node in before you move the head.** More generally: in any pointer manipulation,
save the address you are about to overwrite, *first*.

### The near-miss: dot instead of arrow

```cpp
Node* p = new Node(5);
std::cout << p.value;
```

```
main.cpp:9:20: error: request for member 'value' in 'p', which is of non-class type 'Node*'
    9 |     std::cout << p.value;
      |                    ^~~~~
```

`which is of non-class type 'Node*'` means "this is an address, not an object". Caught at compile
time, so it cannot ship. **Dot when you have the thing, arrow when you have its address.**

---

## 8. In the interview

### How it gets asked

- *"What's the difference between a pointer and a reference?"* — the direct version, and one of
  the two most-asked C++ questions there are.
- *"What is a dangling pointer? How would you get one?"* — the follow-up, and the one where a
  concrete example beats a definition.
- *"Reverse a linked list."* — where they watch whether you save `next` before overwriting it.
- *"Who owns this memory?"* — asked in design rounds, where the expected answer names
  `unique_ptr`.

### What to say out loud, in the first ninety seconds

1. **Say what a pointer is.** *"A pointer is a variable holding a memory address. It can be null,
   it can be reassigned, and I dereference it with `*` or `->` to reach the object."*
2. **Say what a reference is.** *"A reference is an alias — another name for an existing object.
   It must be bound when it is created, it can never be re-seated, and it cannot be null."*
3. **Give the decision rule.** *"So I use a reference by default, and a pointer when I need
   something only a pointer offers — most often when 'nothing' is a legitimate value."*
4. **Give the concrete case.** *"A linked list is the obvious example: `next == nullptr` is how I
   say 'end of the list', and a reference cannot express that."*
5. **Name the danger.** *"The cost of pointers is lifetime. A pointer can outlive what it points
   at — `delete` does not change the pointer, so it still holds the same address into memory that
   is no longer mine. Reading it usually still gives the old value, which is what makes it
   dangerous rather than merely broken."*
6. **Name the modern answer.** *"In production I would not manage that by hand — `unique_ptr` for
   single ownership, `shared_ptr` where ownership is genuinely shared. Raw pointers I keep for
   non-owning observation, where somebody else is responsible for the lifetime."*

Step 6 is what moves this from a syntax answer to an engineering answer.

### The follow-ups

**"What is a dangling pointer, concretely?"**
A pointer holding an address whose object no longer exists. Three ways I get one. `delete p` and
then use `p` — `delete` frees the memory but leaves the pointer's value alone. Returning a pointer
or reference to a local variable, since the stack frame is gone at return; g++ catches that one
with `-Wreturn-local-addr`. And keeping a pointer to a vector element across a `push_back`, which
can reallocate the buffer and free the old one. The reason it is so nasty is that reading freed
memory usually still gives the old value, because nothing has reused it yet — so it passes testing
and fails in production. `-fsanitize=address` catches all three at run time and prints the line
that allocated, the line that freed, and the line that read.

**"What's the difference between `new`/`delete` and `malloc`/`free`?"**
`new` allocates *and* runs the constructor; `delete` runs the destructor *and* frees. `malloc` and
`free` only move memory around — they know nothing about types, so an object allocated with
`malloc` is never properly constructed. `new` also returns the right type without a cast and
throws `std::bad_alloc` on failure rather than returning null. They cannot be mixed: freeing a
`new`'d pointer with `free` is undefined behaviour, as is `delete` on `malloc`'d memory. And there
is a third pair — `new[]` and `delete[]` — where using the wrong one is also undefined behaviour,
which is one more reason to prefer `vector` and `unique_ptr` over arrays and raw `new`.

**"When would you use `shared_ptr` over `unique_ptr`?"**
Only when ownership is genuinely shared — several independent owners, and the object should live
until the last of them is done. A cache handing out entries, or a graph where several structures
legitimately keep the same node alive. It is not free: it carries a reference count that is
updated atomically, so copying one is meaningfully more expensive than copying a raw pointer, and
the control block is a second allocation unless you use `make_shared`. The bigger problem is that
two `shared_ptr`s pointing at each other form a cycle whose count never reaches zero, so neither is
ever freed — that is what `weak_ptr` exists to break. My default is `unique_ptr`, and I move it
when ownership transfers.

**"Why is walking a linked list so much slower than a vector, when both are O(n)?"**
Cache behaviour. A vector's elements are adjacent, so one 64-byte cache line brings in sixteen
integers, and the hardware prefetcher can see the pattern and fetch the next line before it is
asked. A linked list's nodes were allocated separately and can be anywhere in memory, so each step
is likely a cache miss at around a hundred nanoseconds. Worse, it is inherently serial: the
address of the next node is stored *inside* the current one, so nothing can be prefetched until
the current node has actually arrived. In practice that is a ten-to-twenty-times difference on a
simple traversal, and it is why "O(1) insertion" is a weaker argument than it looks — you still had
to walk to the insertion point.

### A model answer

> "A pointer is a variable that holds a memory address. It is an ordinary value — eight bytes on a
> 64-bit machine — so I can copy it, reassign it, compare it, set it to `nullptr`, and do
> arithmetic on it to walk an array. To reach the object I dereference it, with `*p` or `p->member`.
>
> A reference is an alias: a second name for an object that already exists. It must be bound at the
> point it is created, it can never be re-seated to name something else, and there is no such thing
> as a null reference. I use it as if it were the object itself — no stars, no arrows.
>
> My rule is to prefer references, because they cannot be null and cannot be dangling in the ways
> pointers can, and I reach for a pointer when I need one of the three things only a pointer does:
> represent 'nothing', be reassigned, or point into an array. A linked list is the clean example —
> `next == nullptr` is how the list says it has ended, and a reference simply cannot say that. So
> every list, tree and graph in C++ is built from pointers.
>
> The cost of pointers is lifetime, and that is the real content of the question. A pointer can
> outlive what it points at. `delete p` returns the memory but does not touch `p`, so `p` still
> holds the same address into memory that is no longer mine. And the reason that is dangerous
> rather than merely broken is that reading it usually still gives the old value — the memory has
> not been reused yet — so the bug passes my tests and fails in production, on a different machine,
> weeks later. I always write `delete p; p = nullptr;` so a later use crashes immediately instead
> of lying to me, and I compile locally with `-fsanitize=address`, which reports the line that
> allocated it, the line that freed it, and the line that read it.
>
> In anything that ships I would not be doing this by hand. `unique_ptr` for single ownership,
> which frees automatically when it goes out of scope and cannot be copied, so there is never a
> question of who is responsible. `shared_ptr` only where ownership is really shared, knowing it
> costs an atomic reference count and needs `weak_ptr` to break cycles. Raw pointers I keep for
> non-owning observation, where something else owns the object and I am only looking at it.
>
> For a linked-list interview problem, though, I would use raw pointers, because that is what the
> problem hands me."

That answer defines both, gives a decision rule, gives the concrete case, identifies lifetime as
the real issue, gives the reason the bug is subtle, names the tooling, gives the modern practice,
and then says when the old practice is still right.

---

## 9. Recall card

1. **A pointer holds an address. `&x` is "address of x", `*p` is "the thing at p", `p->m` is
   `(*p).m`.** Dot when you have the thing, arrow when you have its address.
2. **Pointer versus reference: a pointer can be null, reassigned, and walked. A reference can do
   none of those and is bound for life.** Prefer references; use a pointer when "nothing" is a
   legitimate value.
3. **Every `new` needs exactly one `delete`.** Zero is a leak, two is a double free. Write
   `delete p; p = nullptr;` so a later use crashes instead of quietly reading somebody else's data.
4. **In pointer surgery, save the address you are about to overwrite, first.** `Node* nxt =
   cur->next;` before `cur->next = prev;`. Every list bug is a version of forgetting this.
5. **Walking a list is 10-20× slower than a vector despite both being O(n)**, because every step is
   a cache miss the hardware cannot predict. A list node is 16 bytes plus allocator overhead for
   4 bytes of data.

---

**Next in C++:** [day 125 — graphs and recursion in
C++](../day-125-what-a-graph-is/04-cpp-graphs-and-recursion.md).
