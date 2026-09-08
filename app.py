import streamlit as st

from decision_engine import (
    calculate_decision,
    compare_scenarios,
    explain_decision,
    get_best_decision,
)


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Business Decision Engine",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# Session State
# ============================================================

if "business_result" not in st.session_state:
    st.session_state.business_result = None

if "business_explanation" not in st.session_state:
    st.session_state.business_explanation = None

if "scenario_results" not in st.session_state:
    st.session_state.scenario_results = None

if "best_decision" not in st.session_state:
    st.session_state.best_decision = None


# ============================================================
# Helper Functions
# ============================================================

def format_runway(value):
    if value == float("inf"):
        return "Unlimited"

    return f"{value:.2f} mo"


def format_money(value):
    return f"${value:,.0f}"


def score_status(score):
    if score >= 75:
        return "Strong"
    elif score >= 50:
        return "Moderate"
    else:
        return "Weak"


def recommendation_message(recommendation):
    if recommendation == "CONTINUE":
        return (
            "🟢 CONTINUE — The current business direction "
            "shows acceptable health."
        )

    if recommendation == "HOLD":
        return (
            "🟡 HOLD — The business can continue, but weak "
            "areas should be improved before expansion."
        )

    if recommendation == "PIVOT":
        return (
            "🟠 PIVOT — The current direction requires "
            "a different approach."
        )

    if recommendation == "CUT":
        return (
            "🔴 CUT — Consider stopping or significantly "
            "reducing the current activity."
        )

    return recommendation


# ============================================================
# Header
# ============================================================

st.title("📊 Business Decision Engine")

st.caption(
    "Evaluate business health, compare strategic scenarios, "
    "and identify the best available decision."
)


# ============================================================
# Business Information
# ============================================================

st.header("Business Information")

