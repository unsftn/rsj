# -*- coding: utf-8 -*-
from django.apps import AppConfig


class OdredniceConfig(AppConfig):
    name = 'odrednice'
    verbose_name = 'одреднице'

    def ready(self):
        import odrednice.signals  # noqa
