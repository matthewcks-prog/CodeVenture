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

For a detailed list of functional requirements, see:  
`Documents/Main features implemented for Code Venture.pdf`.

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

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

Then visit `http://localhost:8000/` in your browser.

---

## Environment Configuration 🌱

Key environment variables (see `.env.example` for the full list):

- **DJANGO_SECRET_KEY** – required in production  
- **DJANGO_DEBUG** – `True`/`False`  
- **DJANGO_ALLOWED_HOSTS** – comma-separated, e.g. `localhost,127.0.0.1,codeventure.onrender.com`  
- **DJANGO_CSRF_TRUSTED_ORIGINS** – comma-separated origins with scheme, e.g. `https://codeventure.onrender.com`  
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

### 2. Attach a PostgreSQL database

1. In Render, create a **PostgreSQL** instance (Free tier is fine for demos).  
2. Once created, copy the generated `DATABASE_URL`.  
3. In the `codeventure` service settings, add an environment variable:
   - **Key**: `DATABASE_URL`
   - **Value**: the value from the Postgres instance.

Render will automatically inject this into the app during build and runtime.

### 3. Configure Django environment on Render

Add these environment variables in the Render dashboard for the `codeventure` service:

- `DJANGO_SECRET_KEY` – long random string.
- `DJANGO_DEBUG` – `False`.
- `DJANGO_ALLOWED_HOSTS` – e.g. `codeventure.onrender.com`.
- `DJANGO_CSRF_TRUSTED_ORIGINS` – e.g. `https://codeventure.onrender.com`.

The `render.yaml` file configures:

- **Build command**:
  - `pip install -r requirements.txt`
  - `python manage.py collectstatic --noinput`
  - `python manage.py migrate --noinput`
- **Start command**:
  - `gunicorn CodeVenture.wsgi:application`

Static assets are served by **WhiteNoise** via Django’s `STATIC_ROOT` (`staticfiles/`).

### 4. Verifying the deployment

After deployment:

1. Visit the Render URL (e.g. `https://codeventure.onrender.com`).
2. Ensure that static assets (CSS, images) load correctly.
3. Run in the Render shell (or locally with the same env vars):
   - `python manage.py check --deploy`
   - `python manage.py collectstatic --noinput`
   - `python manage.py migrate --noinput`

Any failing checks should be reviewed; the current configuration aims to satisfy Django’s standard deployment checklist when `DJANGO_DEBUG=False`.

---

## Testing Instructions 🧪

To thoroughly test the platform, four example user accounts are provided:

- **Admin**
  - Username: `admin`
  - Password: `Codeventure2023`

- **Student**
  - Username: `studentaccount`
  - Password: `Codeventure2023`

- **Parent**
  - Username: `parentaccount`
  - Password: `Codeventure2023`

- **Teacher**
  - Username: `teacheraccount`
  - Password: `Codeventure2023`

> These example credentials are for demo environments only; do **not** reuse them in production.

You can also run the automated test suite locally:

```bash
pytest
```

---

## License 📝

This project is licensed under the MIT License. For more information, see the [`LICENSE`](LICENSE) file in this repository.

