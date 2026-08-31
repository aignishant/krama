---
day: 69
track: dsa
title: "Balanced brackets and the parsing family"
phase: "Stacks and queues"
status: written
---

# Day 069 · DSA — Balanced brackets and the parsing family

**After today you can:** You can validate nested structures and evaluate simple expressions with a stack.

**The interviewer asks it as:** *Check whether the brackets in this string are balanced.*

---

## 1. What this is, and why they ask it

Given a string of brackets — `()`, `[]`, `{}` — decide whether every opener has a matching closer of
the same type, in the right order. `"({[]})"` is balanced. `"([)]"` is not, even though the counts
are equal. The answer is a stack, and the whole idea fits in one sentence: **when you meet a closer,
the only thing it can legally close is whatever is on top of the stack.**

They ask it because it is the cheapest way to find out whether you can turn a rule into an invariant.
The problem is easy enough that nobody fails to write *something*, and there are exactly three ways
to be wrong — a mismatched pair, a closer with nothing open, and something still open at the end.
Candidates who name all three before writing code are doing a different thing from candidates who
discover them when a test fails.

The second reason is that this is the doorway to a family. Once you can say "the stack holds the
context I am inside and have not yet left", the same shape solves expression evaluation, nested
string decoding, calculators with parentheses, JSON and XML validity, and the compiler front end that
told you about your own unclosed brace. Interviewers know that the family is worth more than the
problem, so the follow-up is almost always a harder member of it.

---

## 2. The story

After the housewarming lunch, Kamala was putting the vessels away, which is a job she does not mind
because it is the one part of the day with nobody talking to her.

There are three sets in that kitchen and they all nest. The steel ones, five of them, largest to
smallest. The aluminium ones, four. And a plastic set of three that somebody gave them and nobody
likes but which is useful for the fridge.

The way they go away is that the small one goes inside the next one up, which goes inside the next
one up, and so on, and each one gets its own lid on before the next one goes over it. So opening the
whole thing back up happens in the exact reverse order — the outermost lid first, then the vessel
under it, then that one's lid, all the way down.

Two rules, and Kamala has never once said them out loud because they are obvious to her.

The first is that a lid belongs to its own vessel. The steel lids and the aluminium lids are close
enough in size that a distracted person will put a steel lid on an aluminium vessel, and it will sit
there, and it will look fine, and three weeks later somebody will pick it up by the lid and the
vessel will come off and land on the floor. It fits. It is not the right one.

The second is that you cannot put a lid on nothing. This sounds too obvious to state, and yet on the
day of the lunch her sister-in-law was helping and there was a moment where she had a lid in her hand
and nothing in front of her to put it on, because the vessel it belonged to had already gone into the
cupboard under three others.

And the third thing, which is not a rule so much as the end of the job: when everything is put away,
there should be nothing left on the counter. If there is a vessel still sitting there with no lid on
it, the job is not finished, however tidy the rest of it looks.

That evening there was one — the second-smallest steel one, still open, next to the sink. Everything
else was away and stacked and looked completely correct, and the job was still wrong.

---

## 3. The idea in plain English

Each vessel being opened is an **opening bracket**. Each lid going on is a **closing bracket**. The
nesting is the nesting, and the pile on the counter is the **stack**.

Kamala's two rules and her end-of-job check are exactly the three ways the algorithm can fail.

| Kamala | In the string | The check |
|---|---|---|
| Steel lid on an aluminium vessel | `"([)]"` | the closer does not match the top of the stack |
| A lid with nothing to put it on | `"())"` | a closer arrives and the stack is empty |
| A vessel still open at the end | `"(()"` | the stack is not empty when the string ends |

**Say all three out loud before writing.** That is the whole difference between a good answer and an
adequate one.

### Why counting does not work

The tempting shortcut is to count openers and closers and check they match. It works for one type of
bracket and it is wrong the moment there are two.

```
 "([)]"    one '(' , one ')' , one '[' , one ']'    counts all match
                                                    and it is NOT balanced
```

Counting throws away order, and order is the entire question. Say this out loud when you reject the
counting approach — it shows you considered it rather than never thought of it.

