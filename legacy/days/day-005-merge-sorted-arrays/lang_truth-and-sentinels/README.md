# Day 005 — Truth and sentinels

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the intuition, mechanism, and limits.
2. **Trace and check readiness:** follow [the worked trace](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the assignment:** use [the experiment task](#assignment), then predict the behavior before running code.
4. **Experiment independently:** implement [lab.py](lab.py); use your installed interpreter and record its version.
5. **Verify:** run your lab and apply [the acceptance check](#acceptance-check), including an assertion that can detect the mistake.
6. **Record:** save predictions, observations, and the explanation in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [Python summary file](../../../docs/LANG_RECALL.md#day-005-truth-and-sentinels) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-05.
**Weekly theme:** Object semantics.

## Assignment

Distinguish None, zero and empty values in an API using an identity-tested sentinel.

## Work method

Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.

## References

Optional deeper reading: [Truth Value Testing](https://docs.python.org/3.12/library/stdtypes.html#truth-value-testing) and [Identity comparisons](https://docs.python.org/3.12/reference/expressions.html#is).
Official pages checked on 2026-09-22; see [source records](../../../docs/SOURCES.md).
Start with [the lesson](CONCEPTS.md) before the assignment.

## Acceptance check

- [ ] Distinguish omission, None, zero, false, and empty values using an identity-tested marker and an explicit API policy.
- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save observations in [NOTES.md](NOTES.md). Run lab.py from its folder or by its full relative path; no packages are required for the core experiments.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
