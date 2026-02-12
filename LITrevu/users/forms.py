from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class CustomUserCreationForm:
    pass

class signUp(forms.Form):
    username = forms.CharField(max_length=63)
    password = forms.CharField(max_length=63)