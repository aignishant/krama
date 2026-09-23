---
day: 26
track: practice
title: "Practice — Strings revision and mock round"
status: written
---

# Day 026 · Practice

**DSA topic:** Strings revision and mock round
**System design topic:** Tables, rows, and keys

---

## Code these, in this order

Four problems from four different families. **Before writing anything, say which of the six patterns
it is and why.** If you cannot name the family in fifteen seconds, that is the thing to practise, not
the code.

Run each as a timed round: twenty minutes, six beats, narrate out loud.

| # | Problem | Source | Family, and what it is really testing |
|---|---|---|---|
| 1 | Isomorphic Strings | LeetCode 205 (Easy) | Two indices. Whether you find the second map — `"badc"`/`"baba"` passes every example in the statement with one dictionary. |
| 2 | Longest Substring Without Repeating Characters | LeetCode 3 (Medium) | Sliding window. The `last[ch] >= start` guard, which `"abba"` and `"dvdf"` expose. |
| 3 | Group Anagrams | LeetCode 49 (Medium) | Canonical form as a key, and that a list is not hashable. |
| 4 | Longest Palindrome | LeetCode 409 (Easy) | Counting, with a genuine think at the end: how many odd-count characters can you keep, and why exactly one? |

### Before each problem, run the recognition script

Out loud, in under fifteen seconds:

1. What shape is the answer — a number, a boolean, a string, a list of groups?
2. Contiguous, or gaps allowed?
3. One string or two?
4. Therefore: which of the six families?

Then confirm it against the statement before writing a line. Getting this wrong costs the whole
round; getting it right makes the code fifteen lines you already know.

### On problem 1, produce the counterexample first

Before coding, find the input that breaks the one-dictionary version. Do not look it up — reason about
what "one-to-one" means and construct it. When you have it, check that it passes with one map and
fails with two.

Producing that input unprompted, in the interview, is worth more than the solution.

### On problem 4, do the thinking part

`"abccccdd"` gives 7 — `"dccaccd"`. Work out on your own, before coding:

1. For a character appearing `k` times, how many of them can go into a palindrome?
2. Why can exactly one character contribute an odd count, and no more?
3. What is the answer for `"a"`, for `"ab"`, and for `""`?

Then write it. The code is four lines and the reasoning is the question.

### The pattern-recognition drill

For each, name the family and the cost, in under five seconds each:

1. "Find the first character that appears exactly once."
2. "Do these two strings contain the same letters?"
3. "Reverse the words in this sentence."
4. "Longest substring with at most two distinct characters."
5. "Is this a palindrome, ignoring punctuation?"
6. "Compress runs of repeated characters."
7. "Is A a subsequence of B?"
8. "Find the first occurrence of one string inside another."
9. "Group these words by which letters they contain."
10. "Longest substring that appears in both strings."

Number 10 is the trap: it says *substring*, so a mismatch resets to zero and the answer is the maximum
cell — not the bottom-right one. Say what would go wrong if you wrote the subsequence version.

### The five-inputs drill

Take any solution you wrote today and run it on all five without changing anything:

```python
""          # empty
"a"         # one character
"aaaa"      # all the same
"abcd"      # all different
".,! "      # nothing that counts
```

For each solution, say which of the five was most likely to break it, and why. Then check whether you
were right.

### The silent-quadratic drill

Both of these are correct and both are `O(n²)`. Find the line, and rewrite each:

```python
# A
def compress(s):
    out = ""
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        out += s[i] + str(j - i)
        i = j
    return out
```

```python
# B
def find_first(s, needle):
    for i in range(len(s)):
        if s[i:].startswith(needle):
            return i
    return -1
```

Then say the general rule for each: one is about immutability, the other about slicing. Both produce
right answers and only get slow, which is why neither shows up in testing.

### The mock-round drill

Have somebody pick two of these without telling you which, or pick at random. Twenty minutes each,
timed, narrating.

