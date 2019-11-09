# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView

from .models import HaskerUser
from .forms import SignUpForm, SettingsForm


class SignUpView(TemplateView):
    template_name = "signup.html"
    form = SignUpForm

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        form = self.form()
        context["form"] = form
        return context

    def post(self, request):
        form = self.form(request.POST, request.FILES)
        if form.is_valid():
            # @TODO: Resize image, transaction
            user = form.save()
            hasker_user = HaskerUser(user=user)
            hasker_user.avatar = form.cleaned_data.get("avatar")
            if not hasker_user.avatar:
                hasker_user.avatar = "avatars/default.png"
            hasker_user.save()
            password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=password)
            login(request, user)
            return redirect(reverse("index"))
        context = {
            "form": form
        }
        return render(request, self.template_name, context)


class SettingsView(LoginRequiredMixin, TemplateView):
    login_url = "login"
    redirect_field_name = "next"
    template_name = "settings.html"
    form = SettingsForm

    def get_context_data(self, **kwargs):
        context = super(TemplateView, self).get_context_data(**kwargs)
        user = self.request.user
        avatar = user.hasker_user.avatar
        initial_values = {"avatar": avatar}
        form = self.form(instance=user, initial=initial_values)
        context["form"] = form
        return context

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            profile = user.hasker_user
            clear_avatar = request.POST.get("avatar-clear", False)
            if request.FILES:
                profile.avatar = form.cleaned_data.get("avatar")
                profile.save()
            elif clear_avatar:
                profile.avatar = "avatars/default.png"
                profile.save()
            return redirect(reverse("settings"))
        avatar = request.user.hasker_user.avatar
        context = {
            "form": form,
            "avatar": avatar
        }
        return render(request, self.template_name, context)
