# CSS Architecture Documentation

(moved from `Documents/CSS_ARCHITECTURE.md` to live under `docs/` to better
reflect that this is project documentation rather than runtime assets.)

```note
If you update CSS structure, page wrappers, or shared components, please
update this document as part of the same pull request.
```

## Overview

CodeVenture uses a modular CSS architecture with shared base styles and
module-specific customizations. This document outlines the structure,
naming conventions, and best practices.

## File Structure

```text
CodeVenture/
├── WelcomePage/static/css/
│   └── global.css                    # Global variables, reset, navbar, utilities
├── LearningResource/static/css/
│   ├── ModulesCommon.css             # Shared styles for all module pages
│   ├── BasicModulesPage.css          # Basic modules list page specific
│   ├── ConceptModulesPage.css        # Concept modules list page specific
│   └── Submodules.css                # Submodule/lecture page specific
└── QuizChallengeSystem/static/css/
    ├── quiz.css                      # Quiz taking interface
    ├── quiz_result.css               # Quiz results page
    └── QuizSummary.css               # Quiz summary page
```

## CSS Loading Order

Templates should import CSS in this order:

1. **global.css** – Loaded automatically in `base_generic.html`.
2. **ModulesCommon.css** – Shared module styles (for module/quiz pages).
3. **Page-specific CSS** – Component-level styles.

**Example** (`quiz_list.html`):

```html
{% block css %}
<link rel="stylesheet" href="{% static 'css/ModulesCommon.css' %}" />
<!-- Page-specific CSS would go here if needed -->
{% endblock %}
```

## Page Wrapper Pattern

All module and quiz pages use a two-layer wrapper system:

### 1. Outer Page Wrapper (Applied via `css-container` block)

Defines the full-page background and minimum height:

```html
{% block css-container %} concept-module-page {% endblock %}
```

**Available Wrapper Classes**:

- `.learning-modules-page` – For basic module list pages (whitesmoke background).
- `.concept-modules-page` – For concept module list pages (whitesmoke background).
- `.concept-module-page` – For individual concept/quiz pages (oldlace background).
- `.submodule-page` – For lecture/submodule pages (oldlace background).

### 2. Inner Content Container

Contains the actual page content with max-width and centering:

```html
<div class="module-container">
    <!-- Page content -->
</div>
```

Or for list pages:

```html
<div class="links4">
    <!-- For BasicModulesPage -->
    <!-- or -->
    <div class="concept-modules-parent">
        <!-- For ConceptModulesPage -->
        <!-- Page content -->
    </div>
</div>
```

## CSS Custom Properties (Variables)

### Layout Constants

```css
--navbar-height: 112px; /* Standard navbar height */
```

### Color Palette

**Learning Module Colors**:

```css
--color-oldlace: #fdf5e6; /* Warm cream background for content */
--color-whitesmoke: #f5f5f5; /* Light grey for list pages */
--color-gainsboro-100: #dcdcdc; /* Light grey for sections */
--color-darkseagreen: #8fbc8f; /* Green for buttons */
--color-deepskyblue: #00bfff; /* Blue for primary actions */
--color-steelblue-100: #4682b4; /* Steel blue for text/links */
```

### Spacing

```css
--spacing-xs: 0.25rem; /* 4px */
--spacing-sm: 0.5rem;  /* 8px */
--spacing-md: 1rem;    /* 16px */
--spacing-lg: 1.5rem;  /* 24px */
--spacing-xl: 2rem;    /* 32px */
--spacing-2xl: 3rem;   /* 48px */
--spacing-3xl: 4rem;   /* 64px */
```

## Component Classes (ModulesCommon.css)

### Module Container

```css
.module-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-lg) var(--spacing-md);
    width: 100%;
    background-color: var(--color-oldlace);
}
```

### Module Header

```css
.module-header {
    text-align: center;
    margin-bottom: var(--spacing-lg);
}

.module-title {
    font-size: var(--font-size-3xl);
    font-weight: 700;
    color: var(--color-brand-dark);
}

.module-breadcrumb {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    font-size: var(--font-size-sm);
}
```

### Progress List (Used for quizzes/sub-modules)

```css
.progress-list {
    list-style: none;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: var(--spacing-xl);
    max-width: 800px;
    margin: 0 auto;
}

.progress-item {
    display: flex;
    align-items: center;
    gap: var(--spacing-xl);
}

.progress-icon {
    width: 65px;
    height: 65px;
    border-radius: 50%;
    background-color: var(--neutral-4);
}

.progress-link {
    flex-grow: 1;
    font-size: var(--font-size-lg);
    font-weight: 500;
    color: var(--color-steelblue-300);
}
```

## Responsive Design Strategy

- Mobile-first base styles.
- Enhancements via media queries:

```css
@media (max-width: 768px) {
    /* Tablet and below */
}
@media (max-width: 480px) {
    /* Mobile */
}
```

## Best Practices

- Prefer shared styles in `ModulesCommon.css` before writing page-specific CSS.
- Use CSS variables instead of hardcoded values.
- Ensure each module/quiz page:
  - Defines `css-container` with the correct wrapper class.
  - Wraps content with `.module-container` / `.links4` / `.concept-modules-parent`.
- Avoid duplicate rules; refactor into shared components.
- Maintain accessibility (semantic HTML, contrast, keyboard, alt text).

## Maintenance Checklist

- [ ] Uses CSS custom properties.
- [ ] Applies an appropriate page wrapper class.
- [ ] Imports `ModulesCommon.css` when using shared components.
- [ ] No duplicated styles across files.
- [ ] Responsive behaviour tested on mobile, tablet, desktop.

