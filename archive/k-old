#!/usr/bin/env bash
# k — the Krama daily driver. Six commands run 230 days.
set -euo pipefail
cd "$(dirname "$0")"

RUN="uv run"
DAYS="days"
DOCS="docs"

die() { printf '\033[31m%s\033[0m\n' "$*" >&2; exit 1; }
ok()  { printf '\033[32m%s\033[0m\n' "$*"; }

day_dir() {  # day_dir N -> the day's folder, or empty if the day is not on disk yet
  local n="$1"                       # folders are day-NN-<slug>, so the shelf reads as a shelf
  local -a hits=()
  while IFS= read -r line; do hits+=("$line"); done < <(
    find "$DAYS" -mindepth 1 -maxdepth 1 -type d -name "$(printf 'day-%02d-*' "$n")" | sort
  )
  case ${#hits[@]} in
    0) : ;;
    1) printf '%s\n' "${hits[0]}" ;;
    *) die "day $n has ${#hits[@]} folders (${hits[*]}) — one day, one folder" ;;
  esac
}

usage() {
  cat <<'EOF'
usage: ./k <command> [args]

  status            progress, computed from disk and the index
  start N           print day N's hub and list its parts in reading order
  scaffold N        create the day's lab/ from the stubs
  depth N           enforce the Part 11 depth contract on day N
  check             ruff + format + offline pytest + depth on every written day
  done N            commit gate: checklist ticked, checks green, tracker regenerated
  ladder PREFIX     print every catalogued problem for a prefix or concept id
  miss ID           log a concept you got wrong (e.g. ./k miss BSR-03)
EOF
}

cmd_status() { $RUN python scripts/tracker.py --print; }

cmd_start() {
  local d; d=$(day_dir "$1")
  [ -n "$d" ] && [ -f "$d/LESSON.md" ] \
    || die "day $1 is not written yet. Write it with:  /day-krama $1"
  ${PAGER:-cat} "$d/LESSON.md"
  if [ -d "$d/parts" ]; then
    echo; ok "parts, in reading order:"
    find "$d/parts" -name '*.md' | sort
  fi
}

cmd_scaffold() {
  local n="$1" d; d=$(day_dir "$n")
  [ -n "$d" ] || die "day $n has no folder yet — write the day first, or create days/$(printf 'day-%02d' "$n")-<slug>/"
  mkdir -p "$d/lab"
  [ -f "$d/lab/implement.py" ] && die "lab already exists at $d/lab — refusing to overwrite your work"
  cat > "$d/lab/implement.py" <<PY
"""Day $n — your implementation. You type every line."""


def solve():  # replace with the signature from the hub's build brief
    """See $d/LESSON.md's build brief for the contract: pre, post, time, space."""
    raise NotImplementedError
PY
  cat > "$d/lab/reference.py" <<PY
"""Day $n — the oracle. Brute force. Correct by inspection. Slow is fine."""


def solve():
    raise NotImplementedError
PY
  cat > "$d/lab/test_implement.py" <<PY
"""Day $n — property-based tests against the oracle."""
from hypothesis import given, strategies as st

from implement import solve as implement
from reference import solve as reference


@given(st.lists(st.integers()))
def test_matches_reference(xs: list[int]) -> None:
    assert implement(xs) == reference(xs)


def test_edge_battery() -> None:
    for xs in ([], [0], [1, 1, 1], [1, 2, 3], [3, 2, 1], [-1, -2], [0] * 1000):
        assert implement(xs) == reference(xs), xs
PY
  cat > "$d/lab/bench.py" <<'PY'
"""Doubling benchmark. The ratio column is the proof; the wall clock is noise."""
import random
import time

from implement import solve


def main() -> None:
    random.seed(20260823)
    prev = None
    print(f"{'n':>10} {'seconds':>12} {'ratio':>8}")
    n = 1_000
    for _ in range(7):
        xs = [random.randint(-10**6, 10**6) for _ in range(n)]
        t0 = time.perf_counter()
        solve(xs)
        dt = time.perf_counter() - t0
        ratio = f"{dt / prev:8.2f}" if prev else "       -"
        print(f"{n:>10} {dt:>12.6f} {ratio}")
        prev, n = dt, n * 2


if __name__ == "__main__":
    main()
PY
  cat > "$d/lab/conftest.py" <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
PY
  ok "scaffolded $d/lab — implement.py is a stub, and stays a stub until you fill it"
}

cmd_depth() { $RUN python scripts/depth_check.py "$1"; }

cmd_check() {
  $RUN ruff format --check .
  $RUN ruff check .
  $RUN pytest days -q
  $RUN python scripts/depth_check.py --all
  ok "all checks green"
}

cmd_done() {
  local n="$1" d; d=$(day_dir "$n")
  [ -n "$d" ] || die "day $n has no folder yet"
  [ -f "$d/CHECKLIST.md" ] || die "no CHECKLIST.md in $d"
  if grep -q '^\- \[ \]' "$d/CHECKLIST.md"; then
    echo "unticked boxes remain:"; grep -n '^\- \[ \]' "$d/CHECKLIST.md"
    die "refusing to commit day $n"
  fi
  if grep -qi 'gate' "$d/CHECKLIST.md" && [ -f "$d/NOTES.md" ] && [ ! -s "$d/NOTES.md" ]; then
    die "gate day with an empty NOTES.md — write down what you kept getting wrong"
  fi
  cmd_check
  $RUN python scripts/tracker.py --write
  git add -A
  git commit -m "day $n complete"
  ok "day $n committed; docs/TRACKER.md regenerated"
}

cmd_ladder() {
  local q="$1"
  [ -f "$DOCS/PROBLEM_INDEX.md" ] || die "no docs/PROBLEM_INDEX.md"
  ok "problems tagged $q"
  grep -E "^\|.*\b${q}(-[0-9]{2})?\b" "$DOCS/PROBLEM_INDEX.md" \
    | awk -F'|' '{printf "  %-52s %-9s %-8s %s\n", $2, $3, $5, $6}' \
    || die "nothing catalogued for $q — add it to docs/PROBLEM_INDEX.md first"
}

cmd_miss() {
  local id="$1"
  mkdir -p "$DOCS"
  [ -f "$DOCS/MISSES.md" ] || printf '# Misses — concept IDs I got wrong\n\nGate days read this file first.\n\n' > "$DOCS/MISSES.md"
  printf -- '- `%s` — %s\n' "$id" "$(date +%Y-%m-%d)" >> "$DOCS/MISSES.md"
  ok "logged $id"
}

case "${1:-}" in
  status)   cmd_status ;;
  start)    cmd_start "${2:?day number}" ;;
  scaffold) cmd_scaffold "${2:?day number}" ;;
  depth)    cmd_depth "${2:?day number}" ;;
  check)    cmd_check ;;
  done)     cmd_done "${2:?day number}" ;;
  ladder)   cmd_ladder "${2:?concept id or prefix}" ;;
  miss)     cmd_miss "${2:?concept id}" ;;
  *)        usage ;;
esac
