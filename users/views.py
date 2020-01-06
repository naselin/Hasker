# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model

from .forms import LogInForm, SignUpForm, SettingsForm


HaskerUser = get_user_model()


class LogInView(LoginView):
    template_name = "login.html"
    authentication_form = LogInForm
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if self.request.user != AnonymousUser():
            raise PermissionDenied()
        return super(LogInView, self).get(*args, **kwargs)


class SignUpView(CreateView):
    model = HaskerUser
    template_name = "signup.html"
    form_class = SignUpForm

    def form_valid(self, form):
        # @TODO: Resize image?
        user = form.save()
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(reverse("index"))


class SettingsView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    redirect_field_name = "next"
    model = HaskerUser
    template_name = "settings.html"
    form_class = SettingsForm

    def get_object(self):
        return get_object_or_404(HaskerUser, pk=self.request.user.id)

    def form_valid(self, form):
        form.save()
        return redirect(reverse("settings"))