For **one** bracket type, counting does work, and it is worth knowing because it gives an O(1)-space
answer:

```python
depth = 0
for ch in text:
    depth += 1 if ch == "(" else -1
    if depth < 0:
        return False        # a closer with nothing open
return depth == 0
```

If the interviewer says "only round brackets, O(1) space", this is the answer.

### The algorithm

```python
pairs = {")": "(", "]": "[", "}": "{"}    # closer -> its opener
stack: list[str] = []

for character in text:
    if character in pairs.values():        # an opener
        stack.append(character)
    else:                                  # a closer
        if not stack or stack.pop() != pairs[character]:
            return False
return not stack
```

The invariant, and this is the sentence to say: **at every point, the stack holds exactly the openers
that have been seen and not yet closed, in the order they were opened.**

Two details that get asked about.

**Map closers to openers, not openers to closers.** When you meet `)` you already know what you have;
you need to know what it *should* have found. `pairs[")"]` gives `"("` directly. The other direction
needs a search.

**`if not stack or ...` — the emptiness check comes first.** Python's `or` short-circuits, so
`stack.pop()` never runs on an empty stack. Write it in that order and the third failure mode is
handled by the same line as the first.

### The generalisation: a stack of contexts

Now the part that makes this a family rather than a problem.

> **When you meet an opener, push the context you are leaving. When you meet a closer, pop it and
> combine.**

Brackets are the degenerate case where the "context" is just the bracket character. In real parsing
problems the context is more.

**Decode String** — `"3[a2[c]]"` becomes `"accaccacc"`. When you meet `[`, push the string built so
far *and* the repeat count, then start fresh. When you meet `]`, pop them and combine.

**Reverse Polish notation** — `["2","1","+","3","*"]` is 9. Push numbers; on an operator, pop two,
apply, push the result. No brackets at all, same stack.

**Basic Calculator** — `"1 + (2 - (3 + 4))"`. On `(`, push the running result and the sign; on `)`,
pop and combine.

All three are the same two lines with a richer thing being pushed. If you can say that sentence in an
interview, the follow-up stops being a new problem.

### The related question they will ask next

**Longest valid parentheses** — the longest balanced substring of `")()())"`, which is 4. The trick
is to push **indices** rather than characters, and to keep a sentinel at the bottom marking "the last
position that was invalid". The length of a valid run is then `current_index - stack[-1]`. It is the
standard hard follow-up and it is worth recognising even if you do not write it.

---

## 4. The picture

`"({[]})"` processed one character at a time. The stack grows as things open and shrinks as they
close.

```
 char:    (        {        [        ]        }        )
        +---+    +---+    +---+    +---+    +---+    +---+
        |   |    |   |    | [ |    |   |    |   |    |   |
        |   |    | { |    | { |    | { |    |   |    |   |
        | ( |    | ( |    | ( |    | ( |    | ( |    |   |
        +---+    +---+    +---+    +---+    +---+    +---+
        push     push     push     pop [    pop {    pop (
                                   matches  matches  matches

 end: stack empty  ->  balanced
```

What to notice: the stack is a picture of *how deep you currently are*. Its height at any moment is
the nesting depth, and the top is always the thing that must close next.

Now the three failures, drawn on their smallest inputs:

```
 (a) wrong type          "([)]"
       ( -> push (        stack: [ ( ]
       [ -> push [        stack: [ (, [ ]
       ) -> pop gives [   but ')' needs '('     -> MISMATCH

 (b) closer, nothing open   "())"
       ( -> push           stack: [ ( ]
       ) -> pop            stack: [ ]
       ) -> stack empty    -> NOTHING TO CLOSE

 (c) still open at the end  "(()"
       ( -> push           stack: [ ( ]
       ( -> push           stack: [ (, ( ]
       ) -> pop            stack: [ ( ]
       end of string, stack is NOT empty        -> UNCLOSED
```

Three failures, three checks, and they map one-to-one onto three lines of code. Nothing else can go
wrong.

---

## 5. The code, built step by step

### Step 1 — the map, in the right direction

```python
PAIRS = {")": "(", "]": "[", "}": "{"}
```

