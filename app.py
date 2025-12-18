 import streamlit as st
import pandas as pd
import os

# Set page title
st.set_page_config(page_title="Home Energy Digital Twin", layout="wide")

st.title("🏠 Smart Home Digital Twin")

# The name must match exactly what you have on GitHub
filename = 'data.csv'

if os.path.exists(filename):
    # Load the data
    df = pd.read_csv(filename)
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    # Success Message
    st.sidebar.success(f"✅ Connected to {filename}")
    
    # Simple Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Data Points", len(df))
    col2.metric("Avg Electricity Price", f"${df['electricity_price'].mean():.2f}")
    col3.metric("Peak Load", f"{df['Total Load'].max()} kW")

    # Chart
    st.subheader("Live Energy Load (kW)")
    st.line_chart(df.set_index('datetime')['Total Load'].tail(100))
    
    # Show Table
    if st.checkbox("Show Raw Data Logs"):
        st.write(df.head(20))
else:
    # Error Message if file is missing
    st.error(f"❌ Still can't find '{filename}'")
    st.write("Current files in your GitHub repository:")
    st.write(os.listdir("."))
    st.info("Check if the file is named 'data.csv' (all lowercase) on GitHub.")
