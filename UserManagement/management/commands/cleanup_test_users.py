from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = (
        "Safely clean up non-essential/test user accounts while preserving "
        "learning content, quizzes, and challenges.\n\n"
        "By default this runs in DRY-RUN mode and only prints what would be "
        "deleted. Use the --execute flag to actually delete users."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--execute",
            action="store_true",
            help="Actually delete the users (otherwise dry-run).",
        )

    def handle(self, *args, **options):
        User = get_user_model()

        # Keep all staff & superusers – they are required for admin access.
        keep_qs = User.objects.filter(is_staff=True) | User.objects.filter(
            is_superuser=True
        )
        keep_ids = set(keep_qs.values_list("id", flat=True))

        # Project-specific: preserve your primary real account by email if present.
        primary_emails = {"matthew888.mcks@gmail.com"}
        primary_users = User.objects.filter(email__in=primary_emails)
        keep_ids.update(primary_users.values_list("id", flat=True))

        # Everything else is considered disposable sample/test data.
        delete_qs = User.objects.exclude(id__in=keep_ids)
        delete_count = delete_qs.count()

        self.stdout.write("=" * 72)
        self.stdout.write(self.style.WARNING("CodeVenture User Cleanup"))
        self.stdout.write("=" * 72)
        self.stdout.write(f"Total users:       {User.objects.count()}")
        self.stdout.write(f"Will keep:         {len(keep_ids)}")
        self.stdout.write(f"Candidates to delete: {delete_count}")
        self.stdout.write("")

        if not delete_count:
            self.stdout.write(self.style.SUCCESS("Nothing to delete."))
            return

        self.stdout.write("Users that would be deleted:")
        for u in delete_qs.order_by("id"):
            self.stdout.write(
                f"  - id={u.id}, username={u.username}, "
                f"email={u.email!r}, staff={u.is_staff}, superuser={u.is_superuser}"
            )

        self.stdout.write("")

        if not options["execute"]:
            self.stdout.write(
                self.style.WARNING(
                    "DRY RUN only. No users have been deleted.\n"
                    "Run again with --execute to apply these changes:\n"
                    "  python manage.py cleanup_test_users --execute"
                )
            )
            return

        deleted_info = list(
            delete_qs.values_list("id", "username", "email")
        )  # capture for logging
        delete_qs.delete()

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Deleted users:"))
        for uid, uname, email in deleted_info:
            self.stdout.write(f"  - id={uid}, username={uname}, email={email!r}")

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Cleanup complete. Remaining users: {User.objects.count()}"
            )
        )

