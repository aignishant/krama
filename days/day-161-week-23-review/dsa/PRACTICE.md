# Practice — Cold re-solve: Mock heap

## Weekly assessment

Use the 60-minute session as 5 recall + 20 re-solve + 20 second re-solve + 10 critique + 5 log.
First re-solve [day 155](../../day-155-mock-arrays/dsa/README.md), then the core below from
[day 159](../../day-159-mock-heap/dsa/README.md), both from blank code. A harder unresolved problem
may replace the second. The local fixture checks the second problem only; run the first day's
tests against your first re-solve too. Score correctness/explanation/complexity/tests 0–2 each;
pass at 6/8 with correctness=2 and at least one hint-free solve. Review is not a new problem.

## Contract

Return minimum cost to connect all given 2D points using Manhattan-distance edges; empty returns 0.

Implement `solve(data)` in [solution.py](solution.py). `data` is the JSON object below.
Return the described JSON-compatible result. Python uses `None`, `True` and `False` for JSON
null/true/false. All unspecified inputs satisfy the stated preconditions; define any additional
edge behavior before adding a case. Numbers use the usual unit-cost interview model unless
you explicitly analyze arbitrary-size integer operations. Tree inputs are null or nested
`[value,left,right]`; graphs use integer vertices; linked-list tasks must build real nodes.

## Example

Input:
```json
{"points":[[0,0],[2,2],[3,10],[5,2],[7,0]]}
```

Expected output:
```json
20
```

## Complete practice sequence

1. Restate inputs, outputs, valid ranges, tie rules and allowed mutation.
2. Describe a simple baseline and its cost; keep it as a small-input oracle where practical.
3. Trace the example by hand and state one invariant or recurrence.
4. Implement independently. After a sustained attempt, reveal one hint at a time.
5. Run `python course.py practice 161` from the repository root. The starter is intentionally RED.
6. Add at least four independent cases to cases.json: smallest valid input, repeated/equal
   values when allowed, an adversarial ordering or topology, and a boundary/no-answer case.
7. If practical, compare random tiny inputs with the baseline using a fixed seed.
8. Deliberately introduce one plausible bug, observe a failing test, then undo the bug.
9. Explain correctness, time, auxiliary space and output space. Target: **O(n^2) dense spanning-tree approach**.
10. Record whether you solved independently or used hints; schedule a cold re-solve.

## Optional extension

Change one contract assumption (tie rule, online arrival, mutation permission or duplicate
policy). Write the new contract and a distinguishing test before adapting the solution. Explain
which invariant survives and which fails. Skip this if the core or due review needs the time.

## Evidence

Record test command/output, four added cases, the invariant, complexity and the minimal failure
in [NOTES.md](NOTES.md). The provided sample is a smoke test, not an exhaustive judge.
