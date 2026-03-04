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
]

