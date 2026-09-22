# Day 002 — Quality requirements

## Navigation — where to start

1. **Learn:** read [the topic explanation](CONCEPTS.md) for the intuition, state, and reasoning.
2. **Trace and check readiness:** follow [the worked example](CONCEPTS.md#worked-trace), then answer [the readiness questions](CONCEPTS.md#readiness-before-practice).
3. **Read the assignment:** use [the bounded design task](#assignment) after the explanation.
4. **Choose your route:** read [the complete reference design](REFERENCE_DESIGN.md) first for guided learning, or attempt independently and compare afterwards.
5. **Write your decision:** fill the `TODO(me)` prompts in [DESIGN.md](DESIGN.md) with your own assumptions, artifact, alternative, and failure trace.
6. **Verify:** apply [the acceptance check](#acceptance-check), testing whether the stated user outcome is observable.
7. **Record:** keep actual evidence, uncertainty, and status in [DESIGN.md](DESIGN.md).
8. **Recall later without practice:** read the [system design summary file](../../../docs/SD_RECALL.md#day-002-quality-requirements) for previously studied topics. Cards appear as days are taught; their presence does not mark study complete.

[Back to the day hub](../LESSON.md) · [Independent study and progress](../../../docs/STUDY_WORKFLOW.md)

**Track:** sd. **Budget:** 30 minutes (5 recall + 10 concept/reference + 12 design + 3 critique). **Outcome:** SD-02.
**Weekly theme:** Requirements and estimation.

## Assignment

Define availability, latency percentile, durability and freshness targets for that service; mark every number as an assumption.

## Who fills the TODOs?

The assistant has written [REFERENCE_DESIGN.md](REFERENCE_DESIGN.md) as a complete answer to
this day's assignment. **You fill the TODOs in [DESIGN.md](DESIGN.md) when practicing.**
You can read the reference without doing the exercise; it is one reasoned answer under stated
assumptions. Your practice file records your own reasoning, actual observations, and help used.
Reading or copying the reference alone does not meet the completion criteria.

Use the existing concept/reference and critique time for reading and comparison; no extra
mandatory design is added. See [the SD workflow](../../../docs/SD_DESIGN_GUIDE.md#who-fills-the-todos).

## Work method

Produce one bounded artifact: a small diagram, a calculation with units, a state table or a short decision memo. Label assumptions before reasoning from them. Trace one concrete request or failure through the result. Compare at least one alternative and state why your choice fits the requirements.

## References

Optional deeper reading: [Service Level Objectives](https://sre.google/sre-book/service-level-objectives/).
The exact page was checked on 2026-09-22; see [source records](../../../docs/SOURCES.md).

## Acceptance check

- [ ] Name the population, boundary, window, and assumed target for each quality requirement.
- [ ] I completed the specific assignment above and saved evidence.
- [ ] I can explain the mechanism or tradeoff without reading my notes.
- [ ] I named one failure or counterexample and the response to it.
- [ ] I distinguished an assumption from an observed result.
- [ ] I recorded complete, partial or needs-review in the independent track ledger.

Save the answer in [DESIGN.md](DESIGN.md). Full service implementation is not required.
When the cap is reached, record the next step. Continue this track later without blocking the other two.
