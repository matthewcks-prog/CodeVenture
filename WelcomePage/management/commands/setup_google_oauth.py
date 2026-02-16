"""
Ensure Google OAuth SocialApp record exists and is properly configured.

django-allauth requires a SocialApp database record even when using
settings-based configuration. This command ensures:
1. The SocialApp record exists for the Google provider
2. It's linked to the correct Site (SITE_ID)
3. Credentials match environment variables

Called automatically during build (build.sh) to prevent OAuth callback errors.
"""
import os
import logging

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create or update Google OAuth SocialApp record and link to Site"

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-if-missing-creds',
            action='store_true',
            help='Skip setup if credentials are not configured (useful for local dev)',
        )

    def handle(self, *args, **options):
        client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID', '').strip()
        client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET', '').strip()

        # Check if credentials are configured
        if not client_id or not client_secret:
            if options['skip_if_missing_creds']:
                self.stdout.write(
                    self.style.WARNING(
                        "Google OAuth credentials not configured. Skipping SocialApp setup."
                    )
                )
                return
            else:
                self.stdout.write(
                    self.style.WARNING(
                        "Google OAuth credentials not configured. "
                        "Set GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET "
                        "to enable Google OAuth."
                    )
                )
                # Still create the SocialApp record but without credentials
                # This prevents errors when credentials are added later
                client_id = ''
                client_secret = ''

        try:
            with transaction.atomic():
                self._ensure_socialapp(client_id, client_secret)
                self.stdout.write(
                    self.style.SUCCESS("Google OAuth SocialApp configured successfully")
                )
        except Exception as e:
            logger.error(f"Error setting up Google OAuth SocialApp: {str(e)}", exc_info=True)
            self.stdout.write(
                self.style.ERROR(f"Failed to setup Google OAuth SocialApp: {str(e)}")
            )
            raise

    def _ensure_socialapp(self, client_id: str, client_secret: str):
        """
        Ensure SocialApp exists and is properly configured.

        Args:
            client_id: Google OAuth client ID from environment
            client_secret: Google OAuth client secret from environment
        """
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site

        # Get or create the Site
        try:
            site = Site.objects.get(pk=settings.SITE_ID)
        except Site.DoesNotExist:
            raise Exception(
                f"Site with ID {settings.SITE_ID} does not exist. "
                "Run 'python manage.py setup_site' first."
            )

        # Get or create the SocialApp
        socialapp, created = SocialApp.objects.get_or_create(
            provider='google',
            defaults={
                'name': 'Google',
                'client_id': client_id,
                'secret': client_secret,
            }
        )

        # Update credentials if they've changed (important for production updates)
        if socialapp.client_id != client_id or socialapp.secret != client_secret:
            socialapp.client_id = client_id
            socialapp.secret = client_secret
            socialapp.save(update_fields=['client_id', 'secret'])
            self.stdout.write("  Updated SocialApp credentials")

        # Ensure SocialApp is linked to the Site
        if site not in socialapp.sites.all():
            socialapp.sites.add(site)
            self.stdout.write(f"  Linked SocialApp to Site: {site.domain}")
        else:
            self.stdout.write(f"  SocialApp already linked to Site: {site.domain}")

        if created:
            self.stdout.write(f"  Created SocialApp for provider: google")
        else:
            self.stdout.write(f"  SocialApp already exists for provider: google")

        # Validate configuration
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    "  Warning: SocialApp exists but credentials are empty. "
                    "Google OAuth will not work until credentials are configured."
                )
            )
        else:
            self.stdout.write("  SocialApp is fully configured with credentials")
