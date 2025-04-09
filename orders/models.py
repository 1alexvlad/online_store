from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.qauntity for cart in self)
        return 0

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None)
    created_timestamp = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    requires_delivery = models.BooleanField(default=False)
    delivery_address = models.TextField(null=True, blank=True)
    payment_on_get = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50, default='В обработке')


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"