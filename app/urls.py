from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('account/', include('account.urls'), name='account'),
    path('cart/', include('carts.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('product.urls'), name='product')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
