
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LogInForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, request=None, *args, **kwargs):
        super(LogInForm, self).__init__(request, *args, **kwargs)


class SignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(label=("Email address"), required=True,
                             help_text=("Required. Enter valid address."))

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email", "avatar")


class SettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "avatar")
