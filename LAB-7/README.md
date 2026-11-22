# Lab 7 — Fuzz Testing

The module validates meter readings, daily unit CSV, and tariff codes. The
Hypothesis tests explore arbitrary text and generated valid values; malformed
inputs consistently raise `ValueError`.

Install the test dependencies and run from this directory:

```sh
python -m pip install pytest hypothesis
python -m pytest
```
