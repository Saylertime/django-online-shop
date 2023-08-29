from django.urls import path
from .views import CartView, order, delivery, payment, \
    confirmation, card_online, \
    card_someone, progress_page, \
    second_page, repayment, result2, add_amount, reduce_amount, delete_cartitem

urlpatterns = [
    path('cart', CartView.as_view(), name='cart'),
    path('order', order, name='order'),
    path('delivery', delivery, name='delivery'),
    path('amount/<int:item_pk>', add_amount, name='add_amount'),
    path('reduce/<int:item_pk>', reduce_amount, name='reduce_amount'),
    path('delete/<int:item_pk>', delete_cartitem, name='delete_cartitem'),
    path('payment', payment, name='payment'),
    path('confirmation', confirmation, name='confirmation'),
    path('card_online', card_online, name='card_online'),
    path('card_someone', card_someone, name='card_someone'),
    path('repayment', repayment, name='repayment'),
    path('progress', progress_page, name='progress'),
    path('result', second_page, name='result'),
    path('result2/<str:order_id>/', result2, name='result2'),
]