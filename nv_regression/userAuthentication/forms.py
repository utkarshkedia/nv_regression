from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User #saves in the database
        fields = ["username","email","password1","password2"] #order in which we want our fields to appear