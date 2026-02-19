## Assets Overview

This folder stores product screenshots and other visual assets used across:

- The root `README.md` and project documentation
- Portfolio case studies and slide decks
- Store/listing pages (e.g. university showcase, demo sites)

All images in this folder are **source of truth** for CodeVenture’s visual narrative.

---

## Current Screenshots

| File                         | Purpose / View                                         | Suggested Caption                                  |
|-----------------------------|--------------------------------------------------------|----------------------------------------------------|
| `welcome_page.png`          | First-touch welcome/hero screen                        | “Welcome screen introducing the CodeVenture journey” |
| `sign_up_page.png`          | Registration / account creation flow                   | “Student sign-up flow with simple onboarding”      |
| `home.png`                  | Main home/dashboard after login                        | “Student dashboard with quick access to modules”   |
| `learning_module.png`       | Learning module detail page / lesson view              | “Interactive Python learning module in progress”   |
| `quizzes.png`               | Quiz selection or in-progress quiz                     | “Auto-graded quizzes reinforcing each concept”     |
| `challenges.png`            | Coding challenges / practice area                      | “Project-style coding challenges for deeper practice” |
| `python_playground.png`     | In-browser Python playground (Monaco-based editor)     | “Python playground where students can run code safely” |

These filenames are used in documentation; avoid renaming them without updating references.

---

## How to Add or Update Assets

1. **Capture screenshots**
   - Prefer a **16:9** aspect ratio where possible.
   - Hide any sensitive or personally identifiable information.
   - Use a neutral or dark theme consistently across screenshots.

2. **File format & size**
   - Use **PNG** for UI screenshots (crisp text, lossless).
   - Keep individual files under **1–2 MB** to avoid bloating the repo.

3. **Naming convention**
   - Use **lowercase**, words separated by underscores:  
     - `section_purpose.png` (e.g. `progress_report.png`, `admin_dashboard.png`)
   - Keep names stable once referenced from:
     - `README.md`
     - `docs/` files
     - Portfolio case studies

4. **Versioning changes**
   - When replacing a screenshot with the **same context** (e.g. new UI for home page), keep the filename and overwrite the image.
   - When adding a **new context**, create a new filename (e.g. `home_teacher_view.png` vs `home_student_view.png`).

---

## Referencing These Assets

- In Markdown (root `README.md`, docs, or portfolio):
  - `![CodeVenture Home](assets/home.png)`
  - `![Python Playground](assets/python_playground.png)`
- In slide decks or docs outside this repo, keep the captions aligned with the table above so messaging is consistent.

If you add more assets, update the table in this file so future contributors (and your future self) know what each screenshot is for.

