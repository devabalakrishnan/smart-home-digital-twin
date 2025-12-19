import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime
import time

# 1. Page Setup for IEEE Publication Quality
st.set_page_config(page_title="Digital Twin Co-Simulation", layout="wide")
st.title("🔬 Cyber-Physical Systems: Virtual Home Digital Twin")
st.markdown("---")

# 2. THE VIRTUAL HOME ENGINE (Mathematical Model)
# This simulates the "Physics" of your home without hardware
def run_virtual_home_iteration():
    now = datetime.now()
    hour = now.hour
    
    # Stochastic Occupancy Model (Markov-like chain)
    is_occupied = 1 if (7 <= hour <= 9 or 18 <= hour <= 23) else 0
    
    # Power Consumption Formula: P = P_base + P_active + Noise
    base_load = 0.4  # standby power in kW
    activity_spike = np.random.normal(1.5, 0.2) if is_occupied else 0.05
    total_load = base_load + activity_spike + np.random.normal(0, 0.02)
    
    # Dynamic Pricing Model
    price = round(1.2 + 0.6 * np.sin(hour * np.pi / 12), 2)
    
    return {
        "datetime": now.strftime("%H:%M:%S"),
        "Total Load": round(max(0, total_load), 3),
        "Price": price,
        "Occupancy": is_occupied
    }

# 3. SPATIAL VISUALIZATION (The "Virtual Home" Model)
def draw_house_model(load, occupied):
    # Color changes based on Load Intensity
    color = "#2ecc71" if load < 1.0 else "#e67e22" if load < 2.0 else "#e74c3c"
    window_color = "#f1c40f" if occupied else "#2c3e50"
    
    svg = f"""
    <svg width="400" height="250" viewBox="0 0 400 250">
        <path d="M50 100 L200 20 L350 100 Z" fill="#34495e" stroke="white" stroke-width="2"/>
        <rect x="70" y="100" width="260" height="120" fill="{color}" stroke="white" stroke-width="3"/>
        <rect x="110" y="130" width="40" height="40" fill="{window_color}" stroke="white"/>
        <rect x="250" y="130" width="40" height="40" fill="{window_color}" stroke="white"/>
        <text x="110" y="240" fill="white" font-weight="bold">Digital Twin Load: {load} kW</text>
    </svg>
    """
    st.markdown(svg, unsafe_allow_html=True)

# 4. INITIALIZE DATA STREAM
if 'history' not in st.session_state:
    st.session_state.history = []

# 5. LIVE EXECUTION LOOP
# This generates a new "Virtual State" every time the page refreshes
new_state = run_virtual_home_iteration()
st.session_state.history.append(new_state)

# Keep only last 50 data points for performance
if len(st.session_state.history) > 50:
    st.session_state.history.pop(0)

# 6. DASHBOARD LAYOUT
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🏠 Spatial Virtual Model")
    draw_house_model(new_state["Total Load"], new_state["Occupancy"])
    st.metric("Real-Time Load", f"{new_state['Total Load']} kW", delta=f"{new_state['Price']} $/kWh")
    st.write("**Simulation Status:** Transmitting...")

with col2:
    st.subheader("📊 Real-Time Telemetry Stream")
    hist_df = pd.DataFrame(st.session_state.history)
    fig = px.line(hist_df, x='datetime', y='Total Load', 
                   title="Simulated IoT Data Stream (IEEE Standard)",
                   template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    # --- Add this to your Sidebar ---
st.sidebar.header("🕹️ Simulation Controls")
fault_trigger = st.sidebar.button("🚨 Simulate Appliance Fault")

# --- Update your Virtual Home Engine function ---
def run_virtual_home(is_fault):
    now = datetime.now()
    hour = now.hour
    
    # Normal Logic
    is_occupied = 1 if (7 <= hour <= 9 or 18 <= hour <= 23) else 0
    base_load = 0.4 
    
    # If button is pressed, force a massive spike (Fault Injection)
    if is_fault:
        activity = 5.5  # Simulate a short circuit or heavy motor fault
        status = "FAULT DETECTED"
    else:
        activity = np.random.normal(1.5, 0.2) if is_occupied else 0.05
        status = "Operating Normally"
        
    total_load = base_load + activity + np.random.normal(0, 0.02)
    price = round(1.2 + 0.6 * np.sin(hour * np.pi / 12), 2)
    
    return {
        "time": now.strftime("%H:%M:%S"), 
        "load": round(total_load, 3), 
        "price": price, 
        "occ": is_occupied,
        "status": status
    }

# --- Call the function with the trigger ---
current_state = run_virtual_home(fault_trigger)

# --- Display the Status in your UI ---
if fault_trigger:
    st.error(f"CRITICAL SYSTEM ALERT: {current_state['status']}")

# 7. AUTOMATED REFRESH (Simulates Live Data Flow)
time.sleep(2)
st.rerun()


