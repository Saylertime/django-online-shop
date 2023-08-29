from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app_users.models import Profile
from django.core.exceptions import ValidationError


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ExtendedRegisterForm(UserCreationForm):
    middle_name = forms.CharField(required=False)
    phone = forms.IntegerField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'middle_name',
                  'last_name', 'password1', 'password2',
                  'email', 'phone', 'avatar')

def first_name(name):
    if name and 'es' in name:
        raise forms.ValidationError('В имени есть "es"')

class ProfileUpdate(forms.ModelForm):
    first_name = forms.CharField(max_length=30, validators=[first_name])
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    new_password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('phone', 'avatar')

    def clean(self):
        cleaned_data = super().clean()
        first = cleaned_data.get("new_password1")
        second = cleaned_data.get("new_password2")
        image = cleaned_data.get('avatar')
        if first != second:
            raise ValidationError("Пароли не совпадают")
        elif image:
            if image.size > 2048 * 2048:
                raise forms.ValidationError("Максимальный размер аватара — 2 Мб")
        return cleaned_data


