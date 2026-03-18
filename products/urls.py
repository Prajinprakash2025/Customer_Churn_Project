from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("search/", views.search_products, name="search_products"),

    path("wishlist/", views.wishlist_detail, name="wishlist_detail"),
    path("wishlist/add/<int:product_id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),

    path("category/<int:pk>/", views.category_products, name="category_products"),

    path("become-seller/", views.become_seller, name="become_seller"),
    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    # Seller panel
    path("seller/dashboard/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/add-products/", views.add_product, name="add_products"),
    path("seller/products/", views.seller_products, name="seller_products"),
    path("seller/orders/", views.seller_orders, name="seller_orders"),


]

