from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=150, verbose_name='категория')
    is_active = models.BooleanField(verbose_name='активность')
    sort_index = models.PositiveIntegerField(verbose_name='индекс сортировки')
    photo = models.ImageField(verbose_name='фото категории', null=True)
    has_subcategory = models.BooleanField(default=False, verbose_name='наличие подкатегорий')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.category


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', related_name='subcat')
    title = models.CharField(max_length=150, verbose_name='название')
    photo = models.ImageField(blank=True)

    class Meta:
        verbose_name = 'подкатегория'
        verbose_name_plural = 'подкатегории'

    def __str__(self):
        return self.title



class Seller(models.Model):
    name = models.CharField(max_length=155, verbose_name='продавец')

    class Meta:
        verbose_name = 'продавец'
        verbose_name_plural = 'продавцы'

    def __str__(self):
        return self.name


class Delivery(models.Model):
    delivery_type = models.CharField(max_length=100, verbose_name='тип доставки')

    class Meta:
        verbose_name = 'доставка'
        verbose_name_plural = 'типы доставки'

    def __str__(self):
        return self.delivery_type


class Item(models.Model):
    title = models.CharField(max_length=155, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория', related_name='items')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='подкатегория',
                                     related_name='sub_items', null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, verbose_name='продавец', null=True)
    image = models.ImageField(verbose_name="фотография")
    image2 = models.ImageField(verbose_name="фотография 2", blank=True)
    image3 = models.ImageField(verbose_name="фотография 3", blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=30, verbose_name='цена')
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, verbose_name='доставка', null=True)
    limited = models.BooleanField(default=False, verbose_name="ограниченный или нет")
    is_active = models.BooleanField(default=True, null=True, verbose_name='активность')
    sold_quantity = models.PositiveIntegerField(default=0, null=True, verbose_name='сколько продаж')

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', default=User)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='товар', null=True, related_name='review')
    text = models.TextField(verbose_name='текст отзыва')
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'

    def __str__(self):
        return self.text


class Payment(models.Model):
    payment_type = models.CharField(max_length=100, verbose_name='вид оплаты')

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'виды оплаты'

    def __str__(self):
        return self.payment_type


