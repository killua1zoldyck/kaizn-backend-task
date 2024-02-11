# kaizn_app/models.py

from django.db import models
from django.contrib.auth.models import User

class ItemInventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sku = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    in_stock = models.IntegerField()
    available_stock = models.IntegerField()

    def __str__(self):
        return self.name
