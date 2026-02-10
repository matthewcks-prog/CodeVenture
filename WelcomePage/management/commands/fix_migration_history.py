"""
Django management command to fix migration history inconsistencies.
Handles the case where socialaccount migrations were applied before
sites migrations, which breaks Django's consistency check.

Run: python manage.py fix_migration_history --execute
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Fix migration history inconsistencies in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--execute',
            action='store_true',
            help='Actually fix the migrations (dry-run by default)',
        )

    def _table_exists(self, cursor, table_name):
        """Check if a table exists in the database (works for PostgreSQL and SQLite)."""
        try:
            cursor.execute(
                "SELECT 1 FROM information_schema.tables WHERE table_name = %s",
                [table_name],
            )
            return cursor.fetchone() is not None
        except Exception:
            # Fallback for SQLite which doesn't have information_schema
            try:
                cursor.execute(
                    "SELECT 1 FROM sqlite_master WHERE type='table' AND name=%s",
                    [table_name],
                )
                return cursor.fetchone() is not None
            except Exception:
                return False

    def _migration_is_recorded(self, cursor, app, name):
        """Check if a migration is recorded in django_migrations."""
        cursor.execute(
            "SELECT COUNT(*) FROM django_migrations WHERE app = %s AND name = %s",
            [app, name],
        )
        return cursor.fetchone()[0] > 0

    def _record_migration(self, cursor, app, name):
        """Insert a migration record into django_migrations."""
        cursor.execute(
            "INSERT INTO django_migrations (app, name, applied) VALUES (%s, %s, NOW())",
            [app, name],
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.WARNING("Django Migration History Fix Tool"))
        self.stdout.write("=" * 70)

        with connection.cursor() as cursor:
            # Ensure django_migrations table exists
            if not self._table_exists(cursor, 'django_migrations'):
                self.stdout.write(self.style.ERROR(
                    "django_migrations table doesn't exist! "
                    "Run 'migrate' first to create it."
                ))
                return

            # Check current state
            socialaccount_applied = self._migration_is_recorded(
                cursor, 'socialaccount', '0001_initial'
            )
            sites_0001_applied = self._migration_is_recorded(
                cursor, 'sites', '0001_initial'
            )
            sites_0002_applied = self._migration_is_recorded(
                cursor, 'sites', '0002_alter_domain_unique'
            )

            self.stdout.write(f"  sites.0001_initial applied:          {sites_0001_applied}")
            self.stdout.write(f"  sites.0002_alter_domain_unique:      {sites_0002_applied}")
            self.stdout.write(f"  socialaccount.0001_initial applied:   {socialaccount_applied}")
            self.stdout.write("")

            # Determine if there's an inconsistency
            needs_fix = socialaccount_applied and not sites_0001_applied

            if not needs_fix:
                if not socialaccount_applied and not sites_0001_applied:
                    self.stdout.write(self.style.SUCCESS(
                        "No migrations applied yet - database is clean."
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        "No migration order issues detected!"
                    ))
                return

            # We have an inconsistency!
            self.stdout.write(self.style.ERROR(
                "ISSUE: socialaccount.0001_initial is applied "
                "but sites.0001_initial is NOT recorded!"
            ))
            self.stdout.write("")

            if not options['execute']:
                self.stdout.write(self.style.WARNING("DRY RUN - no changes made."))
                self.stdout.write("Run with --execute to fix:")
                self.stdout.write("  python manage.py fix_migration_history --execute")
                return

            # ---- Actually fix the issue ----
            self.stdout.write(self.style.SUCCESS("Applying fix..."))

            # 1. Ensure the django_site table exists
            site_table_exists = self._table_exists(cursor, 'django_site')
            if not site_table_exists:
                self.stdout.write("  Creating django_site table...")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_site (
                        id serial PRIMARY KEY,
                        domain varchar(100) NOT NULL,
                        name varchar(50) NOT NULL
                    )
                """)
                cursor.execute("""
                    INSERT INTO django_site (id, domain, name)
                    VALUES (1, 'codeventure-ez4m.onrender.com', 'CodeVenture')
                    ON CONFLICT (id) DO NOTHING
                """)
                self.stdout.write(self.style.SUCCESS("  -> django_site table created"))
            else:
                self.stdout.write("  django_site table already exists - good")

            # 2. Record sites.0001_initial
            if not sites_0001_applied:
                self.stdout.write("  Recording sites.0001_initial...")
                self._record_migration(cursor, 'sites', '0001_initial')
                self.stdout.write(self.style.SUCCESS("  -> Done"))

            # 3. Record sites.0002_alter_domain_unique
            if not sites_0002_applied:
                self.stdout.write("  Recording sites.0002_alter_domain_unique...")
                self._record_migration(cursor, 'sites', '0002_alter_domain_unique')
                # Also ensure unique constraint exists on domain
                if site_table_exists:
                    try:
                        cursor.execute("""
                            ALTER TABLE django_site
                            ADD CONSTRAINT django_site_domain_uniq UNIQUE (domain)
                        """)
                    except Exception:
                        pass  # Constraint may already exist
                self.stdout.write(self.style.SUCCESS("  -> Done"))

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS(
                "Migration history fixed! 'manage.py migrate' should now work."
            ))

        self.stdout.write("=" * 70)
