import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodeVenture.settings')
django.setup()

from LearningResource.models import SubModule, LearningModule
from QuizChallengeSystem.models import Quiz, Challenge

print("Existing Learning Modules:")
for module in LearningModule.objects.all():
    print(f"- {module.name} (Short: {module.short_name})")

print("\nExisting SubModules:")
for submodule in SubModule.objects.all():
    print(f"- {submodule.name} (Parent: {submodule.parent_module.short_name}, Difficulty: {submodule.difficulty_level})")
    if hasattr(submodule, 'quiz'):
        print(f"  -> Has Quiz: {submodule.quiz.name}")
    else:
        print("  -> No Quiz")

print("\nExisting Challenges:")
for challenge in Challenge.objects.all():
    print(f"- {challenge.name}")
