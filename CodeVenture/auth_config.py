"""
Central configuration for authentication and OAuth.

Single source of truth for paths and URLs used by django-allauth and
Google OAuth. Use these constants when documenting or validating
redirect URIs (e.g. in Google Cloud Console) to avoid redirect_uri_mismatch.
"""
# django-allauth Google provider callback path. Full redirect URI = scheme + netloc + this path.
GOOGLE_OAUTH_CALLBACK_PATH = "/accounts/google/login/callback/"


def build_google_redirect_uri(scheme: str, netloc: str) -> str:
    """Build the exact redirect URI Google OAuth will use for a given origin.

    This is the URI that must be listed in Google Cloud Console under
    "Authorised redirect URIs". django-allauth sends this URL after the user
    signs in at Google.

    Args:
        scheme: 'https' or 'http'
        netloc: e.g. 'codeventure-ez4m.onrender.com' or 'localhost:8000'

    Returns:
        Full redirect URI, e.g. https://codeventure-ez4m.onrender.com/accounts/google/login/callback/
    """
    return f"{scheme}://{netloc.rstrip('/')}{GOOGLE_OAUTH_CALLBACK_PATH}"
