    import streamlit as st
import pandas as pd
import plotly.express as px
import os
import time

# Page Config
st.set_page_config(page_title="IEEE Digital Twin Research", layout="wide")
st.title("🔬 Research Interface: Virtual Home Digital Twin")

# --- VIRTUAL MODEL VISUALIZER ---
def draw_spatial_model(load):
    # Logic: Green for low energy, Red for high energy
    color = "#2ecc71" if load < 2.0 else "#e74c3c"
    # Research-grade SVG Visualization
    svg = f"""
    <svg width="300" height="200" viewBox="0 0 300 200">
        <rect x="50" y="80" width="200" height="100" fill="{color}" stroke="white" stroke-width="2"/>
        <path d="M50 80 L150 20 L250 80 Z" fill="#34495e" stroke="white" stroke-width="2"/>
        <rect x="125" y="130" width="50" height="50" fill="#f1c40f"/>
        <text x="80" y="195" fill="white" font-size="12">Spatial Load State: {load} kW</text>
    </svg>
    """
    st.markdown(svg, unsafe_allow_html=True)

# --- DATA INGESTION ---
# This looks for the latest data "transmitted" by your simulation
if os.path.exists('data.csv'):
    df = pd.read_csv('data.csv')
    latest_data = df.iloc[-1]
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🏠 Virtual Spatial Model")
        draw_spatial_model(latest_data['Total Load'])
        st.write(f"**Transmission Status:** Active")
        st.write(f"**Timestamp:** {latest_data['datetime']}")

    with col2:
        st.subheader("📈 Real-Time Telemetry Stream")
        fig = px.line(df.tail(50), x='datetime', y='Total Load', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    # Auto-refresh logic for the dashboard
    time.sleep(2)
    st.rerun()
else:
    st.error("Waiting for data transmission from Virtual Home Simulator...")
