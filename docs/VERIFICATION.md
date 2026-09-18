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
