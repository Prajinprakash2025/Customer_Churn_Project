from django.urls import path
from . import admin_views

urlpatterns = [
    path("", admin_views.admin_dashboard, name="management_dashboard"),
    path("products/", admin_views.admin_products, name="manage_products"),
    path("products/add/", admin_views.admin_product_add, name="add_product"),
    path("products/<int:pk>/edit/", admin_views.admin_product_edit, name="edit_product"),
    path("products/<int:pk>/delete/", admin_views.admin_product_delete, name="delete_product"),
    path("products/bulk-delete/", admin_views.admin_bulk_delete_products, name="bulk_delete_products"),
    path("orders/", admin_views.admin_orders, name="manage_orders"),
    path("categories/", admin_views.admin_category_list, name="manage_categories"),
    path("categories/add/", admin_views.admin_category_add, name="add_category"),
    path("categories/<int:pk>/edit/", admin_views.admin_category_edit, name="edit_category"),
    path("categories/<int:pk>/delete/", admin_views.admin_category_delete, name="delete_category"),
    path("categories/bulk-delete/", admin_views.admin_bulk_delete_categories, name="bulk_delete_categories"),
    path("approve-seller/<int:id>/",admin_views.approve_seller,name="approve_seller"),
    path("seller-requests/",admin_views.seller_requests,name="seller_requests"),
]