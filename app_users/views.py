from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app_users.forms import ExtendedRegisterForm, ProfileUpdate, AuthForm
from app_cart.models import CartItem, ComplitedOrder
from app_users.models import Profile
from django.db import transaction
from django.urls import reverse
from django.views.generic import UpdateView, DetailView, ListView


@transaction.atomic
def register_view(request):
    if request.method == 'GET':
        form = ExtendedRegisterForm()
        return render(request, 'app_users/register.html', context={'form': form})
    else:
        form = ExtendedRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            middle_name = form.cleaned_data.get('middle_name')
            phone = form.cleaned_data.get('phone')
            avatar = form.cleaned_data.get('avatar')
            Profile.objects.create(
                user=user,
                middle_name=middle_name,
                phone=phone,
                avatar=avatar
            )
            user = form.save()
            user.save()
            return redirect('/')
        else:
            return HttpResponse('Форма не валидна')

def authview(request):
    old_session_key = request.COOKIES.get('session_key')
    if request.method == 'POST':
        form = AuthForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                old_cartitems = CartItem.objects.filter(session_key=old_session_key).all()
                new_cartitems = CartItem.objects.filter(user=request.user).all()

                for old_item in old_cartitems:
                    new_item = new_cartitems.filter(item=old_item.item).first()

                    if new_item:
                        new_item.quantity += old_item.quantity
                        new_item.user = request.user
                        new_item.save()
                        CartItem.objects.filter(session_key=old_session_key).delete()

                    else:
                        old_item.session_key = request.session.session_key
                        old_item.user = request.user
                        old_item.save()

                return redirect('index')

    form = AuthForm()
    return render(request, 'app_users/login.html', {'form': form, 'old': old_session_key})


class ProfileListView(ListView):
    model = Profile
    template_name = 'app_users/profile_list.html'
    context_object_name = 'profiles'


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'app_users/profile.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user
        return context

class ProfileUpdateView(UpdateView):
    model = Profile
    form_class = ProfileUpdate
    template_name = 'app_users/profile.html'

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'first_name': self.object.user.first_name,
            'last_name': self.object.user.last_name,
            'email': self.object.user.email
        })
        return initial

    def form_valid(self, form):
        user = User.objects.get(id=self.object.user_id)
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        new_password1 = form.cleaned_data.get('new_password1')
        new_password2 = form.cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 == new_password2:
            user.set_password(new_password1)

        user.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(
            'profile-detail',
            kwargs={'pk': self.object.pk}
        )


class AccountDetailView(DetailView):
    template_name = 'app_users/account.html'
    model = Profile
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_order'] = ComplitedOrder.objects.filter(user=self.request.user).last()
        return context


class HistoryListView(ListView):
    template_name = 'app_users/historyorder.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = ComplitedOrder.objects.filter(user=self.request.user)[::-1]
        return queryset


class HistoryDetailView(DetailView):
    template_name = 'app_users/account-order.html'
    context_object_name = 'order'
    model = ComplitedOrder