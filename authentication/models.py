from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db.models.signals import *
from django.db import models


class UserProfile(models.Model):
    profile = models.OneToOneField(User, related_name='profile', null=True)
    author = models.ForeignKey('auth.User', null=True)

    def __unicode__(self):  # __str__
        return unicode_literals(self.profile)



