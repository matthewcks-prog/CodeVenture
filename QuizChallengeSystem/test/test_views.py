import json

import pytest
from django.urls import reverse

from CodeVenture.services.judge0_service import Judge0Service
from QuizChallengeSystem.models import Challenge


@pytest.mark.django_db
def test_challenge_view_renders_for_existing_challenge(client):
    challenge = Challenge.objects.create(
        name="Sample Challenge",
        description="Do something interesting.",
        hints="Some hints",
        solution_code="print('solution')",
        sample_output="42",
    )

    response = client.get(reverse("challenge", args=[challenge.id]))

    assert response.status_code == 200
    assert "challenge.html" in [template.name for template in response.templates]
    assert challenge.name.encode() in response.content


@pytest.mark.django_db
def test_challenge_run_code_success_response_shape(client, monkeypatch):
    challenge = Challenge.objects.create(
        name="Echo",
        description="Echo input",
        hints="",
        solution_code="print(input())",
        std_in="hello",
        expected_output="hello",
        sample_output="hello",
    )

    def fake_run_code(self, source_code, language_id=71, stdin=None, expected_output=None, timeout=10):
        return {
            "status_id": Judge0Service.SUCCESS,
            "success": True,
            "stdout": "hello",
            "description": "Accepted",
            "expected_output": "hello",
        }

    monkeypatch.setattr(Judge0Service, "run_code", fake_run_code)

    payload = {"code": "print(input())", "challenge_id": challenge.id}

    response = client.post(
        reverse("challenge_run_code"),
        data=json.dumps(payload),
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.json()

    assert data["result"] is True
    assert data["stdout"] == "hello"
    assert data["expected_output"] == "hello"
    assert data["status_id"] == Judge0Service.SUCCESS

