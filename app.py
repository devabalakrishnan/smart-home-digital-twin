  import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Config
st.set_page_config(page_title="AI Digital Twin Pro", layout="wide")
st.title("🏙️ AI Digital Twin: Professional Energy Analytics")

# 2. THE FORCE DETECTOR: This finds your CSV regardless of its name
def get_any_csv():
    # Get a list of all files in the repository
    files = os.listdir('.')
    # Find any file that ends with .csv
    csv_files = [f for f in files if f.lower().endswith('.csv')]
    
    if csv_files:
        # Load the first CSV file it finds
        return csv_files[0]
    return None

target_file = get_any_csv()

if target_file:
    try:
        df = pd.read_csv(target_file)
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        st.sidebar.success(f"✅ Auto-Detected: {target_file}")
        
        # --- DASHBOARD METRICS ---
        m1, m2 = st.columns(2)
        m1.metric("Current Total Load", f"{df['Total Load'].iloc[-1]} kW")
        m2.metric("Avg Electricity Price", f"${df['electricity_price'].mean():.2f}")

        # --- CHARTS ---
        st.subheader("📊 Energy Consumption Trend")
        fig = px.line(df.tail(100), x='datetime', y='Total Load', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

        # --- EXPORT FEATURE ---
        csv_data = df.tail(100).to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Analysis Report", data=csv_data, file_name='twin_report.csv')

    except Exception as e:
        st.error(f"⚠️ Found file {target_file} but could not read it. Error: {e}")
else:
    st.error("❌ NO CSV FILE FOUND!")
    st.write("Files currently in your GitHub: ", os.listdir('.'))
    st.info("Please upload your 'data.csv' file to the main GitHub folder.")
