# Python labs for an experienced developer

The purpose of a 15-minute session is to sharpen one mental model, not relearn syntax or build
a whole application. Use the assigned topic to produce one small reproducible experiment.

## Predict, observe, explain

Write the expected result before running. Use inputs that distinguish two plausible explanations.
For example, an ownership experiment needs nested mutable state; copying a list of only integers
does not expose the distinction between shallow and deep copies. Run from a fresh process when
imports, global state or cached results could affect the observation. Save the actual exception
or result rather than reconstructing it from memory.

Then explain why the result follows from the relevant protocol or lifecycle. Add an assertion
that would fail if the unwanted behavior returned. State one production consequence, such as
leaked state across requests, an unreleased resource, unbounded task creation or a misleading type.

## Keep guarantees separate

| Layer | Question |
| --- | --- |
| Language semantics | What behavior can Python programs rely on? |
| Standard-library contract | What does this version's documented API promise? |
| Interpreter implementation | Is this observation specific to CPython or its build configuration? |
| Operating system/environment | Does process creation, timezone data or file behavior vary here? |
| Your application | Which ownership, validation and failure policies must you define yourself? |

The local baseline is Python 3.12.10. Documentation for newer releases can describe behavior
that does not apply to that interpreter. Read version notes, report the interpreter used and
do not turn a local measurement into a universal performance claim.

## Concurrency reasoning

For each unit of work, identify who owns it, who can cancel it and who waits for cleanup.
Bound task creation and queues rather than merely adding workers. A timeout controls waiting;
it does not necessarily undo a completed side effect or forcibly stop underlying work. Use
events and fake clocks in tests when possible instead of exact wall-clock assertions.

## Advanced typing reasoning

Annotations express expectations to tools and readers. They do not replace validation at an
untrusted boundary. Prefer a small meaningful protocol to an elaborate type hierarchy. Explain
whether an interface reads, mutates or retains an argument: this often matters more than adding
another generic parameter.

## Review evidence

A lab is complete when its prediction, actual observation, explanation and regression assertion
are recorded. Reading an API page alone is not completion. If you already know the assigned
behavior, use the same time to reproduce a subtler failure or audit an existing solution against it.
