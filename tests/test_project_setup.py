"""Smoke tests for the Django project foundation."""

from __future__ import annotations

from django.core.management import call_command
from django.test import SimpleTestCase


class ProjectSetupTests(SimpleTestCase):
    def test_django_system_checks_pass(self) -> None:
        call_command("check")
