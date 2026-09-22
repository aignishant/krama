# Day 007 — Week 1 review

## Navigation — where to start

1. **Choose the decision:** read [the assignment](#assignment) and select your weakest decision from Days 1?6.
2. **Attempt cold:** revise and defend it in [DESIGN.md](DESIGN.md) before opening notes or reference answers. Its TODOs belong to you.
3. **Verify:** trace a failure and apply [the acceptance check](#acceptance-check), including the design rubric.
4. **Repair afterwards:** read [CONCEPTS.md](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness questions](CONCEPTS.md#readiness-after-repair). Compare the assistant's [complete reference](REFERENCE_DESIGN.md) only now.
5. **Recheck:** defend your revised choice and one alternative aloud. Reference reading alone does not establish completion.
6. **Record:** keep your artifact, evidence, assumptions, help used, and status in [DESIGN.md](DESIGN.md).
7. **Recall later without practice:** use [system design recall](../../../docs/SD_RECALL.md) for studied topics.

Original reading, after cold recall: [Day 1](../../day-001-count-target-values/sd_functional-scope/README.md) · [Day 2](../../day-002-find-the-first-maximum/sd_quality-requirements/README.md) · [Day 3](../../day-003-stable-compaction/sd_traffic-estimates/README.md) · [Day 4](../../day-004-reverse-a-segment/sd_storage-estimates/README.md) · [Day 5](../../day-005-merge-sorted-arrays/sd_latency-budgets/README.md) · [Day 6](../../day-006-best-single-trade/sd_single-node-baseline/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 cold recall + 12 revision + 10 comparison/repair + 3 critique). **Outcome:** SD-07.
**Weekly theme:** Requirements and estimation.

## Assignment

After the cold attempt, use [the repair lesson](CONCEPTS.md) to address gaps.

Revisit days 1–6. Choose your weakest design decision, revise its diagram or memo, then defend one alternative and walk through one failure.

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

- [ ] I revised an earlier decision, defended an alternative, and walked through a failure before comparing the reference.
- [ ] I scored requirements, data/API, scale, and failure tradeoffs 0?2 each; the gate is 6/8 with no unexplained source of truth.
- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save the answer in [DESIGN.md](DESIGN.md). Full service implementation is not required.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
