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
        Ensure the Google SocialApp exists in a canonical, de-duplicated form.

        This method is intentionally defensive to avoid production 500s caused
        by misconfigured or duplicate SocialApp records (which surface as
        django.core.exceptions.MultipleObjectsReturned inside django-allauth).

        Invariants enforced for the current SITE_ID:
        - Exactly one SocialApp is linked to the Site for provider='google'
        - That SocialApp has credentials matching the environment variables
        - Any duplicate records linked to the same Site are de-duplicated

        Args:
            client_id: Google OAuth client ID from environment
            client_secret: Google OAuth client secret from environment
        """
        from allauth.socialaccount.models import SocialApp
        from django.contrib.sites.models import Site

        # ------------------------------------------------------------------
        # Resolve Site for current environment
        # ------------------------------------------------------------------
        try:
            site = Site.objects.get(pk=settings.SITE_ID)
        except Site.DoesNotExist as exc:
            raise Exception(
                f"Site with ID {settings.SITE_ID} does not exist. "
                "Run 'python manage.py setup_site' first."
            ) from exc

        # ------------------------------------------------------------------
        # Find or create canonical SocialApp for this Site
        # ------------------------------------------------------------------
        qs = (
            SocialApp.objects.filter(provider="google")
            .prefetch_related("sites")
            .order_by("id")
        )

        # Prefer SocialApps already linked to this Site
        site_qs = qs.filter(sites=site).distinct()

        socialapp = None
        created = False
        duplicates = []

        if site_qs.exists():
            # Use the oldest SocialApp as the canonical one for this Site
            socialapp = site_qs.first()
            duplicates = list(site_qs.exclude(pk=socialapp.pk))
        else:
            # No SocialApp currently linked to this Site
            socialapp = qs.first()
            if socialapp is None:
                socialapp = SocialApp.objects.create(
                    provider="google",
                    name="Google",
                    client_id=client_id,
                    secret=client_secret,
                )
                created = True
            else:
                # There are existing SocialApps for other Sites, but none for
                # this Site yet. Reuse the oldest one as canonical.
                duplicates = list(qs.exclude(pk=socialapp.pk))

        # ------------------------------------------------------------------
        # Ensure credentials are up to date on the canonical SocialApp
        # ------------------------------------------------------------------
        if socialapp.client_id != client_id or socialapp.secret != client_secret:
            socialapp.client_id = client_id
            socialapp.secret = client_secret
            socialapp.save(update_fields=["client_id", "secret"])
            self.stdout.write("  Updated SocialApp credentials")

        # ------------------------------------------------------------------
        # Ensure canonical SocialApp is linked to the current Site
        # ------------------------------------------------------------------
        if site not in socialapp.sites.all():
            socialapp.sites.add(site)
            self.stdout.write(f"  Linked SocialApp to Site: {site.domain}")
        else:
            self.stdout.write(f"  SocialApp already linked to Site: {site.domain}")

        if created:
            self.stdout.write("  Created SocialApp for provider: google")
        else:
            self.stdout.write("  Reusing existing SocialApp for provider: google")

        # ------------------------------------------------------------------
        # De-duplicate additional SocialApps linked to this Site to prevent
        # MultipleObjectsReturned inside django-allauth.
        # ------------------------------------------------------------------
        cleaned_count = 0
        for dup in duplicates:
            if site in dup.sites.all():
                dup.sites.remove(site)
                cleaned_count += 1

                # If the duplicate is no longer linked to any Sites, remove it
                if dup.sites.count() == 0:
                    dup.delete()

        if cleaned_count:
            msg = (
                f"  Cleaned up {cleaned_count} duplicate SocialApp record(s) "
                f"for provider 'google' linked to Site: {site.domain}"
            )
            self.stdout.write(msg)
            logger.warning(msg)

        # ------------------------------------------------------------------
        # Validate final configuration
        # ------------------------------------------------------------------
        if not client_id or not client_secret:
            self.stdout.write(
                self.style.WARNING(
                    "  Warning: SocialApp exists but credentials are empty. "
                    "Google OAuth will not work until credentials are configured."
                )
            )
        else:
            self.stdout.write("  SocialApp is fully configured with credentials")
