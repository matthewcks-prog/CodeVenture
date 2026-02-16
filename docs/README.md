## Documentation Overview

This `docs/` folder centralizes project documentation for **CodeVenture**.

### Contents

- `AUTH_AND_ONBOARDING_FLOW.md` – login, signup, role selection, profile completion, and home redirect logic (single source of truth for onboarding).
- `OAUTH_AND_GOOGLE.md` – Google OAuth setup, redirect URIs (callback URL), and fixing redirect_uri_mismatch (single source of truth for OAuth).
- `CSS_ARCHITECTURE.md` – explanation of the shared CSS architecture and layout patterns used across learning modules and quizzes.
- `BROWSER_COMPATIBILITY.md` – browser and device compatibility notes (e.g. birthday field and Safari/macOS).
- `CURRICULUM.md` – how modules, submodules, quizzes, and challenges are defined and seeded (curriculum_config, assessment_config, seed_data).
- `DEPLOYMENT.md` – Render deployment, env vars, and troubleshooting (e.g. 500 on basic_module, seeding).

### Conventions

- Keep high-level project and setup information in the root `README.md`.
- Use `docs/` for architectural notes, deep dives, and maintenance guides.
- When adding new technical documentation, prefer placing it here and link to it from the root `README.md` if it is important for contributors.

