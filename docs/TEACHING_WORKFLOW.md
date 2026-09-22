# Learn the topic before attempting the problem

Every subject README is the entry point. Its navigation section answers: where do I start,
what will I learn there, when should I open the assignment, and where does my work belong?
Use this order for every future day that is expanded, across DSA, system design, and Python.

## Reading order

1. **Learn:** open CONCEPTS.md for the topic explanation. If the day has several teaching
   documents, this entry point lists them in prerequisite order.
2. **Trace:** work through a small teaching example and explain why each state change happens.
3. **Check readiness:** answer the short questions before opening the assigned problem. If
   a concept is unclear, return to its explanation rather than guessing at code.
4. **Attempt:** read the assignment's exact contract, compare it with the mechanism just learned,
   and produce your own solution, design, or experiment.
5. **Verify:** test a boundary and a plausible mistake, then explain why the result is correct.
6. **Record:** save actual evidence, help used, remaining uncertainty, and a next step.

For a cold review, recall the mechanism without notes first. Reread explanations after the cold
attempt or when deliberately repairing a gap, and record the help used. A review should still
offer navigation to the original teaching material.

## What a complete topic explanation contains

Use the vendored teaching contract's motivation, mechanism, observed failure, production, and
check sections. Make the following content explicit within them; headings alone are insufficient.

| Content | What the learner should understand |
| --- | --- |
| Prerequisites and vocabulary | The few concepts needed now, explained or linked precisely |
| Motivation and intuition | What difficulty the technique addresses, with a concrete example |
| Recognition cues | Which features of an input or requirement suggest this technique |
| State or representation | What information is retained, what is discarded, and why that is sufficient |
| Step-by-step mechanism | A hand trace or object/request diagram before a finished demonstration |
| Correctness | The reason every step is valid and the final state meets the intended contract |
| Cost and tradeoffs | Where the work or memory goes and when another approach fits better |
| Limits and failure | A violated assumption, a distinguishing counterexample, and observed failure evidence |
| Readiness | Questions that require explaining or tracing the mechanism before attempting the assignment |

In DSA, teach the pattern and the reason it saves work. The useful “trick” is an explained
invariant, representation, or reused computation, not a memorized code template. If a LeetCode
companion needs an additional idea, teach that idea before sending the learner to it. Separate
core reading from optional depth, and explain which route needs each section.

In system design, teach the decision framework and its tradeoff with a worked example before
asking for a memo. In Python, explain the language or runtime model and trace it before the
learner implements a prediction-driven experiment. Assume experienced Python syntax knowledge.

## Teaching versus hints

Explain general counting, frequency tables, invariants, or other assigned concepts openly in
the teaching documents. A student does not need to fail first to receive the lesson.
HINTS.md is for progressively stronger help applying those ideas to the particular exercise.
Complete teaching demonstrations use a separate example; learner solution files and personal
evidence stay under learner control. “Complete day documents” means finish the instruction and
navigation, not fill in TODO(me) exercises or mark the day studied.

## Navigation in each README

Place a numbered `Navigation — where to start` section immediately after the title. Link the
explanation first, then its worked example/readiness check, the assignment, implementation or
design file, verification steps, and evidence. Explain each destination's purpose. For DSA,
show LeetCode and local practice as alternative routes within one hour and identify hints as
help for after an attempt. Include a way back to the day hub.

A day with a full topic lesson must link CONCEPTS.md. A future day that still has only a brief
must label its shared guide as preparation and state that the full topic explanation is not yet
expanded. A link to a broad guide does not count as authoring the day's teaching material.

## Future day authoring and validation

Every expansion must also add a compact day card to the matching common file:
[DSA_RECALL.md](DSA_RECALL.md), [LANG_RECALL.md](LANG_RECALL.md), or
[SD_RECALL.md](SD_RECALL.md). Keep one file per track, with cards in day order and an index.
Each card states the recognition cue, central mechanism, why it works, costs or tradeoffs,
one small memory anchor, and the main trap. Link the full lesson and personal evidence.
Keep the card short enough to reread directly; do not require a practice task, command,
questionnaire, or new implementation to use recall mode. Add a link from every subject README.

Cards summarize authored lessons, not learner achievements. Keep actual completion exclusively
in the independent track ledger, and tell readers to select days they have studied. Do not
prefill cards for all planned topics or silently mark newly documented topics complete.
Quick recall is separate from the scheduled weekly cold assessments; it does not change their
requirements or count as their completion.

Read the existing track files and preserve any learner work. Write the requested day's concept
explanations before expanding its assignment. Link related teaching parts from CONCEPTS.md in
reading order, replace the README's preparation notice with the real lesson link, and connect
the assignment back to the relevant explanation. Include the explanation in the day checklist.

Keep the core 60/30/15-minute budgets. Deeper reading may need another sitting; label it clearly
and let the learner record partial progress. Do not silently grow the mandatory practice quota.

Verify sources when used and execute teaching code before recording its output. Run
`python course.py check`, check navigation links and their order, and confirm learner files
and progress have not been modified by document authoring. Report which days have full lessons
and which only have navigation or preparation guides.
