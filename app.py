#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import numpy as np
import math

# Page setup
st.set_page_config(page_title="Chemical Kinetics Activation Energy Lab Dashboard", layout="wide")
st.title("🧪 Chemical Kinetics Activation Energy Lab Dashboard")

# Ideal gas constant
R = 8.314

# --- PART A: UNCATALYZED REACTION ---
st.header("Part A: Activation Energy ($E_a$) of the Uncatalyzed Reaction")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Parameters")
    x_input_a = st.text_input("1/T Values (separated by commas):", "0.003384, 0.003314, 0.003224, 0.003143")
    y_input_a = st.text_input("ln(k) Values (separated by commas):", "-5.236, -4.898, -4.346, -3.829")

with col2:
    st.subheader("Calculated Results")
    try:
        x_a = np.array([float(i.strip()) for i in x_input_a.split(",") if i.strip()])
        y_a = np.array([float(i.strip()) for i in y_input_a.split(",") if i.strip()])

        if len(x_a) == len(y_a) and len(x_a) > 1:
            slope_a, intercept_a = np.polyfit(x_a, y_a, 1)
            Ea_uncat = -slope_a * R

            st.metric(label="Slope ($m$)", value=f"{slope_a:.2f} K")
            st.metric(label="Activation Energy ($E_a$)", value=f"{Ea_uncat / 1000:.2f} kJ/mol")
        else:
            st.error("Error: Array lengths must match and have at least 2 data points.")
    except Exception as e:
        st.error(f"Invalid input format. Ensure numbers are comma-separated. Error: {e}")

st.markdown("---")

# --- PART B: CATALYZED REACTION RATE LAW ---
st.header("Part B: Rate Law with a Catalyst Present")
col3, col4 = st.columns(2)

with col3:
    st.subheader("Input Parameters")
    x_input_b = st.text_input("ln[Catalyst] Values (separated by commas):", "-3.777, -3.478, -3.301, -3.176")
    y_input_b = st.text_input("ln(Initial Rate) Values (separated by commas):", "-4.700, -4.538, -4.401, -4.289")

with col4:
    st.subheader("Calculated Results")
    try:
        x_b = np.array([float(i.strip()) for i in x_input_b.split(",") if i.strip()])
        y_b = np.array([float(i.strip()) for i in y_input_b.split(",") if i.strip()])

        if len(x_b) == len(y_b) and len(x_b) > 1:
            slope_b, intercept_b = np.polyfit(x_b, y_b, 1)

            st.metric(label="Slope ($\mathrm{Cu^{2+}}$ Order)", value=f"{slope_b:.3f}")
        else:
            st.error("Error: Array lengths must match and have at least 2 data points.")
    except Exception as e:
        st.error(f"Invalid input format. Error: {e}")

st.markdown("---")

# --- PART C: CATALYZED REACTION ACTIVATION ENERGY ---
st.header("Part C: Activation Energy of a Catalyzed Reaction ($E_{a,\mathrm{cat}}$)")
col5, col6 = st.columns(2)

with col5:
    st.subheader("Input Experimental Points")
    t5 = st.number_input("Temperature 1 ($T_1$) in K:", value=297.7, format="%.1f")
    t9 = st.number_input("Temperature 2 ($T_2$) in K:", value=314.3, format="%.1f")
    k5 = st.number_input("Rate Constant 1 ($k_1$):", value=1.99e-5, format="%.2e")
    k9 = st.number_input("Rate Constant 2 ($k_2$):", value=6.25e-5, format="%.2e")

with col6:
    st.subheader("Calculated Results")
    if t5 != t9 and k9 > 0 and k5 > 0:
        rate_term = math.log(k5 / k9)
        temp_term = (t5 - t9) / (t5 * t9)
        Ea_cat_val = R * (rate_term / temp_term)

        st.metric(label="Catalyzed $E_a$", value=f"{Ea_cat_val / 1000:.2f} kJ/mol")

        # Theoretical validation statement block
        st.subheader("Theoretical Evaluation")
        if 'Ea_uncat' in locals():
            if Ea_cat_val > Ea_uncat:
                st.warning(
                    f"⚠️ **Discrepancy Detected:** The activation energy of the catalyzed reaction "
                    f"({Ea_cat_val/1000:.2f} kJ/mol) is **greater** than that of the uncatalyzed reaction "
                    f"({Ea_uncat/1000:.2f} kJ/mol). This contradicts collision theory, which "
                    f"dictates that a catalyst must lower the required activation energy barriers."
                )
            else:
                st.success("✅ **Success:** The catalyzed activation energy is lower than the uncatalyzed activation energy, verifying theoretical models.")
    else:
        st.error("Error: Please provide non-zero temperatures and rate constants.")

