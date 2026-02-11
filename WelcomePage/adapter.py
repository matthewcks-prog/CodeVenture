"""
Custom social account adapter for handling OAuth authentication.
Implements proper error handling and user profile management.
"""
import logging
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger(__name__)


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter for social authentication with enhanced error handling.
    Follows SOLID principles with single responsibility for OAuth user management.
    """
    
    def save_user(self, request, sociallogin, form=None):
        """
        Save social login user with proper profile data extraction.
        
        Args:
            request: HTTP request object
            sociallogin: Social login instance from provider
            form: Optional form data
            
        Returns:
            User: The saved user instance
        """
        try:
            user = super().save_user(request, sociallogin, form)
            
            # Extract additional profile data from OAuth provider
            extra_data = sociallogin.account.extra_data
            user.first_name = extra_data.get('given_name', '')
            user.last_name = extra_data.get('family_name', '')
            
            # Ensure email is set (critical for user identification)
            if not user.email and extra_data.get('email'):
                user.email = extra_data.get('email')
            
            user.save()
            logger.info(f"Successfully created/updated social user: {user.username}")
            return user
            
        except Exception as e:
            logger.error(f"Error saving social login user: {str(e)}", exc_info=True)
            raise
    
    def pre_social_login(self, request, sociallogin):
        """
        Handle existing users who sign in via OAuth.
        Links OAuth account to existing user if email matches.
        """
        try:
            # If user is already logged in, link the account
            if request.user.is_authenticated:
                return
            
            # Check if user with this email already exists
            if sociallogin.is_existing:
                return
            
            # Try to link to existing user by email
            from django.contrib.auth.models import User
            try:
                email = sociallogin.account.extra_data.get('email', '').lower()
                if email:
                    existing_user = User.objects.get(email__iexact=email)
                    sociallogin.connect(request, existing_user)
                    logger.info(f"Connected OAuth account to existing user: {existing_user.username}")
            except User.DoesNotExist:
                pass
            except User.MultipleObjectsReturned:
                logger.warning(f"Multiple users found with email: {email}")
                
        except Exception as e:
            logger.error(f"Error in pre_social_login: {str(e)}", exc_info=True)
    
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Handle OAuth authentication errors gracefully.
        """
        logger.error(
            f"OAuth authentication error for provider {provider_id}: "
            f"error={error}, exception={exception}",
            exc_info=True
        )
        messages.error(
            request,
            f"Authentication with {provider_id} failed. Please try again or use another login method."
        )
        return super().authentication_error(request, provider_id, error, exception, extra_context)
