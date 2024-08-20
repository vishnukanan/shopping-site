from django import forms
from django.forms import ModelForm
from .models import *
class LoginForm(forms.Form):
    class Meta:
        model=userregister
        field=['password','email']