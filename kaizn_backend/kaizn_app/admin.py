from django.contrib import admin

# Register your models here.
# kaizn_app/admin.py
from .models import User, ItemInventory

admin.site.register(ItemInventory)
