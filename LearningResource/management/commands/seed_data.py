"""
Management command to seed the database with initial learning modules and assessments.

Uses curriculum_config (single source of truth) and assessment_config for CPE quizzes/challenges.
Usage:
    python manage.py seed_data
    python manage.py seed_data --clear  # Clear existing data first
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User

from LearningResource.models import LearningModule, SubModule, VideoTutorial
from LearningResource.curriculum_config import MODULES
from LearningResource.assessment_config import (
    CPE_SUBMODULE_ASSESSMENTS,
    PYTHON_SUBMODULE_ASSESSMENTS,
    WEB_SUBMODULE_ASSESSMENTS,
)
from QuizChallengeSystem.models import Quiz, Question, Choice, Challenge, QuizResult, UserAnswer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Seeds the database with learning modules, submodules, and CPE assessments"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing learning and assessment data before seeding",
        )
        parser.add_argument(
            "--admin",
            action="store_true",
            help="Create admin superuser (username: admin, password: superuser)",
        )

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))
        self.stdout.write("=" * 70)

        try:
            with transaction.atomic():
                if options["admin"]:
                    self._create_admin_user()
                if options["clear"]:
                    self._clear_data()
                self._seed_learning_modules()
                self._seed_python_assessments()
                self._seed_web_assessments()
                self._seed_cpe_assessments()
            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("=" * 70))
            self.stdout.write(self.style.SUCCESS("[SUCCESS] Database seeding completed successfully!"))
            self.stdout.write(self.style.SUCCESS("=" * 70))
        except Exception as e:
            logger.error("Error during database seeding: %s", str(e), exc_info=True)
            self.stdout.write(self.style.ERROR("[ERROR] %s" % str(e)))
            raise

    def _create_admin_user(self):
        self.stdout.write("\n[1/3] Creating admin user...")
        username = "admin"
        password = "superuser"
        email = "admin@codeventure.com"
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING("  [WARNING] Admin user already exists: %s" % username))
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS("  [OK] Updated admin user permissions"))
        except User.DoesNotExist:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name="Admin",
                last_name="User",
            )
            self.stdout.write(self.style.SUCCESS("  [OK] Created admin user: %s" % username))
        self.stdout.write("    Username: %s" % username)
        self.stdout.write("    Password: %s" % password)
        self.stdout.write("    Email: %s" % email)

    def _clear_data(self):
        """Clear learning and assessment data. Order respects FKs and CASCADE."""
        self.stdout.write("\nClearing existing data...")
        # Assessment data that references Quiz / SubModule
        ua = UserAnswer.objects.count()
        qr = QuizResult.objects.count()
        QuizResult.objects.all().delete()
        UserAnswer.objects.all().delete()
        Quiz.objects.all().delete()  # CASCADE deletes Question, Choice
        Challenge.objects.all().delete()
        submodule_count = SubModule.objects.count()
        video_count = VideoTutorial.objects.count()
        module_count = LearningModule.objects.count()
        SubModule.objects.all().delete()
        VideoTutorial.objects.all().delete()
        LearningModule.objects.all().delete()
        self.stdout.write(
            self.style.WARNING(
                "  [OK] Deleted %d modules, %d submodules, %d videos, quizzes, %d results, %d answers, all challenges"
                % (module_count, submodule_count, video_count, qr, ua)
            )
        )

    def _seed_learning_modules(self):
        """Seed all modules and submodules from curriculum_config."""
        self.stdout.write("\n[2/3] Seeding learning modules...")
        modules_created = 0
        submodules_created = 0

        for mod_cfg in MODULES:
            module, created = LearningModule.objects.get_or_create(
                name=mod_cfg["name"],
                defaults={
                    "short_name": mod_cfg["short_name"],
                    "description": mod_cfg["description"],
                    "thumbnail": mod_cfg.get("thumbnail") or "",
                },
            )
            if created:
                modules_created += 1
                self.stdout.write(self.style.SUCCESS("  [OK] Created module: %s" % module.name))
            else:
                # Update description/thumbnail if config changed
                module.description = mod_cfg["description"]
                module.thumbnail = mod_cfg.get("thumbnail") or ""
                module.save()

            prev_submodule = None
            for sub_cfg in mod_cfg["submodules"]:
                video, _ = VideoTutorial.objects.update_or_create(
                    name=sub_cfg["video_name"],
                    defaults={"video_id": sub_cfg["video_id"]},
                )
                submodule, created = SubModule.objects.get_or_create(
                    name=sub_cfg["name"],
                    parent_module=module,
                    defaults={
                        "difficulty_level": sub_cfg["difficulty_level"],
                        "description": sub_cfg["description"],
                        "video": video,
                        "prev_submodule": prev_submodule,
                    },
                )
                if prev_submodule:
                    prev_submodule.next_submodule = submodule
                    prev_submodule.save()
                prev_submodule = submodule
                if created:
                    submodules_created += 1
            self.stdout.write("    [OK] %d submodules for %s" % (len(mod_cfg["submodules"]), module.name))

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("  Summary: %d new modules, %d new submodules" % (modules_created, submodules_created)))
        self.stdout.write("    Total modules: %d" % LearningModule.objects.count())
        self.stdout.write("    Total submodules: %d" % SubModule.objects.count())

    def _seed_cpe_assessments(self):
        """Create quizzes and challenges for Computational Process Engineering submodules."""
        self.stdout.write("\n[3/3] Seeding CPE assessments...")
        try:
            cpe = LearningModule.objects.get(short_name="cpe")
        except LearningModule.DoesNotExist:
            self.stdout.write(self.style.WARNING("  [SKIP] No CPE module found; run module seed first."))
            return

        quiz_count = 0
        challenge_count = 0
        for sub in cpe.ordered_submodules():
            assessments = CPE_SUBMODULE_ASSESSMENTS.get(sub.name)
            if not assessments:
                continue

            if "quiz" in assessments:
                q_cfg = assessments["quiz"]
                quiz, _ = Quiz.objects.get_or_create(
                    sub_module=sub,
                    defaults={"name": q_cfg["name"]},
                )
                quiz.name = q_cfg["name"]
                quiz.save()
                quiz.questions.all().delete()
                for q_data in q_cfg["questions"]:
                    question = Question.objects.create(
                        quiz=quiz,
                        text=q_data["text"],
                        points=q_data.get("points", 1),
                    )
                    for c_data in q_data["choices"]:
                        Choice.objects.create(
                            question=question,
                            text=c_data["text"],
                            is_correct=c_data["is_correct"],
                        )
                quiz_count += 1

            if "challenge" in assessments:
                ch_cfg = assessments["challenge"]
                defaults = {
                    "name": ch_cfg["name"],
                    "description": ch_cfg["description"],
                    "hints": ch_cfg["hints"],
                    "solution_code": ch_cfg["solution_code"],
                    "std_in": ch_cfg.get("std_in") or "",
                    "expected_output": ch_cfg.get("expected_output") or "",
                    "sample_output": ch_cfg.get("sample_output") or "",
                }
                challenge, created = Challenge.objects.get_or_create(
                    sub_module=sub,
                    defaults=defaults,
                )
                if not created:
                    for key, value in defaults.items():
                        setattr(challenge, key, value)
                    challenge.save()
                challenge_count += 1

        self.stdout.write(self.style.SUCCESS("  [OK] CPE: %d quizzes, %d challenges" % (quiz_count, challenge_count)))

    def _seed_python_assessments(self):
        """Create quizzes for Python Fundamentals submodules."""
        self.stdout.write("\n[3/3] Seeding Python Fundamentals assessments...")
        try:
            python_module = LearningModule.objects.get(short_name="python")
        except LearningModule.DoesNotExist:
            self.stdout.write(self.style.WARNING("  [SKIP] No Python Fundamentals module found; run module seed first."))
            return

        quiz_count = 0
        for sub in python_module.ordered_submodules():
            assessments = PYTHON_SUBMODULE_ASSESSMENTS.get(sub.name)
            if not assessments or "quiz" not in assessments:
                continue

            q_cfg = assessments["quiz"]
            quiz, _ = Quiz.objects.get_or_create(
                sub_module=sub,
                defaults={"name": q_cfg["name"]},
            )
            quiz.name = q_cfg["name"]
            quiz.save()
            quiz.questions.all().delete()

            for q_data in q_cfg["questions"]:
                question = Question.objects.create(
                    quiz=quiz,
                    text=q_data["text"],
                    points=q_data.get("points", 1),
                )
                for c_data in q_data["choices"]:
                    Choice.objects.create(
                        question=question,
                        text=c_data["text"],
                        is_correct=c_data["is_correct"],
                    )
            quiz_count += 1

        self.stdout.write(self.style.SUCCESS("  [OK] Python Fundamentals: %d quizzes" % quiz_count))

    def _seed_web_assessments(self):
        """Create quizzes for Web Development submodules."""
        self.stdout.write("\n[3/3] Seeding Web Development assessments...")
        try:
            web_module = LearningModule.objects.get(short_name="web")
        except LearningModule.DoesNotExist:
            self.stdout.write(self.style.WARNING("  [SKIP] No Web Development module found; run module seed first."))
            return

        quiz_count = 0
        for sub in web_module.ordered_submodules():
            assessments = WEB_SUBMODULE_ASSESSMENTS.get(sub.name)
            if not assessments or "quiz" not in assessments:
                continue

            q_cfg = assessments["quiz"]
            quiz, _ = Quiz.objects.get_or_create(
                sub_module=sub,
                defaults={"name": q_cfg["name"]},
            )
            quiz.name = q_cfg["name"]
            quiz.save()
            quiz.questions.all().delete()

            for q_data in q_cfg["questions"]:
                question = Question.objects.create(
                    quiz=quiz,
                    text=q_data["text"],
                    points=q_data.get("points", 1),
                )
                for c_data in q_data["choices"]:
                    Choice.objects.create(
                        question=question,
                        text=c_data["text"],
                        is_correct=c_data["is_correct"],
                    )
            quiz_count += 1

        self.stdout.write(self.style.SUCCESS("  [OK] Web Development: %d quizzes" % quiz_count))
