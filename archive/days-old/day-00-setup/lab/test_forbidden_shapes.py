"""Day 0 — what you are not allowed to write, checked by reading your syntax tree.

This one does not import your function. It reads implement.py as text, parses it,
and looks at the shapes in it. So it runs even while implement.py is a stub, and
it cannot be fooled by a function that happens to return the right answer.

Two forbidden things, for two different reasons.

`itertools.accumulate` and `numpy` are forbidden because they *name* the result
instead of producing it. Day 0's whole point is that you can produce it.

`max()` applied to a slice is forbidden because of what it costs. Slicing copies,
and the copy grows with the loop index, so the total work is 1 + 2 + ... + n.
That is the quadratic version. Write it, run bench.py, watch the ratio column,
then delete it -- the deleting is the part this test enforces.
"""

import ast
from pathlib import Path

IMPLEMENT = Path(__file__).parent / "implement.py"
BANNED_MODULES = {"itertools", "numpy"}
BANNED_NAMES = {"accumulate"}


def _tree() -> ast.Module:
    return ast.parse(IMPLEMENT.read_text(encoding="utf-8"), filename=str(IMPLEMENT))


def test_no_banned_imports() -> None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                assert root not in BANNED_MODULES, f"line {node.lineno}: `import {alias.name}`"
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            assert (
                root not in BANNED_MODULES
            ), f"line {node.lineno}: `from {node.module} import ...`"
            for alias in node.names:
                assert alias.name not in BANNED_NAMES, f"line {node.lineno}: `{alias.name}`"


def test_no_max_over_a_slice() -> None:
    """`max(xs[:i + 1])` and friends -- the O(n^2) shape, spelled any way you like."""
    for node in ast.walk(_tree()):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Name)):
            continue
        if node.func.id not in {"max", "min"}:
            continue
        for argument in node.args:
            sliced = isinstance(argument, ast.Subscript) and isinstance(argument.slice, ast.Slice)
            assert not sliced, (
                f"line {node.lineno}: `{node.func.id}()` on a slice. Each call copies and "
                f"scans a prefix, so the total work is 1 + 2 + ... + n = n(n+1)/2. "
                f"That is the quadratic version bench.py exists to show you."
            )
