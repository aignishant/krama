---
name: day-krama
description: Expand one Krama subject assignment into teaching parts while preserving its practice and the user's independent daily budgets.
---

Read CLAUDE.md, the master plan, ADR-0001 and the requested day's subject files. Ask which subject
only if it is genuinely ambiguous; a request for all three means all three. Use the vendored
Granth SKILL.md's full teaching contract for depth, but keep parts within the manifest's dsa_<topic>/, sd_<topic>/ or lang_<topic>/ folders
and preserve the 60/30/15-minute core assignment. Mark deeper reading optional. Inspect that
track's progress rather than blocking on another track. Never overwrite learner code or notes.
Use one idea per document, a plain-language explanation, mechanism, observed failure, production
implication and a check. Keep exercise solutions unsolved. Verify sources when used. Run
python course.py check after writing, and report exactly which teaching documents were added.

For every requested day, follow docs/TEACHING_WORKFLOW.md. Write the topic explanation before
the practice directions: intuition, recognition cues, state, a worked trace, why it works,
costs, limits, and readiness questions. CONCEPTS.md is the entry point and links any further
teaching parts in order. Explain the general technique openly, including any extra mechanism
needed by a LeetCode companion; keep exercise-specific rescue hints separate.

Put numbered navigation immediately after each subject README title: learn, trace/check
readiness, open the assignment, implement, verify, record. When expanding a future brief,
replace its preparation-guide notice with a link to the completed topic explanation and
add backlinks from practice. Preserve cold recall on review days. Completing documents never
means completing the learner's exercises or study ledger.

Extend the corresponding common recall file (docs/DSA_RECALL.md, docs/LANG_RECALL.md, or
docs/SD_RECALL.md) whenever a subject's lesson is expanded. Add an indexed day card with the
idea, recognition cue, mechanism, reason, tradeoff, memory anchor, and trap. Link the full
lesson and learner evidence. Recall requires no exercise or code execution; retain separate
weekly cold assessments. Link recall from each README and never infer learner completion
from the presence of a lesson or summary card.
