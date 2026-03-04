import pandas as pd
import pickle
import os
from datetime import date
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from orders.models import Order
from .forms import UploadFileForm
from django.db.models import Sum, F

# Load trained model & scaler
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_model/ecommerce_model.pkl")
SCALER_PATH = os.path.join(settings.BASE_DIR, "ml_model/ecommerce_scaler.pkl")

def load_ml_assets():
    try:
        with open(MODEL_PATH, "rb") as f:
            model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f:
            scaler = pickle.load(f)
        return model, scaler
    except Exception:
        return None, None

model, scaler = load_ml_assets()

def upload_file(request):
    if not model or not scaler:
        return render(request, "upload.html", {"error": "ML Model files not found."})
    
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES["file"]
            try:
                original_df = pd.read_csv(file)
            except Exception:
                return render(request, "upload.html", {
                    "form": form,
                    "error": "Invalid file format."
                })

            df = original_df.copy()
            columns_to_drop = [col for col in ["Customer_ID", "Churn"] if col in df.columns]
            X = df.drop(columns=columns_to_drop)
            
            # Ensure correct column order for scaler
            # Expected: Tenure_Months, Purchase_Frequency, Avg_Order_Value, Total_Spend, Last_Purchase_Days, Website_Visits, Discount_Usage, Support_Tickets
            expected_cols = ["Tenure_Months", "Purchase_Frequency", "Avg_Order_Value", "Total_Spend", "Last_Purchase_Days", "Website_Visits", "Discount_Usage", "Support_Tickets"]
            X = X[expected_cols]

            X_scaled = scaler.transform(X)
            probabilities = model.predict_proba(X_scaled)[:, 1]
            original_df["Churn_Probability"] = probabilities

            def risk_level(prob):
                if prob > 0.7: return "High Risk"
                elif prob > 0.4: return "Medium Risk"
                else: return "Low Risk"

            original_df["Risk_Level"] = original_df["Churn_Probability"].apply(risk_level)
            
            predictions = []
            for _, row in original_df.iterrows():
                predictions.append({
                    "customer_id": row.get("Customer_ID", "N/A"),
                    "probability": round(row["Churn_Probability"] * 100, 2),
                    "risk": row["Risk_Level"]
                })

            return render(request, "result.html", {
                "predictions": predictions,
                "total": len(predictions)
            })
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})

@login_required
def auto_predict_user_churn(request):
    if not model or not scaler:
        return render(request, "admin/churn_result.html", {"error": "ML Model files not found."})

    results = []
    users = User.objects.filter(is_superuser=False, is_staff=False).distinct()

    for user in users:
        orders = Order.objects.filter(user=user)
        if not orders.exists():
            continue

        # Calculate Total Spend
        from orders.models import OrderItem
        total_spent = OrderItem.objects.filter(order__user=user).aggregate(
            total=Sum(F('price') * F('qty'))
        )['total'] or 0

        total_orders = orders.count()

        # Feature Calculations
        tenure_months = (date.today() - user.date_joined.date()).days / 30
        avg_order_value = float(total_spent) / total_orders if total_orders > 0 else 0
        last_order = orders.order_by("-created_at").first()
        last_purchase_days = (date.today() - last_order.created_at.date()).days if last_order else 0

        # Features not tracked yet (using safe defaults or randomized for demo if needed, but 0 is safe)
        website_visits = 10 # Default
        discount_usage = 0.1 # Default
        support_tickets = 0

        # Correct Order as per CSV:
        # Tenure_Months, Purchase_Frequency, Avg_Order_Value, Total_Spend, Last_Purchase_Days, Website_Visits, Discount_Usage, Support_Tickets
        
        input_df = pd.DataFrame([[
            tenure_months,
            total_orders, # Purchase_Frequency
            avg_order_value,
            float(total_spent),
            last_purchase_days,
            website_visits,
            discount_usage,
            support_tickets
        ]], columns=[
            "Tenure_Months", "Purchase_Frequency", "Avg_Order_Value", "Total_Spend",
            "Last_Purchase_Days", "Website_Visits", "Discount_Usage", "Support_Tickets"
        ])

        # Scale + Predict
        input_scaled = scaler.transform(input_df)
        prob = model.predict_proba(input_scaled)[0][1]
        probability = round(prob * 100, 2)

        if prob > 0.7: risk = "High Risk"
        elif prob > 0.4: risk = "Medium Risk"
        else: risk = "Low Risk"

        results.append({
            "username": user.username,
            "email": user.email,
            "probability": probability,
            "risk": risk,
            "orders": total_orders,
            "total_spent": round(float(total_spent), 2)
        })

    # Sort by highest probability
    results = sorted(results, key=lambda x: x["probability"], reverse=True)

    high_count = sum(1 for r in results if r["risk"] == "High Risk")
    medium_count = sum(1 for r in results if r["risk"] == "Medium Risk")
    low_count = sum(1 for r in results if r["risk"] == "Low Risk")

    return render(request, "admin/churn_result.html", {
        "results": results,
        "high_count": high_count,
        "medium_count": medium_count,
        "low_count": low_count,
        "total_customers": len(results),
        "total_customers_count": len(results) # backup variable name
    })
