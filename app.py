import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# --- PAGE CONFIG ---
st.set_page_config(page_title="Smart Home Digital Twin", layout="wide")
st.title("🏠 Smart Home Digital Twin Energy Dashboard")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv('PPO_SYNTHETIC_DATASET_MODIFIED.xlsx - Sheet1.csv')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['hour'] = df['datetime'].dt.hour
    return df

df = load_data()

# --- SIDEBAR: DIGITAL TWIN CONTROLS ---
st.sidebar.header("Digital Twin Simulation Settings")
optimization_enabled = st.sidebar.checkbox("Enable Energy Optimization AI")
price_threshold = st.sidebar.slider("Electricity Price Threshold (Limit)", 0.0, 4.0, 1.5)

# --- APP LAYOUT ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Real-Time Energy Consumption")
    # Interactive Appliance Breakdown
    appliances = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
    totals = df[appliances].sum().reset_index()
    totals.columns = ['Appliance', 'Total Consumption']
    fig_pie = px.pie(totals, values='Total Consumption', names='Appliance', hole=0.4,
                     title="Total Energy Distribution")
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.subheader("💡 Digital Twin Predictions")
    # Training the model (Simplistic version for dashboard)
    features = ['hour', 'occupancy', 'electricity_price']
    X = df[features]
    y = df['Total Load']
    
    # We use a subset for speed in the dashboard
    model = RandomForestRegressor(n_estimators=20, random_state=42)
    model.fit(X.tail(1000), y.tail(1000))
    
    # Predict for the next 24 hours
    prediction_input = df[features].tail(24)
    preds = model.predict(prediction_input)
    
    pred_df = pd.DataFrame({'Hour': range(24), 'Predicted Load (kW)': preds})
    fig_line = px.line(pred_df, x='Hour', y='Predicted Load (kW)', 
                       title="Predicted Load for Next 24 Hours")
    st.plotly_chart(fig_line, use_container_width=True)

# --- OPTIMIZATION ENGINE ---
st.divider()
st.subheader("🤖 Optimization Simulation (The 'Smart' Twin)")

if optimization_enabled:
    # Logic: Reduce Heater usage by 30% when price is above threshold
    df['optimized_heater'] = np.where(df['electricity_price'] > price_threshold, 
                                      df['Heater'] * 0.7, df['Heater'])
    df['optimized_total'] = df['Total Load'] - df['Heater'] + df['optimized_heater']
    
    orig_cost = (df['Total Load'] * df['electricity_price']).sum()
    opt_cost = (df['optimized_total'] * df['electricity_price']).sum()
    savings = ((orig_cost - opt_cost) / orig_cost) * 100
    
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Original Estimated Cost", f"${orig_cost/1000:.2f}k")
    kpi2.metric("Optimized Cost", f"${opt_cost/1000:.2f}k", delta=f"-{savings:.1f}%")
    kpi3.metric("Energy Saved", f"{(df['Total Load'].sum() - df['optimized_total'].sum()):.0f} Units")
    
    st.success(f"AI Strategy: Heater power reduced by 30% during high-price periods (Above ${price_threshold}).")
else:
    st.info("Check 'Enable Energy Optimization AI' in the sidebar to simulate cost savings.")

# --- RAW DATA VIEW ---
if st.checkbox("Show Raw Data Source"):
    st.write(df.head(100))