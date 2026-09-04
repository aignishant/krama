---
day: 3
track: cpp
title: "Input, output, and the competitive template"
phase: "C++ and competitive programming"
status: written
---

# Day 003 · C++ — Input, output, and the competitive template

**After today you can:** You can read any judge's input format fast enough, and say what every line of your template actually does.

**The interviewer asks it as:** *Your algorithm is optimal and it still times out. What do you check?*

---

> Third of the twelve C++ days. Today's DSA lesson gives you Big-O. This gives you the table that
> turns a Big-O into a yes-or-no answer about whether your solution will pass, and the template
> you start every contest problem from.

---

## 1. What this is, and why they ask it

Reading input is not free. A problem that gives you 10^6 numbers is handing you a file of about
seven megabytes, and how you read those seven megabytes can be the difference between 0.05
seconds and 0.8 seconds. On a two-second limit with heavy work to do, that is the whole margin.

C++ gives you two separate input systems that both work and do not cost the same. `cin` and
`cout` are the C++ ones, safe and readable. `scanf` and `printf` are the C ones, inherited,
faster by default, and easy to get wrong. And by default, C++ keeps the two in step with each
other on every single character, which costs you a large fraction of your reading time in
exchange for a guarantee you are not using.

Two lines turn that guarantee off. Every competitive C++ solution you will ever read starts with
them, and most people who type them cannot say what they do. You will be able to.

This matters in interviews less as a question and more as a diagnosis: when your correct
solution times out and you can say "that is not the method, that is the reading, and here is the
fix", you have demonstrated something a memorised Big-O table cannot.

---

## 2. The story

Ganesh delivers milk to the Sai Krupa building in Kothrud, four floors, no lift. He starts at
half past five in the morning and he is done by seven, and by his own account the job is mostly
stairs.

For the first month he did it the obvious way. Take a packet from the crate in the tempo, carry
it up, hand it over or leave it at the door, come down, take the next one. Fifty-two flats. He
worked out once that this was somewhere over a hundred and eighty flights of stairs before
breakfast, and it took him until twenty past seven, and by Thursday his knees were telling him
about it.

The man who had the round before him came by one morning and watched for about four minutes
before saying anything. Then he pointed at the crate and asked why Ganesh was not taking the
whole thing up.

So Ganesh started loading the crate — sixteen packets, everything for one floor and a bit —
carrying it up once, walking the corridor, and coming down empty. Four trips instead of
fifty-two. He was finishing by ten past six.

The second thing took longer to notice. The society had an app, and Ganesh was supposed to tap
each delivery into it as he made it. Fine. But the secretary had also asked him, back in March,
to send her a message after every flat, because in March the app had been new and she had not
trusted it. So for every packet he was tapping the app and then typing a message. Two entries,
every single time, one of them for a woman who had stopped opening those messages in April.

He mentioned it to her in September, a bit carefully, and she was surprised he was still doing
it. She had forgotten she had ever asked.

He stopped that morning. It took thirty-five minutes off the round on its own — more than the
crate had.

Two changes, neither of them clever. Carry a lot at once instead of one at a time. And stop
keeping two things in step when only one of them is being read.

---

## 3. The idea in plain English

Both halves of Ganesh's morning have exact names in C++.

### A stream is a sequence of characters going past

`std::cin` is the **standard input stream** — everything typed at the keyboard or fed in from a
file. `std::cout` is the **standard output stream** — your terminal. A **stream** is a sequence
of characters with a current position in it, and reading moves the position forward.

You have already used `std::cout << x`. Input is the mirror image:

```cpp
int n;
std::cin >> n;
```

Read `>>` as "take from the stream into". The arrows point the way the data travels.

### `>>` skips whitespace and stops at whitespace

This one rule explains almost everything about `>>`.

When you do `cin >> n`, it first skips over any spaces, tabs and newlines sitting in front of
the position. Then it reads characters as long as they could be part of a number, and stops at
the first one that could not — usually a space or a newline. It leaves that character in the
stream.

