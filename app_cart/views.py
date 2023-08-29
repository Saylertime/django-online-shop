from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.shortcuts import render, redirect
from app_cart.models import CartItem, Order, ComplitedOrder
from django.views.generic import ListView
from .forms import AddToCartForm, DeleteItemForm
from app_cart.forms import OrderForm, RegisterOrderForm, DeliveryForm, PaymentForm, BankCardForm
from app_users.models import Profile
import random


def create_new_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_sum = sum(cart_item.item_sum() for cart_item in cart_items)
    order = Order.objects.filter(user=request.user).first()
    if order:
        order.total_sum = total_sum
        order.save()
        order.cartitems.clear()
        order.cartitems.add(*cart_items)
    else:
        for item in cart_items:
            item.session_key = ''
            item.save()
        new_order = Order(user=request.user, active=True, total_sum=total_sum)
        new_order.save()
        new_order.cartitems.add(*cart_items)


def order(request):
    register_form = RegisterOrderForm()
    if request.method == 'GET':
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            first_name = request.user.first_name
            middle_name = request.user.profile.middle_name
            last_name = request.user.last_name
            phone = request.user.profile.phone
            email = request.user.email
            form = OrderForm(initial={'first_name': first_name, 'middle_name': middle_name,
                                      'last_name': last_name,
                                      'email': email, 'phone': phone})
            return render(request, 'app_cart/order.html', context={'form': form,
                                                                   'profile': profile,
                                                                   'register_form': register_form})
        else:
            return render(request, 'app_cart/order.html', context={'register_form': register_form})

    elif request.method == 'POST':
        register_form = RegisterOrderForm(request.POST)
        form = OrderForm(request.POST)

        if form.is_valid():
            create_new_order(request)
            user = request.user

            User.objects.filter(pk=user.pk).update(first_name=form.cleaned_data['first_name'],
                                                   last_name=form.cleaned_data['last_name'],
                                                   email=form.cleaned_data['email'])
            Profile.objects.filter(pk=user.profile.pk).update(phone=form.cleaned_data['phone'],
                                                              middle_name=form.cleaned_data['middle_name'])


            # create_new_order(request)
            print('LOL')
            return redirect('delivery')

        if register_form.is_valid():
            old_session_key = request.COOKIES.get('session_key')
            email = register_form.cleaned_data.get('email')
            fio = register_form.cleaned_data.get('fio')
            try:
                first_name, middle_name, last_name = fio.split(" ")
            except:
                first_name, middle_name, last_name = fio
            user = register_form.save(commit=False)
            user.username = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            phone = register_form.cleaned_data.get('phone')
            Profile.objects.create(
                user=user,
                middle_name=middle_name,
                phone=phone,
            )
            login(request, user)

            old_cartitems = CartItem.objects.filter(session_key=old_session_key).all()
            new_cartitems = CartItem.objects.filter(session_key=request.session.session_key).all()

            for old_item in old_cartitems:
                new_item = new_cartitems.filter(item=old_item.item).first()
                if new_item:
                    new_item.quantity += old_item.quantity
                    new_item.user = request.user
                    # new_item.session_key = 'ppp'
                    new_item.save()
                    CartItem.objects.filter(session_key=old_session_key).delete()
                else:
                    old_item.session_key = request.session.session_key
                    old_item.user = request.user
                    old_item.save()

            create_new_order(request)

            return redirect('delivery')
        else:
            return redirect(request.path)



def delivery(request):
    if request.method == 'POST':
        form = DeliveryForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:
                order = Order.objects.filter(user=request.user).first()
            else:
                return redirect('login')
            # order = Order.objects.filter(user=request.user).first()
            total_sum = order.total_sum
            choice = form.cleaned_data['choice']
            city = form.cleaned_data['city']
            address = form.cleaned_data['address']
            free_or_not = True if choice == 'regular' else False

            if choice == 'regular':
                if total_sum < 2000:
                    total_sum += 200
            elif choice == 'express':
                total_sum += 500

            Order.objects.filter(user=request.user).update(total_sum=total_sum,
                                                           free_or_not=free_or_not,
                                                           city=city,
                                                           address=address,
                                                           )
            return redirect('payment')
    else:
        form = DeliveryForm()
        return render(request, 'app_cart/delivery.html', {'form': form})

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            payment_method = True if choice == 'online' else False
            Order.objects.filter(user=request.user).update(payment_method=payment_method)
        return redirect('confirmation')
    else:
        form = PaymentForm()
        return render(request, 'app_cart/payment.html', {'form': form})

