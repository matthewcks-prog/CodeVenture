## CodeVenture - Learn Python the Fun Way! 🐍🎮

### Overview

**CodeVenture** is an engaging and interactive platform aimed at young learners to make Python programming not just educational, but also fun and exciting. The platform incorporates game-like elements, quizzes, interactive tutorials, and weekly progress tracking to make learning Python a thrill.

![CodeVenture Screenshot](assets/homepage.png)

### Features 🌟

- **Welcome Page**
  - Simple and secure login and sign-up features.
  - **Google OAuth Integration** (via `django-allauth`) for easy sign-in.

- **Learning Modules**
  - Lessons tailored to enhance the Python programming skills of learners.

- **Quizzes & Challenges**
  - Comprehensive quizzes after each module.
  - Real-world style coding challenges from beginner to advanced.

- **Python Playground**
  - Integrated IDE environment (Monaco-based) where students can practice Python coding in real-time.
  - Safely execute Python scripts and see immediate results.

- **Progress Report**
  - PDF exports and reports to help track learning milestones and areas for improvement.

- **Feedback**
  - Feedback form at the bottom of the page to gather suggestions and improvements.

### Tech Stack

- **Backend**: Django 4.2
- **Auth**: `django-allauth` with Google OAuth
- **Database**:
  - Local: SQLite (by default) or MySQL (via `DATABASE_URL`)
  - Production: PostgreSQL on Render (recommended)
- **Static Files**: Django staticfiles + WhiteNoise
- **Testing/CI**: `pytest`, `pytest-django`, GitHub Actions

For more detailed architecture notes, see the `docs/` folder:

- [CSS Architecture](docs/CSS_ARCHITECTURE.md)

---

## Local Development 🚀

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/CodeVenture.git
cd CodeVenture
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and edit as needed:

```bash
cp .env.example .env  # On Windows: copy .env.example .env
```

Update `.env` with:

- `DJANGO_SECRET_KEY` – any random string for local dev.
- `DJANGO_DEBUG` – `True` for local.
- `DATABASE_URL` – usually leave blank to use SQLite locally.
- `GOOGLE_OAUTH_CLIENT_ID` – from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- `GOOGLE_OAUTH_CLIENT_SECRET` – from Google Cloud Console

**Google OAuth:** Redirect URIs in Google Console must be the **callback** URL (path `/accounts/google/login/callback/`), not the login page. See **[docs/OAUTH_AND_GOOGLE.md](docs/OAUTH_AND_GOOGLE.md)** for exact URIs and fixing `redirect_uri_mismatch`.

### 5. Apply migrations and seed data

```bash
# Apply database migrations
python manage.py migrate

# Create admin user and seed learning modules
python manage.py seed_data --admin
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then visit `http://localhost:8000/` in your browser.

**Access admin panel**: `http://localhost:8000/admin/`
- Username: `admin`
- Password: `superuser`

---

## Environment Configuration 🌱

Key environment variables (see `.env.example` for the full list):

- **DJANGO_SECRET_KEY** – required in production  
- **DJANGO_DEBUG** – `True`/`False`  
- **DJANGO_ALLOWED_HOSTS** – comma-separated, e.g. `localhost,127.0.0.1,codeventure-ez4m.onrender.com`  
- **DJANGO_CSRF_TRUSTED_ORIGINS** – comma-separated origins with scheme, e.g. `https://codeventure-ez4m.onrender.com`  
- **DJANGO_SITE_DOMAIN** – (production) domain for Sites framework and OAuth; set to your Render host, e.g. `codeventure-ez4m.onrender.com`  
- **DATABASE_URL**
  - Local default: SQLite if unset.
  - MySQL example: `mysql://user:password@host:3306/codeventure-db`
  - Postgres example: `postgres://user:password@host:5432/codeventure`

In production, you must set a strong `DJANGO_SECRET_KEY`, disable `DJANGO_DEBUG`, and configure `DJANGO_ALLOWED_HOSTS` and `DJANGO_CSRF_TRUSTED_ORIGINS`.

---

## Render Deployment 🌐

This repo includes a `render.yaml` blueprint for one-click deployment to Render.

### 1. Create a new Render Web Service

