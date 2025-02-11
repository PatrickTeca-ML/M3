import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 🚀 Page Configuration
st.set_page_config(page_title="Purchase Evolution", layout="wide")

# 📌 🚀 Function to Load Data


@st.cache_data
def load_data():
    file_path = "df_new_3.csv"  # Replace with the correct path
    try:
        df = pd.read_csv(file_path)
        df["Creation Date"] = pd.to_datetime(
            df["Creation Date"], errors='coerce')
        return df
    except FileNotFoundError:
        st.error("Error: File 'df_new_3.csv' not found!")
        return pd.DataFrame()  # Returns an empty DataFrame


# Load the data
df = load_data()

if df.empty:
    st.warning("No data available for display.")
    st.stop()

# 📌 🚀 Create Interactive Filters
st.sidebar.header("Filters")
date_range = st.sidebar.date_input("Select Date Range", [
                                   df["Creation Date"].min(), df["Creation Date"].max()])

# Apply filters if selected
filtered_df = df.copy()
if date_range:
    filtered_df = filtered_df[(filtered_df["Creation Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Creation Date"] <= pd.to_datetime(date_range[1]))]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(["📈 Purchase Evolution", "📊 Price Trends",
               "📉 Department Comparisons", "🔎 Peak Purchase Analysis"])

with tabs[0]:
    st.subheader("📈 Total Purchases Over Time")
    trend_data = filtered_df.groupby("Creation Date")[
        "Extended Price"].sum().reset_index()
    fig_trend = px.line(trend_data, x="Creation Date",
                        y="Extended Price", title="Total Purchase Evolution")
    st.plotly_chart(fig_trend)

with tabs[1]:
    st.subheader("📊 Average Prices Over Time")
    price_trend = filtered_df.groupby("Creation Date")[
        "Unit Price"].mean().reset_index()
    fig_price_trend = px.line(price_trend, x="Creation Date",
                              y="Unit Price", title="Average Prices Over Time")
    st.plotly_chart(fig_price_trend)

with tabs[2]:
    st.subheader("📉 Purchase Comparison Between Departments")
    dept_trend = filtered_df.groupby(["Creation Date", "Department"])[
        "Extended Price"].sum().reset_index()
    fig_dept_trend = px.line(dept_trend, x="Creation Date", y="Extended Price", color="Department",
                             title="Purchase Comparison Between Departments")
    st.plotly_chart(fig_dept_trend)

with tabs[3]:
    st.subheader("🔎 Identification of Purchase Peaks")
    peak_purchases = filtered_df.groupby("Creation Date")[
        "Extended Price"].sum().reset_index()
    peak_purchases = peak_purchases.sort_values(
        "Extended Price", ascending=False).head(10)
    fig_peaks = px.bar(peak_purchases, x="Creation Date",
                       y="Extended Price", title="Days with Highest Purchase Volume")
    st.plotly_chart(fig_peaks)
