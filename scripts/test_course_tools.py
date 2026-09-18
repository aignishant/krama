"""Regression checks for progress isolation and the exercise runner."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import course


class ToolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'docs').mkdir()
        self.entries = [{'day': 1, 'folder': 'day-001-fixture'}, {'day': 2, 'folder': 'day-002-fixture'}]
        (self.root / 'docs/sessions.json').write_text(json.dumps(self.entries), encoding='utf-8')
        self.ledger = self.root / 'docs/TRACK_PROGRESS.csv'
        self.header = 'day,track,status,date,evidence,notes\n'
        self.ledger.write_text(self.header, encoding='utf-8')

    def tearDown(self):
        self.temp.cleanup()

    def test_latest_event_is_independent_per_track(self):
        self.ledger.write_text(self.header +
            '1,dsa,partial,2026-09-18,a.md,first attempt\n'
            '1,lang,complete,2026-09-18,b.md,lab done\n'
            '1,dsa,complete,2026-09-19,c.md,retest done\n', encoding='utf-8')
        progress = course.read_progress(self.root)
        self.assertEqual(progress[(1, 'dsa')]['evidence'], 'c.md')
        self.assertEqual(progress[(1, 'lang')]['evidence'], 'b.md')
        self.assertNotIn((1, 'sd'), progress)
        self.assertEqual(len(self.ledger.read_text().splitlines()), 4)

    def test_completion_requires_evidence(self):
        self.ledger.write_text(self.header + '1,dsa,complete,2026-09-18,,\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence'):
            course.read_progress(self.root)

    def test_malformed_csv_is_not_silently_accepted(self):
        self.ledger.write_text(self.header + '1,dsa,partial,date,a.md,unquoted,comma\n', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'column count'):
            course.read_progress(self.root)

    def test_unknown_day_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'No day'):
            course.get_session(99, self.root)

    def test_runner_detects_wrong_answer_and_accepts_correct_answer(self):
        # Synthetic echo fixture tests the runner without solving a learner exercise.
        folder = self.root / 'days/day-001-fixture/dsa'
        folder.mkdir(parents=True)
        source = next((course.ROOT / 'days').glob('day-001-*/dsa/test_solution.py'))
        (folder / 'test_solution.py').write_text(source.read_text(encoding='utf-8'), encoding='utf-8')
        (folder / 'solution.py').write_text('def solve(data):\n    return data["sentinel"]\n', encoding='utf-8')
        fixture = folder / 'cases.json'
        fixture.write_text(json.dumps([{'name': 'synthetic', 'input': {'sentinel': 'ok'}, 'expected': 'ok'}]), encoding='utf-8')
        command = [sys.executable, str(folder / 'test_solution.py')]
        self.assertEqual(subprocess.run(command, capture_output=True).returncode, 0)
        fixture.write_text(json.dumps([{'name': 'synthetic', 'input': {'sentinel': 'ok'}, 'expected': 'wrong'}]), encoding='utf-8')
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertIn('AssertionError', failed.stderr)


if __name__ == '__main__':
    unittest.main()
