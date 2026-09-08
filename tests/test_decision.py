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
    assert results[0]["name"] == "Cut Expenses"
    assert results[1]["name"] == "Increase Revenue"
    assert results[2]["name"] == "Current"

    assert results[0]["decision_score"] == 90
    assert results[1]["decision_score"] == 60
    assert results[2]["decision_score"] == 35

def test_explain_decision():
    from decision_engine import calculate_decision, explain_decision

    result = calculate_decision(
        revenue=20000,
        expenses=8000,
        cash=2500,
        growth_rate=8,
        customers=50
    )

    explanation = explain_decision(result)

    assert "Business is profitable" in explanation["strengths"]
    assert "Strong profit margin" in explanation["strengths"]
    assert "Cash runway is critically low" in explanation["concerns"]
    assert "Secure additional cash runway immediately" in explanation["actions"]
def test_decision_quality():
    from decision_engine import calculate_decision, compare_scenarios

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
    ]

    results = compare_scenarios(scenarios)

    assert "decision_quality" in results[0]
    assert "survival_improvement" in results[0]
    assert "profit_improvement" in results[0]
    assert "runway_improvement" in results[0]
def test_survival_override():
    from decision_engine import apply_survival_override

    score = apply_survival_override(
        decision_score=80,
        current_runway=0.3,
        scenario_runway=0.3,
    )

    assert score == 60

    improved_score = apply_survival_override(
        decision_score=80,
        current_runway=0.3,
        scenario_runway=0.5,
    )

    assert improved_score == 90

def test_get_best_decision():
    from decision_engine import compare_scenarios, get_best_decision

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
    best = get_best_decision(results)

    assert best["name"] == "Cut Expenses"
    assert best["decision_score"] == 90
    assert best["decision_quality"] == "HIGH"

def test_validate_business_inputs():
    from decision_engine import validate_business_inputs

    assert validate_business_inputs(
        revenue=20000,
        expenses=8000,
        cash=2500,
        growth_rate=8,
        customers=50,
    ) is True


def test_validate_business_inputs_rejects_negative_revenue():
    from decision_engine import validate_business_inputs

    import pytest

    with pytest.raises(ValueError):
        validate_business_inputs(
            revenue=-1,
            expenses=8000,
            cash=2500,
            growth_rate=8,
            customers=50,
        )


def test_validate_business_inputs_rejects_negative_cash():
    from decision_engine import validate_business_inputs

    import pytest

    with pytest.raises(ValueError):
        validate_business_inputs(
            revenue=20000,
            expenses=8000,
            cash=-1,
            growth_rate=8,
            customers=50,
        )


def test_validate_business_inputs_rejects_negative_customers():
    from decision_engine import validate_business_inputs

    import pytest

    with pytest.raises(ValueError):
        validate_business_inputs(
            revenue=20000,
            expenses=8000,
            cash=2500,
            growth_rate=8,
            customers=-1,
        )