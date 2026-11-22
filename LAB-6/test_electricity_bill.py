import pytest

from electricity_bill import energy_charge, late_fee, subsidy


@pytest.mark.parametrize(
    ("units", "connection", "expected"),
    [
        (0, "domestic", 50),
        (50, "domestic", 200),
        (100, "domestic", 350),
        (101, "domestic", 355),
        (300, "domestic", 1350),
        (301, "domestic", 1358),
        (100, "commercial", 750),
        (301, "commercial", 2866),
    ],
)
def test_energy_charge_slabs_and_connections(units, connection, expected):
    assert energy_charge(units, connection) == expected


@pytest.mark.parametrize("connection", ["unknown", "Domestic", ""])
def test_energy_charge_rejects_unknown_connection(connection):
    with pytest.raises(ValueError, match="unknown connection"):
        energy_charge(10, connection)


def test_energy_charge_rejects_negative_units():
    with pytest.raises(ValueError, match="invalid units"):
        energy_charge(-1, "domestic")


@pytest.mark.parametrize(
    ("bill", "days", "expected"),
    [(500, 0, 0), (500, -2, 0), (500, 1, 50), (500, 15, 50),
     (500, 16, 100), (2000, 16, 100), (2001, 16, 200)],
)
def test_late_fee_boundaries(bill, days, expected):
    assert late_fee(bill, days) == expected


@pytest.mark.parametrize(
    ("units", "senior", "solar", "expected"),
    [(50, False, False, 0), (50, True, False, 50),
     (101, True, False, 0), (50, False, True, 100),
     (50, True, True, 150), (300, False, True, 100),
     (301, True, True, 0), (301, True, False, 0)],
)
def test_subsidy_conditions(units, senior, solar, expected):
    assert subsidy(units, senior, solar) == expected
