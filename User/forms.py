from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Enter your email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Enter your password'
    }))

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Last Name'
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Phone Number'
    }))

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control neural-input'
            self.fields[field].widget.attrs['placeholder'] = field.title()

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'class': 'form-control neural-input',
        'placeholder': 'Enter OTP'
    })) 