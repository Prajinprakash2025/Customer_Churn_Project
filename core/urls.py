
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("django-admin/", admin.site.urls),

    # User side
    path("", include("products.urls")),
    path("accounts/", include("accounts.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),

    # Management Dashboard (sidebar)
    path("management/", include("products.admin_urls")),   
    path("management/churn/", include("predictor.urls")),  
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)