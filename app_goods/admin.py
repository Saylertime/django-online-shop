from django.contrib import admin
from app_goods.models import Category, SubCategory, Item, Review, Seller, Delivery, Payment


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'is_active', 'sort_index']


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'is_active']


class SellerAdmin(admin.ModelAdmin):
    list_display = ['name']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['item', 'author']


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ['delivery_type']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['payment_type']

admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(Payment, PaymentAdmin)