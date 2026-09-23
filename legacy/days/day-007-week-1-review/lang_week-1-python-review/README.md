# Day 007 — Week 1 review

## Navigation — where to start

1. **Choose the behavior:** read [the assignment](#assignment) and select one surprise from Days 1?6.
2. **Attempt cold:** predict and reproduce it from memory in [lab.py](lab.py), then repair it without copying prior code.
3. **Verify:** write a regression assertion, explain the mechanism, and apply [the acceptance check](#acceptance-check).
4. **Repair understanding afterwards:** read [CONCEPTS.md](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness questions](CONCEPTS.md#readiness-after-repair). Revisit the original lessons below for specific gaps.
5. **Recheck:** confirm the regression assertion detects the original defect and explain the ownership or value contract aloud.
6. **Record:** save your prediction, actual output, repair, help used, and status in [NOTES.md](NOTES.md).
7. **Recall later without practice:** use [Python recall](../../../docs/LANG_RECALL.md) for studied topics.

Original reading, after cold recall: [Day 1](../../day-001-count-target-values/lang_identity-and-equality/README.md) · [Day 2](../../day-002-find-the-first-maximum/lang_shallow-and-deep-copies/README.md) · [Day 3](../../day-003-stable-compaction/lang_mutable-defaults/README.md) · [Day 4](../../day-004-reverse-a-segment/lang_hash-and-equality/README.md) · [Day 5](../../day-005-merge-sorted-arrays/lang_truth-and-sentinels/README.md) · [Day 6](../../day-006-best-single-trade/lang_mutation-contracts/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-07.
**Weekly theme:** Object semantics.

## Assignment

After the cold attempt, use [the repair lesson](CONCEPTS.md) to address gaps.

Revisit days 1–6. From memory reproduce one surprising behavior, write a regression test for its repair, and explain the mechanism.

## Work method

Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.

## References

The [topic lesson](CONCEPTS.md#the-source-behind-it) names the exact official pages checked
on 2026-09-22. The broader references below are optional background.

Read the [track method](../../../docs/PYTHON_LAB_GUIDE.md) when starting this track.

[The Python Standard Library](https://docs.python.org/3.12/library/index.html) and [Data model](https://docs.python.org/3/reference/datamodel.html). Use the named module or protocol; compare version notes with your local interpreter.
Source records were checked on 2026-09-18; fetch the exact relevant section when studying.
For later case studies, reuse earlier track notes rather than adding a new reading project.

## Acceptance check

- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save observations in [NOTES.md](NOTES.md). Run lab.py from its folder or by its full relative path; no packages are required for the core experiments.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
