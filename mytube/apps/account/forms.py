from django.forms import forms, models, fields
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(models.ModelForm):
    class Meta:
        fields = ['username', 'password']


class RegisterForm(models.ModelForm):
    pass
