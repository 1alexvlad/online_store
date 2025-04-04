from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from .models import Product


class MainView(TemplateView):
    template_name = 'base.html'


class CatalogProduct(ListView):
    model = Product
    template_name = 'product/catalog.html'

    context_object_name = 'products'


class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.all()
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, slug=self.kwargs.get(self.slug_url_kwarg))