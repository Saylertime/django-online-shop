from django.urls import path
from app_goods.views import index, CategoryDetailView, \
                             SubCategoryDetailView, ItemListView, ItemDetailView, about
from app_goods.api import ItemList

urlpatterns = [
    path('', index, name='index'),
    path('catalog', ItemListView.as_view(), name='catalog'),
    path('about', about, name='about'),
    path('catalog/<int:pk>', ItemDetailView.as_view(), name='item-detail'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('category/subcategory/<int:pk>', SubCategoryDetailView.as_view(), name='subcategory-detail'),
    path('api/items', ItemList.as_view(), name='item_list'),
]