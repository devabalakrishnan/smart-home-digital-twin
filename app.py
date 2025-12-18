 import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration
st.set_page_config(page_title="Smart Home Digital Twin", layout="wide")

st.title("🏠 Smart Home Digital Twin Energy Dashboard")
st.markdown("---")

# 2. Robust Data Loading
# This logic checks for the file 'data.csv' in the GitHub root folder
FILENAME = 'data.csv'

@st.cache_data
def load_data():
    if os.path.exists(FILENAME):
        df = pd.read_csv(FILENAME)
        # Ensure datetime is formatted correctly
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    else:
        return None

df = load_data()

# 3. Handling the Error if File is Missing
if df is None:
    st.error(f"❌ Error: The file '{FILENAME}' was not found.")
    st.info("Please rename your CSV file to 'data.csv' on GitHub and ensure it is in the main folder.")
    st.write("Current files in repository:", os.listdir("."))
    st.stop()

# 4. Dashboard Metrics
st.sidebar.header("Digital Twin Controls")
st.sidebar.write("Connected to: " + FILENAME)

col1, col2, col3 = st.columns(3)
col1.metric("Average Load", f"{df['Total Load'].mean():.2f} kW")
col2.metric("Avg Price", f"${df['electricity_price'].mean():.2f}")
col3.metric("Peak Demand", f"{df['Total Load'].max():.2f} kW")

# 5. Visualizations
st.subheader("📊 Energy Consumption Trends")

tab1, tab2 = st.tabs(["Energy Load", "Price Analysis"])

with tab1:
    # Interactive line chart of the last 100 data points
    fig_load = px.line(df.tail(100), x='datetime', y='Total Load', title="Real-Time Energy Load")
    st.plotly_chart(fig_load, use_container_width=True)

with tab2:
    # Scatter plot showing relationship between Price and Load
    fig_price = px.scatter(df.tail(500), x='electricity_price', y='Total Load', 
                           color='occupancy', title="Price vs. Demand Relationship")
    st.plotly_chart(fig_price, use_container_width=True)

# 6. Raw Data Inspection
if st.checkbox("View Digital Twin Telemetry (Raw Data)"):
    st.dataframe(df.tail(50))
