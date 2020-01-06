# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url
from django.contrib.auth import views as auth_views

from users import views as users_views

urlpatterns = [
    url(r"^signup/$", users_views.SignUpView.as_view(), name="signup"),
    url(r"^settings/$",
        users_views.SettingsView.as_view(), name="settings"),
    url(r"^login/$", users_views.LogInView.as_view(), name="login"),
    url(r"^logout/$", auth_views.logout,
        {"next_page": "login"},
        name="logout"),
]
