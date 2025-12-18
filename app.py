import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration
st.set_page_config(page_title="Smart Home Digital Twin", layout="wide", page_icon="🏠")

st.title("🏠 Smart Home Digital Twin Energy Dashboard")
st.markdown("---")

# 2. Fail-Safe Data Loading
def load_data():
    # This checks for common names to prevent crashes
    possible_files = ['data.csv', 'ppo_data.csv', 'PPO_SYNTHETIC_DATASET_MODIFIED.xlsx - Sheet1.csv']
    
    target_file = None
    for f in possible_files:
        if os.path.exists(f):
            target_file = f
            break
            
    if target_file:
        df = pd.read_csv(target_file)
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df, target_file
    return None, None

df, file_used = load_data()

# 3. Error Handling UI
if df is None:
    st.error("❌ Data File Not Found!")
    st.write("Current files in your GitHub repository:", os.listdir("."))
    st.info("Please ensure your CSV file is named 'data.csv' and is in the main folder.")
    st.stop()

# 4. Success UI & Metrics
st.sidebar.success(f"✅ Connected to: {file_used}")

col1, col2, col3 = st.columns(3)
col1.metric("Average Load", f"{df['Total Load'].mean():.2f} kW")
col2.metric("Avg Price", f"${df['electricity_price'].mean():.2f}")
col3.metric("Max Demand", f"{df['Total Load'].max():.2f} kW")

# 5. Visualizations
st.subheader("📊 Energy Consumption Trends")
fig_load = px.line(df.tail(100), x='datetime', y='Total Load', 
                   title="Real-Time Energy Load (Last 100 points)",
                   template="plotly_white")
st.plotly_chart(fig_load, use_container_width=True)

# 6. Raw Data View
if st.checkbox("View Raw Telemetry Data"):
    st.dataframe(df.tail(20))
