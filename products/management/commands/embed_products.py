from django.core.management.base import BaseCommand
from products.models import Product
from ai_chat.services import embed_text


class Command(BaseCommand):
    help = "Tạo embedding cho sản phẩm trà"

    def handle(self, *args, **kwargs):
        products = Product.objects.all()

        for product in products:
            text = product.ai_text()
            embedding = embed_text(text)

            product.embedding = embedding
            product.save(update_fields=["embedding"])

            self.stdout.write(self.style.SUCCESS(
                f"Đã tạo embedding: {product.name}"
            ))

        self.stdout.write(self.style.SUCCESS("Hoàn tất tạo embedding."))