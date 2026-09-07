from decision_engine import calculate_decision


def test_profitable_business():
    result = calculate_decision(
        revenue=20000,
        expenses=10000,
        cash=60000,
        growth_rate=10,
        customers=100
    )

    assert result["profit"] == 10000
    assert result["recommendation"] == "CONTINUE"


def test_low_runway():
    result = calculate_decision(
        revenue=20000,
        expenses=8000,
        cash=2500,
        growth_rate=8,
        customers=50
    )

    assert result["runway"] < 1
    assert result["recommendation"] == "PIVOT"


def test_losing_business():
    result = calculate_decision(
        revenue=5000,
        expenses=10000,
        cash=5000,
        growth_rate=-10,
        customers=5
    )

    assert result["profit"] == -5000
    assert result["recommendation"] == "PIVOT"