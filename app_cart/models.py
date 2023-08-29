from django.contrib.auth.models import User
from django.db import models
from app_goods.models import Item, Delivery, Payment


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='товар')
    quantity = models.PositiveIntegerField(verbose_name='количество')
    session_key = models.CharField(max_length=40, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    active = models.BooleanField(verbose_name='активно')

    class Meta:
        verbose_name = 'товар в корзине'
        verbose_name_plural = 'товары в корзине'

    def item_sum(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cartitems = models.ManyToManyField(CartItem, related_name='orders')
    total_sum = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    active = models.BooleanField(verbose_name='активно')
    free_or_not = models.BooleanField(default=True, verbose_name="беслпатная доставка")
    city = models.CharField(max_length=150, null=True)
    address = models.CharField(max_length=300, null=True)
    payment_method = models.BooleanField(default=True, verbose_name='оплата онлайн')
    card_number = models.IntegerField(verbose_name='номер карты', null=True, blank=True)

    class Meta:
        verbose_name = 'временный заказ'
        verbose_name_plural = 'временные заказы'


class ComplitedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, related_name='items')
    order_id = models.PositiveIntegerField(null=True)
    total_sum = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    payed = models.BooleanField(verbose_name='оплачен')
    i_payed = models.BooleanField(verbose_name='платил со своей карты', null=True)
    delivery_method = models.BooleanField(default=False, verbose_name='экспресс-доставка')
    error = models.CharField(max_length=155, verbose_name='текст ошибки')

    class Meta:
        verbose_name = 'завершенный заказ'
        verbose_name_plural = 'завершенные заказы'

    def __str__(self):
        return f"Заказ № {self.order_id}"