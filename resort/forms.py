from django import forms
from django.contrib.auth.models import User
from django.core.validators import EmailValidator

ACCOUNT_TYPES = (
    ('guest', 'Guest'),
    ('stakeholder', 'Resort Stakeholder')
)

class RegistrationForm(forms.Form):
    email = forms.EmailField(
        validators=[EmailValidator()],
        widget=forms.EmailInput(attrs={
            'class': 'form-control neural-input',
            'placeholder': 'Enter your email',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control neural-input',
            'placeholder': 'Create password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control neural-input',
            'placeholder': 'Confirm password'
        })
    )
    account_type = forms.ChoiceField(
        choices=[
            ('guest', 'Guest'),
            ('stakeholder', 'Resort Stakeholder')
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'neural-radio'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control neural-input-field',
            'placeholder': 'Enter your username',
            'id': 'id_username',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control neural-input-field',
            'placeholder': 'Enter your password',
            'id': 'id_password'
        })
    ) 