Keyed by the closer. When you are holding a `)` you want to ask "what should this have found?" and
get `(` in one lookup.

### Step 2 — the loop

```python
def is_balanced(text: str) -> bool:
    stack: list[str] = []
    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in PAIRS:
            if not stack or stack.pop() != PAIRS[character]:
                return False
    return not stack
```

Nine lines, and every one of the three failures is covered. `not stack` catches the empty case;
`stack.pop() != PAIRS[character]` catches the mismatch; `return not stack` catches the leftovers.

Note the `elif character in PAIRS` rather than a bare `else`. If the string can contain other
characters — letters, spaces, an entire program — anything that is neither an opener nor a closer
should be ignored, not treated as a closer. Ask whether the input is brackets only; if it is not,
this line is why you pass.

### Step 3 — the generalisation, on a harder problem

**Decode String.** `"3[a2[c]]"` becomes `"accaccacc"`. Repeat counts can be multi-digit, and nesting
can be arbitrary.

The context to push at a `[` is two things: the string built so far, and the number that will repeat
what comes next.

```python
def decode_string(text: str) -> str:
    stack: list[tuple[str, int]] = []
    current = ""
    number = 0
    ...
```

Digits accumulate, because `12[a]` is twelve, not one then two:

```python
    for character in text:
        if character.isdigit():
            number = number * 10 + int(character)
```

`number * 10 + digit` is the standard way to build a multi-digit integer as you read it. Writing
`number = int(character)` gives 2 for `"12"` and is the single most common bug in this problem.

On `[`, save the outer context and reset:

```python
        elif character == "[":
            stack.append((current, number))
            current, number = "", 0
```

On `]`, restore it and combine:

```python
        elif character == "]":
            previous, repeat = stack.pop()
            current = previous + current * repeat
```

Read that line carefully. `current` is what was built *inside* the brackets, so it gets repeated;
`previous` is what was built *outside*, so it goes in front, unrepeated. Getting these the wrong way
round produces plausible garbage.

And anything else is a literal character:

```python
        else:
            current += character
```

### The complete solution

```python
PAIRS = {")": "(", "]": "[", "}": "{"}
OPENERS = "([{"


def is_balanced(text: str) -> bool:
    """True if every bracket is closed by its own kind, in the right order.

    Invariant: the stack holds exactly the openers seen and not yet closed,
    in the order they were opened. Three ways to fail — wrong type on top,
    a closer with an empty stack, and leftovers at the end.
    """
    stack: list[str] = []
    for character in text:
        if character in OPENERS:
            stack.append(character)
        elif character in PAIRS:
            if not stack or stack.pop() != PAIRS[character]:
                return False
        # anything else is ignored — letters, spaces, digits
    return not stack


def is_balanced_one_type(text: str) -> bool:
    """One bracket type only: O(1) space, no stack needed."""
    depth = 0
    for character in text:
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
            if depth < 0:            # closed one that was never opened
                return False
    return depth == 0


def min_additions_to_balance(text: str) -> int:
    """Fewest brackets to add to make it valid. Same counter, two totals."""
    open_needed = 0        # unmatched ')' seen so far
    close_needed = 0       # unmatched '(' still open
    for character in text:
        if character == "(":
            close_needed += 1
        else:
            if close_needed:
                close_needed -= 1
            else:
                open_needed += 1
    return open_needed + close_needed


def decode_string(text: str) -> str:
    """'3[a2[c]]' -> 'accaccacc'.

    The stack holds the context being left: the string built outside these
    brackets, and the number of times the inside will repeat.
    """
    stack: list[tuple[str, int]] = []
    current = ""
    number = 0

    for character in text:
        if character.isdigit():
            number = number * 10 + int(character)   # multi-digit counts
        elif character == "[":
            stack.append((current, number))
            current, number = "", 0
        elif character == "]":
            previous, repeat = stack.pop()
            current = previous + current * repeat   # inside repeats, outside does not
        else:
            current += character

    return current


def evaluate_rpn(tokens: list[str]) -> int:
    """Reverse Polish notation: no brackets, same stack.
    ['2','1','+','3','*'] -> 9"""
    stack: list[int] = []
    for token in tokens:
        if token in {"+", "-", "*", "/"}:
            right = stack.pop()
            left = stack.pop()                       # order matters for - and /
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(int(left / right))      # truncate toward zero
        else:
            stack.append(int(token))
    return stack[0]


if __name__ == "__main__":
    print(is_balanced("({[]})"))            # True
    print(is_balanced("([)]"))              # False  — wrong type
    print(is_balanced("())"))               # False  — nothing to close
    print(is_balanced("(()"))               # False  — still open
    print(is_balanced(""))                  # True   — vacuously balanced
    print(is_balanced("if (x[0]) { go(); }"))  # True — other characters ignored
    print(is_balanced_one_type(")("))       # False
    print(min_additions_to_balance("())"))  # 1
    print(decode_string("3[a]2[bc]"))       # aaabcbc
    print(decode_string("3[a2[c]]"))        # accaccacc
    print(decode_string("2[abc]3[cd]ef"))   # abcabccdcdcdef
    print(evaluate_rpn(["2", "1", "+", "3", "*"]))  # 9
    print(evaluate_rpn(["4", "13", "5", "/", "+"]))  # 6
```

