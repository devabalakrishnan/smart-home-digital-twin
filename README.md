# 🔬 Virtual Home Digital Twin: A Cyber-Physical Co-Simulation

This repository contains an AI-powered Digital Twin designed for residential energy monitoring and optimization. This project was developed as a research framework for simulating real-time interactions between a virtual environment and a digital monitoring interface.

## 🚀 Research Overview
The system utilizes a **Virtual Home Engine (VHE)** to generate stochastic energy telemetry, which is then synchronized with a **Spatial Digital Twin** visualization.

### Key Features:
* **Stochastic Load Simulation:** Uses Gaussian distributions and Markov-based occupancy models to generate realistic power consumption data ($P_{total}$).
* **Spatial-Temporal Mapping:** Real-time SVG-based visualization that changes color states (Green/Orange/Red) based on simulated load intensity.
* **Live Telemetry Stream:** Continuous data logging and visualization using Plotly for trend analysis.
* **Zero-Hardware Architecture:** Entirely self-contained co-simulation environment, perfect for edge-case testing and algorithmic validation.

## 🛠️ Methodology & Equations
The simulator is grounded in physical modeling. The total load at time $t$ is defined as:
$$P_{total}(t) = P_{base} + P_{active}(t) + \epsilon(t)$$



## 📦 Tech Stack
* **Language:** Python 3.x
* **Framework:** Streamlit (Real-time Web UI)
* **Mathematics:** NumPy (Stochastic modeling)
* **Visualization:** Plotly & SVG (Spatial state mapping)

## 🔧 Installation
To run this research interface locally:
1. Clone this repo: `git clone [YOUR_REPO_URL]`
2. Install dependencies: `pip install -r requirements.txt`
3. Launch app: `streamlit run app.py`

## 📑 IEEE Citation
If using this framework for academic purposes, please cite as:
*Author, "Real-time Co-Simulation of Residential Digital Twins using Stochastic Load Modeling," 2025.*
