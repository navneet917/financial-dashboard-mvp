# Streamlit Corporate-Level MVP for Financial Dashboard

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# Set page layout
st.set_page_config(layout="wide", page_title="Financial Dashboard MVP")
st.title("🏦 Personal Financial Health Dashboard")

# Dummy client data (replace with DB or upload later)
clients = {
    "John Doe": {
        "income": 1200000,
        "expenses": 800000,
        "assets": {
            "Cash": 200000,
            "FDs": 300000,
            "Equity": 400000,
            "MFs": 300000,
            "EPF": 200000,
            "Gold": 100000,
            "Real Estate": 1000000
        },
        "liabilities": {
            "Home Loan": 800000,
            "Car Loan": 200000
        },
        "portfolio": {
            "Equity": 400000,
            "MFs": 300000
        },
        "emergency_fund": 100000
    },
    "Anita Sharma": {
        "income": 900000,
        "expenses": 550000,
        "assets": {
            "Cash": 100000,
            "FDs": 250000,
            "Equity": 250000,
            "MFs": 200000,
            "EPF": 150000,
            "Gold": 80000,
            "Real Estate": 800000
        },
        "liabilities": {
            "Home Loan": 500000
        },
        "portfolio": {
            "Equity": 250000,
            "MFs": 200000
        },
        "emergency_fund": 80000
    }
}

client_names = list(clients.keys())
selected_client = st.sidebar.selectbox("Select Client", client_names)
data = clients[selected_client]

# --- Net Worth Calculation ---
net_worth = sum(data["assets"].values()) - sum(data["liabilities"].values())

# --- Scoring Models ---
savings_rate = 1 - data['expenses'] / data['income']
debt_ratio = sum(data['liabilities'].values()) / data['income']
emergency_months = data['emergency_fund'] / (data['expenses'] / 12)

scores = {
    "Investment Score": int(min(100, (sum(data['portfolio'].values()) / data['income']) * 100)),
    "Debt Score": int(max(0, 100 - (debt_ratio * 100))),
    "Budgeting Score": int(savings_rate * 100),
    "Emergency Fund Score": int(min(100, emergency_months / 6 * 100))
}

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("💼 Financial Summary")
    st.metric("Income (Annual)", f"Rs {data['income']:,}")
    st.metric("Expenses (Annual)", f"Rs {data['expenses']:,}")
    st.metric("Net Worth", f"Rs {net_worth:,}")

    st.subheader("📊 Asset Allocation")
    asset_df = pd.DataFrame.from_dict(data['assets'], orient='index', columns=['Value'])
    st.bar_chart(asset_df)

with col2:
    st.subheader("📈 Portfolio Overview")
    port_df = pd.Series(data['portfolio'])
    fig, ax = plt.subplots()
    ax.pie(port_df, labels=port_df.index, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

    st.subheader("📋 Financial Health Scores")
    for k, v in scores.items():
        st.progress(v / 100, text=f"{k}: {v}/100")

# Recommendations section (optional)
st.subheader("🧠 Recommendations")
if savings_rate < 0.2:
    st.warning("Consider increasing savings. Your current savings rate is below 20%.")
if emergency_months < 6:
    st.info("Build up your emergency fund to cover at least 6 months of expenses.")
if debt_ratio > 0.4:
    st.error("Your debt ratio is high. Try to reduce liabilities.")