Run the empty string. `is_balanced("")` is `True`, because there is nothing unmatched — vacuously
balanced. Interviewers ask about it, and "true, because nothing is left open" is the answer.

---

## 6. What it costs

### `is_balanced`, counted

The loop runs once per character: `n` iterations. Inside, each iteration does at most one push or one
pop plus one dictionary lookup, all O(1).

```
 n iterations x constant work  ->  O(n) time
```

Space is the stack. In the worst case — `"((((((..."` — every character is an opener and nothing is
popped, so the stack holds `n` entries.

```
 worst case space:  O(n)      "(((((((("
 best case space:   O(1)      "()()()()"  — pushed and popped immediately
```

Say both. "O(n) in the worst case, when the input is entirely openers" is more precise than "O(n)"
and takes two extra seconds.

### The counting version, for one bracket type

```
 time:   O(n)
 space:  O(1)      one integer
```

That is the trade to offer when asked for constant space, and the reason it only works for one type
is that a single integer cannot remember *which* kind of bracket is open.

### `decode_string`, counted

Trickier, and worth being careful because the naive answer is wrong.

The loop runs `n` times over the input. But `current = previous + current * repeat` builds a string
whose length can be much larger than `n` — `"10[10[10[a]]]"` is 13 characters of input and a thousand
characters of output.

```
 time:   O(n + m) where m is the LENGTH OF THE OUTPUT
 space:  O(n + m)
```

The honest statement is: *linear in the size of the output, not the input.* An interviewer who asks
"what is the complexity" is often checking exactly this, because the input length is a misleading
measure for any problem that expands.

There is also a hidden cost in `current += character` inside a loop, which is the string-building trap
from [day 020](../day-020-building-strings/README.md). For interview inputs it is fine; for very
large outputs, accumulate into a list and `"".join` at the end.

### The stack argument, again

Same sentence as [day 068](../day-068-stacks/README.md): **each character is pushed at most once and
popped at most once**, so even with a `pop` inside the loop the total work is linear. It will keep
being the answer for the rest of this phase.

---

## 7. The traps

### Trap 1 — counting instead of matching

```python
return text.count("(") == text.count(")")     # WRONG
```

Returns `True` for `")("`, which is not balanced. And with multiple bracket types it returns `True`
for `"([)]"`. The counts are a necessary condition, never a sufficient one.

### Trap 2 — popping an empty stack

```python
if stack.pop() != PAIRS[character]:      # no emptiness check
```

```python
>>> is_balanced_buggy("]")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
IndexError: pop from empty list
```

A one-character input finds it. The fix is `if not stack or stack.pop() != ...`, relying on `or`
short-circuiting so `pop` is never reached on an empty stack.

### Trap 3 — forgetting the end-of-string check

```python
    for character in text:
        ...
    return True            # WRONG — should be `return not stack`
```

Returns `True` for `"((("`, because nothing ever mismatched. This is Kamala's vessel by the sink:
every individual step was correct and the job is not done. It is the most common wrong answer to this
problem.

