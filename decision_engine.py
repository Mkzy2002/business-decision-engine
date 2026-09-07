import argparse
import json


def calculate_decision(revenue, expenses, cash, growth_rate, customers):
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
        "--json",
        action="store_true",
        help="Output the decision as JSON"
    )

    args = parser.parse_args()

    # If CLI business arguments are provided, use them.
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

    # Otherwise use interactive mode.
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

    # JSON mode
    if args.json:
        output = {
            "profit": result["profit"],
            "margin": result["margin"],
            "runway": result["runway"],
            "score": result["score"],
            "recommendation": result["recommendation"],
            "risk": result["risk"],
            "reasons": result["reasons"],
        }

        print(json.dumps(output, indent=2))
        return

    # Normal output
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

    print("-" * 40)


if __name__ == "__main__":
    main()