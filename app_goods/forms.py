from django import forms
from .models import Review

class ReviewForm(forms.Form):
    name = forms.CharField(max_length=155)
    email = forms.EmailField()
    text = forms.CharField(max_length=1111, widget=forms.Textarea(attrs={'rows': 5, 'cols': 80}))
