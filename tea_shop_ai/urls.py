from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import RoleBasedLoginView


urlpatterns = [
    path("", RoleBasedLoginView.as_view(), name="home"),

    path("shop/", include("products.urls")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("ai/", include("ai_chat.urls")),

    # Admin tự code
    path("admin/", include("manager.urls")),

    # Django Admin mặc định, chỉ để dự phòng. Có thể xóa nếu không muốn dùng.
    path("django-admin/", admin.site.urls),

    path("accounts/", include("accounts.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)