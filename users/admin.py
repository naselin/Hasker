# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import HaskerUser


@admin.register(HaskerUser)
class HaskerUserAdmin(admin.ModelAdmin):
    pass
