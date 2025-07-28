import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Page config
st.set_page_config(page_title="Budget Tracker", layout="wide")

st.title("💰 Budget Tracker")
st.write("Track your expenses and visualize your spending.")

# Initialize session state
if "expenses" not in st.session_state:
    st.session_state.expenses = pd.DataFrame(columns=["Date", "Category", "Amount"])

# Sidebar – Add expense
st.sidebar.header("➕ Add New Expense")
with st.sidebar.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    category = st.selectbox("Category", ["Food", "Rent", "Utilities", "Entertainment", "Travel", "Shopping", "Others"])
    amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    submitted = st.form_submit_button("Add Expense")

    if submitted:
        new_expense = {"Date": date, "Category": category, "Amount": amount}
        st.session_state.expenses = pd.concat([st.session_state.expenses, pd.DataFrame([new_expense])], ignore_index=True)
        st.success("Expense added!")

# Main: Show Data
st.subheader("📋 Expense Table")
st.dataframe(st.session_state.expenses, use_container_width=True)

# Visualizations
if not st.session_state.expenses.empty:
    df = st.session_state.expenses

    # Grouped data
    grouped = df.groupby("Category")["Amount"].sum().reset_index()

    # Bar Chart
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Spending by Category (Bar)")
        bar_chart = px.bar(grouped, x="Category", y="Amount", color="Category", title="Spending Distribution")
        st.plotly_chart(bar_chart, use_container_width=True)

    with col2:
        st.subheader("🥧 Spending Breakdown (Pie)")
        pie_chart = px.pie(grouped, names="Category", values="Amount", title="Expense Share")
        st.plotly_chart(pie_chart, use_container_width=True)

    # Download option
    st.download_button("📥 Download Expenses CSV", df.to_csv(index=False), "expenses.csv", "text/csv")

else:
    st.info("No expenses yet. Add some from the sidebar!")