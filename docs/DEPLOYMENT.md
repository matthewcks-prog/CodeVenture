# Deployment (Render)

This document covers deploying CodeVenture to Render and ensuring the database has curriculum data so learning pages work.

## Build and database

- The **build** (see `build.sh`) runs:
  - Migrations (`python manage.py migrate --noinput`)
  - Site setup (`python manage.py setup_site`)
  - **Curriculum seeding** (`python manage.py seed_data`)
- Seeding is **idempotent**: safe to run on every deploy. It creates/updates learning modules, submodules, videos, and CPE assessments from `curriculum_config` and `assessment_config`.
- **No manual seed step is required** for Basic Modules or concept modules to appear. If you deployed before seeding was added to the build, trigger a **new deploy** so the build runs again, or run once in the Render shell: `python manage.py seed_data`.

## Environment variables on Render

Set these in the Render dashboard for the web service:

| Variable | Required | Notes |
|----------|----------|--------|
| `DATABASE_URL` | Yes (unless linked via blueprint) | Postgres URL. Set automatically if the database is linked in `render.yaml`. |
| `DJANGO_SECRET_KEY` | Yes | Use a long random value in production. |
| `DJANGO_DEBUG` | Yes | Set to `false` in production. |
| `DJANGO_ALLOWED_HOSTS` | Yes | Your Render host, e.g. `codeventure-ez4m.onrender.com`. |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Yes | `https://codeventure-ez4m.onrender.com` (your host with `https://`). |
| `GOOGLE_OAUTH_CLIENT_ID` / `GOOGLE_OAUTH_CLIENT_SECRET` | Optional | For Google login. See [OAUTH_AND_GOOGLE.md](OAUTH_AND_GOOGLE.md). |

## First-time admin user

To create the default admin user (e.g. for first production deploy), run once in the Render **Shell**:

```bash
python manage.py seed_data --admin
```

Default credentials: username `admin`, password `superuser`. Change the password after first login.

## Troubleshooting

- **500 on `/learning/basic_module/` or “Concept modules” empty**  
  The app expects the “Basic Modules” learning module and submodules to exist. Ensure:
  1. `DATABASE_URL` is set and points to a Postgres database.
  2. A deploy has completed so that `build.sh` ran (migrations + `seed_data`).  
  If the database was empty or you deployed before seeding was in the build, trigger a **new deploy** or run in the Render shell: `python manage.py seed_data`.

- **Using an external Postgres URL**  
  If you attach a database that Render did not create (e.g. you paste a `postgresql://...` URL), set `DATABASE_URL` in the service environment. The next deploy will run migrations and `seed_data` against that database.

- **Local data to production**  
  Curriculum is defined in code (`curriculum_config.py`, `assessment_config.py`). Production gets the same content by running `seed_data`; you do **not** need to copy data from your local DB. If you have custom content only in local DB, use Django’s `dumpdata`/`loaddata` for the relevant app labels, or add it to the config and re-run `seed_data`.
