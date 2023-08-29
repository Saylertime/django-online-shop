from django.contrib import admin
from .models import CartItem, Order, ComplitedOrder


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['item']


class ComplitedOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']

admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ComplitedOrder, ComplitedOrderAdmin)
