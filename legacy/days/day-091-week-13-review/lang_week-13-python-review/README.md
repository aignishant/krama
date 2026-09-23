# Day 091 — Week 13 review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair understanding:** revisit the original subject READMEs linked below, or use the [Python lab method](../../../docs/PYTHON_LAB_GUIDE.md) as a preparation reference.
3. **Read the assignment:** use [the experiment task](#assignment), then predict the behavior before running code.
4. **Experiment independently:** implement [lab.py](lab.py); use your installed interpreter and record its version.
5. **Verify:** run your lab and apply [the acceptance check](#acceptance-check), including an assertion that can detect the mistake.
6. **Record:** save predictions, observations, and the explanation in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [Python summary file](../../../docs/LANG_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 85](../../day-085-maximum-compatible-meetings/lang_coroutine-lifecycle/README.md) · [Day 86](../../day-086-reach-the-end/lang_blocking-the-loop/README.md) · [Day 87](../../day-087-minimum-jumps/lang_concurrent-tasks/README.md) · [Day 88](../../day-088-circular-fuel-route/lang_cancellation/README.md) · [Day 89](../../day-089-task-cooldown-length/lang_timeout-scopes/README.md) · [Day 90](../../day-090-optimal-merge-cost/lang_async-context-managers/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-91.
**Weekly theme:** Async fundamentals.

## Assignment

Revisit days 85–90. From memory reproduce one surprising behavior, write a regression test for its repair, and explain the mechanism.

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
