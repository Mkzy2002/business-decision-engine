# Business Decision Engine

A lightweight open-source decision-support engine for evaluating business health, comparing business scenarios, and identifying stronger business decisions.

The goal is simple:

> **Turn business numbers into clearer decisions.**

The engine considers profitability, profit margin, cash runway, growth, customers, scenario impact, and survival risk instead of relying on a single business metric.

## Features

### Business Health Analysis

The engine evaluates:

* Monthly profit
* Profit margin
* Cash runway
* Revenue growth
* Customer base
* Overall health score
* Recommendation
* Risk level
* Decision reasons

Possible recommendations:

* `CONTINUE`
* `HOLD`
* `PIVOT`
* `CUT`

### Scenario Comparison

Compare multiple business scenarios using a JSON scenario file.

Example scenarios include:

* Current business
* Cut expenses
* Increase revenue
* Hire employees
* Launch a new product
* Enter a new market

The engine calculates the impact of each scenario and ranks them.

### Decision Quality

The engine measures how each scenario changes the current business.

It evaluates:

* Profit improvement
* Runway improvement
* Margin improvement
* Growth improvement
* Survival improvement
* Decision quality

Decision quality can be:

* `HIGH`
* `MEDIUM`
* `LOW`

### Decision Score

The `Decision Score` evaluates the quality of a business scenario relative to the current situation.

It considers:

* Current business health
* Profit improvement
* Cash runway improvement
* Margin improvement
* Survival risk

### Survival Override

Cash survival receives priority when the current business has less than one month of runway.

Scenarios that do not improve survival can receive a penalty, while scenarios that improve runway can receive additional decision value.

This helps prevent the engine from recommending a scenario simply because it produces higher profit while ignoring an immediate cash crisis.

### Best Decision

After comparing scenarios, the engine identifies the highest-ranked option.

Example:

```text
==================================================
              BEST DECISION
==================================================

Recommended Scenario: Cut Expenses
Decision Score:       90/100
Decision Quality:     HIGH
Recommendation:       PIVOT
Risk:                 CRITICAL

ACTION:
-> Secure additional cash runway immediately
-> Test a different business approach before committing more resources
==================================================
```

## How It Works

The engine follows this decision process:

```text
Business Data
     |
     v
Business Health
     |
     v
Scenario Comparison
     |
     v
Decision Impact
     |
     v
Decision Quality
     |
     v
Decision Score
     |
     v
Survival Override
     |
     v
Scenario Ranking
     |
     v
Best Decision
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Mkzy2002/business-decision-engine.git
```

Enter the project directory:

```bash
cd business-decision-engine
```

Python 3.10+ is recommended.

The core engine has no external runtime dependencies.

## Basic Usage

Run the interactive CLI:

```bash
python decision_engine.py
```

The program will ask for:

* Monthly revenue
* Monthly expenses
* Cash available
* Monthly growth rate
* Number of customers

Example:

```text
Monthly revenue: $20000
Monthly expenses: $8000
Cash available: $2500
Monthly growth rate (%): 8
Number of customers: 50
```

## Command-Line Usage

The engine can also be used directly with command-line arguments:

```bash
python decision_engine.py --revenue 20000 --expenses 8000 --cash 2500 --growth 8 --customers 50
```

Example output:

```text
Monthly profit:    $12,000.00
Profit margin:     60.0%
Runway:            0.3 months
Health score:      55/100
Recommendation:    PIVOT
Risk level:        CRITICAL
```

## JSON Output

The engine supports machine-readable JSON output.

```bash
python decision_engine.py --revenue 20000 --expenses 8000 --cash 2500 --growth 8 --customers 50 --json
```

Example:

```json
{
  "profit": 12000.0,
  "margin": 60.0,
  "runway": 0.3125,
  "score": 55,
  "recommendation": "PIVOT",
  "risk": "CRITICAL",
  "reasons": [
    "WARNING: Extremely low cash runway",
    "OK: Business is profitable",
    "OK: Strong profit margin",
    "OK: Established customer base"
  ],
  "explanation": {
    "strengths": [
      "Business is profitable",
      "Strong profit margin",
      "Healthy unit economics"
    ],
    "concerns": [
      "Cash runway is critically low"
    ],
    "actions": [
      "Secure additional cash runway immediately",
      "Test a different business approach before committing more resources"
    ]
  }
}
```

JSON output makes the engine easier to integrate with:

* Applications
* Dashboards
* APIs
* Automation tools
* Other Python programs

## Scenario Comparison

Create a scenario file named `scenarios.json`:

```json
[
  {
    "name": "Current",
    "revenue": 20000,
    "expenses": 8000,
    "cash": 2500,
    "growth": 8,
    "customers": 50
  },
  {
    "name": "Cut Expenses",
    "revenue": 20000,
    "expenses": 5000,
    "cash": 2500,
    "growth": 8,
    "customers": 50
  },
  {
    "name": "Increase Revenue",
    "revenue": 30000,
    "expenses": 8000,
    "cash": 2500,
    "growth": 15,
    "customers": 50
  }
]
```

Run the comparison:

```bash
python decision_engine.py --scenario-file scenarios.json
```

The engine will:

1. Evaluate each scenario.
2. Compare each scenario against the current scenario.
3. Calculate scenario improvements.
4. Calculate decision quality.
5. Calculate the decision score.
6. Apply the survival override.
7. Rank the scenarios.
8. Select the best decision.

### Example Ranking

```text
1. Cut Expenses
   Score:          55/100
   Decision Score: 90
   Recommendation: PIVOT
   Risk:            CRITICAL

2. Increase Revenue
   Score:          60/100
   Decision Score: 60
   Recommendation: PIVOT
   Risk:            CRITICAL

3. Current
   Score:          55/100
   Decision Score: 35
   Recommendation: PIVOT
   Risk:            CRITICAL
```

This demonstrates an important principle:

> Higher revenue does not automatically mean a better decision.

A cost-reduction scenario can rank higher when it improves cash survival more effectively.

## Python API

The core engine is designed to be used directly from Python.

### `calculate_decision()`

Evaluates the health of a single business.

```python
calculate_decision()
```

### `explain_decision()`

Generates strengths, concerns, and recommended actions.

```python
explain_decision()
```

### `calculate_decision_quality()`

Measures how a scenario changes the current business.

```python
calculate_decision_quality()
```

### `calculate_decision_score()`

Calculates the decision score for a scenario.

```python
calculate_decision_score()
```

### `apply_survival_override()`

Adjusts the decision score when cash survival is critical.

```python
apply_survival_override()
```

### `compare_scenarios()`

Compares and ranks multiple business scenarios.

```python
compare_scenarios()
```

### `get_best_decision()`

Returns the highest-ranked scenario.

```python
get_best_decision()
```

## Python Example

Evaluate a single business:

```python
from decision_engine import calculate_decision

result = calculate_decision(
    revenue=20000,
    expenses=8000,
    cash=2500,
    growth_rate=8,
    customers=50,
)

print(result)
```

Compare multiple scenarios:

```python
from decision_engine import compare_scenarios, get_best_decision

results = compare_scenarios(scenarios)

best = get_best_decision(results)

print(best)
```

## Project Structure

```text
business-decision-engine/
|
├── decision_engine.py
├── scenarios.json
|
├── tests/
│   └── test_decision.py
|
├── README.md
├── LICENSE
├── .gitignore
|
└── decision_engine_vXX_backup.py
```

Version backup files are kept locally for development and excluded from Git tracking.

## Testing

The project uses `pytest`.

Run the test suite:

```bash
python -m pytest
```

The current test suite covers:

* Basic business calculations
* Profitability
* Profit margin
* Cash runway
* Business recommendations
* JSON output
* Scenario comparison
* Decision explanations
* Decision quality
* Decision score
* Survival override
* Scenario ranking
* Best decision selection

Current test status:

```text
10 passed
```

## Design Philosophy

The engine is intentionally lightweight and explainable.

It is not designed to replace:

* Accountants
* Financial advisors
* Investors
* Business consultants
* Professional financial analysis

Instead, it is designed as a decision-support tool.

The core idea is:

```text
Numbers
   |
   v
Business Context
   |
   v
Scenario Impact
   |
   v
Decision
```

A business decision should not be based on a single metric.

For example:

```text
Higher Revenue
      !=
Better Decision
```

A stronger decision may instead be the option that:

* Extends cash runway
* Improves profitability
* Reduces downside risk
* Improves margins
* Preserves optionality
* Creates more time to test the next move

## Current Version

**V7.4**

Current capabilities:

* Business health analysis
* CLI interface
* JSON output
* Scenario comparison
* Decision explanations
* Decision quality
* Decision scoring
* Survival override
* Scenario ranking
* Best decision selection

## Roadmap

### V7 — Decision Quality & Scenario Analysis

* [x] Scenario comparison
* [x] Decision explanation
* [x] Decision quality
* [x] Decision score
* [x] Survival override
* [x] Scenario ranking
* [x] Best decision

### V7.5 — Engine/API Improvements

Planned:

* [ ] Cleaner Python API
* [ ] Input validation
* [ ] Better error handling
* [ ] Baseline/current scenario validation
* [ ] Improved decision explanations
* [ ] More robust JSON output

### V8 — Streamlit Interface

Planned:

* [ ] Streamlit interface
* [ ] Business input form
* [ ] Scenario builder
* [ ] Scenario comparison dashboard
* [ ] Decision visualization
* [ ] Best decision panel

The intended architecture is:

```text
                Streamlit GUI
                     |
                     v
          Business Decision Engine
                     |
          +----------+----------+
          |          |          |
          v          v          v
       Health    Scenarios   Decision
       Analysis  Analysis     Logic
```

The business logic will remain in the Python engine so it can be reused by different interfaces and applications.

## License

This project is open source under the MIT License.

See `LICENSE` for details.

## Contributing

Contributions, improvements, bug reports, and new decision models are welcome.

Before submitting changes, run:

```bash
python -m pytest
```

Please keep the core decision logic:

* Simple
* Explainable
* Testable
* Reusable

## Disclaimer

This project provides analytical decision support based on the information supplied by the user.

It does not provide financial, legal, accounting, investment, or professional business advice.

Users are responsible for evaluating the assumptions and decisions produced by the engine.