### Trap 4 — mapping openers to closers

```python
PAIRS = {"(": ")", "[": "]", "{": "}"}     # the wrong direction
```

Now when you meet `)` you cannot look it up. You end up either searching the dictionary's values or
writing a second dictionary. Key by the closer; you are always looking up the thing in your hand.

### Trap 5 — treating every non-opener as a closer

```python
    else:
        if not stack or stack.pop() != PAIRS[character]:
```

On `"a"` this raises:

```
KeyError: 'a'
```

If the input can contain anything other than brackets — and real inputs like source code always can —
use `elif character in PAIRS` and let everything else fall through. Ask the interviewer whether the
input is brackets only. It is a ten-second question that changes the code.

### Trap 6 — single-digit numbers in `decode_string`

```python
number = int(character)        # WRONG for "12[a]"
```

Gives 2 instead of 12, so `"12[a]"` returns `"aa"`. Use `number = number * 10 + int(character)`, and
remember to reset `number = 0` after pushing.

### Trap 7 — the wrong side of the concatenation

```python
current = current * repeat + previous     # WRONG — outside goes AFTER inside
```

On `"a2[b]"` the correct answer is `"abb"` and this gives `"bba"`. The rule to say out loud: *what
was inside the brackets repeats; what was outside stays in front.*

### Trap 8 — operand order in RPN

```python
left = stack.pop()
right = stack.pop()        # WRONG WAY ROUND
```

The **second** pop is the left operand, because the right one was pushed last. `+` and `*` hide the
bug because they commute; `-` and `/` expose it. `["4","13","5","/","+"]` should be 6 and comes out
wrong.

---

## 8. In the interview

### How it gets asked

- *"Given a string containing just `(`, `)`, `{`, `}`, `[` and `]`, determine if the input is
  valid."* LeetCode 20, almost word for word, at nearly every company.
- The follow-up that always comes: *"what if the string also contains letters and spaces?"* or
  *"what is the minimum number of brackets to add to make it valid?"*
- The family: *"decode `3[a2[c]]`"*, *"evaluate this expression with parentheses"*, *"evaluate this
  reverse Polish expression"*.
- The disguised one: *"validate this JSON without a library"* — same algorithm, richer contexts.

### What to say out loud, in the first ninety seconds

1. **Name the three failure modes before writing anything.** "There are exactly three ways this can
   be invalid: a closer that does not match the most recent opener, a closer when nothing is open, and
   something still open when the string ends. My code will have one check for each."
2. **Say the invariant.** "The stack holds exactly the openers I have seen and not yet closed, in
   order. So when I meet a closer, the only thing it can legally close is the top."
3. **Reject counting, out loud.** "Counting brackets is not enough — `([)]` has matching counts and
   is invalid — because counting throws away the order, and the order is the question."
4. **Ask the one clarifying question.** "Can the string contain other characters?" It changes one
   line and shows you thought about real inputs.
5. **State the cost.** "O(n) time. Space is O(n) in the worst case, which is a string of all openers,
   and O(1) on something like `()()()`."

### The follow-ups

**"Can you do it in O(1) space?"**
"Only for one bracket type. Then a counter works: increment on `(`, decrement on `)`, fail if it ever
goes negative, and check it ends at zero. With three types a single integer cannot remember *which*
kind is open, so I need the stack. The only way around that would be three counters, and that still
fails on `([)]` because counters do not preserve order."

**"What is the minimum number of brackets to add to make it valid?"**
"Two counters instead of one. One counts unmatched closers seen so far, the other counts openers
still waiting. On `)` I either cancel an open one or record that I need an opener. The answer is the
sum at the end. Same O(n) time, and O(1) space because I never needed to know which bracket it was."

**"Now decode `3[a2[c]]`."**
"Same shape with a richer context. On `[` I push what I have built so far and the repeat count, then
start fresh. On `]` I pop them and set `current = previous + current * repeat`. Two things to get
right: multi-digit numbers need `number * 10 + digit`, and the outside string goes in front of the
repeated inside, not after."

