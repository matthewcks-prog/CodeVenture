"""
Custom social account adapter for handling OAuth authentication.
Implements proper error handling and user profile management.

This adapter provides robust error handling for OAuth flows, ensuring
that authentication errors are properly logged and user-friendly messages
are displayed. It follows SOLID principles with single responsibility
for OAuth user management.
"""
import logging
from typing import Optional
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social authentication with enhanced error handling.

    Provides comprehensive error handling for OAuth callbacks, user creation,
    and account linking. All errors are logged with full context for debugging.
    """

    def populate_username(self, request, user):
        """
        Auto-generate a unique username to bypass the signup form.

        Attempts to use:
        1. First part of email address
        2. First name + Last name
        3. Appends random numbers if conflict exists
        """
        from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
        from allauth.utils import generate_unique_username

        # Get variable from the user instance or sociallogin (if available in context)
        # Note: 'user' passed here is the instance being populated

        first_name = user.first_name or ""
        last_name = user.last_name or ""
        email = user.email or ""

        username = ""

        if email:
            username = email.split('@')[0]
        elif first_name and last_name:
            username = f"{first_name}{last_name}"
        elif first_name:
            username = first_name

        # Clean username (alphanumeric only recommended)
        import re
        username = re.sub(r'[^a-zA-Z0-9]', '', username)

        if not username:
            username = "user"

        # Helper to check uniqueness
        user.username = generate_unique_username([username, 'user'])

    def save_user(self, request, sociallogin, form=None):
        """
        Save social login user with proper profile data extraction.

        Validates OAuth data, extracts profile information, and ensures
        email is set. All errors are logged with full context.

        Args:
            request: HTTP request object
            sociallogin: Social login instance from provider
            form: Optional form data

        Returns:
            User: The saved user instance

        Raises:
            Exception: Re-raises exceptions after logging for proper error handling
        """
        try:
            # Validate sociallogin has required data
            if not sociallogin.account:
                raise ValueError("sociallogin.account is missing")

            if not sociallogin.account.extra_data:
                logger.warning("sociallogin.account.extra_data is empty")
                sociallogin.account.extra_data = {}

            # Ensure username is populated before saving (critical for bypassing signup form)
            if not sociallogin.user.username:
                self.populate_username(request, sociallogin.user)

            user = super().save_user(request, sociallogin, form)

            # Extract additional profile data from OAuth provider
            extra_data = sociallogin.account.extra_data
            if extra_data:
                user.first_name = extra_data.get('given_name', '') or user.first_name or ''
                user.last_name = extra_data.get('family_name', '') or user.last_name or ''

            # Ensure email is set (critical for user identification)
            if not user.email:
                email = extra_data.get('email', '') if extra_data else ''
                if email:
                    user.email = email
                else:
                    logger.warning(
                        f"User {user.username} created via OAuth but no email provided. "
                        "This may cause issues with account recovery."
                    )

            user.save()
            logger.info(
                f"Successfully created/updated social user: {user.username} "
                f"(email: {user.email}, provider: {sociallogin.account.provider})"
            )
            return user

        except Exception as e:
            logger.error(
                f"Error saving social login user: {str(e)}\n"
                f"Provider: {sociallogin.account.provider if sociallogin.account else 'unknown'}\n"
                f"Request path: {request.path}\n"
                f"User agent: {request.META.get('HTTP_USER_AGENT', 'unknown')}",
                exc_info=True
            )
            # Re-raise to let django-allauth handle the error flow
            raise

    def pre_social_login(self, request, sociallogin):
        """
        Handle existing users who sign in via OAuth.

        Links OAuth account to existing user if email matches. This allows
        users who previously signed up with email/password to use OAuth
        with the same account.

        Args:
            request: HTTP request object
            sociallogin: Social login instance from provider
        """
        try:
            # If user is already logged in, link the account
            if request.user.is_authenticated:
                logger.debug(f"User {request.user.username} already authenticated, linking account")
                return

            # Check if user with this email already exists
            if sociallogin.is_existing:
                logger.debug("Social login is for existing account")
                return

            # Validate we have account data
            if not sociallogin.account or not sociallogin.account.extra_data:
                logger.warning("Cannot link account: missing account or extra_data")
                return

            # Try to link to existing user by email
            from django.contrib.auth.models import User
            try:
                email = sociallogin.account.extra_data.get('email', '').strip().lower()
                if not email:
                    logger.debug("No email in OAuth data, skipping account linking")
                    return

                existing_user = User.objects.get(email__iexact=email)
                sociallogin.connect(request, existing_user)
                logger.info(
                    f"Connected OAuth account ({sociallogin.account.provider}) "
                    f"to existing user: {existing_user.username} (email: {email})"
                )
            except User.DoesNotExist:
                logger.debug(f"No existing user found with email: {email}")
            except User.MultipleObjectsReturned:
                logger.warning(
                    f"Multiple users found with email: {email}. "
                    "Cannot automatically link OAuth account."
                )

        except Exception as e:
            logger.error(
                f"Error in pre_social_login: {str(e)}\n"
                f"Provider: {sociallogin.account.provider if sociallogin.account else 'unknown'}\n"
                f"Request path: {request.path}",
                exc_info=True
            )
            # Don't raise - allow the login to proceed even if linking fails

    def get_login_redirect_url(self, request):
        """
        Determine where to redirect after a successful social login.

        Checks if the user has a selected role (Student/Teacher/Parent).
        If not, redirects to the role selection page.
        Otherwise, follows standard redirect logic (next param or default).
        """
        user = request.user

        # Check if we have a robust enough user object to check attributes
        if not user or not user.is_authenticated:
             return super().get_login_redirect_url(request)

        # Check for role attributes
        has_role = (
            hasattr(user, 'student') or
            hasattr(user, 'teacher') or
            hasattr(user, 'parent')
        )

        if not has_role:
            logger.info(f"User {user.username} logged in via social auth but has no role. Redirecting to selection.")
            return reverse('choose_user_type')

        # If they have a role, proceed as normal
        return super().get_login_redirect_url(request)

    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Handle OAuth authentication errors gracefully.

        This method is called when an OAuth authentication error occurs.
        It logs the error with full context and displays a user-friendly
        error message.

        Args:
            request: HTTP request object
            provider_id: OAuth provider identifier (e.g., 'google')
            error: Error message from the provider
            exception: Exception object if available
            extra_context: Additional context data

        Returns:
            HttpResponseRedirect: Redirect to login page with error message
        """
        # Log with comprehensive context
        error_details = {
            'provider': provider_id,
            'error': str(error) if error else 'Unknown error',
            'exception_type': type(exception).__name__ if exception else None,
            'exception_message': str(exception) if exception else None,
            'request_path': request.path,
            'request_method': request.method,
            'query_params': dict(request.GET),
        }

        logger.error(
            f"OAuth authentication error for provider {provider_id}:\n"
            f"  Error: {error_details['error']}\n"
            f"  Exception: {error_details['exception_type']}: {error_details['exception_message']}\n"
            f"  Path: {error_details['request_path']}\n"
            f"  Query params: {error_details['query_params']}",
            exc_info=exception is not None
        )

        # Display user-friendly error message
        messages.error(
            request,
            f"Authentication with {provider_id.title()} failed. "
            "Please try again or use another login method."
        )

        # Redirect to login page
        try:
            login_url = reverse('login')
            return HttpResponseRedirect(login_url)
        except Exception as redirect_error:
            logger.error(f"Failed to redirect after OAuth error: {str(redirect_error)}")
            # Fallback to default behavior
            return super().authentication_error(request, provider_id, error, exception, extra_context)
