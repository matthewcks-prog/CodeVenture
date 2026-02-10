"""
Django management command to fix migration history inconsistencies
Run this via Render Shell: python manage.py fix_migration_history
"""
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    help = 'Fix migration history inconsistencies in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--execute',
            action='store_true',
            help='Actually fix the migrations (dry-run by default)',
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.WARNING("Django Migration History Fix Tool"))
        self.stdout.write("=" * 70)
        self.stdout.write("")

        # Check current migration state
        recorder = MigrationRecorder(connection)
        applied_migrations = list(recorder.applied_migrations())

        # Check for the specific issue
        socialaccount_applied = any(
            app == 'socialaccount' and name == '0001_initial'
            for app, name in applied_migrations
        )
        sites_applied = any(
            app == 'sites' and name == '0001_initial'
            for app, name in applied_migrations
        )

        self.stdout.write(f"Sites 0001_initial applied: {sites_applied}")
        self.stdout.write(f"Socialaccount 0001_initial applied: {socialaccount_applied}")
        self.stdout.write("")

        if socialaccount_applied and not sites_applied:
            self.stdout.write(self.style.ERROR(
                "ISSUE DETECTED: socialaccount.0001_initial is applied "
                "but sites.0001_initial is not!"
            ))
            self.stdout.write("")

            if not options['execute']:
                self.stdout.write(self.style.WARNING(
                    "DRY RUN MODE - No changes will be made."
                ))
                self.stdout.write("")
                self.stdout.write("To fix this issue, we will:")
                self.stdout.write("1. Mark sites.0001_initial as applied")
                self.stdout.write("2. Mark sites.0002_alter_domain_unique as applied")
                self.stdout.write("")
                self.stdout.write(self.style.SUCCESS(
                    "Run with --execute to actually fix the migrations:"
                ))
                self.stdout.write("  python manage.py fix_migration_history --execute")
                return

            # Fix the migration history
            self.stdout.write(self.style.SUCCESS("Fixing migration history..."))
            self.stdout.write("")

            # Insert the missing sites migrations
            with connection.cursor() as cursor:
                # Check if table exists
                cursor.execute(
                    "SELECT COUNT(*) FROM information_schema.tables "
                    "WHERE table_name = 'django_migrations'"
                )
                if cursor.fetchone()[0] == 0:
                    self.stdout.write(self.style.ERROR(
                        "django_migrations table doesn't exist!"
                    ))
                    return

                # Insert sites.0001_initial
                self.stdout.write("1. Marking sites.0001_initial as applied...")
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) "
                    "VALUES (%s, %s, NOW()) "
                    "ON CONFLICT (app, name) DO NOTHING",
                    ['sites', '0001_initial']
                )

                # Insert sites.0002_alter_domain_unique
                self.stdout.write("2. Marking sites.0002_alter_domain_unique as applied...")
                cursor.execute(
                    "INSERT INTO django_migrations (app, name, applied) "
                    "VALUES (%s, %s, NOW()) "
                    "ON CONFLICT (app, name) DO NOTHING",
                    ['sites', '0002_alter_domain_unique']
                )

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(
                "SUCCESS! Migration history has been fixed."
            ))
            self.stdout.write("")
            self.stdout.write("You can now run: python manage.py migrate")

        elif not socialaccount_applied and not sites_applied:
            self.stdout.write(self.style.SUCCESS(
                "No migrations applied yet. Database is clean."
            ))
            self.stdout.write("")
            self.stdout.write("You can now run: python manage.py migrate")

        else:
            self.stdout.write(self.style.SUCCESS(
                "No migration order issues detected!"
            ))
            self.stdout.write("")
            self.stdout.write("Migration history looks good.")

        self.stdout.write("")
        self.stdout.write("=" * 70)
