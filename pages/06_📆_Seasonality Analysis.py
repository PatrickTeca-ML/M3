import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# 📌 🚀 Page Configuration
st.set_page_config(page_title="Seasonality Analysis", layout="wide")

# 📌 🚀 Function to Load Data


@st.cache_data
def load_data():
    file_path = "df_new_3.csv"  # Replace with the correct path
    try:
        df = pd.read_csv(file_path)
        df["Creation Date"] = pd.to_datetime(
            df["Creation Date"], errors='coerce')
        df["Year"] = df["Creation Date"].dt.year
        df["Month"] = df["Creation Date"].dt.month
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
selected_year = st.sidebar.multiselect("Select Year", df["Year"].unique())
selected_month = st.sidebar.multiselect("Select Month", df["Month"].unique())

# Apply filters if selected
filtered_df = df.copy()
if selected_year:
    filtered_df = filtered_df[filtered_df["Year"].isin(selected_year)]
if selected_month:
    filtered_df = filtered_df[filtered_df["Month"].isin(selected_month)]

# 📌 🚀 Create Tabs for Organization
tabs = st.tabs(["📆 Seasonal Trends", "📊 Purchases by Month",
               "📈 Annual Comparison", "🔍 Time Series Decomposition", "📉 Forecast for 2025"])

with tabs[0]:
    st.subheader("📆 Seasonal Purchase Trends")
    df_seasonality = filtered_df.groupby(["Year", "Month"]).agg(
        {"Extended Price": "sum"}).reset_index()
    fig_seasonality = px.line(df_seasonality, x="Month", y="Extended Price", color="Year",
                              title="Seasonal Purchase Trends by Month and Year")
    st.plotly_chart(fig_seasonality)

with tabs[1]:
    st.subheader("📊 Purchases by Month")
    df_monthly = filtered_df.groupby(
        "Month")["Extended Price"].sum().reset_index()
    fig_monthly = px.bar(df_monthly, x="Month", y="Extended Price", title="Total Purchases by Month",
                         color="Extended Price", color_continuous_scale="viridis")
    st.plotly_chart(fig_monthly)

with tabs[2]:
    st.subheader("📈 Annual Purchase Comparison")
    df_annual = filtered_df.groupby(
        "Year")["Extended Price"].sum().reset_index()
    fig_annual = px.bar(df_annual, x="Year", y="Extended Price", title="Annual Purchase Comparison",
                        color="Extended Price", color_continuous_scale="plasma")
    st.plotly_chart(fig_annual)

with tabs[3]:
    st.subheader("🔍 Time Series Decomposition")
    df_time = df.groupby("Creation Date")["Extended Price"].sum().reset_index()
    df_time.set_index("Creation Date", inplace=True)
    df_time = df_time.asfreq("D").fillna(method="ffill")
    decomposition = seasonal_decompose(
        df_time["Extended Price"], model="additive", period=30)

    fig, axs = plt.subplots(4, 1, figsize=(10, 8))
    axs[0].plot(decomposition.observed, label="Original Series")
    axs[0].legend()
    axs[1].plot(decomposition.trend, label="Trend", color="red")
    axs[1].legend()
    axs[2].plot(decomposition.seasonal, label="Seasonality", color="green")
    axs[2].legend()
    axs[3].plot(decomposition.resid, label="Residuals", color="black")
    axs[3].legend()
    plt.tight_layout()
    st.pyplot(fig)

with tabs[4]:
    st.subheader("📉 Forecast for 2025")
    df_time = df.groupby("Creation Date")["Extended Price"].sum().reset_index()
    df_time.set_index("Creation Date", inplace=True)
    df_time = df_time.asfreq("D").fillna(method="ffill")
    model = ExponentialSmoothing(
        df_time["Extended Price"], trend="add", seasonal="add", seasonal_periods=30)
    fitted_model = model.fit()
    forecast = fitted_model.forecast(steps=365)

    fig_forecast = px.line(x=forecast.index, y=forecast.values, title="Purchase Forecast for 2025",
                           labels={"x": "Date", "y": "Purchase Forecast (€)"})
    st.plotly_chart(fig_forecast)
