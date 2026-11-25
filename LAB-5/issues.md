# Static Analysis Findings

Findings below are from the initial analysis of `society_dues.py`. They are ordered with security findings first, followed by quality and style issues.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| B608 | Medium severity, security | 9 | `addDue` interpolated flat, month, and amount directly into an SQL statement, allowing crafted values to alter the query. | Use SQLite placeholders and pass values separately; validate required text and positive amounts. |
| B307 | Medium severity, security | 21 | `eval` executed arbitrary Python while calculating a penalty. | Parse the expression and evaluate only numeric literals and explicitly allowed arithmetic operators. |
| W0102 | Low severity, correctness | 8 | The default `history=[]` was shared by calls that omitted the argument. | Default to `None`, then create a new list for each call. |
| B105 | Low severity, security | 5 | A treasurer password was hard-coded in the source. It was unused, but could be mistaken for a real credential and exposed if reused. | Remove the unused credential; secrets should be supplied through a protected configuration mechanism if needed. |
| W0718 | Low severity, robustness | 22 | `penalty` caught every `Exception`, hiding programming errors and treating invalid input like a valid zero fee. | Catch only parse and division errors and raise a clear `ValueError`; reject unsupported AST nodes. |
| R1710 | Low severity, correctness | 12-16 | `collect` returned an amount for a match but implicitly returned `None` otherwise. | Return `None` explicitly when no matching due exists. |
| C0121 / E711 | Low severity, style | 29 | The code compared a value to `None` with `!=`, instead of using identity comparison. | Remove the unnecessary check because `fetchall()` always returns a list. |
| C0103 / E302 / E501 | Low severity, style | 8-15 | `addDue` used camelCase, functions lacked spacing/docstrings, and several lines exceeded style limits. | Rename to `add_due`, document functions, and format statements to meet conventional Python style. |

## Verification

The final Pylint, Bandit, and Flake8 outputs are saved alongside this file. The final code retains the demonstration behavior while removing the listed findings.
