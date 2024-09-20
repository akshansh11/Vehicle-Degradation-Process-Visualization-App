# -*- coding: utf-8 -*-
"""shift.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tG_do7mHn922lQmxkFSiwZdMaUpNTazK
"""

# Import necessary libraries

import scipy
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from scipy.stats import norm

# Set the page configuration
st.set_page_config(page_title="Degradation Process Modeling", layout="wide")

# Load and display the company logo
logo_path = "shift.jpg"
st.image(logo_path, width=200)  # Adjust width as needed

# Title and description
st.title("Vehicle Degradation Process Visualization App")
st.write("This app simulates various degradation processes in materials based on mathematical models.")

# Sidebar for user inputs
st.sidebar.title("Model Parameters")
process_type = st.sidebar.selectbox("Choose Degradation Process",
                                    ["Static Overload", "Fatigue", "Creep", "Corrosion"])

# Model parameters based on degradation type
if process_type == "Static Overload":
    st.sidebar.write("**Static Overload Model**: Failure when stress exceeds tensile strength.")
    tensile_strength = st.sidebar.slider("Tensile Strength (MPa)", 100, 1000, 300)
    applied_load = st.sidebar.slider("Applied Load (MPa)", 100, 1500, 700)
    Z = lambda x, y: np.where(applied_load > tensile_strength, 1, 0)

elif process_type == "Fatigue":
    st.sidebar.write("**Fatigue Model**: Failure occurs due to cyclic loading below tensile strength.")
    cycles = st.sidebar.slider("Number of Cycles (x10^3)", 1, 1000, 300)
    stress_ratio = st.sidebar.slider("Stress Ratio (σ_min/σ_max)", 0.1, 1.0, 0.5)
    S_N_curve = lambda S, N: S * (1 / np.sqrt(N))  # Simplified S-N curve model
    Z = lambda x, y: S_N_curve(stress_ratio * 1000, cycles)

elif process_type == "Creep":
    st.sidebar.write("**Creep Model**: Material deformation under long-term stress at high temperature.")
    temp = st.sidebar.slider("Temperature (°C)", 20, 800, 300)
    time_hours = st.sidebar.slider("Time (hours)", 1, 10000, 5000)
    creep_eq = lambda T, t: (T * 0.0001) * np.log(1 + t)  # Simplified creep law
    Z = lambda x, y: creep_eq(temp, time_hours)

elif process_type == "Corrosion":
    st.sidebar.write("**Corrosion Model**: Material degradation due to environmental factors.")
    pH = st.sidebar.slider("Environmental pH Level", 0.0, 14.0, 7.0)
    temp = st.sidebar.slider("Temperature (°C)", 0, 100, 25)
    corrosion_rate = lambda pH, T: np.exp(-0.1 * pH) * (1 + T / 100)  # Simplified corrosion rate model
    Z = lambda x, y: corrosion_rate(pH, temp)

# Create a meshgrid for contour plotting
x = np.linspace(0, 100, 100)
y = np.linspace(0, 100, 100)
X, Y = np.meshgrid(x, y)

# Generate Z-values based on the selected degradation model
Z_values = Z(X, Y)

# Plotting the degradation process using contour plot
fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(X, Y, Z_values, 20, cmap=cm.plasma)
fig.colorbar(contour, ax=ax)
ax.set_title(f"{process_type} Degradation Model", fontsize=16)
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# Display the plot in Streamlit
st.pyplot(fig)

# High-resolution image download option
st.sidebar.header("Export Options")
dpi = st.sidebar.slider("DPI", 100, 600, 300)
st.write(f"Download high-resolution image ({dpi} DPI)")
if st.button('Download Image'):
    fig.savefig("degradation_plot.png", dpi=dpi)
    with open("degradation_plot.png", "rb") as file:
        btn = st.download_button(label="Download Image", data=file, file_name="degradation_plot.png", mime="image/png")
