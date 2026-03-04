# ==============================
# Customer Churn Prediction
# Telco Kaggle Dataset
# ==============================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score
)

# ==============================
# 1️⃣ Load Dataset
# ==============================

df = pd.read_csv("WA_Fn-UseC_-Telco-Customer-Churn.csv")

print("\nDataset Loaded Successfully\n")
print(df.head())

# ==============================
# 2️⃣ Data Cleaning
# ==============================

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# Fill missing values in TotalCharges
df["TotalCharges"] = df["TotalCharges"].fillna(df["TotalCharges"].median())

# Convert target variable to binary
df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# Drop customerID (not useful for prediction)
df.drop("customerID", axis=1, inplace=True)

# Encode categorical variables
df = pd.get_dummies(df, drop_first=True)

# Final safety check for missing values
df = df.fillna(0)

print("\nData Cleaning Completed\n")

# ==============================
# 3️⃣ Define Features & Target
# ==============================

X = df.drop("Churn", axis=1)
y = df["Churn"]

# ==============================
# 4️⃣ Train-Test Split
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ==============================
# 5️⃣ Logistic Regression
# ==============================

# Scaling (important for Logistic Regression)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

log_model = LogisticRegression(max_iter=1000)
log_model.fit(X_train_scaled, y_train)

log_pred = log_model.predict(X_test_scaled)

print("========== Logistic Regression ==========")
print("Accuracy:", accuracy_score(y_test, log_pred))
print("ROC-AUC:", roc_auc_score(y_test, log_model.predict_proba(X_test_scaled)[:,1]))
print("\nClassification Report:\n")
print(classification_report(y_test, log_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, log_pred))


# ==============================
# 6️⃣ Random Forest
# ==============================

rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)

print("\n========== Random Forest ==========")
print("Accuracy:", accuracy_score(y_test, rf_pred))
print("ROC-AUC:", roc_auc_score(y_test, rf_model.predict_proba(X_test)[:,1]))
print("\nClassification Report:\n")
print(classification_report(y_test, rf_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, rf_pred))


# ==============================
# 7️⃣ Feature Importance (Top 10)
# ==============================

importances = pd.Series(
    rf_model.feature_importances_,
    index=X.columns
).sort_values(ascending=False)

print("\nTop 10 Important Features:\n")
print(importances.head(10))


# ==============================
# 8️⃣ Churn Probability + Retention Logic
# ==============================

churn_prob = rf_model.predict_proba(X_test)[:,1]

def retention_strategy(prob):
    if prob > 0.7:
        return "High Risk - Offer 20% Discount"
    elif prob > 0.4:
        return "Medium Risk - Loyalty Program"
    else:
        return "Low Risk - Regular Engagement"

retention_actions = [retention_strategy(p) for p in churn_prob]

print("\nSample Retention Decisions:\n")
for i in range(5):
    print(f"Customer {i+1}: Probability={round(churn_prob[i],2)} → {retention_actions[i]}")


print("\n🎉 Model Training Completed Successfully!")



import pickle

# Save Logistic model (better performance in your case)
with open("churn_model.pkl", "wb") as f:
    pickle.dump(log_model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model Saved Successfully!")


with open("churn_model.pkl", "wb") as f:
    pickle.dump(log_model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("model_columns.pkl", "wb") as f:
    pickle.dump(X.columns.tolist(), f)

print("Model & Columns Saved Successfully!")