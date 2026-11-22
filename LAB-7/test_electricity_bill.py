from hypothesis import given, strategies as st
import pytest

from electricity_bill import daily_average, tariff_rate, units_consumed


@given(st.text())
def test_units_consumed_arbitrary_text_is_value_or_rejected(text):
    try:
        result = units_consumed(text)
    except ValueError:
        return
    previous, current = (int(part) for part in text.split(":"))
    assert previous >= 0 and current >= previous
    assert result == current - previous


@given(st.integers(min_value=0, max_value=10**12), st.integers(min_value=0, max_value=10**12))
def test_units_consumed_valid_readings(previous, extra):
    assert units_consumed(f"{previous}:{previous + extra}") == extra


@given(st.text())
def test_daily_average_arbitrary_text_is_value_or_rejected(text):
    try:
        result = daily_average(text)
    except ValueError:
        return
    values = [int(part) for part in text.split(",")]
    assert values and all(value >= 0 for value in values)
    assert result == round(sum(values) / len(values), 2)


@given(st.lists(st.integers(min_value=0, max_value=10**9), min_size=1, max_size=100))
def test_daily_average_valid_lists(values):
    csv = ",".join(map(str, values))
    assert daily_average(csv) == round(sum(values) / len(values), 2)


@given(st.text())
def test_tariff_rate_arbitrary_text_is_value_or_rejected(text):
    try:
        result = tariff_rate(text)
    except ValueError:
        return
    category, slab = (part.strip().upper() for part in text.split("-"))
    assert category in {"DOM", "COM"} and slab in {"A", "B"}
    assert result == {"DOM": 3, "COM": 6}[category] * {"A": 1, "B": 2}[slab]


@given(st.sampled_from(["DOM", "COM", "dom", "com"]), st.sampled_from(["A", "B", "a", "b"]))
def test_tariff_rate_valid_codes(category, slab):
    assert tariff_rate(f"{category}-{slab}") == {"DOM": 3, "COM": 6}[category.upper()] * {"A": 1, "B": 2}[slab.upper()]


@pytest.mark.parametrize("value", [None, 1, [], {}])
def test_functions_reject_non_text_inputs(value):
    for function in (units_consumed, daily_average, tariff_rate):
        with pytest.raises(ValueError):
            function(value)
