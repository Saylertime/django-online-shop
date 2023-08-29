from app_goods.serializers import ItemSerializer
from app_goods.models import Item
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 1


class ItemList(ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = Pagination

    def get_queryset(self):
        queryset = Item.objects.all()
        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title=title)
        return queryset
