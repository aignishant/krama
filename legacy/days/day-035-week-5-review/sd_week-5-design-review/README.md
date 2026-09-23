# Day 035 — Week 5 review

## Navigation — where to start

1. **Cold recall first:** use the assigned review below without notes. Open explanations after the attempt or when deliberately repairing a gap; record any help used.
2. **Repair after the cold attempt:** read [the review lesson](CONCEPTS.md), its [worked trace](CONCEPTS.md#worked-trace), and [readiness checks](CONCEPTS.md#readiness-before-practice). Record help used.
3. **Reference and assignment:** After your cold attempt, compare [the complete reference](REFERENCE_DESIGN.md), then use [the bounded task](#assignment) for your own artifact. The assistant writes the reference; [DESIGN.md](DESIGN.md) and its TODOs are your practice.
4. **Write your decision:** use [DESIGN.md](DESIGN.md) for assumptions, the artifact, an alternative, and a failure trace.
5. **Verify:** apply [the acceptance check](#acceptance-check), testing whether the stated user outcome is observable.
6. **Record:** keep actual evidence, uncertainty, and status in [DESIGN.md](DESIGN.md).
7. **Recall later without practice:** read the [system design summary file](../../../docs/SD_RECALL.md) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

Original reading, after cold recall: [Day 29](../../day-029-stable-record-sorting/sd_tree-indexes/README.md) · [Day 30](../../day-030-merge-overlapping-intervals/sd_log-structured-storage/README.md) · [Day 31](../../day-031-insert-an-interval/sd_access-pattern-modeling/README.md) · [Day 32](../../day-032-minimum-meeting-rooms/sd_hot-partitions/README.md) · [Day 33](../../day-033-kth-smallest/sd_ttl-and-deletion/README.md) · [Day 34](../../day-034-count-inversions/sd_storage-decision-memo/README.md).

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 cold recall + 12 own design + 10 repair/reference + 3 critique). **Outcome:** SD-35.
**Weekly theme:** Storage engine tradeoffs.

## Assignment

Revisit days 29–34. Choose your weakest design decision, revise its diagram or memo, then defend one alternative and walk through one failure.

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
