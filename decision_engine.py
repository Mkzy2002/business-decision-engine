import argparse
import json
import math


def make_json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None

    if isinstance(value, dict):
        return {
            key: make_json_safe(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            make_json_safe(item)
            for item in value
        ]

    return value

def validate_business_inputs(
    revenue,
    expenses,
    cash,
    growth_rate,
    customers,
):
    values = {
        "revenue": revenue,
        "expenses": expenses,
        "cash": cash,
        "growth_rate": growth_rate,
        "customers": customers,
    }

    for name, value in values.items():
        if not isinstance(value, (int, float)):
            raise ValueError(f"{name} must be a number")

    if revenue < 0:
        raise ValueError("revenue cannot be negative")

    if expenses < 0:
        raise ValueError("expenses cannot be negative")

    if cash < 0:
        raise ValueError("cash cannot be negative")

    if growth_rate < -100:
        raise ValueError("growth_rate cannot be below -100")

    if customers < 0:
        raise ValueError("customers cannot be negative")

    if not float(customers).is_integer():
        raise ValueError("customers must be a whole number")

    return True


def calculate_decision(revenue, expenses, cash, growth_rate, customers):
    validate_business_inputs(
        revenue=revenue,
        expenses=expenses,
        cash=cash,
        growth_rate=growth_rate,
        customers=customers,
    )

    monthly_profit = revenue - expenses

    if revenue > 0:
        profit_margin = (monthly_profit / revenue) * 100
    else:
        profit_margin = 0

    if expenses > 0:
        runway = cash / expenses
    else:
        runway = float("inf")

    score = 0

    # Profitability: 25 points
    if monthly_profit > 0:
        score += 25
    elif monthly_profit == 0:
        score += 10

    # Profit margin: 20 points
    if profit_margin >= 30:
        score += 20
    elif profit_margin >= 10:
        score += 10
    elif profit_margin > 0:
        score += 5

    # Runway: 30 points
    if runway >= 12:
        score += 30
    elif runway >= 6:
        score += 25
    elif runway >= 3:
        score += 15
    elif runway >= 1:
        score += 5

    # Growth: 15 points
    if growth_rate >= 20:
        score += 15
    elif growth_rate >= 10:
        score += 10
    elif growth_rate > 0:
        score += 5

    # Customers: 10 points
    if customers >= 100:
        score += 10
    elif customers >= 20:
        score += 5

    # Cash survival takes priority
    if runway < 1:
        recommendation = "PIVOT"
        risk = "CRITICAL"
    elif runway < 3:
        recommendation = "HOLD"
        risk = "HIGH"
    elif score >= 75:
        recommendation = "CONTINUE"
        risk = "LOW"
    elif score >= 50:
        recommendation = "HOLD"
        risk = "MEDIUM"
    elif score >= 30:
        recommendation = "PIVOT"
        risk = "HIGH"
    else:
        recommendation = "CUT"
        risk = "CRITICAL"

    reasons = []

    if runway < 1:
        reasons.append("WARNING: Extremely low cash runway")
    elif runway < 3:
        reasons.append("WARNING: Low cash runway")
    elif runway >= 6:
        reasons.append("OK: Strong cash runway")

    if monthly_profit > 0:
        reasons.append("OK: Business is profitable")
    else:
        reasons.append("WARNING: Business is losing money")

    if profit_margin >= 30:
        reasons.append("OK: Strong profit margin")
    elif profit_margin < 10:
        reasons.append("WARNING: Weak profit margin")

    if growth_rate >= 10:
        reasons.append("OK: Healthy revenue growth")
    elif growth_rate <= 0:
        reasons.append("WARNING: Revenue is not growing")

    if customers >= 50:
        reasons.append("OK: Established customer base")
    elif customers < 10:
        reasons.append("WARNING: Small customer base")

    return {
        "profit": monthly_profit,
        "margin": profit_margin,
        "runway": runway,
        "score": score,
        "recommendation": recommendation,
        "risk": risk,
        "reasons": reasons,
    }


def explain_decision(result):
    strengths = []
    concerns = []
    actions = []

    if result["profit"] > 0:
        strengths.append("Business is profitable")
    else:
        concerns.append("Business is losing money")

    if result["margin"] >= 30:
        strengths.append("Strong profit margin")
    elif result["margin"] < 10:
        concerns.append("Weak profit margin")

    if result["runway"] < 1:
        concerns.append("Cash runway is critically low")
        actions.append("Secure additional cash runway immediately")
    elif result["runway"] < 3:
        concerns.append("Cash runway is low")
        actions.append("Improve cash runway before expanding")
    elif result["runway"] >= 6:
        strengths.append("Strong cash runway")

    if result["score"] >= 75:
        actions.append("Continue the current business direction")
    elif result["recommendation"] == "HOLD":
        actions.append("Hold the current direction and improve weak areas")
    elif result["recommendation"] == "PIVOT":
        actions.append(
            "Test a different business approach before committing more resources"
        )
    elif result["recommendation"] == "CUT":
        actions.append(
            "Consider stopping or significantly reducing the current activity"
        )

    if result["margin"] >= 30:
        strengths.append("Healthy unit economics")

    if result["score"] < 50 and result["runway"] >= 3:
        concerns.append("Overall business health is weak")

    if not strengths:
        strengths.append("No major strengths identified")

    if not concerns:
        concerns.append("No major concerns identified")

    if not actions:
        actions.append("Monitor business performance and reassess regularly")

    return {
        "strengths": strengths,
        "concerns": concerns,
        "actions": actions,
    }


def calculate_decision_quality(
    current_result,
    current_scenario,
    scenario_result,
    scenario,
):
    profit_improvement = (
        scenario_result["profit"] - current_result["profit"]
    )

    margin_improvement = (
        scenario_result["margin"] - current_result["margin"]
    )

    growth_improvement = (
        scenario["growth"] - current_scenario["growth"]
    )

    if (
        current_result["runway"] == float("inf")
        and scenario_result["runway"] == float("inf")
    ):
        runway_improvement = 0
    elif current_result["runway"] == float("inf"):
        runway_improvement = 0
    elif scenario_result["runway"] == float("inf"):
        runway_improvement = float("inf")
    else:
        runway_improvement = (
            scenario_result["runway"] - current_result["runway"]
        )

    survival_improvement = runway_improvement

    if survival_improvement > 0:
        decision_quality = "HIGH"
    elif profit_improvement > 0 and margin_improvement >= 0:
        decision_quality = "MEDIUM"
    else:
        decision_quality = "LOW"

    return {
        "profit_improvement": profit_improvement,
        "runway_improvement": runway_improvement,
        "margin_improvement": margin_improvement,
        "growth_improvement": growth_improvement,
        "survival_improvement": survival_improvement,
        "decision_quality": decision_quality,
    }


def apply_survival_override(
    decision_score,
    current_runway,
    scenario_runway,
):
    if current_runway < 1:
        if scenario_runway <= current_runway:
            decision_score -= 20
        elif scenario_runway > current_runway:
            decision_score += 10

    return decision_score


def calculate_decision_score(
    health_score,
    profit_improvement,
    runway_improvement,
    margin_improvement,
):
    decision_score = health_score

    # Runway improvement: up to 25 points
    if runway_improvement > 1:
        decision_score += 25
    elif runway_improvement > 0.5:
        decision_score += 15
    elif runway_improvement > 0.1:
        decision_score += 10

    # Profit improvement: up to 15 points
    if profit_improvement > 10000:
        decision_score += 15
    elif profit_improvement > 5000:
        decision_score += 10
    elif profit_improvement > 0:
        decision_score += 5

    # Margin improvement: up to 10 points
    if margin_improvement > 10:
        decision_score += 10
    elif margin_improvement > 5:
        decision_score += 5
    elif margin_improvement > 0:
        decision_score += 2

    return decision_score


def get_best_decision(results):
    if not results:
        return None

    best_result = max(
        results,
        key=lambda result: result["decision_score"]
    )

    return {
        "name": best_result["name"],
        "decision_score": best_result["decision_score"],
        "decision_quality": best_result["decision_quality"],
        "recommendation": best_result["recommendation"],
        "risk": best_result["risk"],
        "reasons": best_result["explanation"]["actions"],
    }


def compare_scenarios(scenarios):
    if not isinstance(scenarios, list):
        raise ValueError("scenarios must be a list")

    if not scenarios:
        raise ValueError("scenarios cannot be empty")

    required_fields = {
        "name",
        "revenue",
        "expenses",
        "cash",
        "growth",
        "customers",
    }

    for index, scenario in enumerate(scenarios):
        if not isinstance(scenario, dict):
            raise ValueError(
                f"scenario {index} must be an object"
            )

        missing_fields = required_fields - scenario.keys()

        if missing_fields:
            missing = ", ".join(sorted(missing_fields))
            raise ValueError(
                f"scenario {index} is missing fields: {missing}"
            )

    current_scenario = scenarios[0]

    if current_scenario["name"].lower() != "current":
        raise ValueError(
            "first scenario must be named 'Current'"
        )

    results = []

    for scenario in scenarios:
        result = calculate_decision(
            revenue=scenario["revenue"],
            expenses=scenario["expenses"],
            cash=scenario["cash"],
            growth_rate=scenario["growth"],
            customers=scenario["customers"],
        )

        explanation = explain_decision(result)

        results.append({
            "name": scenario["name"],
            **result,
            "explanation": explanation,
            "_scenario": scenario,
        })

    current_result = results[0]

    for result in results:
        quality = calculate_decision_quality(
            current_result=current_result,
            current_scenario=current_scenario,
            scenario_result=result,
            scenario=result["_scenario"],
        )

        result.update(quality)

        base_decision_score = calculate_decision_score(
            health_score=result["score"],
            profit_improvement=result["profit_improvement"],
            runway_improvement=result["runway_improvement"],
            margin_improvement=result["margin_improvement"],
        )

        result["decision_score"] = apply_survival_override(
            decision_score=base_decision_score,
            current_runway=current_result["runway"],
            scenario_runway=result["runway"],
        )

        del result["_scenario"]

    return sorted(
        results,
        key=lambda result: result["decision_score"],
        reverse=True,
    )


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate business health and recommend an action."
    )

    parser.add_argument("--revenue", type=float)
    parser.add_argument("--expenses", type=float)
    parser.add_argument("--cash", type=float)
    parser.add_argument("--growth", type=float)
    parser.add_argument("--customers", type=int)

    parser.add_argument(
        "--scenario-file",
        type=str,
        help="Compare business scenarios from a JSON file"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output the decision as JSON"
    )

    args = parser.parse_args()

    if args.scenario_file:
        with open(args.scenario_file, "r", encoding="utf-8") as file:
            scenarios = json.load(file)

        results = compare_scenarios(scenarios)
        best_decision = get_best_decision(results)

        if args.json:
            output = {
                "results": results,
                "best_decision": best_decision,
            }

            safe_output = make_json_safe(output)

            print(json.dumps(safe_output, indent=2, allow_nan=False))
            return

        print()
        print("=" * 50)
        print("       BUSINESS SCENARIO COMPARISON")
        print("=" * 50)

        for index, result in enumerate(results, start=1):
            print()
            print(f"{index}. {result['name']}")
            print(f"   Score:          {result['score']}/100")
            print(f"   Decision Score:  {result['decision_score']}")
            print(f"   Recommendation: {result['recommendation']}")
            print(f"   Risk:           {result['risk']}")
            print(f"   Profit:         ${result['profit']:,.2f}")
            print(f"   Margin:         {result['margin']:.1f}%")

            if result["runway"] == float("inf"):
                print("   Runway:         Unlimited")
            else:
                print(f"   Runway:         {result['runway']:.1f} months")

            print()
            print("   DECISION IMPACT:")

            print(
                f"   Profit improvement:  "
                f"${result['profit_improvement']:,.2f}"
            )

            print(
                f"   Runway improvement:  "
                f"{result['runway_improvement']:.2f} months"
            )

            print(
                f"   Margin improvement:  "
                f"{result['margin_improvement']:.1f}%"
            )

            print(
                f"   Growth improvement:  "
                f"{result['growth_improvement']:.1f}%"
            )

            print(
                f"   Survival improvement:"
                f" {result['survival_improvement']:.2f} months"
            )

            print(
                f"   Decision quality:    "
                f"{result['decision_quality']}"
            )

            print()
            print("   WHY:")

            for strength in result["explanation"]["strengths"]:
                print(f"   + {strength}")

            print()
            print("   MAIN CONCERNS:")

            for concern in result["explanation"]["concerns"]:
                print(f"   ! {concern}")

            print()
            print("   ACTION:")

            for action in result["explanation"]["actions"]:
                print(f"   -> {action}")

            print()

        print("=" * 50)
        print("              BEST DECISION")
        print("=" * 50)

        print()
        print(f"Recommended Scenario: {best_decision['name']}")
        print(f"Decision Score:       {best_decision['decision_score']}/100")
        print(f"Decision Quality:     {best_decision['decision_quality']}")
        print(f"Recommendation:       {best_decision['recommendation']}")
        print(f"Risk:                 {best_decision['risk']}")

        print()
        print("ACTION:")

        for action in best_decision["reasons"]:
            print(f"-> {action}")

        print("=" * 50)
        return

    business_values = [
        args.revenue,
        args.expenses,
        args.cash,
        args.growth,
        args.customers,
    ]

    if any(value is not None for value in business_values):
        if any(value is None for value in business_values):
            parser.error(
                "When using CLI arguments, provide all five: "
                "--revenue --expenses --cash --growth --customers"
            )

        revenue = args.revenue
        expenses = args.expenses
        cash = args.cash
        growth_rate = args.growth
        customers = args.customers

    else:
        print("=" * 40)
        print("      BUSINESS DECISION ENGINE")
        print("=" * 40)

        revenue = float(input("Monthly revenue: $"))
        expenses = float(input("Monthly expenses: $"))
        cash = float(input("Cash available: $"))
        growth_rate = float(input("Monthly growth rate (%): "))
        customers = int(input("Number of customers: "))

    result = calculate_decision(
        revenue,
        expenses,
        cash,
        growth_rate,
        customers
    )

    explanation = explain_decision(result)

    if args.json:
        output = {
            "profit": result["profit"],
            "margin": result["margin"],
            "runway": result["runway"],
            "score": result["score"],
            "recommendation": result["recommendation"],
            "risk": result["risk"],
            "reasons": result["reasons"],
            "explanation": explanation,
        }

        safe_output = make_json_safe(output)

        print(json.dumps(safe_output, indent=2, allow_nan=False))
        return

    print()
    print("-" * 40)

    print(f"Monthly profit:    ${result['profit']:,.2f}")
    print(f"Profit margin:     {result['margin']:.1f}%")

    if result["runway"] == float("inf"):
        print("Runway:            Unlimited")
    else:
        print(f"Runway:            {result['runway']:.1f} months")

    print(f"Health score:      {result['score']}/100")
    print(f"Recommendation:    {result['recommendation']}")
    print(f"Risk level:        {result['risk']}")

    print()
    print("WHY?")

    for reason in result["reasons"]:
        print(reason)

    print()
    print("MAIN CONCERNS")

    for concern in explanation["concerns"]:
        print(f"! {concern}")

    print()
    print("RECOMMENDED ACTION")

    for action in explanation["actions"]:
        print(f"-> {action}")

    print("-" * 40)


if __name__ == "__main__":
    main()