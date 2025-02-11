import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# 📌 🚀 Page Configuration
st.set_page_config(page_title="Purchase Dashboard", layout="wide")

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
selected_department = st.sidebar.multiselect(
    "Select Department", df["Department"].unique())
selected_supplier = st.sidebar.multiselect(
    "Select Supplier", df["Supplier Name"].unique())
date_range = st.sidebar.date_input("Select Date Range", [])

# Apply filters if selected
filtered_df = df.copy()
if selected_department:
    filtered_df = filtered_df[filtered_df["Department"].isin(
        selected_department)]
if selected_supplier:
    filtered_df = filtered_df[filtered_df["Supplier Name"].isin(
        selected_supplier)]
if date_range:
    filtered_df = filtered_df[(filtered_df["Creation Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Creation Date"] <= pd.to_datetime(date_range[1]))]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(["📊 Overview", "🔍 Purchase Analysis",
               "📈 Department Comparison", "📉 Trends and Evolution"])

with tabs[0]:
    st.title("📊 Purchase Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Total Purchases (€)",
                f"€{filtered_df['Extended Price'].sum():,.2f}")
    col2.metric("📦 Total Orders", filtered_df.shape[0])
    col3.metric("🏭 Suppliers", filtered_df["Supplier Name"].nunique())
    col4.metric("🏢 Departments", filtered_df["Department"].nunique())

    # Purchase trend over time
    st.subheader("📅 Purchase Evolution")
    df_time_series = filtered_df.groupby(filtered_df["Creation Date"].dt.to_period(
        "M")).agg({"Extended Price": "sum"}).reset_index()
    df_time_series["Creation Date"] = df_time_series["Creation Date"].astype(
        str)
    fig_time_series = px.line(df_time_series, x="Creation Date",
                              y="Extended Price", title="Purchase Evolution Over Time")
    st.plotly_chart(fig_time_series)

with tabs[1]:
    st.subheader("🔍 Purchase Analysis")
    fig = px.bar(filtered_df, x="Supplier Name", y="Extended Price", color="Department",
                 title="Total Purchases by Supplier", height=500)
    st.plotly_chart(fig)

    # Interactive scatter plot
    st.subheader("📊 Relationship Between Quantity and Unit Price")
    fig_scatter = px.scatter(filtered_df, x="Quantity", y="Unit Price", size="Extended Price", color="Department",
                             title="Quantity vs. Unit Price", hover_name="Supplier Name")
    st.plotly_chart(fig_scatter)

with tabs[2]:
    st.subheader("📈 Department Comparison")
    top_departments = filtered_df["Department"].value_counts().reset_index()
    top_departments.columns = ["Department", "Number of Purchases"]
    fig_bar_interactive = px.bar(top_departments.head(10), x="Number of Purchases", y="Department", orientation='h',
                                 color="Number of Purchases", title="Comparison of Purchases by Department", height=500)
    st.plotly_chart(fig_bar_interactive)

    # Interactive distribution plot
    st.subheader("📊 Purchase Value Distribution")
    fig_hist = px.histogram(filtered_df, x="Extended Price",
                            nbins=20, title="Distribution of Purchase Values")
    st.plotly_chart(fig_hist)

with tabs[3]:
    st.subheader("📉 Trends and Evolution")
    fig_trend = px.box(filtered_df, x="Department", y="Extended Price",
                       color="Department", title="Expense Variation by Department")
    st.plotly_chart(fig_trend)
