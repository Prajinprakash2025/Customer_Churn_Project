import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report

# Load dataset
df = pd.read_csv("ecommerce_churn_data.csv")

# Features and target
X = df.drop(["Customer_ID", "Churn"], axis=1)
y = df["Churn"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X_train_scaled, y_train)

# Evaluation
pred = model.predict(X_test_scaled)

print("Accuracy:", accuracy_score(y_test, pred))
print("ROC-AUC:", roc_auc_score(y_test, model.predict_proba(X_test_scaled)[:,1]))
print("\nClassification Report:\n")
print(classification_report(y_test, pred))

# Save model
pickle.dump(model, open("predictor/ecommerce_model.pkl", "wb"))
pickle.dump(scaler, open("predictor/ecommerce_scaler.pkl", "wb"))

print("\nModel Saved Successfully!")