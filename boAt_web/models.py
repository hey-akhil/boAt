from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class AddProduct(models.Model):
    title = models.CharField(max_length=255)
    badge = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    playback_badge = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=0.0)
    price = models.FloatField(null=True, blank=True)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1, null=True, blank=True)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"




