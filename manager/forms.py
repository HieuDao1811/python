from django import forms
from products.models import Product, Category
from orders.models import Order


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "admin-input"}),
            "description": forms.Textarea(attrs={"class": "admin-input", "rows": 4}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "ingredients",
            "taste",
            "benefit",
            "price",
            "stock",
            "image",
        ]

        widgets = {
            "category": forms.Select(attrs={"class": "admin-input"}),
            "name": forms.TextInput(attrs={"class": "admin-input"}),
            "description": forms.Textarea(attrs={"class": "admin-input", "rows": 4}),
            "ingredients": forms.Textarea(attrs={"class": "admin-input", "rows": 3}),
            "taste": forms.TextInput(attrs={"class": "admin-input"}),
            "benefit": forms.Textarea(attrs={"class": "admin-input", "rows": 3}),
            "price": forms.NumberInput(attrs={"class": "admin-input"}),
            "stock": forms.NumberInput(attrs={"class": "admin-input"}),
            "image": forms.ClearableFileInput(attrs={"class": "admin-input"}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]

        widgets = {
            "status": forms.Select(attrs={"class": "admin-input"}),
        }