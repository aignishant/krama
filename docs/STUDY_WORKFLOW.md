# Study separately and record honestly

Run commands from the repository root. `python course.py start N --track dsa` (or sd/lang)
prints the path and assignment. `python course.py practice N` runs that day's DSA example tests.
The tool never opens a GUI, edits progress automatically, or commits your work.

## Independent progress

Append events to TRACK_PROGRESS.csv; keep old events. Allowed tracks: dsa, sd, lang.
Allowed statuses: not-started, partial, needs-review, complete. Example syntax only:

```csv
1,dsa,partial,2026-09-18,days/day-001-count-target-values/dsa/NOTES.md,Baseline written; add boundary tests
1,lang,complete,2026-09-18,days/day-001-count-target-values/lang/NOTES.md,Experiment and explanation recorded
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
