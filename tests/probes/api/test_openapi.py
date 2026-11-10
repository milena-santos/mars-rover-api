"""OpenAPI schema and docs availability."""

from __future__ import annotations

from django.test import SimpleTestCase


class OpenApiDocsTests(SimpleTestCase):
    def test_schema_endpoint_is_available(self) -> None:
        response = self.client.get("/api/schema/")

        assert response.status_code == 200
        assert b"openapi" in response.content

    def test_swagger_ui_is_available(self) -> None:
        response = self.client.get("/api/docs/")

        assert response.status_code == 200
