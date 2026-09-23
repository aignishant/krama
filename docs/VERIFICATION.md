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