So this input:

```
3 14 15
92
```

is read identically by `cin >> a >> b >> c >> d` whether the numbers are separated by single
spaces, five spaces, tabs or newlines. **The layout of the input file does not matter.** This is
why a problem saying "the next line contains n integers" needs no special handling: you read n
integers in a loop.

### `getline` reads a whole line, spaces included

When the input contains text with spaces in it, `>>` is wrong, because it stops at the first
space and gives you one word.

```cpp
std::string line;
std::getline(std::cin, line);
```

`getline` reads everything up to and including the next newline, gives you everything except the
newline, and consumes the newline.

**The trap that follows from these two rules together** is in section 7, and it is the single
most common beginner input bug in C++. It exists because `>>` leaves the newline behind and
`getline` does not skip it.

### The buffer is the crate

Writing a character to the terminal is a **system call** — a request to the operating system —
and a system call is expensive, in the region of a microsecond. Doing one per character for a
million characters is a second of pure overhead.

So the stream keeps a **buffer**: a block of memory, typically a few kilobytes, where outgoing
characters pile up. When it fills, the whole block goes out in one system call. That is the
crate. `std::cout << x` puts a packet in the crate; it does not climb the stairs.

**Flushing** means "go now, whatever is in the crate". `std::endl` writes a newline **and
flushes**. `"\n"` writes a newline and does not. In a loop printing 10^5 lines, `endl` means
100,000 trips up the stairs where `"\n"` means a few dozen.

You do not have to flush at the end of your program: the streams flush themselves when the
program exits normally. The only times you need `endl` are interactive problems, where the judge
is waiting for your line before it sends the next input, and debugging a program that crashes,
where the last unflushed line is exactly the one you needed to see.

### `sync_with_stdio` is the duplicate messages

By default, C++ guarantees that `cin`/`cout` and C's `scanf`/`printf` can be mixed freely in one
program and everything comes out in the right order. To promise that, the C++ streams give up
their own buffering and route through C's, character by character.

You are not mixing them. Almost nobody is. You are paying for a guarantee you do not use, on
every character, exactly like typing a message to somebody who stopped reading in April.

```cpp
std::ios::sync_with_stdio(false);
```

Turn it off and `cin`/`cout` get their own real buffers back. **This is typically a two-to-six
times speedup on input-heavy problems**, and it is the single highest-value line in competitive
C++.

The price: after this line you must not mix `cin`/`cout` with `scanf`/`printf` in the same
program. Pick one. The interleaving becomes unpredictable.

### `cin.tie` is the second, smaller one

By default `cin` is **tied** to `cout`, meaning every read from `cin` flushes `cout` first. This
exists so that a prompt appears before the program waits for input — without it,
`cout << "Enter n: "; cin >> n;` could sit there with a blank screen.

An online judge is not a human. Nobody is looking at your prompt.

```cpp
std::cin.tie(nullptr);
```

