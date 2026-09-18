# Practice — Tree codec round trip

## Contract

Return preorder tokens with null child markers for a nested-list tree; implement an inverse decoder and assert round-trip equality internally.

Implement `solve(data)` in [solution.py](solution.py). `data` is the JSON object below.
Return the described JSON-compatible result. Python uses `None`, `True` and `False` for JSON
null/true/false. All unspecified inputs satisfy the stated preconditions; define any additional
edge behavior before adding a case. Numbers use the usual unit-cost interview model unless
you explicitly analyze arbitrary-size integer operations. Tree inputs are null or nested
`[value,left,right]`; graphs use integer vertices; linked-list tasks must build real nodes.

## Example

Input:
```json
{"tree":[1,[2,null,null],null]}
```

Expected output:
```json
[1,2,null,null,null]
```

## Complete practice sequence

1. Restate inputs, outputs, valid ranges, tie rules and allowed mutation.
2. Describe a simple baseline and its cost; keep it as a small-input oracle where practical.
3. Trace the example by hand and state one invariant or recurrence.
4. Implement independently. After a sustained attempt, reveal one hint at a time.
5. Run `python course.py practice 69` from the repository root. The starter is intentionally RED.
6. Add at least four independent cases to cases.json: smallest valid input, repeated/equal
   values when allowed, an adversarial ordering or topology, and a boundary/no-answer case.
7. If practical, compare random tiny inputs with the baseline using a fixed seed.
8. Deliberately introduce one plausible bug, observe a failing test, then undo the bug.
9. Explain correctness, time, auxiliary space and output space. Target: **O(n) time and serialized space**.
10. Record whether you solved independently or used hints; schedule a cold re-solve.

## Optional extension

Change one contract assumption (tie rule, online arrival, mutation permission or duplicate
policy). Write the new contract and a distinguishing test before adapting the solution. Explain
which invariant survives and which fails. Skip this if the core or due review needs the time.

## Evidence

Record test command/output, four added cases, the invariant, complexity and the minimal failure
in [NOTES.md](NOTES.md). The provided sample is a smoke test, not an exhaustive judge.
