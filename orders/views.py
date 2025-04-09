from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from carts.models import Cart
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import CreateOrderForm
from orders.models import Order

from .models import OrderItem


class CreateOrderView(FormView):
    form_class = CreateOrderForm
    template_name = 'orders/create_orders.html'
    success_url = reverse_lazy('product:index')

    def form_valid(self, form):
        try:
            user = self.request.user
            cart_items = Cart.objects.filter(user=user)
            
            if not cart_items.exists():
                messages.warning(self.request, 'Ваша корзина пуста!')
                return redirect('cart:order')
            
            order = Order.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                requires_delivery=bool(int(form.cleaned_data['requires_delivery'])),
                delivery_address=form.cleaned_data['delivery_address'],
                payment_on_get=bool(int(form.cleaned_data['payment_on_get'])),
                is_paid=form.cleaned_data['payment_on_get'] == '0',
            )
            
            products_info = {}
            for idx, cart_item in enumerate(cart_items):
                product = cart_item.product
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    name=product.name,
                    price=product.price,
                    quantity=cart_item.quantity,
                )
                
                products_info[str(idx)] = {
                    'name': product.name,
                    'price': str(product.price),
                    'quantity': cart_item.quantity,
                    'product_id': product.id
                }
            
            order.products_info = products_info
            order.save()
            
            cart_items.delete()
            
            messages.success(self.request, 'Заказ успешно оформлен!')
            return super().form_valid(form)
            
        except Exception as e:
            messages.error(self.request, f'Ошибка: {str(e)}')
            return redirect('cart:order')