def confirmation(request):
    user = request.user
    order = Order.objects.get(user=user)
    cartitems = order.cartitems.all()

    context = {
        'first_name': user.first_name,
        'middle_name': user.profile.middle_name,
        'last_name': user.last_name,
        'phone': user.profile.phone,
        'email': user.email,
        'delivery_type': 'Обычная' if order.free_or_not else 'Экспресс',
        'city': order.city,
        'address': order.address,
        'payment': 'Онлайн со своей карты' if order.payment_method else 'Онлайн с чужого счета',
        'cartitems': cartitems,
        'total_sum': order.total_sum
    }
    if request.method == 'GET':
        return render(request, 'app_cart/confirmation.html', context=context)
    else:
        if order.payment_method:
            return redirect('card_online')
        else:
            return redirect('card_someone')


def card_online(request):
    order = Order.objects.get(user=request.user)

    if request.method == 'POST':
        form_data = request.POST.copy()
        card_number = form_data.get('card_number')
        new_number = card_number.replace(" ", "")
        form_data['card_number'] = int(new_number)
        form = BankCardForm(form_data)

        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            order.card_number = card_number
            order.save()

        return redirect('progress')

    else:
        form = BankCardForm()
    return render(request, 'app_cart/bank_online.html', {'form': form})



def card_someone(request):
    order = Order.objects.get(user=request.user)
    if request.method == 'POST':
        form_data = request.POST.copy()
        card_number = form_data.get('card_number')
        new_number = card_number.replace(" ", "")
        form_data['card_number'] = int(new_number)
        form = BankCardForm(form_data)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            order.card_number = card_number
            order.save()
        return redirect('progress')

    else:
        form = BankCardForm()
    return render(request, 'app_cart/paymentsomeone.html', {'form': form})


def progress_page(request):
    response = render(request, 'app_cart/progressPayment.html')
    response['Refresh'] = '3;url=result'
    return response


def second_page(request):
    order = Order.objects.get(user=request.user)
    profile = Profile.objects.get(user=request.user)
    last_digit = (str(order.card_number)[-1])
    cartitems = CartItem.objects.filter(user=request.user)
    selected_error = ""
    if last_digit == '0':
        message = 'ОПЛАТА ПРОШЛА, ЖДИТЕ ДОСТАВКУ'
    else:
        message = 'ОПЛАТА НЕ ПРОШЛА'
        errors = [
                'Не хватило денег на карте',
                  'Вы заказали слишком мало, у нас так не принято',
                  'Вы не заказали дрель. Ваш заказ аннулирован',
               'У вас есть деньги, но нет желания. Заказ отменен'
               ]
        selected_error = random.choice(errors)
    complete_order(request, selected_error)
    order.delete()
    cartitems.delete()

    return render(request, 'app_cart/result.html', context={'message': message,
                                                            'error': selected_error,
                                                            'profile': profile})


class CartView(ListView):
    context_object_name = 'cartitems'
    template_name = 'app_cart/cart.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return CartItem.objects.filter(user=self.request.user).order_by('created_at')
        else:
            return CartItem.objects.filter(session_key=self.request.COOKIES.get('session_key')).all().order_by('created_at')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddToCartForm
        context['form_delete'] = DeleteItemForm
        context['session_key'] = self.request.COOKIES.get('session_key')
        if self.request.user.is_authenticated:
            context['total_sum'] = CartItem.objects.filter(user=self.request.user).annotate(
                total_price=Sum('item__price') * F('quantity')
            ).aggregate(Sum('total_price'))['total_price__sum']
        else:
            context['total_sum'] = CartItem.objects.filter(session_key=self.request.COOKIES.get('session_key')).annotate(
                total_price=Sum('item__price') * F('quantity')
            ).aggregate(Sum('total_price'))['total_price__sum']
        return context

    def post(self, request, **kwargs):
        form = AddToCartForm(request.POST)
        if request.user.is_authenticated:
            self.queryset = CartItem.objects.filter(user=request.user).select_related(
                'item').all()
        else:
            self.queryset = CartItem.objects.filter(session_key=self.request.COOKIES.get('session_key')).select_related(
            'item').all()

        if form.is_valid():
            for i in range(len(self.queryset)):
                amount = request.POST.get(f'amount{i + 1}')
                item_pk = request.POST.get(f'item_pk{i + 1}')
                CartItem.objects.filter(pk=item_pk).update(quantity=amount)
                CartItem.objects.filter(quantity=0).delete()

        return redirect('order')


