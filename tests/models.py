# flake8: noqa
"""
isort:skip_file
"""
from __future__ import absolute_import, division, print_function

from django.conf import settings

if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test.db'
            }
        },
        INSTALLED_APPS=[
            'tests',
        ],

        DEBUG=True,
    )

from django.db import models


class Setting(models.Model):
    key = models.CharField(max_length=32, unique=True)
    value = models.CharField(max_length=32, default='')
