# Auth and Onboarding Flow

This document describes how login, signup, role selection, and profile completion work so the home page and learning modules behave correctly.

## Overview

- **Anonymous users**: See the welcome/landing page. Sign up goes to role selection, then registration for that role, then profile completion (for Student/Parent).
- **Authenticated users**: Home view uses `UserManagement.services.get_onboarding_redirect()` to decide if the user must complete a step before seeing the menu.

## Onboarding redirect logic (single source of truth)

Implemented in **`UserManagement.services.get_onboarding_redirect(user)`**. Used by the home view (and can be reused by middleware or decorators).

| User state | Redirect target |
|------------|-----------------|
| No role (no Student/Parent/Teacher) | `choose_user_type` |
| Has Student/Parent, profile not completed | `complete_profile` |
| Has Teacher, or profile completed | None (show home) |
| Staff | None (show home) |

**Important:** Users who already chose a role at signup but have not yet completed their profile are sent to **complete_profile**, not to **choose_user_type**. Role selection is only for users without a role (e.g. OAuth users or legacy accounts).

## Flows

### Sign up (new user)

1. User clicks Sign up → **choose_user_type** (select Student / Parent / Teacher).
2. POST to **choose_user_type** with `role` → redirect to **register_user** for that role.
3. **register_user** creates `User` + corresponding `Student`/`Parent`/`Teacher`, logs in, redirects to **complete_profile**.
4. **complete_profile**: Student/Parent fill optional profile; Teacher is redirected to home. On save, `profile_completed = True`, redirect to **home**.
5. Home shows **MenuPage** (no redirect).

### Login (existing user)

1. User logs in → redirect determined by `UserManagement.account_adapter.CustomAccountAdapter.get_login_redirect_url` (or `next` if specified).
2. Adapter uses `get_onboarding_redirect(user)`:
   - If no role → **choose_user_type**.
   - If role but profile incomplete → **complete_profile**.
   - Otherwise → **home** (MenuPage).

### Google OAuth (Sign in with Google)

1. User clicks "Sign in with Google" → Google OAuth flow.
2. **Auto-signup:** `WelcomePage.adapter.CustomSocialAccountAdapter.populate_user` derives username from email (Google does not provide username), so the 3rd party signup form is bypassed.
3. User is created and logged in → redirect via `CustomAccountAdapter.get_login_redirect_url` → **choose_user_type** (no role yet).
4. User selects role → continues as per Sign up flow from step 3.

### Home link (your issue)

- **Before fix:** Home treated “profile not completed” and “no role” the same and always redirected to **choose_user_type**, so users who had already chosen a role at signup were incorrectly sent back to role selection.
- **After fix:** Home redirects to **complete_profile** when the user has a role but profile is incomplete, and to **choose_user_type** only when the user has no role.

## Learning modules access

- **LearningResource** views use `@login_required(login_url='/login/')`.
- Student-specific views use `_get_student_or_redirect()`: if the user has no `Student` profile, they are redirected to **home** (home will then apply onboarding redirect if needed).
- Teachers and parents do not use the same learning-module content as students; access rules live in the respective apps.

## Code references

- **Onboarding logic:** `UserManagement.services.get_onboarding_redirect`
- **Post-login redirect:** `UserManagement.account_adapter.CustomAccountAdapter.get_login_redirect_url`
- **Social (Google) adapter:** `WelcomePage.adapter.CustomSocialAccountAdapter` (populate_user, pre_social_login)
- **Home view:** `WelcomePage.views.home_view`
- **Role selection:** `UserManagement.views.choose_user_type`
- **Profile completion:** `UserManagement.views.complete_profile`
- **Registration:** `UserManagement.views.register_user`

## Tests

- **`UserManagement.test.test_services`**: Unit tests for `get_onboarding_redirect` (no role, staff, student/parent complete/incomplete, teacher).
- **`WelcomePage.test.test_views`**: Home view redirects (incomplete profile → complete_profile; no role → choose_user_type; complete → MenuPage).
