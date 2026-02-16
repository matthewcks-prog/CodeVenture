import json

import pytest
from django.urls import reverse

from CodeVenture.services.judge0_service import Judge0Service


@pytest.mark.django_db
def test_playground_view_renders(client):
    response = client.get(reverse("playground"))

    assert response.status_code == 200
    assert "playground.html" in [template.name for template in response.templates]


@pytest.mark.django_db
def test_run_code_returns_stdout_from_service(client, monkeypatch):
    def fake_run_code(self, source_code, language_id=71, stdin=None, expected_output=None, timeout=10):
        return {"stdout": "Hello from Judge0", "success": True}

    monkeypatch.setattr(Judge0Service, "run_code", fake_run_code)

    payload = {"code": "print('Hello from Judge0')"}

    response = client.post(
        reverse("run_code"),
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.json()
    assert data["result"] == "Hello from Judge0"

