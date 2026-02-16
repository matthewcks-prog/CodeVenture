"""Tests for UserManagement.services (onboarding redirect logic)."""
import pytest
from django.contrib.auth.models import User

from UserManagement.models import Student, Parent, Teacher
from UserManagement.services import get_onboarding_redirect


@pytest.fixture
def user(db):
    return User.objects.create_user("testuser", "test@example.com", "password")


@pytest.fixture
def staff_user(db):
    u = User.objects.create_user("staffuser", "staff@example.com", "password")
    u.is_staff = True
    u.save()
    return u


@pytest.mark.django_db
def test_no_role_returns_choose_user_type(user):
    assert get_onboarding_redirect(user) == "choose_user_type"


@pytest.mark.django_db
def test_staff_no_role_returns_none(staff_user):
    assert get_onboarding_redirect(staff_user) is None


@pytest.mark.django_db
def test_student_incomplete_returns_complete_profile(user):
    Student.objects.create(user=user, profile_completed=False)
    assert get_onboarding_redirect(user) == "complete_profile"


@pytest.mark.django_db
def test_student_complete_returns_none(user):
    Student.objects.create(user=user, profile_completed=True)
    assert get_onboarding_redirect(user) is None


@pytest.mark.django_db
def test_parent_incomplete_returns_complete_profile(user):
    Parent.objects.create(user=user, profile_completed=False)
    assert get_onboarding_redirect(user) == "complete_profile"


@pytest.mark.django_db
def test_parent_complete_returns_none(user):
    Parent.objects.create(user=user, profile_completed=True)
    assert get_onboarding_redirect(user) is None


@pytest.mark.django_db
def test_teacher_returns_none(user):
    Teacher.objects.create(user=user)
    assert get_onboarding_redirect(user) is None


@pytest.mark.django_db
def test_staff_with_student_incomplete_returns_none(user):
    user.is_staff = True
    user.save()
    Student.objects.create(user=user, profile_completed=False)
    assert get_onboarding_redirect(user) is None
