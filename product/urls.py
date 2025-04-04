from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import MainView, CatalogProduct, ProductDetail, Search


app_name = 'product'

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('catalog/', CatalogProduct.as_view(), name='catalog'),
    path('search/', Search.as_view(), name='search'),
    path('<slug:slug>/', ProductDetail.as_view(), name='product_detail'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)