from rest_framework import serializers
from app_goods.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('title', 'description',
                  'category', 'seller',
                  'price', 'limited',
                  'is_active', 'sold_quantity')