# Day 164 — Capstone consistency

## Navigation — where to start

1. **Prepare before practice:** read the [design method](../../../docs/SD_DESIGN_GUIDE.md). This is a shared preparation guide; the full explanation of **Capstone consistency** is not yet expanded.
2. **Understand before attempting:** when this day is expanded, start with its topic explanation, worked trace, and readiness check. A broad preparation guide alone is not the full lesson; follow [the teaching workflow](../../../docs/TEACHING_WORKFLOW.md).
3. **Read the assignment:** use [the bounded design task](#assignment) after the explanation.
4. **Write your decision:** use [DESIGN.md](DESIGN.md) for assumptions, the artifact, an alternative, and a failure trace.
5. **Verify:** apply [the acceptance check](#acceptance-check), testing whether the stated user outcome is observable.
6. **Record:** keep actual evidence, uncertainty, and status in [DESIGN.md](DESIGN.md).
7. **Recall later without practice:** read the [system design summary file](../../../docs/SD_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 recall + 10 concept/reference + 12 design + 3 critique). **Outcome:** SD-164.
**Weekly theme:** Final design portfolio.

## Assignment

Write three invariants and the consistency or transaction boundary enforcing each.

## Work method

Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.

## References

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
