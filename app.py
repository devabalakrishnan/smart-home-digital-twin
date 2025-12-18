   import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="Live Digital Twin", layout="wide", page_icon="📡")

# 2. Setup placeholders for Live Data
st.title("📡 Live-Stream Digital Twin")
status_box = st.empty()
metric_row = st.columns(3)
chart_spot = st.empty()

# 3. Live Data Function
@st.cache_data(ttl=60) # This forces a data refresh every 60 seconds
def get_live_data():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        # In a real setup, you would fetch from an API here:
        # df = pd.read_json("https://api.your-smart-home.com/data")
        return df
    return None

# 4. Continuous Update Loop
while True:
    df = get_live_data()
    
    if df is not None:
        # Update Status
        status_box.info(f"Last Sync: {datetime.now().strftime('%H:%M:%S')} | Source: Live IoT Stream")
        
        # Update Metrics
        current_data = df.iloc[-1]
        metric_row[0].metric("Live Load", f"{current_data['Total Load']} kW", delta="0.2 kW")
        metric_row[1].metric("Current Price", f"${current_data['electricity_price']}", delta="-0.05")
        metric_row[2].metric("Occupancy", "Occupied" if current_data['occupancy'] > 0 else "Empty")

        # Update Chart
        fig = px.line(df.tail(50), x='datetime', y='Total Load', 
                      title="Real-Time Telemetry (Updating Every 60s)",
                      template="plotly_dark")
        chart_spot.plotly_chart(fig, use_container_width=True)
    
    # Wait for 1 minute before checking again
    time.sleep(60)
    st.rerun() # This triggers the Streamlit refresh