That unties them, so reads stop forcing flushes. `nullptr` is C++'s "points at nothing" value;
[day 078's C++ lesson](../day-078-nodes-and-links/README.md) covers it properly.

**Do not use this in an interactive problem.** In those, the judge genuinely is waiting for your
output before it sends more input, and untying without flushing manually deadlocks you.

---

## 4. The picture

What `>>` actually does to the stream position:

```
  input:   "  42   hello\n7\n"

  start                 position
                        v
           _  _  4  2  _  _  _  h  e  l  l  o  \n  7  \n

  cin >> n;      skip whitespace, read digits, stop at the space
                                 position
                                 v
           _  _  4  2  _  _  _  h  e  l  l  o  \n  7  \n
                 \___/
                  n = 42                (the space is LEFT in the stream)

  cin >> s;      skip whitespace, read non-space, stop at '\n'
                                                    position
                                                    v
           _  _  4  2  _  _  _  h  e  l  l  o  \n  7  \n
                                 \___________/
                                  s = "hello"       (the '\n' is LEFT)
```

**What to notice:** every `>>` stops *before* the whitespace that ended it, and leaves it sitting
there. That leftover newline is the entire cause of the `getline` bug in section 7.

Now the buffer, drawn as the crate:

```
  WITHOUT a buffer (endl every line)

    cout << "a" -> [ SYSTEM CALL ] -> terminal      ~1 microsecond
    cout << "b" -> [ SYSTEM CALL ] -> terminal      ~1 microsecond
    cout << "c" -> [ SYSTEM CALL ] -> terminal      ~1 microsecond
                    100,000 lines = 100,000 system calls


  WITH a buffer ("\n", and sync_with_stdio(false))

    cout << "a" -> +-------------------+
    cout << "b" -> | a b c d e f g ... |   memory, essentially free
    cout << "c" -> +-------------------+
                            |
                       when full, or at exit
                            v
                    [ ONE SYSTEM CALL ] -> terminal
                    100,000 lines = ~30 system calls
```

**What to notice:** the work per character did not change. The number of trips did. This is the
crate, and it is also why `endl` inside a loop is a performance bug rather than a style
preference.

---

## 5. The code, built step by step

### The template

This is what you paste at the top of every contest file.

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) {
        // solve one test case
    }
    return 0;
}
```

That is the whole template. Resist the ones you will see online with forty lines of macros —
they save seconds and cost you the ability to read your own code at minute ninety of a contest.

`<bits/stdc++.h>` is a GCC-specific header that includes the entire standard library in one
line. It is not standard C++, it does not exist on MSVC or on macOS's default clang, and it adds
one to three seconds of compile time. It is also what every competitive programmer uses, because
in a contest you do not want to stop and think about which header `accumulate` lives in.
**Contest files: use it. Anything you would show an interviewer: include what you use.**

`while (t--)` reads as "while t is non-zero, then decrease it". It is idiomatic and you will see
it everywhere.

### Reading the shapes judges actually use

**"The first line contains n. The second line contains n integers."**

```cpp
int n;
cin >> n;
vector<int> a(n);
for (int i = 0; i < n; i++) cin >> a[i];
```

That is it. No line handling, because `>>` does not care about lines.

**Read until the input runs out**, when the problem does not tell you how many:

```cpp
int x;
while (cin >> x) {
    // ...
}
```

`cin >> x` returns the stream, and a stream used as a condition is `true` while it is in a good
state. When it hits the end of the file, or fails to parse, the state goes bad and the loop
ends. This also means malformed input silently ends your loop, which is worth knowing when a
solution mysteriously reads nothing.

**A grid of characters**, which comes up in every flood-fill problem:

```cpp
int rows, cols;
cin >> rows >> cols;
vector<string> grid(rows);
for (int i = 0; i < rows; i++) cin >> grid[i];
```

Read each row as a whole `string` with `>>`. Then `grid[i][j]` is the character at row `i`,
column `j`. Far better than reading `rows * cols` single characters.

**A line containing text with spaces:**

```cpp
int n;
cin >> n;
cin.ignore();                    // <- consume the leftover newline
string line;
getline(cin, line);
```

`cin.ignore()` discards one character — the newline that `>>` left behind. Without it, `getline`
returns an empty string. Section 7 shows exactly what that looks like.

### Printing doubles

The default is six *significant* digits, which will fail a problem asking for six *decimal*
places.

```cpp
double x = 1.0 / 3.0;
cout << x << "\n";                               // 0.333333
cout << fixed << setprecision(10) << x << "\n";  // 0.3333333333
```

`fixed` switches from significant digits to digits after the point. `setprecision(10)` sets how
many. Both are **sticky** — set once, and every `double` printed afterwards uses them. Set them
right after the two fast-I/O lines and forget them.

Geometry and probability problems say "answers within 10^-6 will be accepted". Print ten decimal
places and the tolerance is never your problem.

### The complete program

A realistic multi-test-case judge problem, read and answered end to end.

```cpp
// io.cpp — the input shapes an online judge actually gives you.
//   g++ -std=c++20 -O2 -Wall -Wextra -o io io.cpp && ./io < input.txt
//
// Input format:
//   t                       number of test cases
//   for each test case:
//     n                     how many numbers
//     a[0] a[1] ... a[n-1]  the numbers
//     name                  a line of text, with spaces
//
// Output, per test case: the sum, the largest, the average to 6 places, the name.

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout << fixed << setprecision(6);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> a(n);
        for (int i = 0; i < n; i++) cin >> a[i];

        // long long, because a sum of n ints can exceed 2e9 — see day 002's C++ lesson
        long long sum = 0;
        int best = INT_MIN;                  // the smallest int there is
        for (int x : a) {
            sum += x;
            best = max(best, x);
        }

        cin.ignore();                        // eat the newline left by >>
        string name;
        getline(cin, name);                  // now this reads the real line

        cout << "sum " << sum << "\n";
        cout << "max " << best << "\n";
        cout << "avg " << (double)sum / n << "\n";
        cout << "who " << name << "\n";
    }
    return 0;
}
```

Given this input:

```
2
5
3 1 4 1 5
Ganesh Kulkarni
3
1000000000 1000000000 1000000000
Sai Krupa building
```

it prints exactly:

```
sum 14
max 5
avg 2.800000
who Ganesh Kulkarni
sum 3000000000
max 1000000000
avg 1000000000.000000
who Sai Krupa building
```

Three things in that program are load-bearing. `long long sum` — the second case sums to 3 × 10^9
and would be wrong in an `int`. `(double)sum / n` — without the cast this divides whole numbers
and prints `2.000000`. And `cin.ignore()` — without it, `name` is empty both times.

### `scanf` and `printf`, since you will see them

```cpp
int n;
scanf("%d", &n);              // %d for int, %lld for long long
printf("%d\n", n);
printf("%.6f\n", 3.14159265); // 3.141593
```

They are fast by default, with no preamble needed. They are also unchecked: `scanf("%d", &x)`
where `x` is a `long long` compiles, runs, writes four bytes into an eight-byte variable, and
gives you rubbish. The `&` is required and forgetting it is undefined behaviour.

**Use `cin`/`cout` with the two lines.** It is safe, it is within a hair of `scanf` on speed, and
it is what an interviewer expects from someone writing C++ rather than C. Know `printf("%.6f")`
because it is the shortest way to print a `double`, and know that you must not mix the two
families after `sync_with_stdio(false)`.

---

## 6. What it costs

### The reading itself

Reading 10^6 integers — a seven-megabyte file — on a typical judge machine:

```
  method                                          time
  ---------------------------------------------   ------
  cin >> x,  sync_with_stdio ON  (the default)    ~0.55 s
  cin >> x,  sync_with_stdio OFF                  ~0.09 s
  scanf("%d", &x)                                 ~0.13 s
  a hand-rolled getchar reader                    ~0.02 s
