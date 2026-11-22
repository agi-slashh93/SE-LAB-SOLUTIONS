RATES = {"DOM": 3, "COM": 6}
SLAB = {"A": 1, "B": 2}


def units_consumed(reading):
    """Return usage from a previous:current meter reading."""
    if not isinstance(reading, str):
        raise ValueError("reading must be text")
    parts = reading.split(":")
    if len(parts) != 2 or not all(part.strip().isdigit() for part in parts):
        raise ValueError("reading must contain two non-negative integers")
    previous, current = (int(part.strip()) for part in parts)
    if current < previous:
        raise ValueError("current reading cannot be lower than previous reading")
    return current - previous


def daily_average(units_csv):
    """Return the two-decimal average of a non-empty CSV of non-negative units."""
    if not isinstance(units_csv, str):
        raise ValueError("units must be text")
    parts = units_csv.split(",")
    if not parts or any(not part.strip().isdigit() for part in parts):
        raise ValueError("units must be a non-empty CSV of non-negative integers")
    units = [int(part.strip()) for part in parts]
    return round(sum(units) / len(units), 2)


def tariff_rate(code):
    """Return a rate for DOM/COM and slab A/B (case-insensitive)."""
    if not isinstance(code, str):
        raise ValueError("tariff code must be text")
    parts = code.split("-")
    if len(parts) != 2:
        raise ValueError("tariff code must have the form CATEGORY-SLAB")
    category, slab = (part.strip().upper() for part in parts)
    if category not in RATES or slab not in SLAB:
        raise ValueError("unknown tariff category or slab")
    return RATES[category] * SLAB[slab]


def main():
    print("==== Running units_consumed ====")
    user_input = input("Enter meter readings as previous:current (e.g. 1200:1350): ")
    print("Units Consumed:", units_consumed(user_input))
    print("\n==== Running daily_average ====")
    user_input = input("Enter daily units as CSV (e.g. 5,7,6): ")
    print("Daily Average:", daily_average(user_input))
    print("\n==== Running tariff_rate ====")
    user_input = input("Enter a tariff code (e.g. DOM-A): ")
    print("Rate per Unit:", tariff_rate(user_input))


if __name__ == "__main__":
    main()
