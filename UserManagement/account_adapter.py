"""
Custom account adapter for post-login redirects.

Uses get_onboarding_redirect so users without a role (e.g. OAuth signups)
are sent directly to choose_user_type instead of home, avoiding an extra redirect.
"""
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

from .services import get_onboarding_redirect


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Adapter that redirects users to onboarding steps when needed.
    Single source of truth for post-login redirect (used by allauth).
    """

    def get_login_redirect_url(self, request):
        if request.user.is_authenticated:
            target = get_onboarding_redirect(request.user)
            if target:
                return reverse(target)
        return super().get_login_redirect_url(request)
