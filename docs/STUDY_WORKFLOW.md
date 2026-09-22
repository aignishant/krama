# Study separately and record honestly

Run commands from the repository root. `python course.py start N --track dsa` (or sd/lang)
prints the path and assignment. `python course.py practice N` runs that day's DSA example tests.
The tool never opens a GUI, edits progress automatically, or commits your work.

Subject folders now include their topic, for example `dsa_pair-sum-indices`. Keep passing
`--track dsa`, `sd` or `lang`; the manifest resolves the current path. Historical evidence paths
in append-only ledgers can be translated with [folder_renames.json](folder_renames.json).
Reopen old IDE tabs under the new folder name.

For DSA, [LEETCODE_INDEX.md](LEETCODE_INDEX.md) links each day's online assignment. Record actual
submission outcomes in NOTES.md or append to [LEETCODE_PROGRESS.csv](LEETCODE_PROGRESS.csv).
You can satisfy the daily attempt through the online or local route described in LEETCODE.md;
the local practice command never submits to LeetCode.

## Independent progress

### Recall previous topics without practice

Open one shared file: [DSA recall](DSA_RECALL.md), [Python recall](LANG_RECALL.md), or
[system design recall](SD_RECALL.md). Use its index to reread the cards for topics you have
studied. No new solve, lab, memo, or test run is required for this quick reading mode.
Open the linked full explanation only if you need depth.

Cards are added when teaching documents are expanded. They do not mark study complete. Use
the latest event for the relevant day and track in TRACK_PROGRESS.csv to select recorded
completed topics; track progress may differ between DSA, Python, and system design.
Scheduled weekly cold assessments remain a separate activity with their own acceptance criteria.

### Record actual study

Append events to TRACK_PROGRESS.csv; keep old events. Allowed tracks: dsa, sd, lang.
Allowed statuses: not-started, partial, needs-review, complete. Example syntax only:

```csv
1,dsa,partial,2026-09-18,days/day-001-count-target-values/dsa_count-target-values/NOTES.md,Baseline written; add boundary tests
1,lang,complete,2026-09-18,days/day-001-count-target-values/lang_identity-and-equality/NOTES.md,Experiment and explanation recorded
```

Use your real dates and evidence. The latest event for each day/track is current. Quote CSV
fields containing commas. `python course.py status` shows counts and the first unfinished day
for each track. A complete flag is self-reported, not a certificate from the checker.

Check the boxes in each subject README only after its acceptance criteria pass. When all three
tracks for a day pass, tick its CHECKLIST and append the aggregate row to PROGRESS.md. Example:

```text
| 1 | actual-date | DSA-01, SD-01, PY-01 | links to the three evidence files | yes |
```

Then run `python granth.py index`. Assignment hubs intentionally claim no completed IDs; if
you want the upstream traceability view to reflect earned completion, set that day's hub ids
to exactly its assigned IDs only after all three gates pass. This is separate from authoring
full teaching chapters. Do not mark a subject complete because another subject is finished.

## Catch-up

Use the seventh session for unfinished core work, cold re-solves and a failure review. Keep
budgets unchanged. If a track stays behind, add calendar sessions to that track; never borrow
the Python or design budget silently. Resume from the first unfinished subject session.

REVIEW_QUEUE.csv schedules DSA recall at +1/+7/+21 study-day offsets. Pick one due recall in the
daily recall slot; use weekly sessions for full re-solves. After the course, due dates beyond
168 form optional maintenance. MISTAKES.csv records failed assumptions and minimal examples.
