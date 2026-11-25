"""Track apartment society maintenance dues and payments."""

import ast
import operator
import sqlite3
from collections.abc import Callable

CONNECTION = sqlite3.connect(":memory:")
CONNECTION.execute(
    "CREATE TABLE dues (flat TEXT, month TEXT, amount INTEGER, paid INTEGER)"
)

Numeric = int | float
BinaryOperator = Callable[[Numeric, Numeric], Numeric]
_BINARY_OPERATORS: dict[type[ast.operator], BinaryOperator] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def add_due(
    flat: str,
    month: str,
    amount: int,
    history: list[tuple[str, str]] | None = None,
) -> list[tuple[str, str]]:
    """Record a monthly charge and return the updated history."""
    if not flat.strip() or not month.strip():
        raise ValueError("Flat and month must not be empty")
    if amount <= 0:
        raise ValueError("Dues amount must be positive")

    CONNECTION.execute(
        "INSERT INTO dues VALUES (?, ?, ?, 0)", (flat, month, amount)
    )
    if history is None:
        history = []
    history.append((flat, month))
    return history


def collect(flat: str, month: str) -> int | None:
    """Mark dues as paid and return the amount, or None if not found."""
    row = CONNECTION.execute(
        "SELECT amount FROM dues WHERE flat = ? AND month = ?", (flat, month)
    ).fetchone()
    if row is None:
        return None

    CONNECTION.execute(
        "UPDATE dues SET paid = 1 WHERE flat = ? AND month = ?", (flat, month)
    )
    return int(row[0])


def _evaluate_arithmetic(node: ast.expr) -> int | float:
    """Evaluate basic arithmetic without executing arbitrary code."""
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.UnaryOp) and isinstance(
        node.op, (ast.UAdd, ast.USub)
    ):
        value = _evaluate_arithmetic(node.operand)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        operation = _BINARY_OPERATORS.get(type(node.op))
        if operation is not None:
            left = _evaluate_arithmetic(node.left)
            right = _evaluate_arithmetic(node.right)
            return operation(left, right)
    raise ValueError(
        "Penalty must use numeric literals and +, -, *, or / only"
    )


def penalty(rule: str) -> int | float:
    """Calculate a penalty from a restricted arithmetic expression."""
    try:
        expression = ast.parse(rule, mode="eval")
        return _evaluate_arithmetic(expression.body)
    except (SyntaxError, ZeroDivisionError) as error:
        raise ValueError("Invalid penalty expression") from error


def pending() -> list[str]:
    """Return the flat numbers with unpaid dues."""
    rows = CONNECTION.execute(
        "SELECT flat FROM dues WHERE paid = 0"
    ).fetchall()
    return [row[0] for row in rows]


def main() -> None:
    """Run a short example of the dues ledger."""
    add_due("A-101", "Oct", 2500)
    add_due("A-102", "Oct", 2500)
    print(collect("A-101", "Oct"))
    print(penalty("50 * 2"))
    print(pending())


if __name__ == "__main__":
    main()