```

Read the first two rows again. **Two lines of preamble bought roughly half a second**, on a
problem where the limit is likely two. That is a quarter of your entire budget, recovered for
free, before you have done any real work.

Output, printing 10^5 lines:

```
  cout << x << "\n"      ~0.01 s
  cout << x << endl      ~0.30 s        100,000 flushes
```

Thirty times, for one word. The arithmetic behind it:

```
  a system call costs roughly    1 microsecond = 10^-6 s

  100,000 flushes x 10^-6 s   =  0.1 s   of pure operating-system overhead

  with a 4 KB buffer and ~8 bytes per line:
  100,000 lines x 8 bytes     =  800 KB
  800 KB / 4 KB per flush     =  200 system calls
  200 x 10^-6 s               =  0.0002 s
```

Five hundred times fewer trips up the stairs. That is the crate, with a number on it.

### The table that turns today's Big-O into a verdict

This is the reason this lesson sits on the Big-O day. You now have the working figure — **C++
does about 10^8 simple operations per second** — so a constraint tells you which complexity you
are allowed to aim for. Read the largest n in the problem, find the row, and you know what to
look for before writing a line.

| Largest n | What fits in ~1 second | The shape you are looking for |
|---:|---|---|
| 10-12 | O(n!) | try every ordering |
| ~20 | O(2^n) or O(2^n × n) | try every subset; bitmask over subsets |
| ~100 | O(n^4) | four nested loops, or DP over pairs of pairs |
| ~500 | O(n^3) | Floyd-Warshall, matrix work, interval DP |
| 5,000 | O(n^2) | every pair, DP over two positions |
| 10^5 | O(n log n) | sort, binary search, heap, a balanced structure |
| 10^6 | O(n log n), tight | sort still fine, but watch the constant factor |
| 10^7 | O(n) | one pass, hashing, counting, two pointers |
| 10^9 | O(log n) or O(sqrt n) | binary search on the answer, maths, formula |

The arithmetic behind two of the rows, so you can rebuild the table rather than memorise it:

```
  n = 10^5, O(n^2)  =  10^10 operations  /  10^8 per second  =  100 seconds   -> no
  n = 10^5, O(n log n) = 10^5 x 17       =  1.7 x 10^6       =  0.017 s       -> yes

  n = 20,   O(2^n)  =  1,048,576         =  ~0.01 s                           -> yes
  n = 40,   O(2^n)  =  1.1 x 10^12                           =  3 hours       -> no
