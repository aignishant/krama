# Krama course operating rules

Read docs/00_MASTER_PLAN.md and docs/adr/ADR-0001-the-plan-as-adopted.md first.
The user's 60/30/15-minute budget and dsa_<topic>/sd_<topic>/lang_<topic> layout override Granth's no-clock/shared-parts
defaults. Python assumes five years of experience. Preserve independent study progress.
The current deliverable is a guided assignment course; never call its briefs full depth-checked
teaching chapters. Use course.py check for the actual format and granth.py doctor/index for
planning. granth.py is preserved verbatim from vendor/granth/SKILL.md.

Current plan: v1.1.0. Read ADR-0002 for topic-folder naming and product-company interview
practice. Resolve directories through docs/sessions.json. Each DSA day includes LEETCODE.md;
use the same daily hour and flag contract differences and premium alternatives. Company names
express the user's preparation goal, not verified question-frequency claims. Do not run the
archived v1.0 build script to regenerate an active course.

Read existing files before editing them. Do not overwrite learner solutions or notes. Never
complete learner TODO(me) exercises unless specifically requested. Record actual failures and
source checks, not reconstructed outputs. Do not restore old Git deletions or commit without
authorization. In particular do not invoke granth.py done, which stages the whole repository.

When expanding a day, work inside the requested subject folder, consult the full vendored
Granth teaching contract, verify exact interfaces, and keep core assignment versus optional
deep reading explicit. No assumption that finishing DSA is required before opening Python.

For every day expansion, follow docs/TEACHING_WORKFLOW.md: teach the topic and the reasoning
behind its techniques before directing the learner to practice. Each subject README needs
linked navigation in reading order. CONCEPTS.md is the teaching entry point; explain any
additional mechanism required by the LeetCode companion. General instruction is not a hint
to withhold until failure. Future briefs must label preparation guides honestly until expanded.

Every expanded subject also contributes a short card to docs/DSA_RECALL.md, docs/LANG_RECALL.md,
or docs/SD_RECALL.md. Link that file from its README for optional recall without practice.
Preserve day order and distinguish summary availability from completion in TRACK_PROGRESS.csv.

Expanded SD days must include a complete REFERENCE_DESIGN.md answering the actual assignment
with assumptions, artifact/calculation, decision, alternative, failure walkthrough, and self-review.
The assistant authors that file; DESIGN.md and its TODO(me) sections belong to the learner.
Link both roles clearly and permit guided reading before practice or comparison afterwards.
Preserve cold reviews, the 30-minute budget, learner work, and independent completion criteria.
See docs/adr/ADR-0003-system-design-reference-and-practice.md and docs/TEACHING_WORKFLOW.md.
