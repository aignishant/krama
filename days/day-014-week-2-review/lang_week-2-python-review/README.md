# Day 014 — Week 2 review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair after the cold attempt:** read [the review explanation](CONCEPTS.md), [worked trace](CONCEPTS.md#worked-trace), and [readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the assignment:** use [the experiment task](#assignment), then predict the behavior before running code.
4. **Experiment independently:** implement [lab.py](lab.py); use your installed interpreter and record its version.
5. **Verify:** run your lab and apply [the acceptance check](#acceptance-check), including an assertion that can detect the mistake.
6. **Record:** save predictions, observations, and the explanation in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read [this day's card](../../../docs/LANG_RECALL.md#day-014-week-2-python-review) for a previously studied topic; reading is not completion.

Original reading, after cold recall: [Day 8](../../day-008-first-repeated-value/lang_argument-binding/README.md) · [Day 9](../../day-009-frequency-ranking/lang_closure-binding/README.md) · [Day 10](../../day-010-pair-sum-indices/lang_nonlocal-state/README.md) · [Day 11](../../day-011-group-anagrams/lang_decorator-metadata/README.md) · [Day 12](../../day-012-range-sums/lang_decorator-arguments/README.md) · [Day 13](../../day-013-count-target-subarrays/lang_partial-application/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-14.
**Weekly theme:** Functions and scope.

## Assignment

Revisit days 8–13. From memory reproduce one surprising behavior, write a regression test for its repair, and explain the mechanism.

## Work method

Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.

## References

Start with [the exact topic sources](CONCEPTS.md#the-source-behind-it), checked
2026-09-22. The broad references below are optional background.

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