Valid Anagram · Reverse Words in a String · First Unique Character · Valid Palindrome II ·
Longest Common Prefix · String Compression · Ransom Note · Implement strStr · Isomorphic Strings ·
Longest Palindromic Substring

Score yourself on process, not on finishing:

- [ ] I restated the problem in my own words.
- [ ] I asked the four contract questions.
- [ ] I named the family out loud before writing code.
- [ ] I gave a brute force and its cost.
- [ ] I paused for agreement before typing.
- [ ] I named the trap before I wrote the line that avoids it.
- [ ] I tested with my five inputs, not the given example.

Fewer than six ticks means run it again tomorrow with different problems.

### The schema drill

Design the tables for **a library**: members, books, copies of books, loans, and reservations. Ten
minutes.

The interesting part is that a *book* and a *copy of a book* are different things — the library owns
four copies of the same title, and a loan is of a copy, not of a title. Get that right and the rest
follows.

Then check your own schema:

1. Is every primary key a surrogate?
2. Is every foreign key on the many side?
3. Did you need a join table anywhere? Why or why not?
4. Which columns are nullable, and can you say what each null *means*?
5. What is your `ON DELETE` on every foreign key, and can you justify each?
6. Which foreign keys did you index?
7. What type did you use for the due date, and for a fine amount?

Number 7 has two specific right answers and several wrong ones.

### The keys drill

Answer each in one or two sentences, out loud:

1. What three properties must a primary key have?
2. Why is an email address a bad primary key even though it is unique?
3. Where does a foreign key go in a one-to-many relationship, and why not the other side?
4. How do you model many-to-many, and what is the primary key of that table?
5. What is referential integrity, and what is an orphan row?
6. What does `NULL = NULL` evaluate to, and what do you write instead?
7. Are foreign keys indexed automatically? What is the consequence?
8. `BIGSERIAL` or `UUID` — pick one and defend it, then say when you would switch.
9. Name the four `ON DELETE` options and one use for each.
10. Why must money never be stored in a `FLOAT` column?

### The arithmetic drill

From memory, in under two minutes:

- 10 million comments at 250 bytes — storage, and with indexes. Do you shard?
- `BIGINT` versus `UUID` for a primary key and two foreign key indexes on 10 million rows — the two
  index sizes.
- A 100,000-row table, `WHERE author_id = 5`, with and without an index — the two times.
- 32-bit `INT` ids at 1,000 inserts a second — how long until you run out?
- `COUNT(*)` per read at 3,700 reads a second and 1 ms each — cores, and what you would do instead.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Two string problems, no hints, talk as you go.*
   The scoring is process, not completion. Restate, four contract questions, name the family, brute
   force with cost, pause, code with narration, test with your own five.

2. *Design the tables for a blog with users, posts and comments.*
   Entities first, then cardinality, then the schema. Say the surrogate-key rule as a rule. Say where
   the foreign key goes and why not the other side. Add the index line unprompted. Justify every
   nullable column by saying what its null means.

3. *How do you decide which technique a string problem needs?*
   The three questions — shape of the answer, contiguous or not, one string or two — landing on the
   six families. Then the honest caveat: recognition narrows it, the contract questions confirm it,
   and jumping straight to remembered code is how you solve the wrong problem confidently.

---

## Before you move on

- [ ] I can name the six string patterns and one tell for each.
- [ ] I run the three recognition questions before writing any string code.
- [ ] I ask the four contract questions every time.
- [ ] I test with `""`, `"a"`, `"aaaa"`, `"abcd"` and a punctuation-only input — never the given
      example.
- [ ] I never write `+=` on a string in a loop, and I never slice inside one.
- [ ] I can name the three properties of a primary key and say why email is a bad one.
- [ ] I know the foreign key goes on the many side, and can say why the other side is impossible.
- [ ] I index every foreign key and know that the database does not do it for me.
- [ ] I can redraw the pattern-decision tree and the blog schema from memory, in whatever tool I like.
