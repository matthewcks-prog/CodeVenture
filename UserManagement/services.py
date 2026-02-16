"""
User onboarding and profile state.

Single source of truth for "where should this user be sent?" when they
haven't finished setup. Used by the home view and any future gates
(middleware, decorators) so redirect logic stays consistent and testable.
"""
from typing import Optional


def get_onboarding_redirect(user) -> Optional[str]:
    """
    Return the view name to redirect to if the user must complete onboarding, else None.

    Logic:
    - Staff users: no redirect (they can access home).
    - No role (no Student/Parent/Teacher): send to role selection (choose_user_type).
    - Has role but profile not completed: send to complete_profile.
    - Has role and profile completed (or Teacher): no redirect.

    Args:
        user: Django User instance (assumed authenticated by caller).

    Returns:
        'choose_user_type' | 'complete_profile' | None
    """
    if user.is_staff:
        return None

    has_student = hasattr(user, "student")
    has_parent = hasattr(user, "parent")
    has_teacher = hasattr(user, "teacher")
    has_role = has_student or has_parent or has_teacher

    if not has_role:
        return "choose_user_type"

    profile_completed = False
    if has_student:
        profile_completed = user.student.profile_completed
    elif has_parent:
        profile_completed = user.parent.profile_completed
    elif has_teacher:
        profile_completed = True  # Teachers have no extra profile step

    if not profile_completed:
        return "complete_profile"

    return None
