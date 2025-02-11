import streamlit as st
import pandas as pd
import plotly.express as px

# 📌 🚀 Page Configuration
st.set_page_config(page_title="City Analysis", layout="wide")

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
selected_city = st.sidebar.multiselect(
    "Select Site", df["ShipTo City"].unique())
date_range = st.sidebar.date_input("Select Date Range", [
                                   df["Creation Date"].min(), df["Creation Date"].max()])

# Apply filters if selected
filtered_df = df.copy()
if selected_city:
    filtered_df = filtered_df[filtered_df["ShipTo City"].isin(selected_city)]
if date_range:
    filtered_df = filtered_df[(filtered_df["Creation Date"] >= pd.to_datetime(date_range[0])) &
                              (filtered_df["Creation Date"] <= pd.to_datetime(date_range[1]))]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(["🏙 Site with Most Orders",
               "📈 Purchase Trends by Site"])

with tabs[0]:
    st.subheader("🏙 Top 10 Site with Most Orders")
    top_cities = filtered_df["ShipTo City"].value_counts(
    ).reset_index().head(10)
    top_cities.columns = ["City", "Number of Orders"]
    fig_top_cities = px.bar(top_cities, x="Number of Orders", y="City", orientation='h',
                            color="Number of Orders", title="Top 10 Cities with Most Orders", height=500, color_continuous_scale="magma")
    st.plotly_chart(fig_top_cities)

with tabs[1]:
    st.subheader("📈 Purchase Trends by Site")
    df_cities_trend = filtered_df.groupby(["Creation Date", "ShipTo City"]).agg({
        "Extended Price": "sum"}).reset_index()
    fig_cities_trend = px.line(df_cities_trend, x="Creation Date", y="Extended Price", color="ShipTo City",
                               title="Purchase Trends by Site")
    st.plotly_chart(fig_cities_trend)
