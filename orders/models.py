from django.db import models
from django.contrib.auth.models import User

from product.models import Product


class OrderitemQueryset(models.QuerySet):

    def total_price(self):
        return sum(cart.products_price() for cart in self)
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
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
    products_info = models.JSONField(default=dict)


    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def total_price(self):
        return self.order_items.total_price()
    
    def total_quantity(self):
        return self.order_items.total_quantity()


    def __str__(self):
        return f"Заказ № {self.pk} | Покупатель {self.user.first_name} {self.user.last_name}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, null=True, default=None)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = OrderitemQueryset.as_manager()  

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.name} | Заказ №{self.order.pk}"

    def products_price(self):
        """Стоимость товара с учетом количества"""
        return self.price * self.quantity
