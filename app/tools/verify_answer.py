"""SymPy-backed math verification tool."""

from __future__ import annotations

import re
from typing import Any

from sympy import Eq, diff, integrate, simplify, solve, sympify

SAFE_PATTERN = re.compile(r"^[0-9a-zA-Z_+\-*/^().=,\s]+$")


def _safe_text(value: str) -> str:
    if not SAFE_PATTERN.match(value):
        raise ValueError("Input contains unsupported characters for symbolic verification.")
    return value.replace("^", "**")


def verify_answer(problem: str, expected_answer: str = "") -> dict[str, Any]:
    problem = _safe_text(problem)
    expected_answer = _safe_text(expected_answer) if expected_answer else ""

    if "=" in problem:
        left, right = problem.split("=", 1)
        equation = Eq(sympify(left), sympify(right))
        symbols = list(equation.free_symbols)
        solution = solve(equation, symbols[0]) if symbols else []
        verified = True
        if expected_answer and "=" in expected_answer:
            _, expected_value = expected_answer.split("=", 1)
            expected_value = sympify(expected_value)
            verified = bool(solution and simplify(solution[0] - expected_value) == 0)
        return {
            "verified": verified,
            "kind": "equation",
            "symbolic_solution": str(solution),
            "warning": None,
        }

    expression = sympify(problem)
    result = simplify(expression)
    if expected_answer:
        verified = simplify(result - sympify(expected_answer)) == 0
    else:
        verified = True
    return {
        "verified": bool(verified),
        "kind": "expression",
        "simplified": str(result),
        "warning": None,
    }


def derivative(expression: str, variable: str = "x") -> dict[str, Any]:
    expression = _safe_text(expression)
    variable = _safe_text(variable)
    return {"derivative": str(diff(sympify(expression), sympify(variable)))}


def integral(expression: str, variable: str = "x") -> dict[str, Any]:
    expression = _safe_text(expression)
    variable = _safe_text(variable)
    return {"integral": str(integrate(sympify(expression), sympify(variable)))}
