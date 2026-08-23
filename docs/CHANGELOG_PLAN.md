# Plan changelog

Newest first. Every syllabus change lands here; anything structural also gets an ADR.

## v1.1.1 — 2026-08-23

- **Folders are named for what is inside them.** A day is `days/day-NN-<kebab-slug>/` and a
  section is `parts/NN-<kebab-slug>/`, so `ls days/` and `ls parts/` read as tables of contents
  instead of lists of numbers. `days/day-01/parts/02/2.1-the-ram-model.md` became
  `days/day-01-what-computation-costs/parts/02-model-of-computation/2.1-the-ram-model.md`.
  `CLAUDE.md` Rule 1 and plan Part 6 restated accordingly.
- **Days are still addressed by number.** `./k`, `scripts/depth_check.py` and
  `scripts/tracker.py` now find a day by globbing `day-NN-*` rather than composing the path, so
  a slug can be improved later without touching a command or a stored number.
- **`./k depth N` enforces the shapes** — day folder, section folder, part filename, and that a
  part's front-matter `section` agrees with the folder it sits in. A bare `parts/02/` now fails.

## v1.1.0 — 2026-08-23

- **Track II added: system design, Days 231–308.** Ten phases (33–42), 85 new concept IDs,
  two new gates per phase area, and a second capstone that must survive its own load test.
  Total: 309 day-slots, 43 phases, 357 concept IDs. See ADR 0002.
- **`docs/PROBLEM_INDEX.md` added** — the whole curriculum's problem set (386 entries) keyed to
  concept IDs, plus a 16-drill design bank and 8 critique prompts. Day ladders are now *selected*
  from the catalogue rather than invented at writing time (`CLAUDE.md` Rule 13).
- `./k ladder <PREFIX>` added.
- `CLAUDE.md` Rules 13–15 added (catalogue sourcing, the Track II drill ladder, capacity
  arithmetic must be shown).
- Skill gains `reference/design_day.md`: what changes for Days 231–308 — §6 without an algorithm,
  §7 as capacity arithmetic, and the hinge back to Days 210–214.
- `tests/test_repo_integrity.py` extended: every catalogued problem must target a concept ID some
  day actually owns, must carry a "really testing" line, and may not be listed twice as primary
  unless explicitly marked as a cross-listing.

## v1.0.0 — 2026-08-23

- Initial plan. 33 phases, 231 day-slots (Day 0 + Days 1–230), 272 concept IDs.
- Depth contract v1.0.0 established (Part 11): ten sections per part, with §7 "the cost,
  derived" added as a DSA-specific section beyond the general-purpose doc standard.
- Two exemptions from the `parts/` rule documented: Day 0 (orientation) and gate days.
- `./k` driver, `scripts/depth_check.py`, `scripts/tracker.py` established.
