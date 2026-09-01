---
day: 155
track: practice
title: "Practice — String DP: palindromic substrings"
status: written
---

# Day 155 · Practice

**DSA topic:** String DP: palindromic substrings
**System design topic:** Design Instagram

---

## Code these, in this order

One rule for the whole set: **before writing a loop over a table, say out loud which cell the recurrence
reads, and confirm your loop order computes it first.** Today is the first time the natural order is wrong,
and it fails silently.

| # | Problem | Source | What it is really testing |
|---|---|---|---|
| 1 | Longest Palindromic Substring | LeetCode 5 (Medium) | Expand around centre, and the two kinds of centre. |
| 2 | Palindromic Substrings | LeetCode 647 (Medium) | The same loop, counting instead of measuring. |
| 3 | Longest Palindromic Subsequence | LeetCode 516 (Medium) | A different problem — the LCS reduction. |
| 4 | Palindrome Partitioning II | LeetCode 132 (Hard) | Where the table is required and expansion is not enough. |
| 5 | Shortest Palindrome | LeetCode 214 (Hard) | Prefix palindromes, and a linear approach. |
| 6 | Valid Palindrome II | LeetCode 680 (Easy) | Two pointers, and knowing when no DP is needed. |

### On problem 1, write the DP first and fill it wrongly

Fill the table left to right, top to bottom. Run on `"aabaa"` and print `dp[0][4]`. Record it. **Say what that
`False` actually means**, and why the bug only shows on palindromes longer than three.

Then fix the fill order to go by increasing length, and confirm.

### On problem 1, drop the even centres

Expand from `(i, i)` only. Run on `"abba"` and `"cbbd"` and record both answers. **Say how many centres there
really are and why.**

### On problem 1, forget the step back

Return `left, right` from the expansion instead of `left + 1, right`. Run on `"aba"` and print the returned
pair and the resulting slice. **Say why Python does not raise.**

### On problem 1, compare the two solutions honestly

Time both at `n = 2000` on random text and on a string of 2000 identical characters. Record four numbers.
**Then measure the DP's memory.** Say in one sentence why you would write expansion.

### On problem 2, change one line

Start from your expansion solution and turn it into a counter. **Say why `count += 1` inside the while loop is
correct** — what exactly is being counted.

### On problem 3, notice it is a different problem

Run your substring solution and your subsequence solution on `"bbbab"`. Record both. **Say why
expand-around-centre cannot solve the subsequence version**, in one sentence.

### On problem 4, find why expansion fails

Try to solve it using only `longest_palindrome`. Say what question you need answered and how many times.
**Then compute the cost with the table and without it.**

### Then the fill-order drill

Write the palindrome table twice: once by increasing length, once with `i` decreasing. Confirm they agree on
twenty random strings. **Say why both work**, in terms of the dependency.

---

### The recurrence drill

1. State the recurrence in one sentence about ends and insides.
2. Give both base cases.
3. Say which cell it depends on and where that sits in the table.
4. Say what the natural fill order does, and what the wrong `False` means.
5. Give both correct fill orders and why each works.

### The centre drill

1. Say how many centres there are, and why.
2. Give an odd example and an even example.
3. Say what happens to `"abba"` with odd centres only.
4. Explain the `left + 1` step-back.
5. Say why a negative index does not raise.

### The comparison drill

1. Give time and space for both approaches.
2. Say what the DP buys over expansion. (Nothing — say that.)
3. Give the memory numbers at `n = 1,000` and `n = 10,000`.
4. Name the one problem where the table is required, and why.
5. Say what Manacher's does, in one sentence, and whether you would write it.

### The worst-case drill

1. Give the input that makes expansion quadratic.
2. Say what it does on ordinary text and why.
3. Say what that means for choosing an approach at `n = 10^7`.

### The substring-versus-subsequence drill

1. Give both answers for `"bbbab"`.
2. Say why expansion does not apply to the subsequence version.
3. Give the LCS reduction and justify it in one sentence.
4. Give the direct interval DP for it.
5. Say what word in the statement tells you which is being asked.

### The break-it drill

Trigger each and record the exact output or error:

