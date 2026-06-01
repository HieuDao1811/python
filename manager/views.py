from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from products.models import Product, Category
from orders.models import Order, OrderItem
from ai_chat.models import ChatHistory
from .forms import ProductForm, CategoryForm, OrderStatusForm


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


admin_required = user_passes_test(is_admin, login_url="login")


@admin_required
def admin_dashboard(request):
    total_revenue = Order.objects.filter(status="completed").aggregate(
        total=Sum("total_price")
    )["total"] or 0

    all_revenue = Order.objects.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status="pending").count()
    completed_orders = Order.objects.filter(status="completed").count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_users = User.objects.filter(is_staff=False, is_superuser=False).count()
    total_chats = ChatHistory.objects.count()

    recent_orders = Order.objects.select_related("user").order_by("-created_at")[:8]

    top_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    return render(request, "manager/dashboard.html", {
        "total_revenue": total_revenue,
        "all_revenue": all_revenue,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "completed_orders": completed_orders,
        "total_products": total_products,
        "total_categories": total_categories,
        "total_users": total_users,
        "total_chats": total_chats,
        "recent_orders": recent_orders,
        "top_products": top_products,
    })


@admin_required
def admin_product_list(request):
    products = Product.objects.select_related("category").order_by("-created_at")
    keyword = request.GET.get("q")

    if keyword:
        products = products.filter(name__icontains=keyword)

    return render(request, "manager/product_list.html", {
        "products": products,
        "keyword": keyword,
    })


@admin_required
def admin_product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("admin_product_list")
    else:
        form = ProductForm()

    return render(request, "manager/product_form.html", {
        "form": form,
        "title": "Thêm sản phẩm",
    })


@admin_required
def admin_product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            return redirect("admin_product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "manager/product_form.html", {
        "form": form,
        "title": "Sửa sản phẩm",
        "product": product,
    })


@admin_required
def admin_product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        product.delete()
        return redirect("admin_product_list")

    return render(request, "manager/confirm_delete.html", {
        "object": product,
        "title": "Xóa sản phẩm",
        "cancel_url": "admin_product_list",
    })


@admin_required
def admin_category_list(request):
    categories = Category.objects.all().order_by("name")

    return render(request, "manager/category_list.html", {
        "categories": categories,
    })


@admin_required
def admin_category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("admin_category_list")
    else:
        form = CategoryForm()

    return render(request, "manager/category_form.html", {
        "form": form,
        "title": "Thêm danh mục",
    })


@admin_required
def admin_category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("admin_category_list")
    else:
        form = CategoryForm(instance=category)

    return render(request, "manager/category_form.html", {
        "form": form,
        "title": "Sửa danh mục",
    })


@admin_required
def admin_category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        category.delete()
        return redirect("admin_category_list")

    return render(request, "manager/confirm_delete.html", {
        "object": category,
        "title": "Xóa danh mục",
        "cancel_url": "admin_category_list",
    })


@admin_required
def admin_order_list(request):
    orders = Order.objects.select_related("user").order_by("-created_at")
    status = request.GET.get("status")

    if status:
        orders = orders.filter(status=status)

    return render(request, "manager/order_list.html", {
        "orders": orders,
        "status": status,
        "status_choices": Order.STATUS_CHOICES,
    })


@admin_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderStatusForm(instance=order)

    return render(request, "manager/order_detail.html", {
        "order": order,
        "form": form,
    })


@admin_required
def admin_order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        form = OrderStatusForm(request.POST, instance=order)

        if form.is_valid():
            form.save()

    return redirect("admin_order_detail", order_id=order.id)


@admin_required
def admin_chat_history(request):
    chats = ChatHistory.objects.select_related("user").order_by("-created_at")[:100]

    return render(request, "manager/chat_history.html", {
        "chats": chats,
    })