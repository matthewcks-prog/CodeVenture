"""
Custom template context processors for CodeVenture.

These inject variables into every template context so templates
can conditionally render features based on runtime configuration.
"""
from django.conf import settings


def google_oauth(request):
    """Expose whether Google OAuth is fully configured.

    Templates use ``{{ google_oauth_configured }}`` to conditionally
    show / hide the "Sign in with Google" button, preventing users
    from hitting an allauth endpoint that would 500 when credentials
    are absent.
    """
    return {
        'google_oauth_configured': getattr(
            settings, 'GOOGLE_OAUTH_CONFIGURED', False
        ),
    }
