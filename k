#!/usr/bin/env bash
# k — the Krama daily driver. Five commands run 180 days.
set -euo pipefail
cd "$(dirname "$0")"

PY="python"
command -v uv >/dev/null 2>&1 && PY="uv run python"

die() { printf '\033[31m%s\033[0m\n' "$*" >&2; exit 1; }

day_dir() {  # day_dir N -> the day's folder, or empty
  local n="$1"
  find days -mindepth 1 -maxdepth 1 -type d -name "$(printf 'day-%03d-*' "$n")" | sort | head -1
}

usage() {
  cat <<'EOF'
usage: ./k <command> [args]

  status        progress on both tracks, computed from disk
  day N         print day N's hub and list its files
  next          the first day that is not written yet
  check [N]     verify written lessons against the format contract
  build         create any missing day folders and placeholders

  write a day with:  /day-krama N
EOF
}

case "${1:-}" in
  status) $PY scripts/status.py ;;

  day)
    [ $# -ge 2 ] || die "usage: ./k day N"
    d=$(day_dir "$2")
    [ -n "$d" ] || die "day $2 has no folder — run ./k build"
    ${PAGER:-cat} "$d/README.md"
    printf '\n\033[32mfiles:\033[0m\n'
    find "$d" -maxdepth 1 -name '*.md' | sort
    ;;

  next)
    $PY scripts/status.py | grep -A2 '^  Next:' || echo "all 180 days written"
    ;;

  check)
    if [ $# -ge 2 ]; then $PY scripts/check_day.py "$2"; else $PY scripts/check_day.py; fi
    ;;

  build) $PY scripts/build_skeleton.py "${2:-}" ;;

  *) usage ;;
esac
