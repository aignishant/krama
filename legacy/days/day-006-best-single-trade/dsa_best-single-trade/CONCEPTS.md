---
day: 6
part: "1.1"
title: "Keep the cheapest eligible past choice"
ids: [DSA-06]
level: working
prerequisites: ["Prefix invariants", "First maximum"]
failure: true
---

# Keep the cheapest eligible past choice

Core reading: the prefix state, trace, and counterexample. Returning trade indices or allowing
multiple trades is optional later work. Choose one practice route inside the 60-minute budget.

## One-line answer

For each possible sale, compare its price with the cheapest strictly earlier purchase.

## The story

You keep a notebook of daily prices for a used laptop. A high price on Monday and a low price
on Friday do not let you buy on Friday and sell back on Monday. The order in the notebook matters.

## The idea in plain language

An eligible pair has a purchase index smaller than its sale index. A direct baseline examines
every such pair and keeps the largest positive difference, or zero when doing nothing is best.
That costs O(n²) time. The improvement comes from asking which earlier purchase could possibly
be best for a fixed sale: the cheapest one. Every more expensive earlier purchase is dominated.

Recognize this pattern when a current item must be combined with an earlier item and one
summary of that prefix answers the combination query. Recall
[candidate dominance](../../day-002-find-the-first-maximum/dsa_find-the-first-maximum/CONCEPTS.md).
A prefix is simply the part of the list already processed; an invariant describes what your
saved state means at the same point of each iteration.

## Why Krama needs it

This is the final week-one example of discarding information with a proof. It prepares the
[weekly review](../../day-007-week-1-review/dsa_week-1-dsa-review/README.md) and later problems
where a prefix summary replaces repeated scans.

## The source behind it

[Best Time to Buy and Sell Stock](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/)
(`spec:leetcode-121`, checked 2026-09-22) specifies one purchase followed by a later sale.
The reasoning and fixtures here are original. The local adapter is `solve({"prices": ...})`;
the online route supplies the prices list through its judge interface.

## The mechanism

### Worked trace

Use teaching prices `[8, 3, 6, 2, 7]`. After initializing the earlier minimum to 8 and best
profit to 0, consider each later day as a possible sale:

| Sale index | Sale price | Earlier minimum | Candidate profit | Best after sale | Minimum for next day |
| --- | --- | --- | --- | --- | --- |
| 1 | 3 | 8 | -5 | 0 | 3 |
| 2 | 6 | 3 | 3 | 3 | 3 |
| 3 | 2 | 3 | -1 | 3 | 2 |
| 4 | 7 | 2 | 5 | 5 | 2 |

Before sale index j, retain the minimum of indices below j and the best nonnegative profit
among all completed pairs before j. First consider selling today using that earlier minimum.
Then update the minimum to make today's price eligible for future sales. These are different
roles: a new low price may improve a future trade without improving the answer today.

Correctness has two parts. For a fixed sale price, subtracting the least earlier price maximizes
profit over every eligible purchase. Considering every sale therefore covers an optimum from
every possible ending day. Taking the best with zero also covers the no-trade choice.
The updates preserve both meanings, and after the last day no eligible sale is unexamined.

Empty and one-element local inputs have no eligible pair and return zero. Do not read the first
element until handling that case. The online constraints require a nonempty list. Only the
profit is returned, so equal-profit trades need no index tie rule. Neither route needs sorting
or input mutation. One scan uses O(n) time and O(1) auxiliary and output space under the
unit-cost numeric model; storing a slice of all later prices would add O(n) temporary space.

## When it breaks

This author demonstration compares a tempting global-extrema shortcut with an independent
small-input oracle. It leaves the linear exercise implementation to you.

```python
prices = [9, 2, 5]
wrong = max(prices) - min(prices)
pairs = [(buy, sell) for buy in range(len(prices))
         for sell in range(buy + 1, len(prices))]
expected = max([0] + [prices[sell] - prices[buy] for buy, sell in pairs])
print("global extrema:", wrong, "eligible pairs:", expected)
try:
    assert wrong == expected, "the maximum occurs before the minimum"
except AssertionError as error:
    print(f"AssertionError: {error}")
assert expected == 3
print("chronological oracle: PASS")
```

**Line by line:** the shortcut ignores indices. The nested ranges enumerate only buy-before-sell
pairs. The extra zero represents no trade. The caught assertion exposes the ordering error;
the last assertion verifies this fixture's valid answer. This oracle deliberately uses O(n²)
time and space for clarity and is only suitable for tiny verification inputs.

Author verification on Python 3.12.10, 2026-09-22:

```text
global extrema: 7 eligible pairs: 3
AssertionError: the maximum occurs before the minimum
chronological oracle: PASS
```

## In production

Sorting the prices changes the question. A live stream can retain the same two scalar values,
but it cannot reconstruct trade indices unless those are retained too. Fees, multiple holdings,
and transaction limits change the state and proof; this model does not describe a trading system.
Review questions should ask why the minimum is eligible, why a descending input returns zero,
and whether the claimed constant space accidentally includes a copied suffix.

## Check yourself

### Readiness before practice

1. Trace `[6, 4, 1]`: why does the minimum change while the answer stays zero?
2. Why can an expensive earlier purchase be discarded for every future sale?
3. What breaks if you use a future minimum for today's sale?
4. Why is summing every positive daily increase a different contract?

Run the teaching block to observe the counterexample, then follow [PRACTICE.md](PRACTICE.md)
or [LEETCODE.md](LEETCODE.md). Explain the invariant aloud and add distinguishing tests for
descending, equal, short, and late-improvement inputs. Save your evidence in [NOTES.md](NOTES.md).

[Navigation](README.md) · [Quick recall](../../../docs/DSA_RECALL.md#day-006-best-single-trade)
