from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from product.models import Product
from carts.models import Cart


class CartAddView(View):
    def post(self, request, product_slug):
        
        product = get_object_or_404(Product, slug=product_slug)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        carts = Cart.objects.filter(user=request.user)
        
        return JsonResponse({
            'success': True,
            'total_quantity': carts.total_quantity(),
            'item_quantity': cart_item.quantity,
            'product_name': product.name
        })


class CartChangeView(View):
    def post(self, request, product_slug):
        
        product = get_object_or_404(Product, slug=product_slug)
        cart_item = get_object_or_404(Cart, user=request.user, product=product)
        
        action = request.POST.get('action')
        
        if action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                return JsonResponse({
                    'success': True,
                    'item_quantity': 0,
                    'item_price': 0,
                    'total_quantity': Cart.objects.filter(user=request.user).total_quantity(),
                    'total_price': Cart.objects.filter(user=request.user).total_price(),
                })
        
        carts = Cart.objects.filter(user=request.user)
        
        return JsonResponse({
            'success': True,
            'item_quantity': cart_item.quantity,
            'item_price': cart_item.products_price(),
            'total_quantity': carts.total_quantity(),
            'total_price': carts.total_price(),
        })

class CartRemoveView(View):
    def post(self, request, cart_id):
        cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
        cart_item.delete()
        
        carts = Cart.objects.filter(user=request.user)
        return JsonResponse({
            'success': True,
            'total_quantity': carts.total_quantity(),
            'total_price': carts.total_price(),
        })