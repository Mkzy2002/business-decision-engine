# Business Decision Engine

A lightweight CLI tool that helps entrepreneurs evaluate business health and make clearer decisions using a few simple business metrics.

## Features

The engine evaluates:

- Monthly revenue
- Monthly expenses
- Available cash
- Revenue growth
- Customer count

It calculates:

- Monthly profit
- Profit margin
- Cash runway
- Business health score
- Risk level
- Recommended action

## Decision Framework

| Recommendation | Meaning |
|---|---|
| CONTINUE | Business fundamentals are healthy |
| HOLD | Business is viable but needs attention |
| PIVOT | Current model has significant risk or needs change |
| CUT | Business fundamentals are critically weak |

Cash runway is given priority because a profitable business can still fail if it runs out of cash.

## Usage

### Interactive Mode

Run:

    python decision_engine.py

The program will ask for:

- Monthly revenue
- Monthly expenses
- Cash available
- Monthly growth rate
- Number of customers

### CLI Mode

Provide all metrics directly:

    python decision_engine.py --revenue 20000 --expenses 8000 --cash 2500 --growth 8 --customers 50

Example result:

    Monthly profit:    $12,000.00
    Profit margin:     60.0%
    Runway:            0.3 months
    Health score:      55/100
    Recommendation:    PIVOT
    Risk level:        CRITICAL

## Inputs

| Argument | Description |
|---|---|
| --revenue | Monthly revenue |
| --expenses | Monthly operating expenses |
| --cash | Available cash |
| --growth | Monthly revenue growth rate (%) |
| --customers | Number of customers |

All five CLI arguments are required when using CLI mode.

## How the Score Works

| Area | Weight |
|---|---:|
| Profitability | 25 |
| Profit margin | 20 |
| Cash runway | 30 |
| Revenue growth | 15 |
| Customer base | 10 |
| Total | 100 |

Cash runway receives the highest weight because cash survival is critical for small businesses.

## Testing

Run:

    python -m pytest

Current test coverage includes:

- Profitable business
- Low cash runway
- Losing business
- CLI-style decision calculation

Current result:

    4 passed

## Project Structure

    business-decision-engine/
    |-- decision_engine.py
    |-- README.md
    |-- LICENSE
    |-- .gitignore
    |-- tests/
        |-- test_decision.py

## Roadmap

- Add more business metrics
- Improve decision scoring
- Add configurable decision thresholds
- Add JSON output mode
- Add CSV input support
- Add scenario comparison
- Add industry-specific benchmarks
- Improve test coverage
- Package for easier installation

## Why This Project?

Small businesses often have plenty of data but no clear decision framework.

Business Decision Engine turns a few basic business metrics into a simple decision:

CONTINUE -> HOLD -> PIVOT -> CUT

The goal is not to replace human judgment, but to provide a structured starting point for better business decisions.

## License

MIT License
