import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Digital Twin Dashboard", layout="wide")
st.title("🏠 Smart Home Digital Twin")

# The name must match exactly what you have on GitHub
FILENAME = 'data.csv' 

if os.path.exists(FILENAME):
    df = pd.read_csv(FILENAME)
    st.success(f"✅ Successfully loaded {FILENAME}")
    
    # Simple Visualization
    st.subheader("Energy Usage Overview")
    st.line_chart(df[['Total Load']].tail(100))
    
    if st.checkbox("Show Raw Data"):
        st.dataframe(df.head(20))
else:
    st.error(f"❌ Cannot find '{FILENAME}'")
    st.write("Files currently in your GitHub repository:")
    st.write(os.listdir("."))
