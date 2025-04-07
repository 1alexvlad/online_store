from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from product.models import Product


class CartQueryset(models.QuerySet):
    
    def total_price(self):
        return sum([cart.products_price() for cart in self])
    
    def total_quantity(self):
        if self:
            return sum(cart.quantity for cart in self)
        return 0

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    session_key = models.CharField(max_length=32, blank=True, null=True)
    created_timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'

    objects = CartQueryset().as_manager()

    def products_price(self):
        return round(self.product.price * self.quantity, 2)
    

    def __str__(self):
        return f"Корзина {self.user.username} -- Товар {self.product.name} -- Количестов {self.quantity}"