```

**Use it in reverse and it is worth more.** If n is 10^5 you are not looking for a clever
quadratic; you are looking for a sort, a binary search, or a hash map. The constraint has told
you the shape of the answer before you understood the problem. This is the single most useful
habit in competitive programming, and it comes straight out of today's DSA lesson.

---

## 7. The traps

### The near-miss: mixing `>>` and `getline`

The most common input bug in beginner C++, and it produces no error at all.

```cpp
int n;
string name;
cin >> n;
getline(cin, name);
cout << "n = [" << n << "] name = [" << name << "]\n";
```

Input:

```
5
Ganesh Kulkarni
```

Output:

```
n = [5] name = []
```

The name is empty. Nothing crashed, nothing warned, and the program carried on.

Why: `cin >> n` reads the `5` and **stops at the newline, leaving it in the stream**. Then
`getline` reads from the current position to the next newline — and the very next character *is*
a newline. So it correctly returns the empty string between the `5` and the end of that line,
and consumes the newline. The actual name is still sitting there unread.

Three fixes:

```cpp
cin.ignore();                                          // discard one character
cin.ignore(numeric_limits<streamsize>::max(), '\n');   // discard to end of line, robust
cin >> ws;                                             // skip all whitespace before getline
```

The first is what everybody writes and it is fine when exactly one newline is pending. The second
is correct even with trailing spaces after the number. `>> ws` is tidiest, but it skips *all*
whitespace including blank lines, so it is wrong if an empty line is meaningful data.

**The habit that avoids it entirely:** in a program that needs `getline` at all, read everything
with `getline` and pull the numbers out of the strings with `stringstream`. Do not alternate.

### The near-miss: `endl` in a loop

```cpp
for (int i = 0; i < 100000; i++)
    cout << answer[i] << endl;      // 0.30 s
```

versus

```cpp
for (int i = 0; i < 100000; i++)
    cout << answer[i] << "\n";      // 0.01 s
```

Same output, byte for byte. Three tenths of a second of difference, spent flushing a buffer that
nobody was waiting to read. On a problem with a 1-second limit, this alone is the verdict.

### The real error: forgetting `&` in `scanf`

```cpp
int n;
scanf("%d", n);      // missing the &
```

g++ catches this one, because it understands the format strings:

```
main.cpp:6:19: warning: format '%d' expects argument of type 'int *', but argument 2 has type 'int' [-Wformat=]
    6 |     scanf("%d", n);
      |            ~^   ~
      |             |   |
      |             |   int
      |             int *
