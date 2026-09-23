# Practice — Cold re-solve: Smallest covering window

## Product-company interview practice

Open [today's LeetCode assignment](LEETCODE.md). Use the same 60-minute session;
choose one main attempt rather than adding a second mandatory problem. The local contract
remains the specification for solution.py and cases.json. For an online-only attempt, record
submission evidence, compare the contracts, and use the interview checklist for completion.
The local implementation steps below apply when you choose the local route.

## Weekly assessment

Use the 60-minute session as 5 recall + 20 re-solve + 20 second re-solve + 10 critique + 5 log.
First re-solve [day 120](../../day-120-normalize-text-units/dsa_normalize-text-units/README.md), then the core below from
[day 124](../../day-124-smallest-covering-window/dsa_smallest-covering-window/README.md), both from blank code. A harder unresolved problem
may replace the second. The local fixture checks the second problem only; run the first day's
tests against your first re-solve too. Score correctness/explanation/complexity/tests 0–2 each;
pass at 6/8 with correctness=2 and at least one hint-free solve. Review is not a new problem.

## Contract

Return shortest substring covering all pattern character multiplicities; tie by earliest start; absent or empty pattern returns empty string.

Implement `solve(data)` in [solution.py](solution.py). `data` is the JSON object below.
Return the described JSON-compatible result. Python uses `None`, `True` and `False` for JSON
null/true/false. All unspecified inputs satisfy the stated preconditions; define any additional
edge behavior before adding a case. Numbers use the usual unit-cost interview model unless
you explicitly analyze arbitrary-size integer operations. Tree inputs are null or nested
`[value,left,right]`; graphs use integer vertices; linked-list tasks must build real nodes.

## Example

Input:
```json
{"text":"ADOBECODEBANC","pattern":"ABC"}
```

Expected output:
```json
"BANC"
```

## Complete practice sequence

1. Restate inputs, outputs, valid ranges, tie rules and allowed mutation.
2. Describe a simple baseline and its cost; keep it as a small-input oracle where practical.
3. Trace the example by hand and state one invariant or recurrence.
4. Implement independently. After a sustained attempt, reveal one hint at a time.
5. Run `python course.py practice 126` from the repository root. The starter is intentionally RED.
6. Add at least four independent cases to cases.json: smallest valid input, repeated/equal
   values when allowed, an adversarial ordering or topology, and a boundary/no-answer case.
7. If practical, compare random tiny inputs with the baseline using a fixed seed.
8. Deliberately introduce one plausible bug, observe a failing test, then undo the bug.
9. Explain correctness, time, auxiliary space and output space. Target: **Expected O(n+m) time**.
10. Record whether you solved independently or used hints; schedule a cold re-solve.

## Optional extension

Change one contract assumption (tie rule, online arrival, mutation permission or duplicate
policy). Write the new contract and a distinguishing test before adapting the solution. Explain
which invariant survives and which fails. Skip this if the core or due review needs the time.

## Evidence

Record test command/output, four added cases, the invariant, complexity and the minimal failure
in [NOTES.md](NOTES.md). The provided sample is a smoke test, not an exhaustive judge.
