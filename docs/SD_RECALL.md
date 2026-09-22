# System design — quick recall

Use this file to revisit concepts you have already studied without producing another design,
diagram, or exercise. Each card provides the decision framework, its rationale, and its limits.
Open a full lesson only if the short reminder is insufficient.

Cards represent authored material. To choose completed topics, use each day's latest `sd`
event in [track progress](TRACK_PROGRESS.csv). Missing entries do not mean completed. Day 001
is the first available card; future taught days will extend this file in day order.

## Index

| Day | Topic | Jump |
| --- | --- | --- |
| 001 | Functional scope and observable outcomes | [Recall card](#day-001-functional-scope) |

## Day 001: Functional scope

**Core idea:** agree on what the user can accomplish before choosing how to build it.

**Reusable shape:** given a condition, an actor supplies an input; the service produces an
observable result. A named failure has a defined alternative outcome.

| Term | Keep this distinction |
| --- | --- |
| Functional requirement | The action and observable outcome |
| Quality requirement | A property of that behavior, such as delay or availability |
| Implementation choice | How the behavior is built; “use a database” is not a user action |
| Assumption | A premise still needing confirmation |
| Exclusion | Behavior this version does not promise |
| Success criterion | A defined scenario/population, measurement, and target |

**Memory anchor:** “Item created” is insufficient if the user cannot retrieve the item.
Returning an identifier repairs the response shape, but testing the full promise requires
retrieving the saved item too. One passing fixture does not prove the whole service works.

**Link-shortener boundary:** browser → shortener → redirect → browser → destination.
A correct redirect does not guarantee that the destination is healthy. Define which outcome
your success measure covers and what happens for a code that cannot be resolved.

**Why it helps:** two readers can agree on an acceptance scenario before committing to
infrastructure. A scope memo retains user decisions and postpones choices that lack a requirement.
The cost is clarification now; the benefit is fewer incompatible expectations later.

**Common mistakes:** start with architecture; use untestable words such as “fast”; omit
exclusions; present assumed traffic as measured traffic; count destination failures against an
undefined shortener guarantee. Compare one alternative and state what evidence would change the decision.

[Full explanation](../days/day-001-count-target-values/sd_functional-scope/CONCEPTS.md) ·
[Your Day 1 memo](../days/day-001-count-target-values/sd_functional-scope/DESIGN.md)

---

[DSA recall](DSA_RECALL.md) · [Python recall](LANG_RECALL.md) · [Study workflow](STUDY_WORKFLOW.md)