```

It is a **warning**, not an error. The program compiles. It then treats whatever number `n`
happened to contain as a memory address and writes four bytes there, which is undefined behaviour
and usually:

```
Segmentation fault (core dumped)
```

That is the whole argument for `cin >> n` in one example: it cannot be written wrongly this way,
because the type is known when you compile. And it is the whole argument for `-Wall`: the
compiler saw it and told you.

### The real error: mixing the two families after unsyncing

```cpp
ios::sync_with_stdio(false);
cout << "first ";
printf("second ");
cout << "third\n";
```

Prints, on one run:

```
second first third
```

No error, no warning, no crash. The two systems now have separate buffers that flush at different
times, so the order of your output is whatever the buffers happened to do. On a judge this is a
wrong answer that reproduces differently on your machine. **After `sync_with_stdio(false)`, pick
one family and stay in it.**

### The quiet one: default precision

```cpp
double answer = 123456.789;
cout << answer << "\n";        // 123457
```

Not `123456.789`. The default is six *significant* digits, so a six-digit whole part uses all of
them and the fraction is gone — and it rounded. A geometry problem wanting `123456.789000` gets
`123457` and is marked wrong, and the method was correct.

`cout << fixed << setprecision(10);` once, at the top, next to the two fast-I/O lines.

---

## 8. In the interview

### How it gets asked

- *"Your solution is O(n log n) and it's still timing out. What do you look at?"* — the real
  version, and it is a debugging question, not an I/O question.
- *"What does `sync_with_stdio(false)` do?"* — asked when the interviewer sees it in your
  template and wants to know whether you typed it or understood it.
- *"What's the difference between `endl` and `\n`?"* — small, common, and answered badly by most
  people.
- *"The constraint says n up to 10^5. What does that tell you?"* — the table from section 6, and
  a very common opening move.

### What to say out loud, in the first ninety seconds

1. **Separate the work from the reading.** *"First I'd check whether the time is in my method or
   in reading the input, because with 10^6 numbers those are comparable costs."*
2. **Name the default.** *"By default C++ streams are synchronised with C's `stdio`, so `cin` and
   `scanf` can be mixed. That forces character-by-character routing and gives up the stream's own
   buffering."*
3. **Name the fix and the number.** *"`ios::sync_with_stdio(false)` turns that off. On 10^6
   integers it takes reading from about half a second to under a tenth."*
4. **Add the second line.** *"`cin.tie(nullptr)` unties `cin` from `cout`, so reads stop flushing
   output. That guarantee exists for interactive prompts, and a judge is not a human."*
5. **Name the cost.** *"The price is that I must not mix `cin`/`cout` with `printf`/`scanf` after
   that — the buffers flush independently and the order becomes unpredictable. And I would not
   untie in an interactive problem."*
6. **Add `endl`.** *"Separately, `endl` flushes and `\n` does not. In a loop printing 10^5 lines
   that is 100,000 system calls — about three tenths of a second for nothing."*

Step 5 is the one that matters. Anybody can recite the two lines. Naming what you gave up to get
them is the answer of somebody who understands the trade rather than the incantation.

### The follow-ups

**"What actually is a buffer, and why does it help?"**
A block of memory the stream accumulates characters in before handing them to the operating
system. It helps because the expensive part is not moving the bytes, it is the system call — the
switch into the kernel — which costs on the order of a microsecond whether you are writing one
byte or four thousand. Buffering spreads that fixed cost over many characters. It is the same
idea as batching writes to a database or grouping network packets, and
[day 010's latency table](../day-010-traversal-patterns/README.md) is where those numbers live.

**"When would `endl` be correct?"**
Interactive problems, where the judge reads your line and only then sends the next input — if you
do not flush, both sides wait forever and you get an idleness verdict. Debugging a program that
crashes, because output sitting in an unflushed buffer when the process dies is lost, and it is
usually the line you needed. And logging in a long-running service, where you want the line on
disk before the thing you are about to do possibly kills the process. Everywhere else, `"\n"`.

**"Is `scanf` still faster than an unsynced `cin`?"**
Marginally, and not reliably. Unsynced `cin` is within about thirty per cent of `scanf` on modern
libstdc++, and on some workloads it wins, because `scanf` parses a format string while it runs
whereas `operator>>` is resolved when you compile. The gap is small enough that I choose on
safety: `cin >> x` cannot have a mismatch between a format string and a variable, and `scanf`
can, silently. If I genuinely need faster than either — 10^7 numbers on a tight limit — I would
write a `getchar_unlocked` reader, which is another five to ten times faster than both.

**"The constraint says n ≤ 10^5. What does that tell you?"**
That I am looking for something around n log n, and that a quadratic will not pass. The reasoning
is one multiplication: 10^5 squared is 10^10, and C++ does about 10^8 simple operations a second,
so that is a hundred seconds against a limit of one or two. Whereas n log n is 10^5 × 17, about
1.7 × 10^6, which is under a hundredth of a second. So before I understand the problem I already
know the answer is probably a sort, a binary search, a heap, or a hash map. The constraint is a
hint, and reading it first saves me from designing something that cannot pass.

### A model answer

The candidate's solution is correct and timing out. The interviewer asks what to check.

> "Before I touch the method, I want to know how much of the time is reading, because the
> constraints say up to 10^6 integers and that is not a negligible amount of input.
>
> The default is the thing to check. C++ streams are synchronised with C's `stdio` out of the
> box, so that `cin` and `printf` can be mixed safely in one program. To promise that, `cin`
> gives up its own buffering and goes through C's, effectively character by character. I am not
> mixing them, so I am paying for a guarantee I am not using.
>
> Two lines fix it: `ios::sync_with_stdio(false)` and `cin.tie(nullptr)`. The first restores the
> buffering; the second stops every read from flushing `cout`, which is only there so a prompt
> appears before the program blocks. On 10^6 integers that typically takes reading from around
> half a second to under a tenth — so on a two-second limit I have just recovered a fifth of my
> budget without changing a line of logic.
>
> I would look at the output loop too. If it prints 10^5 lines with `endl`, that is 100,000
> flushes and 100,000 system calls, roughly three tenths of a second. `"\n"` writes the same byte
> and lets the buffer do its job.
>
> The costs are worth stating. After unsyncing I cannot mix `cin` with `scanf` — the buffers
> flush independently and the output order becomes unpredictable, which is a wrong answer that
> will not reproduce on my machine. And I would not untie `cin` in an interactive problem,
> because there the flush is load-bearing.
>
> If it is still slow after that, then it is genuinely the method, and I would look for an
> allocation or a copy inside the hot loop before I assume the complexity is wrong."

That answer separates two possible causes, names the mechanism, gives a number, gives the fix,
states the cost, and says what it would check next. It is a debugging method, not a fact.

---

## 9. Recall card

1. **Two lines, first thing in `main`:** `ios::sync_with_stdio(false); cin.tie(nullptr);` Roughly
   a five-times speedup on input-heavy problems, for free.
2. **`\n` writes a newline. `endl` writes a newline and flushes.** In a 10^5-line loop that is
   0.01 s against 0.30 s. Use `endl` only for interactive problems and crash debugging.
3. **`>>` skips leading whitespace and leaves the trailing newline.** So `getline` straight after
   `>>` returns an empty string. Fix with `cin.ignore()` or `cin >> ws`.
4. **Read the constraint first, then pick the complexity.** n ≤ 20 → 2^n. n ≤ 5,000 → n^2.
   n ≤ 10^5 → n log n. n ≤ 10^7 → n. n ≤ 10^9 → log n or sqrt n.
5. **`cout << fixed << setprecision(10);` once, at the top.** The default is six *significant*
   digits, which silently turns 123456.789 into 123457.

---

**Next in C++:** [day 005 — vector, references, and the array you use for
everything](../day-005-python-lists-and-tuples/04-cpp-vector-references.md).
