"""Independent study navigation and validation for the adapted Granth course."""
from __future__ import annotations

import argparse
import ast
import csv
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
TRACKS = ('dsa', 'sd', 'lang')
STATUSES = {'not-started', 'partial', 'needs-review', 'complete'}


def sessions(root=ROOT):
    return json.loads((root / 'docs/sessions.json').read_text(encoding='utf-8'))


def get_session(day, root=ROOT):
    result = next((s for s in sessions(root) if s['day'] == day), None)
    if result is None:
        raise ValueError(f'No day {day}; choose a day from 1 to 168.')
    return result


def track_folder(entry, track):
    """Resolve stable CLI track names to the manifest's topic-named directories."""
    if track not in TRACKS:
        raise ValueError(f'Unknown track: {track}')
    name = entry['track_folders'][track]
    if not re.fullmatch(rf'{track}_[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError(f'Invalid topic folder: {name}')
    return name


def read_progress(root=ROOT):
    latest = {}
    valid_days = {s['day'] for s in sessions(root)}
    path = root / 'docs/TRACK_PROGRESS.csv'
    with path.open(encoding='utf-8', newline='') as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ['day', 'track', 'status', 'date', 'evidence', 'notes']:
            raise ValueError('TRACK_PROGRESS.csv has invalid column names.')
        for line, row in enumerate(reader, 2):
            if None in row or any(v is None for v in row.values()):
                raise ValueError(f'Track ledger line {line}: wrong column count; quote commas.')
            try:
                day = int(row['day'])
            except ValueError:
                raise ValueError(f'Track ledger line {line}: day must be an integer.') from None
            if day not in valid_days or row['track'] not in TRACKS or row['status'] not in STATUSES:
                raise ValueError(f'Track ledger line {line}: invalid day, track or status.')
            if row['status'] == 'complete' and (not row['date'] or not row['evidence']):
                raise ValueError(f'Track ledger line {line}: completion needs date and evidence.')
            latest[(day, row['track'])] = row
    return latest


def validate(root=ROOT):
    errors = []
    entries = sessions(root)
    numbers = [s['day'] for s in entries]
    if numbers != list(range(1, 169)):
        errors.append('Manifest must contain days 1..168 exactly once and in order.')
    ids = [i for s in entries for i in s['ids']]
    if len(ids) != 504 or len(set(ids)) != 504:
        errors.append('Expected 504 unique session objective IDs.')
    if len({s['folder'] for s in entries}) != len(entries):
        errors.append('Duplicate day folder in manifest.')
    for entry in entries:
        day = entry['day']
        base = root / 'days' / entry['folder']
        if not base.is_dir():
            errors.append(f'Day {day}: missing directory.')
            continue
        directories = {p.name for p in base.iterdir() if p.is_dir() and p.name != '__pycache__'}
        expected_folders = {track_folder(entry, track) for track in TRACKS}
        if directories != expected_folders:
            errors.append(f'Day {day}: expected {expected_folders}; found {directories}.')
        required = ['LESSON.md', 'CHECKLIST.md', 'dsa/README.md', 'dsa/PRACTICE.md',
                    'dsa/HINTS.md', 'dsa/solution.py', 'dsa/cases.json', 'dsa/test_solution.py',
                    'dsa/NOTES.md', 'dsa/LEETCODE.md', 'sd/README.md', 'sd/DESIGN.md', 'lang/README.md',
                    'lang/lab.py', 'lang/NOTES.md']
        for name in required:
            if '/' in name:
                track, filename = name.split('/', 1)
                name = track_folder(entry, track) + '/' + filename
            path = base / name
            if not path.is_file() or not path.stat().st_size:
                errors.append(f'Day {day}: missing or empty {name}.')
        for track, minutes, prefix in zip(TRACKS, (60, 30, 15), ('DSA', 'SD', 'PY')):
            path = base / track_folder(entry, track) / 'README.md'
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                if f'{minutes} minutes' not in text or f'{prefix}-{day:02d}' not in text:
                    errors.append(f'Day {day} {track}: missing budget or objective.')
        try:
            cases = json.loads((base / track_folder(entry, 'dsa') / 'cases.json').read_text(encoding='utf-8'))
            if not isinstance(cases, list) or not cases:
                raise ValueError('expected nonempty case list')
            for case in cases:
                if not isinstance(case, dict) or not {'name', 'input', 'expected'} <= case.keys():
                    raise ValueError('case needs name, input and expected')
                if not isinstance(case['input'], dict):
                    raise ValueError('solve(data) input must be an object')
        except (OSError, ValueError) as exc:
            errors.append(f'Day {day}: invalid fixture: {exc}')
        companions = entry.get('leetcode', [])
        if len(companions) != (2 if entry['review'] else 1):
            errors.append(f'Day {day}: missing LeetCode assignments.')
        lc_path = base / track_folder(entry, 'dsa') / 'LEETCODE.md'
        if lc_path.exists():
            lc_text = lc_path.read_text(encoding='utf-8')
            for problem in companions:
                url = problem.get('url', '')
                if not url.startswith('https://leetcode.com/problems/') or url not in lc_text:
                    errors.append(f'Day {day}: invalid or unlinked LeetCode assignment.')
        hub = base / 'LESSON.md'
        if hub.exists() and 'plan_version: "v1.1.0"' not in hub.read_text(encoding='utf-8'):
            errors.append(f'Day {day}: outdated plan version.')
    # Verify the human plan and machine manifest agree, without importing learner code.
    plan = (root / 'docs/00_MASTER_PLAN.md').read_text(encoding='utf-8')
    block = re.search(r'<!-- granth:day-map:start -->(.*?)<!-- granth:day-map:end -->', plan, re.S)
    if not block:
        errors.append('Master plan is missing day-map markers.')
    else:
        rows = re.findall(r'^\| (\d+) \| (.*?) \| (.*?) \|$', block[1], re.M)
        if [int(row[0]) for row in rows] != numbers:
            errors.append('Plan and manifest day numbers disagree.')
        by_day = {int(row[0]): row for row in rows}
        for entry in entries:
            row = by_day.get(entry['day'])
            if row and (re.findall(r'\b(?:DSA|SD|PY)-\d{2,3}\b', row[2]) != entry['ids']
                        or not all(title in row[1] for title in entry['titles'])):
                errors.append(f"Day {entry['day']}: plan/manifest assignment mismatch.")
    # Every shipped link and Python file gets structural validation; unsolved reps are not executed.
    roots = [root / 'days', root / 'docs']
    md_paths = [root / 'README.md', root / 'CLAUDE.md']
    for folder in roots:
        md_paths.extend(folder.rglob('*.md'))
    for path in md_paths:
        text = path.read_text(encoding='utf-8')
        if '{{' in text:
            errors.append(f'{path.relative_to(root)}: unresolved template placeholder.')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            if target.startswith(('http:', 'https:', 'mailto:', '#')):
                continue
            target = target.split('#', 1)[0]
            if target and not (path.parent / target).exists():
                errors.append(f'{path.relative_to(root)}: broken link {target}.')
    for folder in [root / 'days', root / 'scripts']:
        for path in folder.rglob('*.py'):
            try:
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            except SyntaxError as exc:
                errors.append(f'{path.relative_to(root)}: {exc}')
    raw = (root / 'vendor/granth/SKILL.md').read_text(encoding='utf-8')
    match = re.search(r'^### `granth.py`.*?^````python\n(.*?)^````', raw, re.M | re.S)
    if not match or (root / 'granth.py').read_text(encoding='utf-8') != match[1]:
        errors.append('granth.py differs from the vendored skill code block.')
    try:
        read_progress(root)
    except ValueError as exc:
        errors.append(str(exc))
    return errors


def practice(day, root=ROOT):
    entry = get_session(day, root)
    test = root / 'days' / entry['folder'] / track_folder(entry, 'dsa') / 'test_solution.py'
    return subprocess.call([sys.executable, str(test)], cwd=root)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, 'reconfigure'):
            stream.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    start = commands.add_parser('start', help='Print a subject assignment and its path.')
    start.add_argument('day', type=int)
    start.add_argument('--track', choices=TRACKS, default='dsa')
    run = commands.add_parser('practice', help='Run the selected DSA exercise tests (initially RED).')
    run.add_argument('day', type=int)
    commands.add_parser('status', help='Show independent study progress.')
    commands.add_parser('check', help='Validate layout, plan, links, fixtures and Python syntax.')
    args = parser.parse_args(argv)
    try:
        if args.command == 'start':
            entry = get_session(args.day)
            path = ROOT / 'days' / entry['folder'] / track_folder(entry, args.track) / 'README.md'
            print(f'Open: {path}\n\n{path.read_text(encoding="utf-8")}')
        elif args.command == 'practice':
            return practice(args.day)
        elif args.command == 'status':
            progress = read_progress()
            for track in TRACKS:
                done = [s['day'] for s in sessions() if progress.get((s['day'], track), {}).get('status') == 'complete']
                next_day = next((s['day'] for s in sessions() if s['day'] not in done), None)
                print(f'{track}: {len(done)}/168 complete. Next: {next_day if next_day else "all complete"}.')
        else:
            errors = validate()
            if errors:
                print('\n'.join(f'FAIL {error}' for error in errors))
                return 1
            print('OK: 168 days; 504 subject folders; 504 unique objectives; budgets, links, fixtures, syntax and upstream code verified.')
            print('This checks the course structure, not learner mastery or unsolved exercise correctness.')
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'course: {exc}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
