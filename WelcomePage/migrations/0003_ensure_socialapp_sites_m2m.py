from django.db import migrations


def create_socialapp_sites_m2m(apps, schema_editor):
    """
    Ensure the implicit ManyToMany table used by django-allauth
    (`socialaccount_socialapp_sites`) exists.

    On your local SQLite database this table is created by the
    `socialaccount` app’s own migrations. In production on Render the
    migration history became inconsistent and the table was missing,
    which caused a 500 on `/accounts/google/login/` with:

        ProgrammingError: relation "socialaccount_socialapp_sites" does not exist

    This migration is idempotent: it only creates the table and indexes
    if they do not already exist, so it is safe to run on all
    environments.
    """
    connection = schema_editor.connection

    # Only run for PostgreSQL; on SQLite the table already exists and
    # CREATE TABLE IF NOT EXISTS would require vendor‑specific SQL.
    if connection.vendor != "postgresql":
        return

    with connection.cursor() as cursor:
        # Check if the join table already exists
        cursor.execute(
            """
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = 'socialaccount_socialapp_sites'
            """
        )
        if cursor.fetchone():
            # Table already present – nothing to do.
            return

        # Create the join table with the same structure as on SQLite.
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS socialaccount_socialapp_sites (
                id SERIAL PRIMARY KEY,
                socialapp_id INTEGER NOT NULL
                    REFERENCES socialaccount_socialapp (id)
                    DEFERRABLE INITIALLY DEFERRED,
                site_id INTEGER NOT NULL
                    REFERENCES django_site (id)
                    DEFERRABLE INITIALLY DEFERRED
            );
            """
        )

        # Add supporting indexes & uniqueness constraint. The names
        # mirror Django’s auto‑generated ones but are not relied upon.
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
                socialaccount_socialapp_sites_site_id_2579dee5
            ON socialaccount_socialapp_sites (site_id);
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS
                socialaccount_socialapp_sites_socialapp_id_97fb6e7d
            ON socialaccount_socialapp_sites (socialapp_id);
            """
        )
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS
                socialaccount_socialapp_sites_socialapp_id_site_id_71a9a768_uniq
            ON socialaccount_socialapp_sites (socialapp_id, site_id);
            """
        )


class Migration(migrations.Migration):
    dependencies = [
        ("WelcomePage", "0002_alter_ticket_user"),
    ]

    operations = [
        migrations.RunPython(create_socialapp_sites_m2m, migrations.RunPython.noop),
    ]

