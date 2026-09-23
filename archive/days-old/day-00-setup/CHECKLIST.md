# Day 0 — Checklist

`./k done 0` refuses to commit until every box is ticked.

## Toolchain
- [ ] `uv` installed; `uv python install 3.12` done
- [ ] `uv sync` succeeded and `.venv/` exists
- [ ] `uv run ruff --version` and `uv run pytest --version` both print
- [ ] Repo cloned, `./k status` runs and prints 0 days complete

## Read
- [ ] `FND-01` — the six clauses of the contract, and what each one costs me
- [ ] `FND-02` — why `reference.py` exists and what Hypothesis shrinking does
- [ ] `FND-03` — the ten sections, and the reading protocol for each
- [ ] `FND-04` — the six commands and the three things `./k done` refuses on

## Build
- [ ] Wrote the O(n²) `running_max` first, on purpose
- [ ] Ran `bench.py` on it and looked at the ratio column
- [ ] Wrote the O(n) version from an empty file
- [ ] Ran `bench.py` again; the two ratio columns are visibly different
- [ ] `uv run pytest days/day-00-setup/lab -q` green, Hypothesis included

## Gate
- [ ] All six gate questions answered out loud, without notes
- [ ] `docs/MISSES.md` exists (even if empty) and I know what `./k miss` does
