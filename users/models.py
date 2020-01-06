# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


def uniq_filename(hasker_user, file):
    prefix = hasker_user.username
    orig_name, ext = os.path.splitext(file)
    filename = "%s_%s%s" % (prefix, orig_name, ext)
    return os.path.join("avatars", filename)


class HaskerUser(AbstractUser):
    email = models.EmailField("E-mail", unique=True, blank=False)
    avatar = models.ImageField(upload_to=uniq_filename,
                               null=True,
                               blank=True)

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return settings.DEFAULT_AVATAR

    def __unicode__(self):
        return self.username
