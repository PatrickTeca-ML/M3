import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 🚀 Page Configuration
st.set_page_config(page_title="Supplier Analysis", layout="wide")

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
selected_supplier = st.sidebar.multiselect(
    "Select Supplier", df["Supplier Name"].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

# Apply filters if selected
filtered_df = df.copy()
if selected_supplier:
    filtered_df = filtered_df[filtered_df["Supplier Name"].isin(
        selected_supplier)]
if date_range:
    filtered_df = filtered_df[(filtered_df["Creation Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Creation Date"] <= pd.to_datetime(date_range[1]))]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(
    ["📦 Top Suppliers", "📊 Purchase Trends", "📈 Supplier Comparison"])

with tabs[0]:
    st.subheader("📦 Top 10 Suppliers with Most Orders")
    top_suppliers = filtered_df["Supplier Name"].value_counts(
    ).reset_index().head(10)
    top_suppliers.columns = ["Supplier", "Number of Orders"]
    fig_suppliers = px.bar(top_suppliers, x="Number of Orders", y="Supplier", orientation='h',
                           color="Number of Orders", title="Top 10 Suppliers", height=500)
    st.plotly_chart(fig_suppliers)

with tabs[1]:
    st.subheader("📊 Purchase Trends by Supplier")
    df_supplier_trend = filtered_df.groupby(["Creation Date", "Supplier Name"]).agg({
        "Extended Price": "sum"}).reset_index()
    fig_trend = px.line(df_supplier_trend, x="Creation Date", y="Extended Price", color="Supplier Name",
                        title="Purchase Trends by Supplier")
    st.plotly_chart(fig_trend)

with tabs[2]:
    st.subheader("📈 Supplier Comparison")
    fig_box = px.box(filtered_df, x="Supplier Name", y="Extended Price", color="Supplier Name",
                     title="Spending Distribution by Supplier")
    st.plotly_chart(fig_box)
