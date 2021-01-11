from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.modelfields import PhoneNumberField


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type" : "text",
        "placeholder":"Username"
    }))
    
    email = forms.CharField(widget=forms.TextInput(attrs={
        "type" : "email",
        "placeholder":"Email"
    }))
    
    password1 = forms.CharField(widget=forms.TextInput(attrs={
        "type" : "password",
        "placeholder":"Enter Password"
    }))
    
    password2 = forms.CharField(widget=forms.TextInput(attrs={
        "type" : "password",
        "placeholder":"Confirm Password"
    }))

    class Meta:
        model = User
        fields = ['username', 'email','password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Username"
    }))
    
    email = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Email"
    }))
    
    class Meta:
        model = User
        fields = ['username','email']
class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"First name"
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Last name"
    }))
    bio = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"bio"
    }))
    telephone = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder":"Phone no"
    }))

    class Meta:
        model = Profile
        fields = ['bio','first_name', 'last_name', 'profile_picture','telephone', 'country' ,'career_description','skills']
        widgets = {'country': CountrySelectWidget(), 'class' : "country" }