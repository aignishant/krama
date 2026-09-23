# Day 001 — Identity and equality

## Navigation — where to start

1. **Learn the topic:** read [the explanation](CONCEPTS.md) for intuition, recognition cues, the mechanism, and why it works.
2. **Trace and check readiness:** follow [the worked example](CONCEPTS.md#the-mechanism), then [explain the readiness points](CONCEPTS.md#readiness-before-the-lab) before opening the exercise.
3. **Read the assignment:** use [the experiment task](#assignment), then predict the behavior before running code.
4. **Experiment independently:** implement [lab.py](lab.py); use your installed interpreter and record its version.
5. **Verify:** run your lab and apply [the acceptance check](#acceptance-check), including an assertion that can detect the mistake.
6. **Record:** save predictions, observations, and the explanation in [NOTES.md](NOTES.md).
7. **Recall later without practice:** read the [Python summary file](../../../docs/LANG_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** lang. **Budget:** 15 minutes (3 predict + 8 experiment + 4 explain/test). **Outcome:** PY-01.
**Weekly theme:** Object semantics.


## Assignment

Predict and verify aliasing of two names bound to the same list versus equal distinct lists; avoid relying on interning.

## Work method

Predict the behavior before running code. Write a tiny experiment in lab.py using the local interpreter, observe its actual output, then add an assertion covering the surprise or failure. Finish with a short explanation of the mechanism and where it matters in production. Basic Python syntax is assumed.

## References

The [track method](../../../docs/PYTHON_LAB_GUIDE.md) is a reusable reference. Today's exact
references are [Python 3.12 Data model](https://docs.python.org/3.12/reference/datamodel.html#objects-values-and-types)
and [Expressions: comparisons](https://docs.python.org/3.12/reference/expressions.html#comparisons),
opened on 2026-09-19. The [copy documentation](https://docs.python.org/3.12/library/copy.html)
supports the optional follow-up. Run `python --version` and record your actual interpreter.

## Acceptance check

- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save observations in [NOTES.md](NOTES.md). Run lab.py from its folder or by its full relative path; no packages are required for the core experiments.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
