import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 🚀 Page Configuration
st.set_page_config(page_title="Buyer Analysis", layout="wide")

# 📌 🚀 Function to Load Data


@st.cache_data
def load_data():
    file_path = "df_new_3.csv"  # Replace with the correct path
    try:
        df = pd.read_csv(file_path)
        df["Creation Date"] = pd.to_datetime(
            df["Creation Date"], errors='coerce')
        df["Buyer"] = df["Buyer: First Name"] + " " + df["Buyer: Last Name"]
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
selected_buyer = st.sidebar.multiselect("Select Buyer", df["Buyer"].unique())
selected_department = st.sidebar.multiselect(
    "Select Department", df["Department"].unique())
date_range = st.sidebar.date_input("Select Date Range", [
                                   df["Creation Date"].min(), df["Creation Date"].max()])

# Apply filters if selected
filtered_df = df.copy()
if selected_buyer:
    filtered_df = filtered_df[filtered_df["Buyer"].isin(selected_buyer)]
if selected_department:
    filtered_df = filtered_df[filtered_df["Department"].isin(
        selected_department)]
if date_range:
    filtered_df = filtered_df[(filtered_df["Creation Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Creation Date"] <= pd.to_datetime(date_range[1]))]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(["🛍 Top Buyers", "📈 Purchase Trends", "📊 Purchases by Category",
               "🚀 Fastest Growing Buyers", "🔍 Product and Department Insights"])

with tabs[0]:
    st.subheader("🛍 Top 10 Buyers with Most Orders")
    top_buyers = filtered_df["Buyer"].value_counts().reset_index().head(10)
    top_buyers.columns = ["Buyer", "Number of Orders"]
    fig_top_buyers = px.bar(top_buyers, x="Number of Orders", y="Buyer", orientation='h',
                            color="Number of Orders", title="Top 10 Buyers", height=500, color_continuous_scale="blues")
    st.plotly_chart(fig_top_buyers)

with tabs[1]:
    st.subheader("📈 Purchase Trends by Buyer")
    df_buyer_trend = filtered_df.groupby(["Creation Date", "Buyer"]).agg(
        {"Extended Price": "sum"}).reset_index()
    fig_buyer_trend = px.line(df_buyer_trend, x="Creation Date", y="Extended Price", color="Buyer",
                              title="Purchase Trends by Buyer")
    st.plotly_chart(fig_buyer_trend)

with tabs[2]:
    st.subheader("📊 Purchase Evolution by Product Category")
    top_items = filtered_df["Item Type"].value_counts().head(5).index
    df_top_items = filtered_df[filtered_df["Item Type"].isin(top_items)]
    df_items_trend = df_top_items.groupby(["Creation Date", "Item Type"])[
        "Extended Price"].sum().reset_index()
    fig_items_trend = px.line(df_items_trend, x="Creation Date", y="Extended Price", color="Item Type",
                              title="Purchase Evolution by Product Category")
    st.plotly_chart(fig_items_trend)

with tabs[3]:
    st.subheader("🚀 Buyers with Fastest Growth in Orders")
    top_buyers_growth = filtered_df["Buyer"].value_counts(
    ).reset_index().head(5)
    top_buyers_growth.columns = ["Buyer", "Number of Orders"]
    df_top_growth = filtered_df[filtered_df["Buyer"].isin(
        top_buyers_growth["Buyer"])]
    df_growth_trend = df_top_growth.groupby(["Creation Date", "Buyer"])[
        "Extended Price"].sum().reset_index()
    fig_growth_trend = px.line(df_growth_trend, x="Creation Date", y="Extended Price", color="Buyer",
                               title="Growth in Purchases by Buyer")
    st.plotly_chart(fig_growth_trend)

with tabs[4]:
    st.subheader("🔍 Product and Department Insights")
    unique_products = filtered_df["Product Description"].nunique()
    unique_departments = filtered_df["Department"].nunique()

    st.metric("Unique Products", unique_products)
    st.metric("Unique Departments", unique_departments)

    top_products = filtered_df["Product Description"].value_counts(
    ).reset_index().head(10)
    top_products.columns = ["Product Description", "Number of Purchases"]
    fig_top_products = px.bar(top_products, x="Number of Purchases", y="Product Description", orientation='h',
                              color="Number of Purchases", title="Top 10 Most Purchased Products", height=500, color_continuous_scale="viridis")
    st.plotly_chart(fig_top_products)

    top_departments = filtered_df["Department"].value_counts(
    ).reset_index().head(10)
    top_departments.columns = ["Department", "Number of Purchases"]
    fig_top_departments = px.bar(top_departments, x="Number of Purchases", y="Department", orientation='h',
                                 color="Number of Purchases", title="Top 10 Departments with Most Purchases", height=500, color_continuous_scale="plasma")
    st.plotly_chart(fig_top_departments)

    st.subheader("📋 Top 10 Products Purchased by Department")
    top_products_by_department = filtered_df.groupby(["Department", "Product Description"]).agg(
        {"Quantity": "sum", "Extended Price": "sum"}).reset_index()
    top_products_by_department = top_products_by_department.sort_values(
        by=["Department", "Extended Price"], ascending=[True, False]).groupby("Department").head(10)
    st.dataframe(top_products_by_department)
