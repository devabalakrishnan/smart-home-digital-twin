import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# 1. Page Config
st.set_page_config(page_title="AI Digital Twin", layout="wide", page_icon="🤖")
st.title("🤖 AI-Powered Smart Home Digital Twin")
st.markdown("---")

# 2. Load Data
@st.cache_data
def load_data():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        df['hour'] = df['datetime'].dt.hour
        return df
    return None

df = load_data()

if df is not None:
    # --- SIDEBAR AI CONTROLS ---
    st.sidebar.header("AI Optimization Settings")
    ai_enabled = st.sidebar.toggle("Activate AI Controller", value=True)
    price_threshold = st.sidebar.slider("Price Alert Threshold ($)", 0.5, 3.0, 1.2)
    
    # --- TOP ROW: AI INSIGHTS ---
    st.subheader("💡 AI System Insights")
    col1, col2, col3, col4 = st.columns(4)
    
    current_load = df['Total Load'].iloc[-1]
    avg_price = df['electricity_price'].mean()
    peak_hour = df.groupby('hour')['Total Load'].mean().idxmax()
    
    col1.metric("Current Load", f"{current_load:.2f} kW")
    col2.metric("Avg Price", f"${avg_price:.2f}")
    col3.metric("Peak Usage Hour", f"{peak_hour}:00")
    col4.metric("AI Status", "ACTIVE" if ai_enabled else "OFF")

    # --- MIDDLE ROW: OPTIMIZATION ENGINE ---
    st.markdown("### 📈 Energy Optimization Strategy")
    
    # AI Logic: Simulate shifting load
    # If price is high, we reduce Heater and Washing Machine by 50%
    df['AI_Optimized_Load'] = df['Total Load']
    if ai_enabled:
        high_price_mask = df['electricity_price'] > price_threshold
        # Simulate AI 'Dimming' or 'Shifting'
        reduction = (df['Heater'] * 0.5) + (df['Washing Machine'] * 0.5)
        df.loc[high_price_mask, 'AI_Optimized_Load'] = df['Total Load'] - reduction

    # Comparison Chart
    chart_data = df.tail(48) # Show last 48 readings
    fig_opt = px.line(chart_data, x='datetime', y=['Total Load', 'AI_Optimized_Load'],
                      labels={'value': 'Load (kW)', 'datetime': 'Time'},
                      title="Original vs. AI-Optimized Consumption",
                      color_discrete_map={"Total Load": "red", "AI_Optimized_Load": "green"})
    st.plotly_chart(fig_opt, use_container_width=True)

    # --- BOTTOM ROW: SAVINGS & BREAKDOWN ---
    c1, c2 = st.columns([1, 2])
    
    with c1:
        st.subheader("💰 Savings Calculator")
        original_cost = (df['Total Load'] * df['electricity_price']).sum()
        optimized_cost = (df['AI_Optimized_Load'] * df['electricity_price']).sum()
        savings = original_cost - optimized_cost
        
        st.metric("Estimated Savings", f"${savings:.2f}", delta=f"{(savings/original_cost)*100:.1f}% Total")
        st.write(f"By limiting usage when prices exceed **${price_threshold}**, the AI avoids peak costs.")

    with c2:
        st.subheader("🍽️ Appliance Hog Analysis")
        appliances = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
        app_totals = df[appliances].sum().sort_values(ascending=False)
        fig_bar = px.bar(app_totals, orientation='h', labels={'value': 'Total kW', 'index': 'Appliance'},
                         color=app_totals.values, color_continuous_scale='Reds')
        st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Please ensure 'data.csv' is in your GitHub folder.")
