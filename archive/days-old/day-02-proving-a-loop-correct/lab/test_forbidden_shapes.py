"""Day 2 — what you are not allowed to write, checked by reading your syntax tree.

This one does not import your function. It reads implement.py as text, parses
it, and looks at the shapes in it -- so it cannot be fooled by a function that
happens to return the right numbers.

One forbidden family, for one reason. `//`, `%`, `/`, `divmod` and `math` all
*name* the quotient and the remainder rather than producing them. With any of
them in the file there is no loop, so there is no invariant to maintain and no
variant to decrease, and the whole of today has been skipped in one character.

The rule is not "avoid the fast version". Repeated subtraction is the slow
version, and section 7 of part 2.1 is explicit that it is slow for a reason you
should be able to derive. The rule is that today you are the procedure.
"""

import ast
from pathlib import Path

import pytest

IMPLEMENT = Path(__file__).parent / "implement.py"
BANNED_MODULES = {"math", "numpy", "operator", "fractions", "decimal"}
BANNED_CALLS = {"divmod", "round", "pow", "abs"}
BANNED_OPERATORS: dict[type, str] = {ast.FloorDiv: "//", ast.Mod: "%", ast.Div: "/"}


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


def test_no_division_operators() -> None:
    """`//`, `%` and `/`, spelled as an expression or as an augmented assignment."""
    for node in ast.walk(_tree()):
        if not isinstance(node, ast.BinOp | ast.AugAssign):
            continue
        operator = type(node.op)
        assert operator not in BANNED_OPERATORS, (
            f"line {node.lineno}: `{BANNED_OPERATORS.get(operator)}` names the answer. "
            f"Today you produce it: subtract b from what is left, and count. "
            f"You have `-`, `+`, `<`, `>` and a `while`."
        )


def test_no_banned_calls() -> None:
    for node in ast.walk(_tree()):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert (
                node.func.id not in BANNED_CALLS
            ), f"line {node.lineno}: `{node.func.id}()` does the loop's job for it."


def test_there_is_actually_a_loop() -> None:
    """A procedure, not a claim about one. Section 7 of part 2.1 costs it for you."""
    kinds = {type(node) for node in ast.walk(_tree())}
    assert kinds & {ast.While, ast.For}, (
        "no loop in implement.py. The whole day is about what a loop keeps true "
        "and why it stops; a straight-line function has neither."
    )
