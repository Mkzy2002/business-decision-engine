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


def test_cli_arguments():
    result = calculate_decision(
        revenue=20000,
        expenses=8000,
        cash=2500,
        growth_rate=8,
        customers=50
    )

    assert result["profit"] == 12000
    assert result["margin"] == 60
    assert result["runway"] == 0.3125
    assert result["score"] == 55
    assert result["recommendation"] == "PIVOT"
    assert result["risk"] == "CRITICAL"


def test_json_output_data():
    result = calculate_decision(
        revenue=20000,
        expenses=8000,
        cash=2500,
        growth_rate=8,
        customers=50
    )

    assert result["profit"] == 12000
    assert result["margin"] == 60
    assert result["runway"] == 0.3125
    assert result["score"] == 55
    assert result["recommendation"] == "PIVOT"
    assert result["risk"] == "CRITICAL"
    assert isinstance(result["reasons"], list)


def test_compare_scenarios():
    from decision_engine import compare_scenarios

    scenarios = [
        {
            "name": "Current",
            "revenue": 20000,
            "expenses": 8000,
            "cash": 2500,
            "growth": 8,
            "customers": 50,
        },
        {
            "name": "Cut Expenses",
            "revenue": 20000,
            "expenses": 5000,
            "cash": 2500,
            "growth": 8,
            "customers": 50,
        },
        {
            "name": "Increase Revenue",
            "revenue": 30000,
            "expenses": 8000,
            "cash": 2500,
            "growth": 15,
            "customers": 50,
        },
    ]

    results = compare_scenarios(scenarios)

    assert len(results) == 3
    assert results[0]["name"] == "Increase Revenue"
    assert results[0]["score"] == 60
    assert results[1]["score"] == 55
    assert results[2]["score"] == 55