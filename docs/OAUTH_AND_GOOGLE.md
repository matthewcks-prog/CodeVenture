# Google OAuth (django-allauth)

This document is the **single source of truth** for Google OAuth setup.

## Common Errors

- **Error 400: redirect_uri_mismatch** - Misconfiguring redirect URIs causes this in production while local may still work.
- **Error 500 on callback** - Missing SocialApp database record. django-allauth requires a SocialApp record even when using settings-based configuration.

## Why redirect_uri_mismatch happens

Google OAuth requires the **exact** URL your app sends as `redirect_uri` to be listed in the Google Cloud Console. django-allauth uses a **callback** URL (where Google sends the user back after sign-in), not the initial login page URL.

- **Wrong:** Adding only `https://yoursite.com/accounts/google/login/` (the page where the user clicks “Sign in with Google”).
- **Correct:** Adding `https://yoursite.com/accounts/google/login/callback/` (the URL Google redirects to with the auth code).

If the callback URL is missing in Google Console, you get **Access blocked: This app's request is invalid** with **Error 400: redirect_uri_mismatch** on the deployed site, while local works because localhost is already listed correctly.

## Required Google Cloud Console settings

In [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials), edit your **OAuth 2.0 Client ID** (Web application).

### Authorised JavaScript origins

Add every origin (scheme + host, no path) where your app runs:

| Environment | Origin |
|-------------|--------|
| Local | `http://localhost:8000` |
| Local (alternate) | `http://127.0.0.1:8000` |
| Production (Render) | `https://codeventure-ez4m.onrender.com` |

For a different production URL, add that origin (e.g. `https://your-app.onrender.com`).

### Authorised redirect URIs

Add the **callback** URL for each environment. The path is fixed by django-allauth; only the origin changes:

| Environment | Redirect URI (must match exactly) |
|-------------|------------------------------------|
| Local | `http://localhost:8000/accounts/google/login/callback/` |
| Local (alternate) | `http://127.0.0.1:8000/accounts/google/login/callback/` |
| Production (Render) | `https://codeventure-ez4m.onrender.com/accounts/google/login/callback/` |

**Important:** The path must end with `/accounts/google/login/callback/`. Do **not** add only `/accounts/google/login/`.

For a different production domain, add `https://<your-domain>/accounts/google/login/callback/`.

## Code reference

The callback path is defined once in the codebase:

- **Constant:** `CodeVenture.auth_config.GOOGLE_OAUTH_CALLBACK_PATH`
- **Helper:** `CodeVenture.auth_config.build_google_redirect_uri(scheme, netloc)` builds the full redirect URI for a given origin.

Use these when adding a new environment or validating Console settings.

## Database Configuration

**IMPORTANT:** django-allauth requires a `SocialApp` database record even when using settings-based configuration. The settings provide credentials, but the database record links the provider to your Site.

The SocialApp is automatically created/updated during deployment via:
```bash
python manage.py setup_google_oauth
```

This command:
1. Creates or updates the Google SocialApp record
2. Links it to the Site (SITE_ID = 1)
3. Updates credentials from environment variables
4. Validates the configuration

**Manual setup:** If you need to run this manually:
```bash
python manage.py setup_google_oauth
```

For local development without credentials:
```bash
python manage.py setup_google_oauth --skip-if-missing-creds
```

## Environment variables

- **GOOGLE_OAUTH_CLIENT_ID** – OAuth client ID from Google Cloud Console.
- **GOOGLE_OAUTH_CLIENT_SECRET** – OAuth client secret.
- **DJANGO_SITE_DOMAIN** – (Production) Domain for the Django Sites framework (e.g. `codeventure-ez4m.onrender.com`). Used by `setup_site` and should match the host users see. Set this on Render if your service URL is not the default.

When these are set, the app shows “Sign in with Google”; when either is missing, the button is hidden to avoid 500s.

## Checklist for a new environment

1. Add **Authorised JavaScript origin:** `https://<your-domain>` (or `http://...` for local).
2. Add **Authorised redirect URI:** `https://<your-domain>/accounts/google/login/callback/` (must include `/callback/`).
3. Set **DJANGO_SITE_DOMAIN** to `<your-domain>` in that environment (for production).
4. Set **GOOGLE_OAUTH_CLIENT_ID** and **GOOGLE_OAUTH_CLIENT_SECRET** (same client can list multiple redirect URIs).
5. Ensure **SocialApp database record exists** - This is handled automatically by `build.sh` via `setup_google_oauth` command. If deploying manually, run `python manage.py setup_google_oauth` after migrations.

## Troubleshooting

### Error 500 on `/accounts/google/login/` or `/accounts/google/login/callback/`

**Root cause:** Misconfigured SocialApp database records.

django-allauth expects that, for each Site, there is **exactly one** `SocialApp`
for the Google provider. If there are **zero** records, or if there are
**multiple** records linked to the same Site, you will see 500 errors in
production with log messages such as:

- `django.core.exceptions.ObjectDoesNotExist`
- `django.core.exceptions.MultipleObjectsReturned`

**Solution (idempotent, safe for all environments):**

1. Run the setup command (this is already executed automatically in Render via `build.sh`):
   ```bash
   python manage.py setup_google_oauth
   ```
2. The command will:
   - Create the Google SocialApp if it does not exist.
   - Link it to the current `SITE_ID`.
   - Update credentials from environment variables.
   - **De-duplicate** any extra Google SocialApp records linked to the same Site, so that
     django-allauth never raises `MultipleObjectsReturned` at runtime.
3. Check logs for messages like:
   - `Cleaned up N duplicate SocialApp record(s) for provider 'google'`

**Common issues:**
- SocialApp exists but not linked to Site → Run `setup_google_oauth`.
- Site doesn't exist → Run `python manage.py setup_site` first.
- Credentials mismatch → Run `setup_google_oauth` to sync from environment variables.

## 3rd party signup form bypass

Google OAuth does not provide a username. By default, django-allauth would show a signup form to collect it. We bypass this via:

- **`WelcomePage.adapter.CustomSocialAccountAdapter.populate_user`** – Derives username from email (or name) before auto-signup validation, so `SOCIALACCOUNT_AUTO_SIGNUP = True` succeeds and the form is never shown.
- **`UserManagement.account_adapter.CustomAccountAdapter`** – Redirects new OAuth users directly to role selection (`choose_user_type`) instead of home.

See [AUTH_AND_ONBOARDING_FLOW.md](AUTH_AND_ONBOARDING_FLOW.md) for the full flow.

## Related docs

- [AUTH_AND_ONBOARDING_FLOW.md](AUTH_AND_ONBOARDING_FLOW.md) – Login, signup, and onboarding redirect logic.