**"What is the complexity of that one?"**
"Linear in the size of the *output*, not the input, because the output can be exponentially bigger —
`10[10[10[a]]]` is thirteen characters in and a thousand out. So O(n + m) time and space where m is
the output length."

**"How would a compiler use this?"**
"The same way, with a richer stack. It pushes an entry per open scope — brace, parenthesis, block —
along with the line number where it opened. That is how it can tell you 'unmatched `{` opened at line
41' rather than just 'syntax error', and it is why the error points at the opener rather than the end
of the file."

### A model answer

Asked: *check whether the brackets in this string are balanced.*

> "Before I write anything, let me say the three ways this can be invalid, because my code will have
> one check for each. A closer that does not match the most recent opener, like `([)]`. A closer when
> nothing is open, like the second bracket in `())`. And something still open when the string runs
> out, like `(()`.
>
> That third one is the one people miss, because every individual step is correct and the failure is
> only visible at the end.
>
> The thing I want is a stack, and the invariant is that it holds exactly the openers I have seen and
> not yet closed, in the order I opened them. That makes the rule simple: when I meet a closer, the
> only thing it can legally close is whatever is on top.
>
> Worth saying why counting does not work — it is the obvious first idea. `([)]` has one of each
> bracket, so the counts match perfectly, and it is invalid. Counting throws away order and order is
> the whole question. For a single bracket type counting does work, and it gives an O(1)-space
> answer, so if you tell me it is only round brackets I would use a counter instead.
>
> One question before I write: can the string contain characters other than brackets? If it is source
> code or an expression, I want to ignore letters and spaces rather than treat them as closers —
> otherwise the dictionary lookup raises a `KeyError` on the first letter.
>
> So: a dictionary keyed by the *closer*, giving its opener, because when I am holding a `)` I want
> to look up what it should have found. Push openers. On a closer, check the stack is non-empty and
> that popping gives the matching opener — and the emptiness check has to come first in the same
> condition, so short-circuiting stops me popping an empty stack. At the end, return whether the
> stack is empty.
>
> Cost: O(n) time, one pass. Space is O(n) in the worst case, which is a string of all openers, and
> O(1) on something like `()()()` where every push is popped immediately.
>
> Edge cases: the empty string is balanced, vacuously — there is nothing left open. A single closer
> is the case that catches the missing emptiness check.
>
> And this generalises, which is usually where you are going next. The stack holds *the context I am
> inside and have not yet left*. For brackets the context is just the character. For something like
> `3[a2[c]]` I push the string built so far and the repeat count, and pop and combine on the closer.
> Same two lines, richer thing being pushed."

---

## 9. Recall card

- **Three ways to fail, and name all three before coding:** the closer does not match the top ·
  a closer arrives with an **empty stack** · the stack is **non-empty at the end** (the one people
  forget — every step was fine and the job is not done).
- **Invariant: the stack holds exactly the openers seen and not yet closed, in order.** So a closer
  can only legally close the top. Map **closer → opener**, not the other way, because you look up the
  thing in your hand. Write `if not stack or stack.pop() != PAIRS[c]` — `or` short-circuits, so `pop`
  never hits an empty stack.
- **Counting is not enough:** `"([)]"` has matching counts and is invalid, because counting throws
  away order. For **one** bracket type a counter *does* work — increment/decrement, fail if it goes
  negative, end at zero — giving **O(1) space**. Two counters answer "minimum additions".
- **The family is one sentence: push the context you are leaving, pop and combine on the closer.**
  Decode String pushes `(current, repeat)` · RPN pushes operands · Basic Calculator pushes the
  running result and sign · a compiler pushes the scope *and its line number*, which is why it can
  say "unmatched `{` at line 41".
- **Costs and traps.** `is_balanced`: O(n) time, O(n) space worst case (all openers), O(1) on
  `()()()`. `decode_string`: linear in the **output**, not the input — `10[10[10[a]]]` is 13 in and
  1000 out. Traps: `elif character in PAIRS` or a letter raises `KeyError` · `number*10 + digit` for
  multi-digit counts · `previous + current * repeat` (outside in front, inside repeats) · in RPN the
  **second** pop is the left operand, which only `-` and `/` expose.
