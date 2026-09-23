---
day: 11
part: "1.1"
title: "Use a canonical key that preserves multiplicity"
ids: [DSA-11]
level: working
prerequisites: ["Frequency tables", "Hash and equality"]
failure: true
---

# Use a canonical key that preserves multiplicity

Core: equivalent keys, grouping, and local output ordering. Fixed-alphabet count keys and
Unicode policy are optional depth; sorted-string keys are enough for the core route.

## One-line answer

Give words the same key exactly when they contain the same letters with the same counts.

## The story

A word-game organiser sorts submitted cards into piles. `abb` and `bab` belong together, while
`ab` does not. Remembering only which letters appeared puts the short card in the wrong pile.

## The idea in plain language

An anagram rearranges letters without adding or dropping occurrences. A canonical key is a
common representation for all items that should belong together. Sorting a word's characters
produces such a key: `abb` and `bab` both become `abb`.

Recall [multiplicity](../../day-009-frequency-ranking/dsa_frequency-ranking/CONCEPTS.md) and
[hash/equality](../../day-004-reverse-a-segment/lang_hash-and-equality/CONCEPTS.md).
Use a dictionary from a full immutable key to a list of original words. A key's hash locates
candidate entries; equality distinguishes collisions. Storing only the numeric hash is unsafe.
Recognize canonicalization when many objects are equivalent under a transformation and repeated
pairwise comparisons waste work. A baseline compares every new word with existing group
representatives; up to O(n²) equivalence checks are needed when all words differ.

## Why Krama needs it

[Top frequent words](../../day-144-top-frequent-words/dsa_top-frequent-words/README.md) later
combines string identity, counting, and output ordering. Today's grouping separates those concerns.

## The source behind it

[Group Anagrams](https://leetcode.com/problems/group-anagrams/) (`spec:leetcode-49`, checked
2026-09-22) uses lowercase English letters, permits empty strings, and accepts arbitrary answer
order. The local task additionally sorts each group and the outer list lexicographically.

## The mechanism

### Worked trace

| Word | Sorted-character key | Group after insertion |
| --- | --- | --- |
| abb | abb | `[abb]` |
| ab | ab | `[ab]` |
| bab | abb | `[abb, bab]` |
| ba | ab | `[ab, ba]` |
| abb | abb | `[abb, bab, abb]` |

Every processed word is appended once to the group matching its key. Equal keys imply equal
letter multiplicities because sorting preserves every occurrence. Equal multiplicities imply
equal sorted keys because sorting places the same letters in the same order. Both directions
matter: the first prevents false merges, the second prevents false splits.

After grouping, local practice sorts the words within each group, then sorts those lists.
For the trace the result is `[["ab", "ba"], ["abb", "abb", "bab"]]`. Keep duplicate input
words: grouping does not deduplicate. The empty string uses the empty key; empty local input
produces no groups. Dictionary insertion order is not the requested lexicographic ordering.

Let n be word count, L the maximum length, S total characters, and g group count. Constructing
sorted keys costs O(S log(max(2, L))) as an upper bound; dictionary operations include key
hashing, so do not claim every string operation is O(1). Group membership uses O(n) references
and up to O(S) stored key characters, plus sorting workspace.

Local output sorting adds work. Within groups there are at most O(n log n) string comparisons,
each costing up to O(L+1). Distinct canonical groups cannot contain an identical word, so outer
group comparison is decided by their first words: O(g log g) such comparisons, each O(L+1).
This yields an upper bound O(S log(max(2,L)) + n log(max(2,n))(L+1)) for the local route.
Returning groups stores O(n+g) references; strings need not be copied. State whether you include
that output memory when reporting auxiliary space.

For the explicitly restricted alphabet a 26-count tuple is another canonical key: each position
counts one letter. Counting takes O(S+26n) time before output sorting. This requires validating
the alphabet; a fixed 26-slot representation is not a general lowercase-Unicode solution.

## When it breaks

```python
left, right = "abb", "ab"
wrong_same = frozenset(left) == frozenset(right)
correct_same = "".join(sorted(left)) == "".join(sorted(right))
print("set keys agree:", wrong_same)
print("sorted keys agree:", correct_same)
try:
    assert wrong_same == correct_same, "a set discards letter multiplicity"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert not correct_same
assert "".join(sorted("abb")) == "".join(sorted("bab"))
```

**Line by line:** `frozenset` is hashable but forgets repeated letters. Sorting then joining
retains them in a string key. The caught assertion demonstrates a false merge, and the final
assertions distinguish a true negative from a true positive. Hashability alone is insufficient.

Author verification on Python 3.12.10, 2026-09-22:

```text
set keys agree: True
sorted keys agree: False
AssertionError: a set discards letter multiplicity
```

## In production

Define text identity before grouping user input: case folding, accents, normalization, and
grapheme boundaries are separate decisions. Do not quietly normalize interview inputs or claim
that sorting code points models every language. Long keys and one enormous group can dominate
memory. A reviewer should ask whether output must be deterministic, whether repeated submissions
are preserved, and what limits apply before accepting arbitrary-length strings.

## Check yourself

### Readiness before practice

1. Why do both directions of the key-equivalence argument matter?
2. What distinguishes `abb`, `bab`, and `ab`?
3. Why must two copies of an identical input word remain in the output?
4. Which sorting costs disappear online but remain locally?

Run the key experiment, then explain the grouping invariant aloud. Choose [local practice](PRACTICE.md)
or [LeetCode](LEETCODE.md) and test empty words, duplicates, singleton groups, and reversed arrival order.

[Navigation](README.md) · [Recall](../../../docs/DSA_RECALL.md#day-011-group-anagrams)
