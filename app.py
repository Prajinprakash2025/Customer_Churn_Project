import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load model, scaler, columns
model = pickle.load(open("ml_model/churn_model.pkl", "rb"))
scaler = pickle.load(open("ml_model/scaler.pkl", "rb"))
model_columns = pickle.load(open("ml_model/model_columns.pkl", "rb"))

st.title("📊 Customer Churn Prediction System")
st.write("AI-Powered Retention Intelligence")

st.sidebar.header("Enter Customer Details")

# Numeric Inputs
tenure = st.sidebar.slider("Tenure (Months)", 0, 72, 12)
monthly_charges = st.sidebar.slider("Monthly Charges", 0, 150, 50)
total_charges = st.sidebar.slider("Total Charges", 0, 10000, 2000)

# Create empty dataframe with all model columns
input_df = pd.DataFrame(columns=model_columns)
input_df.loc[0] = 0  # initialize row with zeros

# Fill only numeric columns
if "tenure" in input_df.columns:
    input_df["tenure"] = tenure

if "MonthlyCharges" in input_df.columns:
    input_df["MonthlyCharges"] = monthly_charges

if "TotalCharges" in input_df.columns:
    input_df["TotalCharges"] = total_charges

# Scale
input_scaled = scaler.transform(input_df)

if st.sidebar.button("Predict Churn"):

    probability = model.predict_proba(input_scaled)[0][1]

    st.subheader("Prediction Result")

    st.write(f"Churn Probability: **{round(probability*100,2)}%**")

    if probability > 0.7:
        st.error("High Risk Customer 🚨")
        st.write("Recommended Action: Offer 20% Discount + Loyalty Plan")
    elif probability > 0.4:
        st.warning("Medium Risk Customer ⚠")
        st.write("Recommended Action: Offer Loyalty Rewards")
    else:
        st.success("Low Risk Customer ✅")
        st.write("Recommended Action: Regular Engagement")

st.markdown("---")
st.write("Built using Logistic Regression | Kaggle Telco Dataset")