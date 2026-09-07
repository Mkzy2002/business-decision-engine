# Business Decision Engine

A lightweight CLI tool that helps entrepreneurs evaluate business health and make clearer decisions using a few simple business metrics.

The engine evaluates:

- Monthly revenue
- Monthly expenses
- Available cash
- Revenue growth
- Customer count

It then calculates:

- Monthly profit
- Profit margin
- Cash runway
- Business health score
- Risk level
- Recommended action

## Decision Framework

The engine produces one of four recommendations:

| Recommendation | Meaning |
|---|---|
| CONTINUE | Business fundamentals are healthy |
| HOLD | Business is viable but needs attention |
| PIVOT | Current model has significant risk or needs change |
| CUT | Business fundamentals are critically weak |

Cash runway is given priority because a profitable business can still fail if it runs out of cash.

## Example

```text
========================================
      BUSINESS DECISION ENGINE
========================================
Monthly revenue: $20000
Monthly expenses: $8000
Cash available: $2500
Monthly growth rate (%): 8
Number of customers: 50

----------------------------------------
Monthly profit:    $12,000.00
Profit margin:     60.0%
Runway:            0.3 months
Health score:      55/100
Recommendation:    PIVOT
Risk level:        CRITICAL

WHY?
WARNING: Extremely low cash runway
OK: Business is profitable
OK: Strong profit margin
OK: Established customer base
----------------------------------------