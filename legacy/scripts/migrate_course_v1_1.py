"""One-time, two-phase migration. Directory moves use the accompanying native PowerShell script.

prepare records paths and protected-file hashes; finish updates documents after the native moves.
Never regenerates learner solutions, cases, tests, notes, labs or design responses.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

from leetcode_data import mapping

ROOT = Path(__file__).resolve().parents[1]
TRACKS = ('dsa', 'sd', 'lang')
PROTECTED = {'solution.py', 'cases.json', 'test_solution.py', 'NOTES.md', 'lab.py', 'DESIGN.md'}


def write(path, text):
    path.write_text(text, encoding='utf-8')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    manifest = json.loads((ROOT / 'docs/sessions.json').read_text(encoding='utf-8'))
    records, hashes = [], {}
    for entry in manifest:
        for track, title in zip(TRACKS, entry['titles']):
            slug = re.sub('[^a-z0-9]+', '-', title.lower()).strip('-')
            old = f"days/{entry['folder']}/{track}"
            new = f"days/{entry['folder']}/{track}_{slug}"
            source, dest = ROOT / old, ROOT / new
            if not source.is_dir() or dest.exists():
                raise RuntimeError(f'Expected old folder and absent destination: {old} -> {new}')
            records.append({'old': old, 'new': new})
            for path in source.rglob('*'):
                if path.is_file() and path.name in PROTECTED:
                    hashes[new + '/' + path.relative_to(source).as_posix()] = digest(path)
    for filename, value in [('folder_renames.json', records), ('migration_protected_hashes.json', hashes)]:
        path = ROOT / 'docs' / filename
        if path.exists():
            raise FileExistsError(f'Migration record already exists: {path}')
        write(path, json.dumps(value, indent=2) + '\n')
    print(f'Prepared {len(records)} renames and {len(hashes)} protected-file hashes.')


def finish():
    renames = json.loads((ROOT / 'docs/folder_renames.json').read_text(encoding='utf-8'))
    hashes = json.loads((ROOT / 'docs/migration_protected_hashes.json').read_text(encoding='utf-8'))
    for rename in renames:
        if (ROOT / rename['old']).exists() or not (ROOT / rename['new']).is_dir():
            raise RuntimeError(f'Native rename not complete: {rename}')
    for name, expected in hashes.items():
        if digest(ROOT / name) != expected:
            raise RuntimeError(f'Protected file changed: {name}')
    old_manifest = json.loads((ROOT / 'docs/sessions.json').read_text(encoding='utf-8'))
    if 'track_folders' in old_manifest[0]:
        raise RuntimeError('Already finalized; do not append duplicate assignments.')
    folder_map = {r['old']:r['new'] for r in renames}
    companions = mapping()
    records = {r['url']:r for r in json.loads((ROOT / 'docs/leetcode_sources.json').read_text(encoding='utf-8'))}
    for entry in old_manifest:
        entry['track_folders'] = {t:Path(folder_map[f"days/{entry['folder']}/{t}"]).name for t in TRACKS}
        source_days = [entry['day']-6, entry['day']-2] if entry['review'] else [entry['day']]
        entry['leetcode'] = [{**companions[n], 'source_day':n,
                              'difficulty':records[companions[n]['url']]['difficulty'],
                              'verification':records[companions[n]['url']]['status']}
                             for n in source_days]
    # Read each existing text before narrowly updating known paths. Historical ledgers and
    # decision records remain append-only; the rename map resolves their old evidence paths.
    paths = [ROOT / 'README.md', ROOT / 'CLAUDE.md', ROOT / '.claude/skills/day-krama/SKILL.md']
    paths += list((ROOT / 'days').rglob('*.md'))
    paths += [ROOT / 'docs' / name for name in ('STUDY_WORKFLOW.md', 'PRACTICE_GUIDE.md')]
    for path in paths:
        if path.name in PROTECTED:
            continue
        text = path.read_text(encoding='utf-8')
        for old, new in folder_map.items():
            # Match a directory boundary, avoiding a second replacement of already-renamed paths.
            if old in text:
                text = re.sub(re.escape(old) + r'(?=/|\b(?![_a-zA-Z0-9-]))', lambda m: new, text)
            # Relative cross-day links omit the leading days/.
            if old[5:] in text:
                text = re.sub(re.escape(old[5:]) + r'(?=/)', lambda m: new[5:], text)
        try:
            relative = path.relative_to(ROOT / 'days')
        except ValueError:
            relative = None
        if relative is not None and len(relative.parts) >= 2:
            entry = next((e for e in old_manifest if e['folder']==relative.parts[0]), None)
            if entry:
                for track in TRACKS:
                    # Hub links are relative to the day itself.
                    if path.parent.name == entry['folder']:
                        text = text.replace(f']({track}/', f"]({entry['track_folders'][track]}/")
                text = text.replace('plan_version: "v1.0.0"', 'plan_version: "v1.1.0"')
        write(path, text)
    index = ['# LeetCode interview practice — all 168 days', '',
             'One main attempt per topic day; weekly reviews reuse earlier problems. Repeated problems',
             'are intentional and not counted as unique. See [interview method](INTERVIEW_PREP.md).', '',
             '| Day | Course topic | LeetCode companion | Difficulty | Access / relation |',
             '| --- | --- | --- | --- | --- |']
    for entry in old_manifest:
        base = ROOT / 'days' / entry['folder'] / entry['track_folders']['dsa']
        text = [f"# Day {entry['day']:03d} — LeetCode interview practice", '',
                'Use this inside the existing **60-minute DSA budget**. Choose the online problem or',
                'the local exercise as the main attempt; use its companion as a variation or review.', '',
                '[Interview method](../../../docs/INTERVIEW_PREP.md) · [Local contract](PRACTICE.md) · [Evidence](NOTES.md)', '']
        for problem in entry['leetcode']:
            text += [f"## {problem['number']}. {problem['title']}", '',
                     f"[Open the official problem]({problem['url']})", '',
                     f"**Difficulty:** {problem['difficulty']}. **Original course day:** {problem['source_day']}.", '',
                     f"**Contract comparison:** {problem['note']}", '']
            if problem['premium']:
                text += ['**Premium optional.** The official page exposes a subscription gate. Use the',
                         'complete local exercise if you do not have access; no purchase is required.', '']
            if problem['verification']=='lookup-incomplete':
                text += ['**Source check incomplete:** the official page timed out during authoring.',
                         f"Recheck with `Invoke-WebRequest '{problem['url']}'`; use the local exercise meanwhile.", '']
            else:
                text += ['Official page checked on 2026-09-18; premium statements were not accessible.', '']
            relation = 'Premium; local free fallback' if problem['premium'] else 'Companion; compare contracts'
            index.append(f"| [{entry['day']}](../days/{entry['folder']}/{entry['track_folders']['dsa']}/LEETCODE.md) | {entry['titles'][0]} | [{problem['number']}. {problem['title']}]({problem['url']}) | {problem['difficulty']} | {relation} |")
        text += ['## Interview checklist', '',
                 '- [ ] Clarify constraints and explain a baseline before coding.',
                 '- [ ] State the invariant or recurrence and why the optimization is valid.',
                 '- [ ] Make an independent attempt before hints or an editorial.',
                 '- [ ] Test boundary and adversarial cases; record the actual result.',
                 '- [ ] Explain time, memory, and one changed-constraint follow-up aloud.',
                 '- [ ] Record any hints and a cold re-solve in NOTES.md.', '',
                 'The local `solve(data)` adapter and fixtures do not use the online judge signature.',
                 'A local green test is not an online acceptance. Adapt to the official interface when submitting.', '']
        if entry['review']:
            text += ['## Review pacing', '',
                     '5 minutes recall, 20 minutes per cold attempt, 10 minutes critique and 5 minutes logging.',
                     'A difficult unresolved problem may replace both attempt slots. No new problem quota.', '']
        if (base / 'LEETCODE.md').exists():
            raise FileExistsError(base / 'LEETCODE.md')
        write(base / 'LEETCODE.md', '\n'.join(text))
        for name in ('README.md', 'PRACTICE.md'):
            path = base / name
            old = path.read_text(encoding='utf-8')
            first, rest = old.split('\n', 1)
            insertion = '\n\n## Product-company interview practice\n\nOpen [today\'s LeetCode assignment](LEETCODE.md). Use the same 60-minute session;\nchoose one main attempt rather than adding a second mandatory problem. The local contract\nremains the specification for solution.py and cases.json. For an online-only attempt, record\nsubmission evidence, compare the contracts, and use the interview checklist for completion.\n'
            old = first + insertion + rest
            if name == 'README.md':
                old = old.replace('- [ ] The core solution passes provided and self-authored tests.',
                                  '- [ ] My chosen route meets its contract: local tests plus self-authored cases, or online submission evidence plus a local-contract comparison.')
            write(path, old)
    write(ROOT / 'docs/LEETCODE_INDEX.md', '\n'.join(index)+'\n')
    write(ROOT / 'docs/sessions.json', json.dumps(old_manifest, indent=2)+'\n')
    for name, expected in hashes.items():
        if digest(ROOT / name) != expected:
            raise RuntimeError(f'Protected file changed after finalizing: {name}')
    print(f'Finalized 504 topic folders; 168 LeetCode guides; all {len(hashes)} protected files byte-identical.')


if __name__ == '__main__':
    {'prepare':prepare, 'finish':finish}[sys.argv[1]]()
