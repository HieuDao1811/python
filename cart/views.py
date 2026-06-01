from django.shortcuts import redirect, render, get_object_or_404
from products.models import Product


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    product_id_str = str(product.id)

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session["cart"] = cart
    return redirect("cart_detail")


def cart_detail(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        subtotal = product.price * quantity
        total += subtotal

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(request, "cart/cart_detail.html", {
        "items": items,
        "total": total,
    })


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session["cart"] = cart
    return redirect("cart_detail")


def clear_cart(request):
    request.session["cart"] = {}
    return redirect("cart_detail")