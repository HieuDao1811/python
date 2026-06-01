from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.shortcuts import render, redirect

from orders.models import Order, OrderItem
from products.models import Product
from django.contrib.auth.models import User


@login_required
def dashboard_view(request):
    if not request.user.is_staff and not request.user.is_superuser:
        return redirect("product_list")

    total_revenue = Order.objects.filter(status="completed").aggregate(
        total=Sum("total_price")
    )["total"] or 0

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    completed_orders = Order.objects.filter(status="completed").count()
    total_products = Product.objects.count()
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()

    recent_orders = Order.objects.select_related("user").order_by("-created_at")[:5]

    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    return render(request, "dashboard/dashboard.html", {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_products": total_products,
        "total_users": total_users,
        "recent_orders": recent_orders,
        "top_products": top_products,
    })