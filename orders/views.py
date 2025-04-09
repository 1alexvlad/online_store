from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from carts.models import Cart
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from orders.forms import CreateOrderForm
from orders.models import Order


class CreateOrderView(LoginRequiredMixin, FormView):
    form_class = CreateOrderForm
    template_name = 'orders/create_orders.html'
    success_url = reverse_lazy('product:index')


    def form_valid(self, form):
        try:
            user = self.request.user
            cart_items = Cart.objects.filter(user=user)

            order = Order.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number'],
                requires_delivery=bool(int(form.cleaned_data['requires_delivery'])),
                delivery_address=form.cleaned_data['delivery_address'],
                payment_on_get=bool(int(form.cleaned_data['payment_on_get'])),
            )

            cart_items.delete()
            return super().form_valid(form)

        except Exception as e:
            messages.error(self.request, f'Ошибка: {str(e)}')
            return redirect('cart:order')