1. Push this repository to GitHub.
2. In the Render dashboard, choose **New → Blueprint** and point it at your GitHub repo.
3. Render will detect `render.yaml` and propose a **Python web service** named `codeventure`.

### 2. Database (PostgreSQL)

**If using the blueprint** (`render.yaml`): a PostgreSQL database can be linked to the web service. Render then sets `DATABASE_URL` automatically from the linked database’s connection string (no manual env var needed).

**If using an existing Postgres instance:** in the `codeventure` service, add an environment variable:
- **Key**: `DATABASE_URL`
- **Value**: your PostgreSQL connection URL (e.g. `postgresql://user:password@host/dbname`).

Migrations and curriculum seeding run during **every build** (see below), so the app will have the correct schema and learning modules (Basic Modules, concept modules, CPE) without manual steps.

### 3. Configure Django environment on Render

Add these environment variables in the Render dashboard for the `codeventure` service:

- `DJANGO_SECRET_KEY` – long random string (e.g. `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- `DJANGO_DEBUG` – `False`
- `DJANGO_ALLOWED_HOSTS` – your service host, e.g. `codeventure-ez4m.onrender.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS` – same origin with scheme, e.g. `https://codeventure-ez4m.onrender.com`
- `DJANGO_SITE_DOMAIN` – same as host (e.g. `codeventure-ez4m.onrender.com`); used by OAuth and Sites
- `GOOGLE_OAUTH_CLIENT_ID` – Google OAuth Client ID
- `GOOGLE_OAUTH_CLIENT_SECRET` – Google OAuth Client Secret

In [Google Cloud Console](https://console.cloud.google.com/apis/credentials), add **Authorised redirect URI** `https://<your-render-host>/accounts/google/login/callback/` (see [docs/OAUTH_AND_GOOGLE.md](docs/OAUTH_AND_GOOGLE.md)).

The build is driven by `build.sh`, which:

- Installs dependencies, collects static files, fixes migration history, runs **migrations**, configures the Sites record, and runs **`seed_data`** (learning modules, submodules, and CPE assessments). Seeding is idempotent and safe on every deploy.
- **Start command**: `gunicorn CodeVenture.wsgi:application` (see `render.yaml`).

Static assets are served by **WhiteNoise** via Django’s `STATIC_ROOT` (`staticfiles/`). No manual database seeding is required for modules to appear; to create the default admin user, run once in the Render shell: `python manage.py seed_data --admin`.

### 4. Verifying the deployment

After deployment:

1. Visit the Render URL (e.g. `https://codeventure-ez4m.onrender.com`).
2. Log in and open **Learning Modules → Basic modules**; you should see the curriculum (no 500 error). If you see a 500 or empty modules, ensure a deploy completed (build runs `seed_data`) or run `python manage.py seed_data` once in the Render shell. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for details.
3. Run in the Render shell: `python manage.py check --deploy`.

Any failing checks should be reviewed; the current configuration aims to satisfy Django’s standard deployment checklist when `DJANGO_DEBUG=False`.

---

## Admin Access 👨‍💼

### Creating Admin User

To create an admin superuser, run:

```bash
python manage.py seed_data --admin
```

Default credentials:
- **Username**: `admin`
- **Password**: `superuser`
- **Email**: `admin@codeventure.com`

### Accessing Admin Panel

**Local Development:**
- Visit: `http://localhost:8000/admin/`
- Login with admin credentials

**Production (Render):**
- Visit: `https://your-app-name.onrender.com/admin/`
- Example: `https://codeventure-ez4m.onrender.com/admin/`

> **Important**: Change the default admin password immediately after first login!

### Seeding Sample Data

To populate the database with learning modules:

```bash
# Seed only (requires existing admin user)
python manage.py seed_data

# Seed and create admin user
python manage.py seed_data --admin

# Clear and reseed everything
python manage.py seed_data --admin --clear
```

This creates:
- 3 learning modules (Basic Modules, Python Fundamentals, Web Development)
- 8 submodules with video tutorials
- Admin superuser account

---

## Testing Instructions 🧪

You can run the automated test suite locally:

```bash
pytest
```

---

## License 📝

This project is licensed under the MIT License. For more information, see the [`LICENSE`](LICENSE) file in this repository.

