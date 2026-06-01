from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models import Product
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart_detail")

    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            phone=phone,
            address=address,
            total_price=total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["quantity"],
                price=item["product"].price,
            )

            item["product"].stock -= item["quantity"]
            item["product"].save()

        request.session["cart"] = {}

        return redirect("order_success", order_id=order.id)

    return render(request, "orders/checkout.html", {
        "items": items,
        "total": total,
    })


@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    return render(request, "orders/order_success.html", {
        "order": order,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "orders/order_history.html", {
        "orders": orders,
    })