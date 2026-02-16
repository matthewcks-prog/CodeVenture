from django.db import models
from UserManagement.models import Student
from LearningResource.models import SubModule
import uuid


class Challenge(models.Model):
    """Coding challenge, optionally scoped to a submodule for curriculum alignment."""
    name = models.CharField(max_length=50)
    description = models.TextField()
    hints = models.TextField()
    solution_code = models.TextField()
    std_in = models.TextField(null=True, blank=True)
    expected_output = models.TextField(null=True, blank=True)
    sample_output = models.TextField(null=True, blank=True)
    sub_module = models.ForeignKey(
        SubModule,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="challenges",
    )


class Quiz(models.Model):
    """Model for representing quizzes."""
    name = models.CharField(max_length=50)
    deadline = models.DateTimeField(null=True, blank=True)

    sub_module = models.OneToOneField(SubModule, null=True, on_delete=models.CASCADE, related_name='quiz')

    def __str__(self):
        return self.name


class Question(models.Model):
    """Model for representing quiz questions."""
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    points = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quiz} - {self.text}"


class Choice(models.Model):
    """Model for representing answer choices in quiz questions."""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


class QuizResult(models.Model):
    """Model for storing quiz results."""
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_result')
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class UserAnswer(models.Model):
    """Model for storing user answers to quiz questions."""
    quiz_result = models.ForeignKey(QuizResult, related_name='user_answers', null=True, on_delete=models.SET_NULL)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)
