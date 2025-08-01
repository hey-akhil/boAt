from django.db import models

class Product(models.Model):
    badge = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='products/')
    playback_badge = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=0.0)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=50)

    def __str__(self):
        return self.title
