import pandas as pd
import numpy as np

np.random.seed(42)

n = 2000  # number of customers

data = {
    "Customer_ID": [f"CUST{i}" for i in range(1001, 1001 + n)],
    "Tenure_Months": np.random.randint(1, 48, n),
    "Purchase_Frequency": np.random.randint(1, 20, n),
    "Avg_Order_Value": np.random.randint(200, 5000, n),
    "Total_Spend": np.random.randint(1000, 100000, n),
    "Last_Purchase_Days": np.random.randint(1, 180, n),
    "Website_Visits": np.random.randint(1, 100, n),
    "Discount_Usage": np.round(np.random.uniform(0, 1, n), 2),
    "Support_Tickets": np.random.randint(0, 10, n),
}

df = pd.DataFrame(data)

# 🔥 Create realistic probabilistic churn logic
# Higher recency + more support tickets + low frequency → higher churn risk

churn_score = (
    0.04 * df["Last_Purchase_Days"] +         # more days since purchase → higher churn
    -0.3 * df["Purchase_Frequency"] +        # frequent buyers → less churn
    0.6 * df["Support_Tickets"] +            # more complaints → higher churn
    -0.00002 * df["Total_Spend"] +           # higher spend → less churn
    -0.02 * df["Website_Visits"]             # engaged users → less churn
)

# Convert score to probability using sigmoid function
probability = 1 / (1 + np.exp(-churn_score))

# Assign churn based on probability
df["Churn"] = np.where(probability > 0.5, 1, 0)

# Save dataset
df.to_csv("predictor/ecommerce_churn_data.csv", index=False)

print("E-Commerce Dataset Generated Successfully!")
print("Churn Distribution:")
print(df["Churn"].value_counts())