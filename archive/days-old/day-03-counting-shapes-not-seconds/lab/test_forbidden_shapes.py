"""Day 3 — what you are not allowed to write, checked by reading your syntax tree.

This one does not import your function. It reads implement.py as text, parses
it, and looks at the shapes in it, so it cannot be fooled by a function that
returns the right index the wrong way.

Two forbidden families, for two different reasons.

Slicing and copying -- `f[::-1]`, `f[i:]`, `list(f)`, `reversed(f)`, `sorted(f)`
-- are forbidden because every one of them allocates a copy proportional to the
input. The contract says Theta(1) auxiliary space, and a copy inside a loop is
also the standard way this exercise accidentally becomes quadratic. Part 2.2's
section 6 makes the same point about holding all the ratios versus keeping a
running summary.

`min`, `max` and `sum` over the tables are forbidden because they name a scan
instead of performing one. Today's question is about a *suffix* property, and
reaching for an aggregate is how people avoid noticing that.
"""

import ast
from pathlib import Path

import pytest

IMPLEMENT = Path(__file__).parent / "implement.py"
BANNED_CALLS = {"reversed", "sorted", "list", "min", "max", "sum", "any", "all", "filter", "map"}
BANNED_MODULES = {"itertools", "numpy", "functools", "operator", "bisect"}


def _tree() -> ast.Module:
    return ast.parse(IMPLEMENT.read_text(encoding="utf-8"), filename=str(IMPLEMENT))


def _is_still_a_stub() -> bool:
    """A function whose whole body is a docstring and `raise NotImplementedError`."""
    for node in ast.walk(_tree()):
        if not isinstance(node, ast.FunctionDef):
            continue
        body = [stmt for stmt in node.body if not isinstance(stmt, ast.Expr)]
        if len(body) == 1 and isinstance(body[0], ast.Raise):
            return True
    return False


pytestmark = pytest.mark.skipif(
    _is_still_a_stub(),
    reason="implement.py is still a stub -- write it, and this suite wakes up",
)


def test_no_banned_imports() -> None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                assert root not in BANNED_MODULES, f"line {node.lineno}: `import {alias.name}`"
        elif isinstance(node, ast.ImportFrom):
            root = (node.module or "").split(".")[0]
            assert root not in BANNED_MODULES, f"line {node.lineno}: `from {root} import ...`"


def test_no_slicing() -> None:
    """Every slice of f or g is a copy, and the contract is Theta(1) auxiliary space."""
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice):
            raise AssertionError(
                f"line {node.lineno}: a slice copies. Walk the indices instead; "
                f"the answer is a property of a suffix, not of a new list."
            )


def test_no_aggregate_calls_over_the_tables() -> None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id not in BANNED_CALLS, (
                f"line {node.lineno}: `{node.func.id}()` names a scan instead of performing "
                f"one, and hides whether the scan is over a suffix or over everything."
            )


def test_there_is_actually_a_loop() -> None:
    kinds = {type(node) for node in ast.walk(_tree())}
    assert kinds & {ast.While, ast.For}, "no loop in implement.py -- one pass means one loop"
