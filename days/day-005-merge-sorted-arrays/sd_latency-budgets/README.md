# Day 005 — Latency budgets

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the intuition, mechanism, and limits.
2. **Trace and check readiness:** follow [the worked trace](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the assignment:** use [the bounded design task](#assignment) after the explanation.
4. **Write your decision:** use [DESIGN.md](DESIGN.md) for assumptions, the artifact, an alternative, and a failure trace.
5. **Verify:** apply [the acceptance check](#acceptance-check), testing whether the stated user outcome is observable.
6. **Record:** keep actual evidence, uncertainty, and status in [DESIGN.md](DESIGN.md).
7. **Recall later without practice:** read the [system design summary file](../../../docs/SD_RECALL.md#day-005-latency-budgets) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 recall + 10 concept/reference + 12 design + 3 critique). **Outcome:** SD-05.
**Weekly theme:** Requirements and estimation.

## Assignment

Allocate a hypothetical 200 ms end-to-end p95 budget across client, network, app and storage; explain why summing component p95 values is only a rough budget.

## Work method

Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.

## References

Optional deeper reading: [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).
Official pages checked on 2026-09-22; see [source records](../../../docs/SOURCES.md).
Start with [the lesson](CONCEPTS.md) before the assignment.

## Acceptance check

- [ ] State nonoverlapping timing boundaries and allocations; explain why component p95 values do not determine end-to-end p95.
- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save the answer in [DESIGN.md](DESIGN.md). Full service implementation is not required.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
