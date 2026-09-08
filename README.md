# Business Decision Engine

A lightweight open-source business decision-support engine with a Python core and Streamlit dashboard.

The goal is simple:

> **Turn business numbers into clearer decisions.**

The engine evaluates business health, compares alternative scenarios, measures decision impact, and identifies the strongest available option based on profitability, margins, cash runway, growth, customer base, and survival risk.

---

## Current Version

**V8.2.1**

V8.2.1 combines:

* A reusable Python decision engine
* Command-line interface
* JSON output
* Scenario comparison
* Decision scoring
* Business health analysis
* Streamlit web dashboard
* Scenario ranking visualization
* Best Decision panel

The architecture intentionally separates the decision logic from the user interface:

```text
             Streamlit Dashboard
                    |
                    v
          Business Decision Engine
                    |
        +-----------+-----------+
        |           |           |
        v           v           v
     Health      Scenario    Decision
     Analysis    Analysis     Logic
```

The Python engine remains reusable independently of Streamlit.

---

## Features

### Business Health Analysis

The engine evaluates:

* Monthly profit
* Profit margin
* Cash runway
* Revenue growth
* Customer base
* Health Score
* Risk level
* Recommendation
* Strengths
* Concerns
* Recommended actions

Possible recommendations include:

* `CONTINUE`
* `HOLD`
* `PIVOT`
* `CUT`

---

## Health Score

The `Health Score` measures the condition of the business itself.

It considers factors including:

* Profitability
* Profit margin
* Cash runway
* Growth
* Customer base

Example:

```text
Health Score:    55/100
Risk:            CRITICAL
Recommendation:  PIVOT
```

The Health Score answers:

> **How healthy is this business right now?**

---

## Scenario Comparison

The engine can compare multiple possible business decisions against a baseline scenario.

Typical scenarios might include:

* Current business
* Cut expenses
* Increase revenue
* Hire employees
* Launch a new product
* Enter a new market

Each scenario is evaluated independently and then compared against the `Current` baseline.

---

## Decision Impact

The engine measures how each scenario changes the current business.

It evaluates:

* Profit improvement
* Cash runway improvement
* Margin improvement
* Growth improvement
* Survival improvement

This allows the engine to distinguish between:

> A healthier business

and

> A better decision relative to the current situation

These are not always the same thing.

---

## Decision Quality

Each scenario receives a Decision Quality classification.

Possible values:

* `HIGH`
* `MEDIUM`
* `LOW`

Decision Quality represents the strength of the scenario's improvement relative to the current business.

---

## Decision Score

The `Decision Score` evaluates whether a scenario is worth choosing relative to the current situation.

It considers factors including:

* Current business health
* Profit improvement
* Cash runway improvement
* Margin improvement
* Survival impact

The Decision Score answers:

> **How strong is this decision compared with the available alternatives?**

For example, a business can still have:

```text
Health Score:    55/100
Risk:            CRITICAL
Recommendation:  PIVOT
Decision Score:  90/100
```

This does not mean the business is healthy.

It means that scenario may be the strongest available decision under the current conditions.

---

## Survival Override

Cash survival receives additional priority when the business has critically low runway.

Scenarios that fail to improve survival may receive a Decision Score penalty.

Scenarios that improve runway may receive additional decision value.

This prevents the engine from recommending a scenario simply because it produces higher revenue or profit while ignoring an immediate liquidity problem.

---

## Best Decision

After evaluating and ranking scenarios, the engine identifies the strongest available option.

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

---

# Streamlit Dashboard

V8 introduced a Streamlit interface on top of the Python decision engine.

V8.2.1 includes:

* Business information form
* Business Decision dashboard
* Health Score visualization
* Risk and recommendation display
* Financial metrics
* Strengths and concerns
* Recommended actions
* Scenario Builder
* Scenario comparison
* Decision Score ranking
* Scenario ranking
* Best Decision panel
* Decision impact metrics

The Streamlit interface uses the existing Python engine rather than duplicating the business logic.

---

## Dashboard Example

A typical result may look like:

```text
Business Decision

Health Score:     55/100
Risk:             CRITICAL
Recommendation:   PIVOT
Cash Runway:      0.31 mo

Profit:           $12,000
Margin:           60.0%
Customers:        50
```

Scenario comparison:

```text
Decision Score Ranking

#1 Cut Expenses        90/100
#2 Increase Revenue    60/100
#3 Current             35/100
```

Best Decision:

