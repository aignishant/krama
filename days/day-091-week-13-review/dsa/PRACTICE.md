# Practice — Cold re-solve: Task cooldown length

## Weekly assessment

Use the 60-minute session as 5 recall + 20 re-solve + 20 second re-solve + 10 critique + 5 log.
First re-solve [day 85](../../day-085-maximum-compatible-meetings/dsa/README.md), then the core below from
[day 89](../../day-089-task-cooldown-length/dsa/README.md), both from blank code. A harder unresolved problem
may replace the second. The local fixture checks the second problem only; run the first day's
tests against your first re-solve too. Score correctness/explanation/complexity/tests 0–2 each;
pass at 6/8 with correctness=2 and at least one hint-free solve. Review is not a new problem.

## Contract

Uppercase tasks take one slot, same task occurrences need at least n intervening slots. Return minimum total slots including idle.

Implement `solve(data)` in [solution.py](solution.py). `data` is the JSON object below.
Return the described JSON-compatible result. Python uses `None`, `True` and `False` for JSON
null/true/false. All unspecified inputs satisfy the stated preconditions; define any additional
edge behavior before adding a case. Numbers use the usual unit-cost interview model unless
you explicitly analyze arbitrary-size integer operations. Tree inputs are null or nested
`[value,left,right]`; graphs use integer vertices; linked-list tasks must build real nodes.

## Example

Input:
```json
{"tasks":["A","A","A","B","B","B"],"n":2}
```

Expected output:
```json
8
```

## Complete practice sequence

1. Restate inputs, outputs, valid ranges, tie rules and allowed mutation.
2. Describe a simple baseline and its cost; keep it as a small-input oracle where practical.
3. Trace the example by hand and state one invariant or recurrence.
4. Implement independently. After a sustained attempt, reveal one hint at a time.
5. Run `python course.py practice 91` from the repository root. The starter is intentionally RED.
6. Add at least four independent cases to cases.json: smallest valid input, repeated/equal
   values when allowed, an adversarial ordering or topology, and a boundary/no-answer case.
7. If practical, compare random tiny inputs with the baseline using a fixed seed.
8. Deliberately introduce one plausible bug, observe a failing test, then undo the bug.
9. Explain correctness, time, auxiliary space and output space. Target: **O(number of tasks + alphabet size)**.
10. Record whether you solved independently or used hints; schedule a cold re-solve.

## Optional extension

Change one contract assumption (tie rule, online arrival, mutation permission or duplicate
policy). Write the new contract and a distinguishing test before adapting the solution. Explain
which invariant survives and which fails. Skip this if the core or due review needs the time.

## Evidence

Record test command/output, four added cases, the invariant, complexity and the minimal failure
in [NOTES.md](NOTES.md). The provided sample is a smoke test, not an exhaustive judge.
