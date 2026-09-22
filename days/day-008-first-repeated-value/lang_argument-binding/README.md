# Day 008 — Argument binding

## Navigation — where to start

1. **Learn:** read [CONCEPTS.md](CONCEPTS.md) for the mechanism, reasoning, costs, and limits.
2. **Trace and check readiness:** follow the [worked trace](CONCEPTS.md#worked-trace), inspect the observed failure, and answer the [readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the task:** use [the assignment](#assignment) and predict before running code.
4. **Experiment:** write your independent [lab.py](lab.py) and capture the actual behavior.
5. **Verify:** apply [the acceptance check](#acceptance-check), including a regression assertion and spoken explanation.
6. **Record:** save prediction, actual output, repair, and help used in [NOTES.md](NOTES.md).
7. **Recall later without practice:** use the [track recall cards](../../../docs/LANG_RECALL.md) for topics already studied; cards do not mark completion.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-08.
**Weekly theme:** Functions and scope.

## Assignment

Use [the topic explanation](CONCEPTS.md) before attempting this task.

Write a function with positional-only and keyword-only parameters and capture one invalid call's real exception.

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
