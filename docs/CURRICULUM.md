# Curriculum and Assessments

This document describes how learning modules, submodules, quizzes, and coding challenges are defined and seeded.

## Overview

- **Learning modules** (e.g. Basic Modules, Python Fundamentals, Computational Process Engineering) are top-level courses.
- **Submodules** are ordered lessons within a module; each has a video, description, and optional **quiz** and **challenges**.
- Data is driven by config files and seeded via `python manage.py seed_data`.

## Source of truth

| What | Where |
|------|--------|
| Modules and submodules (names, descriptions, video IDs) | `LearningResource/curriculum_config.py` → `MODULES` |
| CPE quizzes and challenges | `LearningResource/assessment_config.py` → `CPE_SUBMODULE_ASSESSMENTS` |
| Seeding logic | `LearningResource/management/commands/seed_data.py` |

## Adding or changing content

1. **New module or submodule**  
   Edit `curriculum_config.MODULES`: add or change a module dict (name, short_name, description, thumbnail, submodules list). Each submodule needs name, difficulty_level, description, video_name, video_id.

2. **New quizzes/challenges for a submodule**  
   Edit `assessment_config.py`. For CPE, add an entry keyed by submodule name under `CPE_SUBMODULE_ASSESSMENTS` with `quiz` (name, questions with text/points/choices) and/or `challenge` (name, description, hints, solution_code, std_in, expected_output).

3. **Apply changes**  
   - Without clearing: `python manage.py seed_data` (creates new modules/submodules, updates existing; CPE assessments are re-applied).  
   - Full reset: `python manage.py seed_data --clear` (removes all modules, submodules, videos, quizzes, challenges, then re-seeds from config).

## Current modules

- **Basic Modules** (short_name: basics) – Introduction to programming, variables, control flow, functions.
- **Python Fundamentals** (python) – Syntax, lists and dictionaries.
- **Web Development** (web) – HTML/CSS, JavaScript.
- **Computational Process Engineering** (cpe) – Python basics, NumPy, Pandas, Matplotlib, simulation & modelling, optimisation (SciPy). Each CPE submodule has a quiz and a coding challenge.

## Ordering

Submodules are ordered by the `prev_submodule` / `next_submodule` chain. The concept module page and CPE assessment seeding use `LearningModule.ordered_submodules()` to follow this order.
