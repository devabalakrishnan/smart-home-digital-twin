 import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Config
st.set_page_config(page_title="AI Digital Twin Pro", layout="wide")
st.title("🏙️ AI Digital Twin: Energy Analytics")

# 2. Automated File Finder (Fixes FileNotFoundError)
def load_data():
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    if not files:
        return None
    # Prioritize 'data.csv' if it exists
    target = 'data.csv' if 'data.csv' in files else files[0]
    df = pd.read_csv(target)
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df, target

try:
    df, used_file = load_data()
except Exception as e:
    st.error(f"Error reading file: {e}")
    st.stop()

if df is not None:
    st.sidebar.success(f"Connected to: {used_file}")
    
    # AI CALCULATIONS
    avg_price = df['electricity_price'].mean()
    total_load = df['Total Load'].sum()
    
    # DASHBOARD
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Total Consumption", f"{total_load:,.0f} kWh")
        fig = px.line(df.tail(100), x='datetime', y='Total Load', title="Real-Time Load")
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.metric("Avg Price", f"${avg_price:.2f}")
        # Download Report Feature
        report = df[['datetime', 'Total Load', 'electricity_price']].tail(50)
        csv = report.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download AI Energy Report", data=csv, file_name='report.csv', mime='text/csv')
        
        # Appliance Breakdown
        apps = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
        usage = df[apps].sum()
        fig2 = px.pie(values=usage.values, names=usage.index, title="Appliance Energy Stake")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.error("No CSV file found! Please upload your data to GitHub.")