```text
Cut Expenses

Decision Score:       90/100
Decision Quality:     HIGH
Risk:                 CRITICAL
Recommendation:       PIVOT

Profit Improvement:   $3,000
Runway Improvement:   0.19 mo
Margin Improvement:   15.0%
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Mkzy2002/business-decision-engine.git
```

Enter the project directory:

```bash
cd business-decision-engine
```

Python 3.10+ is recommended.

The core decision engine uses only the Python standard library.

The Streamlit dashboard requires Streamlit.

Install Streamlit:

```bash
python -m pip install streamlit
```

Install pytest for development and testing:

```bash
python -m pip install pytest
```

---

# Running the Streamlit Dashboard

Start the web interface with:

```bash
python -m streamlit run app.py
```

Streamlit will provide a local browser address.

The dashboard can then be used to:

1. Enter the current business information.
2. Analyze Business Health.
3. Review risks and recommendations.
4. Build alternative scenarios.
5. Compare those scenarios.
6. Review Decision Score ranking.
7. Identify the Best Decision.

---

# Basic CLI Usage

The Python engine can also be used without Streamlit.

Run:

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

---

# Command-Line Arguments

The engine can be run directly with command-line arguments:

```bash
python decision_engine.py --revenue 20000 --expenses 8000 --cash 2500 --growth 8 --customers 50
```

Example result:

```text
BUSINESS HEALTH

Health Score:       55/100
Risk:               CRITICAL
Recommendation:     PIVOT

FINANCIAL METRICS

Monthly Profit:     $12,000.00
Profit Margin:      60.0%
Cash Runway:        0.3 months
```

---

# JSON Output

The engine supports machine-readable JSON output.

Example:

```bash
python decision_engine.py --revenue 20000 --expenses 8000 --cash 2500 --growth 8 --customers 50 --json
```

Example output:

```json
{
  "profit": 12000.0,
  "margin": 60.0,
  "runway": 0.3125,
  "score": 55,
  "recommendation": "PIVOT",
  "risk": "CRITICAL"
}
```

JSON output makes the engine suitable for integration with:

* Applications
* Dashboards
* APIs
* Automation tools
* Other Python programs

The engine also sanitizes non-finite numeric values before JSON serialization so machine-readable output remains standards-compliant.

---

# Scenario Comparison

The repository includes an example `scenarios.json`.

Example:

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

Run:

```bash
python decision_engine.py --scenario-file scenarios.json
```

The first scenario must be named:

```text
Current
```

This acts as the baseline against which alternative decisions are evaluated.

---

## Example Scenario Ranking

```text
1. Cut Expenses

Health Score:       55/100
Decision Score:     90/100
Decision Quality:   HIGH
Recommendation:     PIVOT
Risk:               CRITICAL


2. Increase Revenue

Health Score:       60/100
Decision Score:     60/100
Decision Quality:   MEDIUM
Recommendation:     PIVOT
Risk:               CRITICAL


3. Current

Health Score:       55/100
Decision Score:     35/100
Decision Quality:   LOW
Recommendation:     PIVOT
Risk:               CRITICAL
```

This demonstrates an important principle:

> **Higher revenue does not automatically mean a better decision.**

For example, reducing expenses can sometimes rank higher than increasing revenue if the expense reduction provides stronger cash-survival improvement.

---

# Input Validation

The engine validates business inputs before performing calculations.

Validation includes checks for:

* Non-numeric values
* Negative revenue
* Negative expenses
* Negative cash
* Negative customers
* Fractional customer counts
* Growth below `-100%`

Scenario comparison also validates:

* Scenario input must be a list
* Scenario list cannot be empty
* Every scenario must be an object
* Required fields must exist
* `Current` must be the first baseline scenario

Invalid inputs raise clear errors rather than silently producing misleading results.

---

# Python API

The engine can be imported and reused by other Python applications.

## `validate_business_inputs()`

Validates business inputs before calculations are performed.

```python
validate_business_inputs()
```

---

## `calculate_decision()`

Evaluates the health of a business.

```python
calculate_decision()
```

---

## `explain_decision()`

Generates:

* Strengths
* Concerns
* Recommended actions

```python
explain_decision()
```

---

## `calculate_decision_quality()`

Measures how a scenario changes the current business.

```python
calculate_decision_quality()
```

---

## `calculate_decision_score()`

Calculates a scenario's Decision Score.

```python
calculate_decision_score()
```

Decision Scores are capped at:

```text
100
```

---

