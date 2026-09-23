# Day 009 — HTTP methods

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the mechanism, assumptions, and reasoning.
2. **Trace and check readiness:** follow [the worked trace](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice) before opening the assignment.
3. **Read the assignment:** use [the bounded design task](#assignment) after the explanation.
4. **Choose guided or independent practice:** read the assistant's [complete reference answer](REFERENCE_DESIGN.md) before a guided attempt, or compare after your own attempt. Write your work in [DESIGN.md](DESIGN.md); its TODOs belong to you.
5. **Verify:** apply [the acceptance check](#acceptance-check), testing whether the stated user outcome is observable.
6. **Record:** keep actual evidence, uncertainty, and status in [DESIGN.md](DESIGN.md).
7. **Recall later without practice:** read [this day's recall card](../../../docs/SD_RECALL.md#day-009-http-methods) for a previously studied topic. Reading is not learner completion.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 recall + 10 concept/reference + 12 design + 3 critique). **Outcome:** SD-09.
**Weekly theme:** Networking and HTTP.

## Assignment

Specify create and redirect routes with method, request fields, response codes and caching implications.

## Reference and practice ownership

The assistant authors [REFERENCE_DESIGN.md](REFERENCE_DESIGN.md); [DESIGN.md](DESIGN.md) is your personal practice. Use the existing concept and critique windows for reference reading. Reading alone does not satisfy the acceptance criteria. Continue deeper reading another sitting if needed.

## Work method

Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.

## References

The [topic source section](CONCEPTS.md#the-source-behind-it) identifies the exact official
references checked on 2026-09-22. Start there; the broad resources below are optional background.

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
