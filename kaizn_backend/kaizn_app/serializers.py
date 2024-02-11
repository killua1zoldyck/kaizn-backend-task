from rest_framework import serializers
from .models import ItemInventory

class ItemInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemInventory
        fields = '__all__'
