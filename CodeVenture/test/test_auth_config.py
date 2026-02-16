"""Tests for CodeVenture.auth_config (OAuth redirect URI building)."""
import pytest

from CodeVenture.auth_config import (
    GOOGLE_OAUTH_CALLBACK_PATH,
    build_google_redirect_uri,
)


def test_callback_path_ends_with_slash():
    assert GOOGLE_OAUTH_CALLBACK_PATH.endswith("/")
    assert "callback" in GOOGLE_OAUTH_CALLBACK_PATH


def test_build_google_redirect_uri_production():
    assert build_google_redirect_uri("https", "codeventure-ez4m.onrender.com") == (
        "https://codeventure-ez4m.onrender.com/accounts/google/login/callback/"
    )


def test_build_google_redirect_uri_local():
    assert build_google_redirect_uri("http", "localhost:8000") == (
        "http://localhost:8000/accounts/google/login/callback/"
    )


def test_build_google_redirect_uri_uses_constant():
    uri = build_google_redirect_uri("https", "example.com")
    assert uri.endswith(GOOGLE_OAUTH_CALLBACK_PATH)


def test_build_google_redirect_uri_strips_trailing_slash_from_netloc():
    assert build_google_redirect_uri("https", "example.com/") == (
        "https://example.com/accounts/google/login/callback/"
    )
