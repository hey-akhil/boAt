from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from decimal import Decimal


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
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return Decimal(str(self.product.price)) * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    address = models.TextField()
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    zip_code = models.CharField(max_length=10,null=True, blank=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    subtotal = models.FloatField(null=True, blank=True)
    tax = models.FloatField(null=True, blank=True)
    shipping = models.FloatField(null=True, blank=True)
    total = models.FloatField(null=True, blank=True)

    def full_name(self):
        return f"{self.first_name} "

    def get_total_from_items(self):
        return sum(item.total_price() for item in self.orderitem_set.all())

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(AddProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.title} x {self.quantity}"