def add_amount(request, item_pk):
    cart_item = CartItem.objects.get(pk=item_pk)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def reduce_amount(request, item_pk):
    cart_item = CartItem.objects.get(pk=item_pk)
    try:
        cart_item.quantity -= 1
        cart_item.save()
    except:
        cart_item.quantity = 0
    CartItem.objects.filter(quantity=0).delete()
    return redirect('cart')


def delete_cartitem(request, item_pk):
    cart_item = CartItem.objects.get(pk=item_pk)
    cart_item.delete()
    return redirect('cart')



# def delete_cartitem(request):
#     if request.user.is_authenticated:
#         cartitems = CartItem.objects.filter(user=request.user)
#     else:
#         cartitems = CartItem.objects.filter(session_key=request.COOKIES.get('session_key')).all()
#     form = AddToCartForm(request.POST)
#     if form.is_valid:
#         item_delete = request.POST.copy()
#         print(item_delete)
#         print(CartItem.objects.filter(user=request.user))
#     # CartItem.objects.filter(user=request.user, ).delete()
#     return redirect('cart')


def complete_order(request, error):
    old_order = Order.objects.get(user=request.user)
    cartitems = old_order.cartitems.all()
    items = [cart_item.item for cart_item in cartitems]
    total_sum = old_order.total_sum
    payment_method = old_order.payment_method
    last_digit = (str(old_order.card_number)[-1])
    payed = True if last_digit == "0" else False
    i_payed = True if payment_method else False
    delivery_method = False if old_order.free_or_not else True
    check_order = ComplitedOrder.objects.filter(user=request.user, order_id=old_order.id)
    if check_order.exists():
        pass
    else:
        new_order = ComplitedOrder(user=request.user,
                                   total_sum=total_sum,
                                   error=error,
                                   payed=payed,
                                   order_id=old_order.id,
                                   delivery_method=delivery_method,
                                   i_payed=i_payed
                                   )
        new_order.save()
        new_order.items.add(*items)


def repayment(request):
    order_id = request.GET.get('id')
    completed_order = ComplitedOrder.objects.get(user=request.user, order_id=order_id)
    if request.method == 'POST':
        form_data = request.POST.copy()
        card_number = form_data.get('card_number')
        new_number = card_number.replace(" ", "")
        form_data['card_number'] = int(new_number)
        form = BankCardForm(form_data)
        if form.is_valid():
            card_number = form.cleaned_data['card_number']
            last_digit = (str(card_number)[-1])
            if last_digit == '0':
                completed_order.payed=True
                completed_order.save()
        return redirect('result2', order_id=order_id)

    else:
        form = BankCardForm()
    return render(request, 'app_cart/bank_online.html', {'form': form})

def result2(request, order_id):
    completed_order = ComplitedOrder.objects.get(user=request.user, order_id=order_id)
    profile = Profile.objects.get(user=request.user)
    selected_error = ''
    if completed_order.payed == True:
        message = 'ОПЛАТА ПРОШЛА, ЖДИТЕ ДОСТАВКУ'
    else:
        message = 'ОПЛАТА НЕ ПРОШЛА'
        errors = [
            'Не хватило денег на карте',
            'Вы заказали слишком мало, у нас так не принято',
            'Вы не заказали дрель. Ваш заказ аннулирован',
            'У вас есть деньги, но нет желания. Заказ отменен'
        ]
        selected_error = random.choice(errors)

    return render(request, 'app_cart/result.html', context={'message': message,
                                                            'error': selected_error,
                                                            'profile': profile})