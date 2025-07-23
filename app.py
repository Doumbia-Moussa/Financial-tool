import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ----------------- CONFIGURATION ------------------
st.set_page_config(page_title="BARKA FUND", layout="wide")

# ----------------- LANGUAGE TOGGLE ------------------
lang = st.sidebar.selectbox("🌐 Language / Langue", ["English", "Français"])
is_en = lang == "English"

# ----------------- LOGO + TITRE ------------------
col1, col2 = st.columns([1, 8])
with col1:
    st.image("barka_logo.png", width=130)
with col2:
    st.title("BARKA FUND – Financial Dashboard")

st.markdown("""
<p style='font-size:16px'>
    <strong>BARKA FUND</strong> provides this tool to help early-stage businesses structure, analyze, and interpret their key financials. 
    Complete the required fields below to automatically generate your financial statements, ratios, and performance indicators.
</p>
""", unsafe_allow_html=True)

# ----------------- INPUT SECTION ------------------
st.header("1. Input Financial Data" if is_en else "1. Saisissez les données financières")

col1, col2 = st.columns(2)
with col1:
    revenue = st.number_input("Revenue (Sales)", min_value=0.0, value=0.0)
    cogs = st.number_input("Cost of Goods Sold (COGS)", min_value=0.0, value=0.0)
    opex = st.number_input("Operating Expenses", min_value=0.0, value=0.0)
    taxes = st.number_input("Taxes", min_value=0.0, value=0.0)
with col2:
    cash = st.number_input("Cash", min_value=0.0, value=0.0)
    receivables = st.number_input("Accounts Receivable", min_value=0.0, value=0.0)
    inventory = st.number_input("Inventory", min_value=0.0, value=0.0)
    fixed_assets = st.number_input("Fixed Assets", min_value=0.0, value=0.0)

st.subheader("Liabilities and Equity")
col1, col2 = st.columns(2)
with col1:
    current_liab = st.number_input("Current Liabilities", min_value=0.0, value=0.0)
    long_term_liab = st.number_input("Long-Term Liabilities", min_value=0.0, value=0.0)
with col2:
    equity = st.number_input("Equity (Initial Capital)", min_value=0.0, value=0.0)

# ----------------- CASH FLOW SETTINGS ------------------
st.subheader("Cash Flow Settings" if is_en else "Paramètres de flux de trésorerie")

cashflow_investing = st.number_input(
    "Cash Flow from Investing Activities" if is_en else "Flux de trésorerie liés aux investissements",
    value=-5000.0
)

# ----------------- CALCULATIONS ------------------
gross_profit = revenue - cogs
operating_profit = gross_profit - opex
net_income = operating_profit - taxes

total_assets = cash + receivables + inventory + fixed_assets
total_liabilities = current_liab + long_term_liab
equity_calc = total_assets - total_liabilities

cashflow_operating = operating_profit
cashflow_financing = equity - equity_calc  # Variation de capital
cashflow_net = cashflow_operating + cashflow_investing + cashflow_financing

# ----------------- ÉTATS FINANCIERS ------------------
st.header("2. Financial Statements" if is_en else "2. États financiers")

st.subheader("📊 Income Statement" if is_en else "📊 Compte de résultat")
income_df = pd.DataFrame({
    "Description": ["Revenue", "COGS", "Gross Profit", "Operating Expenses", "Operating Profit", "Taxes", "Net Income"],
    "Amount": [revenue, -cogs, gross_profit, -opex, operating_profit, -taxes, net_income]
})
st.dataframe(income_df, use_container_width=True)

st.subheader("📄 Balance Sheet" if is_en else "📄 Bilan")
balance_df = pd.DataFrame({
    "Assets": ["Cash", "Accounts Receivable", "Inventory", "Fixed Assets", "", "Total Assets"],
    "Value A": [cash, receivables, inventory, fixed_assets, "", total_assets],
    "Liabilities & Equity": ["Current Liabilities", "Long-Term Liabilities", "", "Equity", "", "Total Liabilities + Equity"],
    "Value B": [current_liab, long_term_liab, "", equity_calc, "", total_liabilities + equity_calc]
})
st.dataframe(balance_df, use_container_width=True)

st.subheader("💸 Cash Flow Statement" if is_en else "💸 Tableau de flux de trésorerie")
cashflow_df = pd.DataFrame({
    "Cash Flow Item": ["Operating Activities", "Investing Activities", "Financing Activities", "Net Cash Flow"],
    "Amount": [cashflow_operating, cashflow_investing, cashflow_financing, cashflow_net]
})
st.dataframe(cashflow_df, use_container_width=True)

# ----------------- RATIOS ------------------
st.header("3. Financial Ratios & Analysis" if is_en else "3. Ratios et interprétations")

ratios = {
    "Net Profit Margin": net_income / revenue if revenue else 0,
    "Operating Margin": operating_profit / revenue if revenue else 0,
    "Gross Margin": gross_profit / revenue if revenue else 0,
    "ROA (Return on Assets)": net_income / total_assets if total_assets else 0,
    "Current Ratio": (cash + receivables + inventory) / current_liab if current_liab else 0,
    "Debt to Equity": total_liabilities / equity_calc if equity_calc else 0,
}

# Interpretation
interpretations = {
    "Net Profit Margin": "Indicates overall profitability.",
    "Operating Margin": "Efficiency of core operations.",
    "Gross Margin": "Profit after production costs.",
    "ROA (Return on Assets)": "Return generated per dollar of assets.",
    "Current Ratio": "Short-term solvency.",
    "Debt to Equity": "Leverage and capital structure."
}

# Display ratio in selectable segments
selected_ratio = st.selectbox("Select a ratio to visualize", list(ratios.keys()))
st.metric(label=selected_ratio, value=f"{ratios[selected_ratio]*100:.2f} %")
st.caption(interpretations[selected_ratio])

# ----------------- FOOTER ------------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align:center; font-size:14px; color:gray'>
        📞 Need help? Schedule a session with BARKA FUND analysts for personalized support.<br>
        📧 <a href='mailto:ornella@barkafund.com'>ornella@barkafund.com</a>
    </div>
    """, unsafe_allow_html=True
)

# ----------------- RESET BUTTON ------------------
if st.button("🔄 Reset all values"):
    st.session_state.clear()
    st.rerun()
