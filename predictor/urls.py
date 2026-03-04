from django.urls import path
from . import views

urlpatterns = [
    path("predict-churn/", views.upload_file, name="upload"),
    path("churn/check/", views.auto_predict_user_churn, name="auto_predict_user_churn"),
]