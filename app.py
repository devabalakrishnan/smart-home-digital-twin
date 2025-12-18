 import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Home Digital Twin", layout="wide", page_icon="🏠")

st.title("🏠 Smart Home Digital Twin: Energy Analytics")
st.markdown("---")

# --- DATA LOADING (FAIL-SAFE) ---
@st.cache_data
def load_data():
    # List of possible names in order of preference
    possible_names = [
        'data.csv', 
        'ppo_data.csv', 
        'PPO_SYNTHETIC_DATASET_MODIFIED.xlsx - Sheet1.csv'
    ]
    
    file_to_load = None
    # Check if any of these files exist in the current folder
    for name in possible_names:
        if os.path.exists(name):
            file_to_load = name
            break
            
    if file_to_load is None:
        st.error("📂 **Dataset Not Found in GitHub!**")
        st.write("Current files in server:", os.listdir("."))
        st.info("Action: Rename your CSV file to 'data.csv' on GitHub.")
        st.stop()
        
    df = pd.read_csv(file_to_load)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    return df, file_to_load

# Run the loader
try:
    df, loaded_filename = load_data()
    st.sidebar.success(f"✅ Loaded: {loaded_filename}")
except Exception as e:
    st.error(f"Error processing data: {e}")
    st.stop()

# --- DASHBOARD LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Consumption by Appliance")
    # Identify appliance columns from your dataset
    appliances = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
    usage_data = df[appliances].sum().reset_index()
    usage_data.columns = ['Appliance', 'Usage']
    fig_pie = px.pie(usage_data, values='Usage', names='Appliance', hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("🤖 Digital Twin Prediction (24h)")
    # Train simple model for prediction using your data
    model = RandomForestRegressor(n_estimators=10, random_state=42)
    # Using small subset of data for fast cloud loading
    train_df = df.tail(1000)
    model.fit(train_df[['hour', 'occupancy']], train_df['Total Load'])
    
    # Predict next 24 hours
    future_hours = pd.DataFrame({'hour': range(24), 'occupancy': [df['occupancy'].iloc[-1]]*24})
    preds = model.predict(future_hours)
    st.line_chart(preds)

# --- RAW DATA ---
if st.checkbox("Show Telemetry Logs"):
    st.write(df.tail(10))