1. The natural fill order on `"aabaa"`.
2. Odd centres only, on `"abba"`.
3. Returning `left, right` from the expansion.
4. The general rule applied to a length-2 substring.
5. The DP table at `n = 50,000`.
6. A sentence with punctuation and capitals.
7. The empty string, with and without the guard.

Five of the seven give no error at all. Name them.

---

### The two-systems drill

1. Give both systems, their sizes and their stores.
2. Give the ratio of media bytes to metadata bytes.
3. Say why you would move quickly past the metadata half.

### The upload drill

1. Give the six steps and say which the user waits for.
2. Say what a pre-signed URL is and what it removes.
3. Compute the bandwidth saved at 1,000 uploads/second.
4. Say what you give up, and how you bound it.
5. Say why the transcode worker must be idempotent.
6. Name the two image-processing steps that are not about size.

### The variants drill

1. List the variants with sizes and what each is for.
2. Give the pre-generate versus on-demand trade.
3. Say who picks the variant, and why that matters more than a backend change.
4. Say what `blurhash` and the dimensions are for.

### The delivery drill

1. Compute daily egress from the user numbers.
2. Give the origin-only bill and the CDN bill.
3. Say what the hit rate does to the origin line.
4. Explain the signed-URL trap and the fix.
5. Say what you accept in exchange.
6. Say what a falling CDN hit rate usually means.

### The storage drill

1. Compute bytes per photo and per year.
2. Give the untiered and tiered monthly costs.
3. Give the access power law that justifies tiering.
4. Say what breaks if a photo goes viral after a year, and the fix.

### The video drill

1. Describe an adaptive ladder and why chunks.
2. Give the transcoding cost rule.
3. Compute the core count at 10 million uploads a day.
4. Say what that implies about hardware.

### The deletion drill

1. Give the three layers and their timings.
2. Say what "deleted" means to a user, and to you.
3. Say why this is legally material.

---

## Say these out loud

Three questions. Answer each one in two minutes, standing up, without looking at the lesson.

1. *Find the longest palindromic substring.*
   The DP with its recurrence and fill-order problem, then expansion with the two centre kinds, the space
   comparison, and where the table is still needed.

2. *Can you do it in `O(1)` space? Is there a linear solution?*
   Expansion with `2n - 1` centres, the step-back, the worst case versus real text, and one sentence on
   Manacher's.

3. *Design Instagram.*
   The two systems and the byte ratio, pre-signed uploads, asynchronous transcoding with the two
   non-size steps, the CDN bill, and the signed-URL cache trap.

---

## Before you move on

- [ ] I can state the palindrome recurrence in one sentence.
- [ ] I know it depends on the cell below and to the left.
- [ ] I know what the natural fill order does and why it is silent.
- [ ] I can give both correct fill orders and justify each.
- [ ] I know why length 2 needs its own base case.
- [ ] I can write expand-around-centre from memory.
- [ ] I know there are `2n - 1` centres and why.
- [ ] I know what odd-centres-only does to `"abba"`.
- [ ] I know why the return is `left + 1, right`.
- [ ] I know a negative index slices rather than raising.
- [ ] I can turn the expansion into a counter with one line.
- [ ] I can give both space costs with real numbers.
- [ ] I know the DP buys nothing over expansion for this question.
- [ ] I know palindrome partitioning is where the table is required.
- [ ] I know the expansion worst case and what real text does instead.
- [ ] I can distinguish substring from subsequence with `"bbbab"`.
- [ ] I know the subsequence version is `LCS(s, reversed(s))` and why.
- [ ] I can say what Manacher's does in one sentence.
- [ ] I can give the media-to-metadata byte ratio.
- [ ] I can explain pre-signed uploads and what they remove.
- [ ] I know what I give up by not seeing the bytes.
- [ ] I know why the transcode worker must be idempotent.
- [ ] I know EXIF orientation and GPS stripping, and why each matters.
- [ ] I can list the variants and say who picks one.
- [ ] I know what blurhash and dimensions do for the client.
- [ ] I can compute daily egress and both bills.
- [ ] I know the signed-URL cache trap and the fix.
- [ ] I can give tiered and untiered storage costs.
- [ ] I know the video transcoding rule and its core count.
- [ ] I know delete has three layers with different timings.
- [ ] I answered all three questions above out loud.
