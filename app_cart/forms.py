from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile
from django.core.exceptions import ValidationError
from .models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = {'id'}


class DeleteItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = {'id'}

class RegisterOrderForm(UserCreationForm):
    phone = forms.IntegerField(required=True)
    fio = forms.CharField()
    class Meta:
        model = User
        fields = ('password1', 'password2',
                  'email', 'phone')
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("Такой email есть")
        return cleaned_data



class OrderForm(forms.ModelForm):
    first_name = forms.CharField(max_length=155)
    middle_name = forms.CharField(max_length=155)
    last_name = forms.CharField(max_length=155)
    email = forms.EmailField()
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Phone number'}))

    class Meta:
        model = Profile
        fields = ('phone',)

    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get("new_password1")
        second = cleaned_data.get("new_password2")
        if first != second:
            raise ValidationError("Пароли не совпадают")
        return cleaned_data


class DeliveryForm(forms.Form):
    choice = forms.ChoiceField(choices=[('regular', 'Обычная доставка'),
                                        ('express', 'Экспресс доставка')],
                               widget=forms.RadioSelect)
    city = forms.CharField()
    address = forms.CharField()


class PaymentForm(forms.Form):
    choice = forms.ChoiceField(choices=[('online', 'Онлайн картой'),
                                        ('other', 'Онлайн со случайного счета')],
                               widget=forms.RadioSelect)


class BankCardForm(forms.Form):
    card_number = forms.IntegerField(max_value=99999999, widget=forms.NumberInput(attrs={'class': 'form-input Payment-bill', 'id':"numero1"}))






