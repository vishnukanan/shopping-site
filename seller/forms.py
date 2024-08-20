from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm


class SellerRegistrationForm(forms.ModelForm):
    password=forms.CharField(label='password',widget=forms.PasswordInput)
    cpassword=forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    email=forms.EmailField(required=True)
    phone=forms.IntegerField(label='phone',widget=forms.TextInput(attrs={'placeholder':'enter your phone number'}))
    class Meta:
        #class meta refers to data associated when a forms structure this include informations such as model and field
        model=User
        fields=['username','first_name','last_name','email','phone','password','cpassword']
    
