# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory
from django.shortcuts import reverse
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from .views import LogInView, SettingsView
from .forms import LogInForm


HaskerUser = get_user_model()


class ModelTestCase(TestCase):
    def test_create_user_ok(self):
        user = HaskerUser.objects.create_user(
            username="User",
            email="user@selin.com.ru",
            password="testuser"
        )
        self.assertEqual(user.username, "User")
        self.assertEqual(user.email, "user@selin.com.ru")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_nok(self):
        with self.assertRaises(ValueError):
            HaskerUser.objects.create_user(username="")
        with self.assertRaises(ValueError):
            HaskerUser.objects.create_user(username="", password="testuser")
        with self.assertRaises(IntegrityError):
            HaskerUser.objects.create_user(username="User")
            HaskerUser.objects.create_user(username="User")

    def test_create_superuser_ok(self):
        super_user = HaskerUser.objects.create_superuser(
            username="Superuser",
            email="superuser@selin.com.ru",
            password="testsuperuser")
        self.assertEqual(super_user.username, "Superuser")
        self.assertEqual(super_user.email, "superuser@selin.com.ru")
        self.assertTrue(super_user.is_active)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_superuser)

    def test_create_superuser_nok(self):
        with self.assertRaises(ValueError):
            HaskerUser.objects.create_superuser(
                username="superuser",
                email="superuser@selin.com.ru",
                password="testsuperuser",
                is_superuser=False)
        with self.assertRaises(ValueError):
            HaskerUser.objects.create_superuser(
                username="",
                email="superuser@selin.com.ru",
                password="testsuperuser",
                is_superuser=True)
        with self.assertRaises(ValueError):
            HaskerUser.objects.create_superuser(
                username="",
                email="superuser@selin.com.ru",
                password="testsuperuser",
                is_staff=False)


class ViewsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = HaskerUser.objects.create(
            username="User", email="user@selin.com.ru")

    def test_login_view_ok(self):
        request = self.factory.get(reverse("login"))
        request.user = AnonymousUser()
        response = LogInView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_nok_authorized_user(self):
        request = self.factory.get(reverse("login"))
        request.user = self.user
        with self.assertRaises(PermissionDenied):
            LogInView.as_view()(request)

    def test_settings_view_ok(self):
        request = self.factory.get(reverse("settings"))
        request.user = self.user
        response = SettingsView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object"], self.user)

    def test_settings_view_nok_anonymous_user(self):
        request = self.factory.get(reverse("settings"))
        request.user = AnonymousUser()
        response = SettingsView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/users/login/?next=/users/settings/")
        redir_response = self.client.get(response.url)
        self.assertEqual(redir_response.status_code, 200)
        self.assertEqual(type(redir_response.context["form"]), LogInForm)
