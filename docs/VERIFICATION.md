# Course verification — 2026-09-18

Executed with the locally observed Python 3.12.10.

| Check | Observed result |
| --- | --- |
| `python course.py check` | Passed: 168 days, 504 subject folders, 504 unique outcome IDs, budgets, links, fixtures, syntax and preserved upstream code. |
| `python granth.py doctor` | Passed: plan markers, ledgers and unique day-to-ID assignments. |
| `python granth.py index` | Generated 173 index documents. |
| `python granth.py check` | Passed: adapted structural check, upstream depth scan and current generated indexes. |
| `python scripts/test_course_tools.py` | Five tests passed: independent latest-event progress, required completion evidence, malformed CSV rejection, unknown day rejection, and correct/wrong-answer runner behavior. |
| `python granth.py brief 1` | Allowed day 1. |
| `python granth.py brief 6` | Printed STOP for an out-of-order whole-course authoring request. |
| `python course.py practice 1` | Intentionally failed with `NotImplementedError: TODO(me): solve the core exercise`. |
| `python course.py status` | All three tracks start at 0/168, next day 1. |

The tool tests initially encountered Windows temporary-directory permission errors in the sandbox;
the authorized rerun outside the sandbox passed. No learner progress was recorded by the tests.

Structural success does not imply that learner exercises are solved. Upstream depth reports
no written full chapters: this deliverable contains assignment hubs and practice workspaces,
not the optional eleven-section Granth teaching chapters. Example fixtures are smoke checks;
the learner adds adversarial cases as part of each DSA practice session. No benchmark or
system-design workload estimate is represented as a measured production result.

## v1.1.0 update — 2026-09-19

- Renamed all 504 subject folders to track plus topic; retained all day numbers and objective IDs.
- Compared SHA256 values after migration: all 1,176 protected learner files remained byte-identical.
- Added 168 LeetCode guides: one companion on each topic day and two prior companions on each review day.
- Linked 140 distinct problems. Verified 138 public problem records; confirmed title/access gates for two Premium companions with local alternatives. Jump Game was verified through its official description URL after its base URL timed out.
- `python course.py check`, `python granth.py doctor` and `python granth.py check` passed.
- Regenerated 173 Granth index documents at v1.1.0.
- All seven course-tool tests passed, including stable track aliases and rejection of a manifest path escaping its subject folder.
- `python course.py practice 10` reached the renamed directory and failed on the untouched `NotImplementedError` starter, as expected.
- Track progress remains unchanged. No learner exercise was solved and no commit was created.

## Days 13–16 documentation expansion — 2026-09-22

- Added 12 topic explanations and four complete SD reference answers; updated reading routes,
  day hubs, checklists, LeetCode contract comparisons, recall cards, and availability indexes.
- Preserved Day 14's two cold DSA re-solves and deferred review explanations/reference answers
  until after cold attempts. The daily 60/30/15-minute caps remain unchanged.
- Executed all 12 new Python teaching blocks on Python 3.12.10 and matched their recorded
  output, including deliberate failures. These are author demonstrations, not learner results.
- Checked 695 local documentation links, including heading anchors; all resolved.
- Compared SHA256 values for 1,010 learner/progress files captured before authoring; all
  remained byte-identical. Earlier working-tree changes were preserved.
- `python course.py check`, `python granth.py doctor`, and `git diff --check` passed.
- Official Python, PostgreSQL, HTTP/timestamp, and LeetCode pages were checked; dated addresses
  and uses are in [SOURCES.md](SOURCES.md). SQL and HTTP reference artifacts are explicitly
  hypothetical designs, not executed service tests or production measurements.
- Days 1–16 now have expanded topic lessons and SD references. Days 17–168 retain assignment
  briefs and preparation navigation. No study completion or commit was recorded.

## Days 17–20 documentation expansion — 2026-09-22

- Added 12 topic explanations and four complete SD reference answers for container capacity,
  fixed windows, distinct substrings, positive windows, and their independent SD/Python tracks.
- Connected subject reading routes, day hubs, checklists, precise LeetCode contract comparisons,
  12 recall cards, the reference index, glossary, and teaching-availability notices.
- Executed all 12 new Python teaching blocks on Python 3.12.10 and compared captured output
  with each recorded transcript. All matched, including the deliberately caught failures.
- Checked 760 local links, including heading anchors, across 70 relevant documents; all resolved.
  Verified that the four new recall cards in each track have unique headings and linked routes.
- Compared SHA256 hashes of 1,179 captured learner/progress files; all remained byte-identical.
  Existing exercises, personal notes, design attempts, fixtures, and study ledgers were preserved.
- `python course.py check`, `python granth.py doctor`, and `git diff --check` passed.
- Opened official Python, PEP, LeetCode, Twelve-Factor, API compatibility, and architecture pages;
  their dated uses appear in [SOURCES.md](SOURCES.md). Reference service behavior and numeric
  budgets are hypothetical designs, not executed deployment tests or performance measurements.
- `python granth.py check` also passed; all 173 generated documents remain current. Its upstream
  depth scan does not assess these adapted topic-folder lessons, as documented in the master plan.
- Days 1–20 now have expanded topic lessons and complete SD references. Days 21–168 retain
  assignment briefs and preparation navigation. The 60/30/15-minute caps remain unchanged.
  No learner study completion or commit was recorded.

## Days 25–28 documentation expansion — 2026-09-23

- Added 12 topic explanations and four complete SD reference answers for integer square root,
  shipping capacity, median partitioning, the Week 4 review, and their independent SD/Python tracks.
