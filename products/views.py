from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


@login_required
def product_list(request):
    products = Product.objects.all().order_by("-created_at")
    categories = Category.objects.all()

    category_id = request.GET.get("category")
    keyword = request.GET.get("q")

    if category_id:
        products = products.filter(category_id=category_id)

    if keyword:
        products = products.filter(name__icontains=keyword)

    return render(request, "products/product_list.html", {
        "products": products,
        "categories": categories,
        "category_id": category_id,
        "keyword": keyword,
    })


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, "products/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })