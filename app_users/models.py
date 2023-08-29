from django.contrib.auth.models import User
from django.db import models
from app_goods.models import Item


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="пользователь")
    middle_name = models.CharField(max_length=155, verbose_name='отчество')
    phone = models.BigIntegerField(verbose_name='телефон')
    viewed_items = models.ManyToManyField(Item, verbose_name='просмотренные товары', default=None, blank=True)
    avatar = models.ImageField(upload_to='files/', verbose_name='аватар')

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
        return self.user.username