with st.form("business_form"):

    input_col1, input_col2 = st.columns(2)

    with input_col1:

        revenue = st.number_input(
            "Monthly Revenue ($)",
            min_value=0.0,
            value=20000.0,
            step=1000.0,
        )

        expenses = st.number_input(
            "Monthly Expenses ($)",
            min_value=0.0,
            value=8000.0,
            step=1000.0,
        )

        cash = st.number_input(
            "Cash Available ($)",
            min_value=0.0,
            value=2500.0,
            step=500.0,
        )

    with input_col2:

        growth = st.number_input(
            "Monthly Growth Rate (%)",
            min_value=-100.0,
            value=8.0,
            step=1.0,
        )

        customers = st.number_input(
            "Number of Customers",
            min_value=0,
            value=50,
            step=1,
        )

    analyze_clicked = st.form_submit_button(
        "Analyze Business",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# Analyze Business
# ============================================================

if analyze_clicked:

    try:

        result = calculate_decision(
            revenue=revenue,
            expenses=expenses,
            cash=cash,
            growth_rate=growth,
            customers=customers,
        )

        explanation = explain_decision(result)

        st.session_state.business_result = result
        st.session_state.business_explanation = explanation

        # Reset scenarios when baseline business changes.
        st.session_state.scenario_results = None
        st.session_state.best_decision = None

    except ValueError as error:

        st.session_state.business_result = None
        st.session_state.business_explanation = None

        st.error(
            f"Invalid business input: {error}"
        )


# ============================================================
# Business Decision Dashboard
# ============================================================

result = st.session_state.business_result
explanation = st.session_state.business_explanation


if result is not None and explanation is not None:

    st.divider()

    st.header("Business Decision")

    # --------------------------------------------------------
    # Primary Dashboard
    # --------------------------------------------------------

    dashboard_col1, dashboard_col2, dashboard_col3, dashboard_col4 = (
        st.columns(4)
    )

    with dashboard_col1:

        st.metric(
            "Health Score",
            f"{result['score']}/100",
            score_status(result["score"]),
        )

        st.progress(
            min(result["score"], 100) / 100
        )

    with dashboard_col2:

        st.metric(
            "Risk",
            result["risk"],
        )

    with dashboard_col3:

        st.metric(
            "Recommendation",
            result["recommendation"],
        )

    with dashboard_col4:

        st.metric(
            "Cash Runway",
            format_runway(result["runway"]),
        )

    st.write("")

    # --------------------------------------------------------
    # Recommendation Banner
    # --------------------------------------------------------

    if result["recommendation"] == "PIVOT":
        st.warning(
            recommendation_message(
                result["recommendation"]
            )
        )

    elif result["recommendation"] == "HOLD":
        st.info(
            recommendation_message(
                result["recommendation"]
            )
        )

    elif result["recommendation"] == "CONTINUE":
        st.success(
            recommendation_message(
                result["recommendation"]
            )
        )

    elif result["recommendation"] == "CUT":
        st.error(
            recommendation_message(
                result["recommendation"]
            )
        )

    # --------------------------------------------------------
    # Financial Metrics
    # --------------------------------------------------------

    st.subheader("Financial Metrics")

    financial1, financial2, financial3, financial4 = (
        st.columns(4)
    )

    with financial1:

        st.metric(
            "Monthly Profit",
            format_money(result["profit"]),
        )

    with financial2:

        st.metric(
            "Profit Margin",
            f"{result['margin']:.1f}%",
        )

    with financial3:

        st.metric(
            "Cash",
            format_money(cash),
        )

    with financial4:

        st.metric(
            "Customers",
            f"{int(customers):,}",
        )

    # --------------------------------------------------------
    # Explanation
    # --------------------------------------------------------

    st.subheader("Decision Explanation")

    why_col, concern_col, action_col = st.columns(3)

    with why_col:

        st.markdown("#### 💪 Strengths")

        for strength in explanation["strengths"]:
            st.success(strength)

    with concern_col:

        st.markdown("#### ⚠️ Main Concerns")

        for concern in explanation["concerns"]:
            st.warning(concern)

    with action_col:

        st.markdown("#### 🎯 Recommended Actions")

        for action in explanation["actions"]:
            st.info(f"→ {action}")


# ============================================================
# Scenario Comparison
# ============================================================

if result is not None:

    st.divider()

    st.header("Scenario Comparison")

    st.caption(
        "Compare the current business with possible "
        "strategic changes."
    )

    st.subheader("Scenario Builder")

    current_scenario = {
        "name": "Current",
        "revenue": revenue,
        "expenses": expenses,
        "cash": cash,
        "growth": growth,
        "customers": int(customers),
    }

    # --------------------------------------------------------
    # Scenario Form
    # --------------------------------------------------------

    with st.form("scenario_form"):

        scenario1_col1, scenario1_col2 = st.columns(2)

        with scenario1_col1:

            scenario1_name = st.text_input(
                "Scenario 1 Name",
                value="Cut Expenses",
            )

            scenario1_revenue = st.number_input(
                "Scenario 1 Revenue ($)",
                min_value=0.0,
                value=float(revenue),
                step=1000.0,
            )

            scenario1_expenses = st.number_input(
                "Scenario 1 Expenses ($)",
                min_value=0.0,
                value=max(
                    0.0,
                    float(expenses) - 3000.0,
                ),
                step=1000.0,
            )

        with scenario1_col2:

            scenario1_cash = st.number_input(
                "Scenario 1 Cash ($)",
                min_value=0.0,
                value=float(cash),
                step=500.0,
            )

            scenario1_growth = st.number_input(
                "Scenario 1 Growth (%)",
                min_value=-100.0,
                value=float(growth),
                step=1.0,
            )

            scenario1_customers = st.number_input(
                "Scenario 1 Customers",
                min_value=0,
                value=int(customers),
                step=1,
            )

        st.divider()

        scenario2_col1, scenario2_col2 = st.columns(2)

        with scenario2_col1:

            scenario2_name = st.text_input(
                "Scenario 2 Name",
                value="Increase Revenue",
            )

            scenario2_revenue = st.number_input(
                "Scenario 2 Revenue ($)",
                min_value=0.0,
                value=float(revenue) + 10000.0,
                step=1000.0,
            )

            scenario2_expenses = st.number_input(
                "Scenario 2 Expenses ($)",
                min_value=0.0,
                value=float(expenses),
                step=1000.0,
            )

        with scenario2_col2:

            scenario2_cash = st.number_input(
                "Scenario 2 Cash ($)",
                min_value=0.0,
                value=float(cash),
                step=500.0,
            )

            scenario2_growth = st.number_input(
                "Scenario 2 Growth (%)",
                min_value=-100.0,
                value=float(growth) + 5.0,
                step=1.0,
            )

            scenario2_customers = st.number_input(
                "Scenario 2 Customers",
                min_value=0,
                value=int(customers),
                step=1,
            )

        st.divider()

        compare_clicked = st.form_submit_button(
            "Compare Scenarios",
            type="secondary",
            use_container_width=True,
        )


    # ========================================================
    # Compare Scenarios
    # ========================================================

    if compare_clicked:

        scenarios = [
            current_scenario,
            {
                "name": scenario1_name,
                "revenue": scenario1_revenue,
                "expenses": scenario1_expenses,
                "cash": scenario1_cash,
                "growth": scenario1_growth,
                "customers": int(scenario1_customers),
            },
            {
                "name": scenario2_name,
                "revenue": scenario2_revenue,
                "expenses": scenario2_expenses,
                "cash": scenario2_cash,
                "growth": scenario2_growth,
                "customers": int(scenario2_customers),
            },
        ]

        try:

            results = compare_scenarios(scenarios)

            best_decision = get_best_decision(results)

            st.session_state.scenario_results = results
            st.session_state.best_decision = best_decision

        except ValueError as error:

            st.session_state.scenario_results = None
            st.session_state.best_decision = None

            st.error(
                f"Unable to compare scenarios: {error}"
            )


# ============================================================
# Scenario Dashboard
# ============================================================

scenario_results = st.session_state.scenario_results
best_decision = st.session_state.best_decision


if scenario_results is not None and best_decision is not None:

    st.divider()

    st.header("Scenario Dashboard")

    # --------------------------------------------------------
    # Best Decision Hero
    # --------------------------------------------------------

    st.success(
        f"🏆 BEST DECISION: "
        f"{best_decision['name']} "
        f"— {best_decision['decision_score']}/100"
    )

    # --------------------------------------------------------
    # Decision Score Ranking
    # --------------------------------------------------------

    st.subheader("Decision Score Ranking")

    ranked_results = sorted(
        scenario_results,
        key=lambda x: x["decision_score"],
        reverse=True,
    )

    for rank, scenario_result in enumerate(
        ranked_results,
        start=1,
    ):

        name = scenario_result["name"]
        score = scenario_result["decision_score"]

        rank_col, bar_col, score_col = st.columns(
            [2, 6, 1]
        )

        with rank_col:

            if rank == 1:
                st.write(f"🏆 **#{rank} {name}**")
            else:
                st.write(f"**#{rank} {name}**")

        with bar_col:

            st.progress(
                min(score, 100) / 100
            )

        with score_col:

            st.write(
                f"**{score}/100**"
            )

    # --------------------------------------------------------
    # Scenario Ranking
    # --------------------------------------------------------

    st.subheader("Scenario Ranking")

    for index, scenario_result in enumerate(
        ranked_results,
        start=1,
    ):

        is_best = (
            scenario_result["name"]
            == best_decision["name"]
        )

        if is_best:

            st.markdown(
                f"### 🏆 #{index} "
                f"{scenario_result['name']} — BEST DECISION"
            )

            expanded = True

        else:

            expanded = False

        with st.expander(
            f"#{index} {scenario_result['name']}",
            expanded=expanded,
        ):

            score1, score2, score3, score4 = (
                st.columns(4)
            )

            with score1:

                st.metric(
                    "Health Score",
                    f"{scenario_result['score']}/100",
                )

            with score2:

                st.metric(
                    "Decision Score",
                    f"{scenario_result['decision_score']}/100",
                )

            with score3:

                st.metric(
                    "Decision Quality",
                    scenario_result[
                        "decision_quality"
                    ],
                )

            with score4:

                st.metric(
                    "Risk",
                    scenario_result["risk"],
                )

            st.write(
                f"**Recommendation:** "
                f"{scenario_result['recommendation']}"
            )

            impact1, impact2, impact3 = st.columns(3)

            with impact1:

                st.metric(
                    "Profit Improvement",
                    format_money(
                        scenario_result[
                            "profit_improvement"
                        ]
                    ),
                )

            with impact2:

                runway_improvement = (
                    scenario_result[
                        "runway_improvement"
                    ]
                )

                if runway_improvement == float("inf"):

                    runway_text = "Unlimited"

                else:

                    runway_text = (
                        f"{runway_improvement:.2f} mo"
                    )

                st.metric(
                    "Runway Improvement",
                    runway_text,
                )

            with impact3:

                st.metric(
                    "Margin Improvement",
                    f"{scenario_result['margin_improvement']:.1f}%",
                )

            explanation_data = scenario_result[
                "explanation"
            ]

            st.markdown("#### Strengths")

            for strength in explanation_data[
                "strengths"
            ]:

                st.success(strength)

            st.markdown("#### Main Concerns")

            for concern in explanation_data[
                "concerns"
            ]:

                st.warning(concern)

            st.markdown("#### Recommended Actions")

            for action in explanation_data[
                "actions"
            ]:

                st.info(f"→ {action}")


        # ========================================================
    # Best Decision Summary
    # ========================================================

    st.divider()

    st.header("🏆 Best Decision")

    # Find the complete scenario result for the best decision.
    best_scenario = next(
        (
            scenario
            for scenario in scenario_results
            if scenario["name"] == best_decision["name"]
        ),
        None,
    )

    if best_scenario is not None:

        st.markdown(
            f"## {best_scenario['name']}"
        )

        best1, best2, best3, best4 = st.columns(4)

        with best1:

            st.metric(
                "Decision Score",
                f"{best_scenario['decision_score']}/100",
            )

        with best2:

            st.metric(
                "Decision Quality",
                best_scenario["decision_quality"],
            )

        with best3:

            st.metric(
                "Risk",
                best_scenario["risk"],
            )

        with best4:

            st.metric(
                "Recommendation",
                best_scenario["recommendation"],
            )

        st.subheader("Decision Impact")

        best_impact1, best_impact2, best_impact3 = (
            st.columns(3)
        )

        with best_impact1:

            st.metric(
                "Profit Improvement",
                format_money(
                    best_scenario["profit_improvement"]
                ),
            )

        with best_impact2:

            runway_improvement = (
                best_scenario["runway_improvement"]
            )

            if runway_improvement == float("inf"):

                runway_text = "Unlimited"

            else:

                runway_text = (
                    f"{runway_improvement:.2f} mo"
                )

            st.metric(
                "Runway Improvement",
                runway_text,
            )

        with best_impact3:

            st.metric(
                "Margin Improvement",
                f"{best_scenario['margin_improvement']:.1f}%",
            )

        st.subheader("Recommended Actions")

        for action in best_decision["actions"]:

            st.info(f"→ {action}")

    else:

        st.error(
            "Unable to locate the best scenario result."
        )

# ============================================================
# Technical Details
# ============================================================

if result is not None:

    st.divider()

    with st.expander("View Decision Engine Details"):

        detail1, detail2 = st.columns(2)

        with detail1:

            st.write("**Health Score**")
            st.write(
                f"{result['score']}/100"
            )

            st.write("**Recommendation**")
            st.write(
                result["recommendation"]
            )

            st.write("**Risk**")
            st.write(
                result["risk"]
            )

        with detail2:

            st.write("**Monthly Profit**")
            st.write(
                f"${result['profit']:,.2f}"
            )

            st.write("**Profit Margin**")
            st.write(
                f"{result['margin']:.1f}%"
            )

            st.write("**Cash Runway**")

            if result["runway"] == float("inf"):

                st.write("Unlimited")

            else:

                st.write(
                    f"{result['runway']:.2f} months"
                )


# ============================================================
# Footer
# ============================================================

st.divider()

st.caption(
    "Business Decision Engine — V8.2.1"
)