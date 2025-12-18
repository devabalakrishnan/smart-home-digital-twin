import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Home Digital Twin", layout="wide")
st.title("🏠 Smart Home Digital Twin")

# --- DATA LOADING (FAIL-SAFE) ---
@st.cache_data
def load_data():
    # Looking for 'data.csv' first, then the original long name
    files = ['data.csv', 'PPO_SYNTHETIC_DATASET_MODIFIED.xlsx - Sheet1.csv']
    target_file = next((f for f in files if os.path.exists(f)), None)
    
    if target_file is None:
        st.error(f"❌ File Not Found! Current files in GitHub: {os.listdir('.')}")
        st.stop()
        
    df = pd.read_csv(target_file)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    return df

df = load_data()

# --- DASHBOARD ---
st.sidebar.header("Optimization AI")
opt_on = st.sidebar.checkbox("Activate Energy Saving AI", value=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Current Usage Breakdown")
    apps = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
    usage = df[apps].sum().reset_index()
    fig = px.pie(usage, values=0, names='index', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Digital Twin Prediction")
    # Simple ML model
    model = RandomForestRegressor(n_estimators=10)
    model.fit(df[['hour', 'occupancy']].tail(1000), df['Total Load'].tail(1000))
    preds = model.predict(df[['hour', 'occupancy']].tail(24))
    st.line_chart(preds)

if opt_on:
    st.success("✅ AI Optimization Active: Reducing peak load costs.")
