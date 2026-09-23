# Day 006 — Single-node baseline

## Navigation — where to start

1. **Learn:** read [CONCEPTS.md](CONCEPTS.md) for the mechanism, reasoning, costs, and limits.
2. **Trace and check readiness:** follow the [worked trace](CONCEPTS.md#worked-trace), inspect the observed failure, and answer the [readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the task:** open [the assignment](#assignment). Read the [complete reference](REFERENCE_DESIGN.md) before a guided attempt or compare after an independent attempt.
4. **Write your decision:** [DESIGN.md](DESIGN.md) is your practice file; its TODOs belong to you. The assistant authors the reference.
5. **Verify:** apply [the acceptance check](#acceptance-check), defend an alternative, and trace a failure.
6. **Record:** keep your evidence, assumptions, help used, and status in [DESIGN.md](DESIGN.md). Reference reading alone does not complete study.
7. **Recall later without practice:** use the [track recall cards](../../../docs/SD_RECALL.md) for topics already studied; cards do not mark completion.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 recall + 10 concept/reference + 12 design + 3 critique). **Outcome:** SD-06.
**Weekly theme:** Requirements and estimation.

## Assignment

Use [the topic explanation](CONCEPTS.md) before attempting this task.

Draw browser -> service -> database and trace create and redirect; name the first bottleneck to measure.

## Work method

Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.

## References

The [topic lesson](CONCEPTS.md#the-source-behind-it) names the exact official pages checked
on 2026-09-22. The broader references below are optional background.

Read the [track method](../../../docs/SD_DESIGN_GUIDE.md) when starting this track.

[HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110.html), [Concurrency Control](https://www.postgresql.org/docs/current/mvcc.html), [consensus paper](https://raft.github.io/raft.pdf), and [reliability book contents](https://sre.google/sre-book/table-of-contents/). Choose the section relevant to this assignment; do not read all four.
Source records were checked on 2026-09-18; fetch the exact relevant section when studying.
For later case studies, reuse earlier track notes rather than adding a new reading project.

## Acceptance check

- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save the answer in [DESIGN.md](DESIGN.md). Full service implementation is not required.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
