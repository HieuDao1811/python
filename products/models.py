from django.db import models
from pgvector.django import VectorField


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )

    name = models.CharField(max_length=200)
    description = models.TextField()

    ingredients = models.TextField(blank=True)
    taste = models.CharField(max_length=255, blank=True)
    benefit = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    embedding = VectorField(dimensions=768, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def ai_text(self):
        return f"""
        Tên sản phẩm: {self.name}
        Loại trà: {self.category.name}
        Mô tả: {self.description}
        Thành phần: {self.ingredients}
        Hương vị: {self.taste}
        Công dụng: {self.benefit}
        Giá: {self.price} VND
        """

    def __str__(self):
        return self.name