# Google OAuth (django-allauth)

This document is the **single source of truth** for Google OAuth setup. Misconfiguring redirect URIs causes **Error 400: redirect_uri_mismatch** in production while local may still work.

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

## Related docs

- [AUTH_AND_ONBOARDING_FLOW.md](AUTH_AND_ONBOARDING_FLOW.md) – Login, signup, and onboarding redirect logic.
