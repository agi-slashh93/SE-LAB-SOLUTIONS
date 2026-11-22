# Lab 6 — Code and Branch Coverage

Tests cover the electricity bill unit slabs, connection types, invalid input,
late-fee thresholds, and subsidy branches. Run from this directory:

```sh
python -m pytest --cov=electricity_bill --cov-branch --cov-report=term-missing
```