## `apply_survival_override()`

Adjusts Decision Score when cash survival is critical.

```python
apply_survival_override()
```

---

## `compare_scenarios()`

Evaluates and ranks multiple scenarios.

```python
compare_scenarios()
```

---

## `get_best_decision()`

Returns a summary of the highest-ranked scenario.

```python
get_best_decision()
```

---

## `make_json_safe()`

Converts output values into JSON-safe structures.

```python
make_json_safe()
```

Non-finite floating-point values are converted into JSON-compatible values before serialization.

---

# Python Example

Evaluate one business:

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

Compare scenarios:

```python
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
]

results = compare_scenarios(scenarios)

best = get_best_decision(results)

print(best)
```

---

# Project Structure

```text
business-decision-engine/
│
├── app.py
│   └── Streamlit V8.2.1 dashboard
│
├── decision_engine.py
│   └── Core decision engine
│
├── scenarios.json
│   └── Example scenario data
│
├── tests/
│   └── test_decision.py
│
├── README.md
├── LICENSE
└── .gitignore
```

Development backup files may exist locally but are excluded from Git tracking.

Python, pytest, and Streamlit cache files are also excluded.

---

# Testing

The project uses `pytest`.

Run:

```bash
python -m pytest
```

Current test status:

```text
19 passed
```

The test suite currently covers:

* Profitable business analysis
* Low cash runway
* Losing businesses
* CLI arguments
* JSON output
* Scenario comparison
* Decision explanations
* Decision Quality
* Survival Override
* Best Decision selection
* Business input validation
* Negative revenue validation
* Negative cash validation
* Negative customer validation
* Empty scenario validation
* Non-list scenario validation
* Missing scenario fields
* Current baseline validation
* Non-object scenario validation

The current V8.2.1 dashboard uses the tested decision engine without changing the core calculation logic.

---

# Design Philosophy

The engine is intentionally:

* Lightweight
* Explainable
* Reusable
* Testable

It is not intended to replace:

* Accountants
* Financial advisors
* Investors
* Business consultants
* Professional financial analysis

Instead, it provides structured decision support.

The core concept is:

```text
Numbers
   |
   v
Business Health
   |
   v
Scenario Impact
   |
   v
Decision Quality
   |
   v
Decision Score
   |
   v
Best Decision
```

A strong business decision should not depend on a single metric.

For example:

```text
Higher Revenue
      !=
Better Decision
```

A stronger option may instead:

* Extend cash runway
* Improve profitability
* Improve margins
* Reduce downside risk
* Improve survival
* Preserve optionality
* Create more time for future decisions

---

# Version History

## V7 — Decision Engine

Completed:

* [x] Business Health analysis
* [x] CLI interface
* [x] JSON output
* [x] Scenario comparison
* [x] Decision explanations
* [x] Decision Quality
* [x] Decision Score
* [x] Survival Override
* [x] Scenario ranking
* [x] Best Decision selection

---

## V7.5 — Engine Reliability

Completed:

* [x] Input validation
* [x] Scenario validation
* [x] Baseline validation
* [x] Safer JSON output
* [x] Improved CLI semantics
* [x] Improved API output
* [x] Decision Score capped at 100
* [x] Improved Best Decision actions

---

## V8 — Streamlit Interface

Completed:

* [x] Streamlit interface
* [x] Business input form
* [x] Business Decision dashboard
* [x] Persistent Streamlit session state
* [x] Scenario Builder
* [x] Scenario comparison dashboard
* [x] Decision Score visualization
* [x] Scenario ranking
* [x] Best Decision panel
* [x] Decision Impact display

---

## V8.2.1 — Current Stable Version

V8.2.1 is the current frozen project milestone.

The focus of this version is:

> **A stable decision engine with a usable Streamlit decision dashboard.**

No V8.3 functionality is included in this version.

---

# License

This project is open source under the MIT License.

See `LICENSE` for details.

---

# Contributing

Contributions, bug reports, improvements, and alternative decision models are welcome.

Before submitting changes, run:

```bash
python -m pytest
```

Please keep the decision logic:

* Simple
* Explainable
* Testable
* Reusable

For code changes, existing tests should continue to pass.

---

# Disclaimer

Business Decision Engine provides analytical decision support based on information supplied by the user.

It does not provide financial, legal, accounting, investment, or professional business advice.

The output is based on heuristic decision rules and should be treated as one input into a broader decision-making process.

Users remain responsible for evaluating assumptions and making final business decisions.
