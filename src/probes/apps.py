"""Django app configuration for probes."""

from django.apps import AppConfig


class ProbesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "probes"
    label = "probes"
    verbose_name = "Probes"
