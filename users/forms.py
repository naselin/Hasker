
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import ValidationError


MAX_AVATAR_SIZE = 1
HaskerUser = get_user_model()


def check_avatar_size(form):
    avatar = form.cleaned_data.get("avatar", False)
    if avatar:
        if avatar._size > MAX_AVATAR_SIZE * 1024 * 1024:
            err_message = "Avatar is too large (> %s MB)" % MAX_AVATAR_SIZE
            raise ValidationError(err_message)
        return avatar


class LogInForm(AuthenticationForm):
    class Meta:
        model = HaskerUser
        fields = ("username", "password")

    def __init__(self, request=None, *args, **kwargs):
        super(LogInForm, self).__init__(request, *args, **kwargs)


class SignUpForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    email = forms.EmailField(label=("Email address"), required=True,
                             help_text=("Required. Enter valid address."))

    class Meta:
        model = HaskerUser
        fields = ("username", "password1", "password2", "email", "avatar")

    def clean_avatar(self):
        return check_avatar_size(self)


class SettingsForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"readonly": "readonly"})
    )
    avatar = forms.ImageField(required=False)

    class Meta:
        model = HaskerUser
        fields = ("username", "email", "avatar")

    def clean_avatar(self):
        return check_avatar_size(self)
