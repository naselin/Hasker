# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
from django.contrib.auth.models import User


def uniq_filename(hasker_user, file):
    orig_name, ext = os.path.splitext(file)
    prefix = hasker_user.user.username
    filename = "%s_%s%s" % (prefix, orig_name, ext)
    return os.path.join('avatars', filename)


class HaskerUser(models.Model):
    user = models.OneToOneField(
        User, related_name="hasker_user", on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=uniq_filename,
                               null=True,
                               blank=True)

    def __unicode__(self):
        return self.user.username
