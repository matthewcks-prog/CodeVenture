"""
Ensure the django.contrib.sites Site record exists.

Called automatically during build (build.sh) so that allauth and any
code relying on SITE_ID = 1 works out of the box.
"""
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = "Create or update the Site record for SITE_ID = 1"

    def handle(self, *args, **options):
        # Determine the domain from env vars or fall back to a sensible default.
        domain = os.environ.get(
            'DJANGO_SITE_DOMAIN',
            'codeventure-ez4m.onrender.com',
        )
        site_name = os.environ.get('DJANGO_SITE_NAME', 'CodeVenture')

        with connection.cursor() as cursor:
            # Check if the row exists
            cursor.execute(
                "SELECT id FROM django_site WHERE id = %s",
                [settings.SITE_ID],
            )
            row = cursor.fetchone()

            if row:
                cursor.execute(
                    "UPDATE django_site SET domain = %s, name = %s WHERE id = %s",
                    [domain, site_name, settings.SITE_ID],
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Site updated: {domain}")
                )
            else:
                cursor.execute(
                    "INSERT INTO django_site (id, domain, name) VALUES (%s, %s, %s)",
                    [settings.SITE_ID, domain, site_name],
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Site created: {domain}")
                )
