# Generated migration: link Challenge to SubModule for scoped, scalable challenges.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("LearningResource", "0011_learningmodule_thumbnail"),
        ("QuizChallengeSystem", "0006_challenge_sample_output"),
    ]

    operations = [
        migrations.AddField(
            model_name="challenge",
            name="sub_module",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="challenges",
                to="LearningResource.submodule",
            ),
        ),
    ]
