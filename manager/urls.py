from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_dashboard, name="admin_dashboard"),

    path("products/", views.admin_product_list, name="admin_product_list"),
    path("products/create/", views.admin_product_create, name="admin_product_create"),
    path("products/<int:product_id>/edit/", views.admin_product_update, name="admin_product_update"),
    path("products/<int:product_id>/delete/", views.admin_product_delete, name="admin_product_delete"),

    path("categories/", views.admin_category_list, name="admin_category_list"),
    path("categories/create/", views.admin_category_create, name="admin_category_create"),
    path("categories/<int:category_id>/edit/", views.admin_category_update, name="admin_category_update"),
    path("categories/<int:category_id>/delete/", views.admin_category_delete, name="admin_category_delete"),

    path("orders/", views.admin_order_list, name="admin_order_list"),
    path("orders/<int:order_id>/", views.admin_order_detail, name="admin_order_detail"),
    path("orders/<int:order_id>/status/", views.admin_order_update_status, name="admin_order_update_status"),

    path("chats/", views.admin_chat_history, name="admin_chat_history"),
]