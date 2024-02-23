from django.db import models
from django.contrib.auth.models import User 

class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=20)
    qtd = models.PositiveIntegerField()
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    active = models.BooleanField(default=True)
    closed_at = models.DateField(null=True, blank=True)

class TickerCache(models.Model):
    ticker = models.CharField(max_length=20)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cached_at = models.DateTimeField(auto_now_add=True)

