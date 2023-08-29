from django.db.models import Min, Count, Max, Q, F
from django.shortcuts import render, redirect
from app_goods.models import Item, Category, SubCategory, Review
from app_cart.models import CartItem
from django.views.generic import DetailView, ListView
from app_goods.forms import ReviewForm
from app_cart.forms import AddToCartForm
from app_users.models import Profile



def header_data(request):
    all_cat = Category.objects.filter(is_active=True).order_by('sort_index').prefetch_related('subcat').all()
    profile = ""
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        cartitems_count = CartItem.objects.filter(user=request.user).count()
        cartitem_sum = sum(item.item_sum() for item in CartItem.objects.filter(user=request.user))
    else:
        cartitems_count = CartItem.objects.filter(session_key=request.COOKIES.get('session_key')).count()
        cartitem_sum = sum(item.item_sum() for item in CartItem.objects.filter(session_key=request.COOKIES.get('session_key')))
    title = request.GET.get('title')
    query = ''
    if title:
        query = Item.objects.filter(Q(title__icontains=title) | Q(description__icontains=title))
    return {'all_cat': all_cat,
            'query': query,
            'cartitems_count': cartitems_count,
            'cartitem_sum': cartitem_sum,
            'profile': profile}


def add_cartitems(request, amount, item, item_pk):
    add_form = AddToCartForm(request.POST)
    if add_form.is_valid():
        cart_item = CartItem.objects.filter(item=item)
        if not request.session.session_key:
            request.session.create()
        old_session_key = request.COOKIES.get('session_key')
        if not cart_item:
            CartItem.objects.create(
                user=request.user if request.user.is_authenticated else None,
                session_key=old_session_key,
                item=item,
                quantity=amount,
                active=True
            )
            response = redirect(request.path)
            response.set_cookie('session_key', old_session_key)
            return response
        else:
            CartItem.objects.filter(item=item, session_key=old_session_key).update(quantity=F('quantity') + amount)
            response = redirect(request.path)
            response.set_cookie('session_key', old_session_key)
            return response


class ItemListView(ListView):
    queryset = Item.objects.prefetch_related('review').all()
    template_name = 'app_goods/catalog.html'
    context_object_name = 'items'
    paginate_by = 8

    def get(self, request, *args, **kwargs):
        page_num = request.GET.get('page', 1)
        page_num = int(page_num)
        if page_num > 1:
            self.page_num = page_num
        else:
            self.page_num = 1
        self.sort_by = request.GET.get('sort_by')
        return super().get(request, *args, **kwargs)

    def post(self, request):
        item_pk = request.POST.get('item_pk')
        item = Item.objects.get(pk=item_pk)

        add_cartitems(request, amount=1, item_pk=item_pk, item=item)
        return redirect(self.request.path)

    def get_queryset(self):
        queryset = super().get_queryset()
        active = self.request.GET.get('active')
        free_delivery = self.request.GET.get('free_delivery')
        price = self.request.GET.get('price')
        title = self.request.GET.get('title')

        if active:
            queryset = queryset.filter(is_active=True)
        if free_delivery:
            queryset = queryset.filter(delivery=2)
        if price:
            queryset = queryset.filter(price__range=price.split(';'))
        if title:
            queryset = queryset.filter(Q(title__icontains=title) | Q(description__icontains=title))

        if self.sort_by == 'popularity':
            queryset = queryset.order_by('-sold_quantity')
        elif self.sort_by == 'unpopularity':
            queryset = queryset.order_by('sold_quantity')
        elif self.sort_by == 'price':
            queryset = queryset.order_by('price')
        elif self.sort_by == 'unprice':
            queryset = queryset.order_by('-price')
        elif self.sort_by == 'reviews':
            queryset = queryset.annotate(review_count=Count('review')).order_by('-review_count')
        elif self.sort_by == 'unreviews':
            queryset = queryset.annotate(review_count=Count('review')).order_by('review_count')
        elif self.sort_by == 'newness':
            queryset = queryset.order_by('-id')
        elif self.sort_by == 'unnewness':
            queryset = queryset.order_by('id')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active'] = self.request.GET.get('active')
        context['free_delivery'] = self.request.GET.get('free_delivery')
        context['price'] = self.request.GET.get('price')
        context['title'] = self.request.GET.get('title')
        context['min_price'] = Item.objects.all().aggregate(Min('price'))['price__min']
        context['max_price'] = Item.objects.all().aggregate(Max('price'))['price__max']
        context['add_form'] = AddToCartForm()
        context['page_num'] = self.page_num
        return context


class ItemDetailView(DetailView):
    queryset = Item.objects.prefetch_related('review').all()
    template_name = 'app_goods/product.html'
    context_object_name = 'item'

    def get(self, request, *args, **kwargs):
        self.add_form = AddToCartForm()
        if request.user.is_authenticated:
            self.form = ReviewForm(initial={'name': f'{request.user.first_name} {request.user.last_name}',
                                            'email': request.user.email})
        else:
            self.form = ReviewForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        form = ReviewForm(request.POST)
        add_form = AddToCartForm(request.POST)
        if form.is_valid():
            user = request.user
            text = form.cleaned_data.get('text')
            item = self.get_object()
            Review.objects.create(
                author=user,
                item=item,
                text=text,
            )
            return redirect(self.request.path)

        elif add_form.is_valid():
            amount = request.POST.get('amount')
            item = Item.objects.get(pk=kwargs['pk'])
            add_cartitems(request, amount=amount, item=item, item_pk=item.pk)
        return redirect(self.request.path)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        context['add_form'] = self.add_form
        return context


class CategoryDetailView(DetailView):
    context_object_name = 'category'
    template_name = 'app_goods/category_detail.html'
    queryset = Category.objects.prefetch_related('items', 'subcat')


class SubCategoryDetailView(DetailView):
    queryset = SubCategory.objects.prefetch_related('category','sub_items')
    context_object_name = 'subcategory'
    template_name = 'app_goods/subcategories.html'


def index(request):
    if request.method == 'GET':
        active_items = Item.objects.filter(is_active=True)
        all_cat = Category.objects.filter(is_active=True).order_by('sort_index')
        sub_category = SubCategory.objects.all()
        best_cats = Category.objects.filter(is_active=True, items__in=active_items).annotate(
            min_price=Min('items__price')).order_by('sort_index')[:3]
        limited_items = Item.objects.filter(limited=True)[:16]
        most_popular = Item.objects.filter(is_active=True).order_by('sold_quantity').all()[::-1]
        return render(request, 'app_goods/index.html', context={'all_cat': all_cat,
                                                                'best_cats': best_cats,
                                                                'sub_category': sub_category,
                                                                'most_popular': most_popular,
                                                                'limited_items': limited_items})
    else:
        item_pk = request.POST.get('item_pk')
        item = Item.objects.get(pk=item_pk)
        add_cartitems(request, amount=1, item=item, item_pk=item_pk)
        return redirect(request.path)


def about(request):
    return render(request, 'app_goods/about.html')