- Added 12 new recall cards and connected reading routes, hubs, checklists, and precise
  LeetCode contract comparisons. Connected the existing Days 21–24 lessons and references to
  their unfinished navigation and added their 12 missing recall cards.
- Preserved cold attempts before repair reading on Days 21 and 28. Clarified the two scheduled
  DSA re-solves within the 60-minute gate; SD and Python retain their 30/15-minute caps.
- Executed the 12 new Python teaching blocks on Python 3.12.10, including deliberate failures,
  and independently re-executed the authored Markdown blocks. All recorded transcripts matched.
- Checked 1,023 local Markdown links, including heading anchors, across the changed and new
  teaching/navigation documents; all resolved.
- The working tree was clean before authoring. Git comparison confirms no changes to learner
  solutions, labs, fixtures, notes, DESIGN.md files, or either study progress ledger.
- `python course.py check` and `python granth.py doctor` passed. The former validates the
  adapted course format; neither tool certifies learner mastery or production behavior.
- Opened the official sources listed in the dated [source ledger](SOURCES.md). PostgreSQL
  schedules, SQL templates, and HTTP reference designs were not deployed or tested against
  concurrent database sessions. Their assumptions and proposed next checks are explicit.
- Days 1–28 now have connected topic lessons, recall cards, and complete SD references.
  Days 29–168 retain assignment briefs and preparation navigation. No learner completion
  was recorded and no commit was created.
- The first `python granth.py check` reported 173 stale generated documents. Ran
  `python granth.py index`, then reran the check successfully; all 173 generated documents
  are current. Its upstream depth scan does not inspect these adapted topic-folder lessons.
  `git diff --check` also passed.

## Days 29–36 documentation expansion — 2026-09-23

- Added 24 topic explanations and eight complete SD reference answers. Connected subject
  navigation, day hubs, checklists, practice routes, 24 recall cards, the SD reference index,
  glossary, and teaching-availability notices. Days 1–36 are expanded; Days 37–168 retain
  assignment briefs and preparation navigation.
- Explained companion-contract differences for stable record sorting, closed versus half-open
  intervals, kth largest versus smallest, reverse pairs versus inversions, and linked-list
  heads versus local serialization. Day 34 teaches the separate reverse-pair counting pass.
- Preserved Day 35 cold attempts before repair reading. Clarified its two DSA re-solves and
  corrected the contradictory note that one unresolved problem could replace both slots.
  The 60/30/15-minute caps and independent assessment criteria remain in place.
- Executed all 24 teaching blocks on Python 3.12.10, then independently extracted and reran
  them from the authored Markdown. Every recorded transcript matched, including deliberate
  failures and the scoped slots memory measurements.
- Checked 1,347 local links and heading anchors across 129 documents; all resolved. All three
  recall files contain exactly one card per authored day in order, Days 1–36.
- Compared SHA256 hashes for 1,179 learner/progress files captured before authoring; all stayed
  byte-identical. Existing uncommitted work was preserved. Solutions, labs, fixtures, personal
  notes, DESIGN.md files, and study ledgers were not filled or marked complete.
- `python course.py check`, `python granth.py doctor`, `python granth.py check`, and
  `git diff --check` passed. All 173 generated documents were already current; no regeneration
  was needed. The upstream depth check does not inspect this adapted topic-folder layout.
- Official-source checks and the unavailable B-tree implementation subpage are recorded in
  [SOURCES.md](SOURCES.md). The page split, storage budgets, retention policy, query projection,
  and cache failure scenarios are explicitly hypothetical. No database, cache, replication
  system, or production performance claim was tested by the Python models.
- No learner completion or commit was recorded.

## Days 37–40 documentation expansion — 2026-09-23

- Added 12 topic explanations and four complete SD reference answers. Connected subject
  navigation, day hubs, checklists, practice routes, 12 recall cards, the SD reference index,
  glossary, and teaching-availability notices. Days 1–40 now have expanded teaching across
  all three tracks; Days 41–168 retain assignment briefs and preparation navigation.
- Clarified online node-return interfaces versus local values, indices, and serialization.
  Day 38 explains why pos is construction metadata rather than a detection shortcut.
  The pointer proofs cover even-length ties, cycle entry, identity-preserving merges, and
  the exact gap/stopping-rule pair for removing a node from the end.
- Executed all 12 teaching blocks on Python 3.12.10, then extracted and reran them from
  the authored Markdown. All recorded output matched, including deliberate failure examples.
- Checked 1,002 local links and heading anchors across 54 teaching/navigation documents;
  all resolved. Each recall file has exactly one indexed card per day for Days 1–40, in order.
- Compared SHA256 hashes for 1,181 learner/progress files captured before authoring; all
  remained byte-identical. Solutions, labs, tests, fixtures, notes, DESIGN.md files, and
  study ledgers were preserved. No learner completion or commit was recorded.
- `python course.py check`, `python granth.py doctor`, `python granth.py check`, and
  `git diff --check` passed. All 173 generated documents were already current. The upstream
  depth checker does not inspect the adapted topic-folder teaching layout, so this is not
  a claim of upstream depth certification or learner mastery.
- `python granth.py brief 37`, `38`, `39`, and `40` each returned a nonzero completion-order
  guard because the whole-day learner ledger still starts at Day 1. Documentation authoring
  continued under the master plan's independent authoring/study distinction, ADR-0001, and
  the explicit request for the next four documents; no study gate or day order was changed.
- Primary-source checks are listed in [SOURCES.md](SOURCES.md). SD calculations use explicit
  hypothetical inputs. The cache examples are deterministic models, not deployed concurrency,
  performance, authorization, or clock tests. Freshness bounds remain conditional on their
  stated assumptions, and the reference designs identify the checks needed to validate them.
