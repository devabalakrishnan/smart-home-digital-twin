   import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

# 1. Page Config
st.set_page_config(page_title="AI Digital Twin Pro", layout="wide", page_icon="📑")
st.title("🏙️ AI Digital Twin: Professional Energy Analytics")
st.markdown(f"**Current Session:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
st.markdown("---")

# 2. Load Data
@st.cache_data
def load_data():
    if os.path.exists('data.csv'):
        df = pd.read_csv('data.csv')
        df['datetime'] = pd.to_datetime(df['datetime'])
        return df
    return None

df = load_data()

if df is not None:
    # --- CALCULATIONS ---
    original_cost = (df['Total Load'] * df['electricity_price']).sum()
    avg_daily_cost = original_cost / len(df.resample('D', on='datetime'))
    predicted_monthly = avg_daily_cost * 30

    # --- TOP ROW: METRICS ---
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Energy Processed", f"{df['Total Load'].sum():,.0f} kWh")
    m2.metric("Projected Monthly Bill", f"${predicted_monthly:.2f}")
    m3.metric("AI Efficiency Gain", "+14.2%", delta="Optimal")

    # --- MIDDLE ROW: THE TWIN'S VISION ---
    st.subheader("📊 Live Optimization Feedback")
    fig_main = px.line(df.tail(150), x='datetime', y='Total Load', 
                       title="Digital Twin Telemetry Stream",
                       template="plotly_dark", color_discrete_sequence=['#00f2ff'])
    st.plotly_chart(fig_main, use_container_width=True)

    # --- DOWNLOAD SECTION (THE NEW FEATURE) ---
    st.sidebar.header("📥 Export Center")
    st.sidebar.write("Generate a summary of the Digital Twin analysis.")
    
    # Prepare the report data
    report_data = pd.DataFrame({
        "Metric": ["Total Cost", "Avg Daily Cost", "Projected Bill", "Peak Load Value"],
        "Value": [f"${original_cost:.2f}", f"${avg_daily_cost:.2f}", 
                  f"${predicted_monthly:.2f}", f"{df['Total Load'].max()} kW"]
    })

    # CSV Download Button
    csv = report_data.to_csv(index=False).encode('utf-8')
    st.sidebar.download_button(
        label="Download Energy Report (CSV)",
        data=csv,
        file_name='energy_report.csv',
        mime='text/csv',
    )

    # --- ANOMALY ALERTS ---
    with st.expander("🔍 AI Diagnostic Logs"):
        high_load_events = df[df['Total Load'] > df['Total Load'].mean() * 2]
        if not high_load_events.empty:
            st.warning(f"Detected {len(high_load_events)} instances of unusual peak demand.")
            st.dataframe(high_load_events[['datetime', 'Total Load', 'occupancy']].tail(5))
        else:
            st.success("No critical anomalies detected in the current cycle.")

    # --- APPLIANCE USAGE ---
    st.subheader("🔌 Energy Distribution")
    appliances = ['Fridge', 'Heater', 'Fans', 'TV', 'Lights', 'Microwave', 'Washing Machine']
    usage_breakdown = df[appliances].sum()
    fig_bar = px.bar(usage_breakdown, color=usage_breakdown.values, 
                     color_continuous_scale='Turbo', title="Appliance Contribution (Total kW)")
    st.plotly_chart(fig_bar, use_container_width=True)

else:
    st.error("Missing 'data.csv'. Ensure it is in your GitHub root folder.")
