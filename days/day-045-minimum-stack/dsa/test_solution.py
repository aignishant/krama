"""Run directly, or with python course.py practice N from the root."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('exercise_solution', HERE / 'solution.py')
solution = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solution)


class ExerciseCases(unittest.TestCase):
    def test_cases(self):
        cases = json.loads((HERE / 'cases.json').read_text(encoding='utf-8'))
        self.assertTrue(cases, 'Keep at least one example case.')
        for case in cases:
            with self.subTest(case=case['name']):
                actual = solution.solve(copy.deepcopy(case['input']))
                self.assertEqual(actual, case['expected'])


if __name__ == '__main__':
    unittest.main()
