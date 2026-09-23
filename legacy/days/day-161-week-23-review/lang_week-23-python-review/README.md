# Day 161 — Week 23 review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair understanding:** revisit the original subject READMEs linked below, or use the [Python lab method](../../../docs/PYTHON_LAB_GUIDE.md) as a preparation reference.
3. **Read the assignment:** use [the experiment task](#assignment), then predict the behavior before running code.
4. **Experiment independently:** implement [lab.py](lab.py); use your installed interpreter and record its version.
5. **Verify:** run your lab and apply [the acceptance check](#acceptance-check), including an assertion that can detect the mistake.
6. **Record:** save predictions, observations, and the explanation in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [Python summary file](../../../docs/LANG_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 155](../../day-155-mock-arrays/lang_semantics-drill/README.md) · [Day 156](../../day-156-mock-search/lang_protocol-drill/README.md) · [Day 157](../../day-157-mock-graph/lang_typing-drill/README.md) · [Day 158](../../day-158-mock-dp/lang_concurrency-drill/README.md) · [Day 159](../../day-159-mock-heap/lang_debugging-drill/README.md) · [Day 160](../../day-160-mock-backtracking/lang_review-drill/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-161.
**Weekly theme:** Python interview drills.

## Assignment

Revisit days 155–160. From memory reproduce one surprising behavior, write a regression test for its repair, and explain the mechanism.

## Work method

Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.

## References

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
