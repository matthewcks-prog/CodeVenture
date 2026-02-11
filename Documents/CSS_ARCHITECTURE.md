# CSS Architecture Documentation

## Overview

CodeVenture uses a modular CSS architecture with shared base styles and module-specific customizations. This document outlines the structure, naming conventions, and best practices.

## File Structure

```
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

1. **global.css** - Loaded automatically in `base_generic.html`
2. **ModulesCommon.css** - Shared module styles (for module/quiz pages)
3. **Page-specific CSS** - Component-level styles

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

- `.learning-modules-page` - For basic module list pages (whitesmoke background)
- `.concept-modules-page` - For concept module list pages (whitesmoke background)
- `.concept-module-page` - For individual concept/quiz pages (oldlace background)
- `.submodule-page` - For lecture/submodule pages (oldlace background)

**Key Properties**:

```css
.concept-module-page {
    width: 100%;
    min-height: 100vh; /* Full viewport height */
    background-color: var(--color-oldlace);
    display: flex;
    flex-direction: column;
}
```

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
--spacing-sm: 0.5rem; /* 8px */
--spacing-md: 1rem; /* 16px */
--spacing-lg: 1.5rem; /* 24px */
--spacing-xl: 2rem; /* 32px */
--spacing-2xl: 3rem; /* 48px */
--spacing-3xl: 4rem; /* 64px */
```

## Component Classes (ModulesCommon.css)

### Module Container

```css
.module-container {
    max-width: 1200px; /* Constrain content width */
    margin: 0 auto; /* Center horizontally */
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

### Mobile-First Approach

All base styles are optimized for mobile, with desktop enhancements added via media queries.

### Breakpoints

```css
@media (max-width: 768px) {
    /* Tablet and below */
}
@media (max-width: 480px) {
    /* Mobile */
}
```

### Navbar Responsiveness

- **Desktop (>960px)**: Full navigation links visible
- **Tablet/Mobile (≤960px)**: Hamburger menu, links hidden

## Best Practices

### 1. Use Shared Styles First

Before creating page-specific CSS, check if ModulesCommon.css has the component you need.

### 2. Use CSS Variables

Always use CSS custom properties instead of hardcoded values:

```css
/* ✅ Good */
color: var(--color-steelblue-100);
padding: var(--spacing-md);

/* ❌ Bad */
color: #4682b4;
padding: 16px;
```

### 3. Apply Page Wrappers Correctly

Every module/quiz page template should:

1. Define `css-container` block with appropriate wrapper class
2. Use semantic inner container (`.module-container`, `.links4`, etc.)
3. Ensure backgrounds are consistent

### 4. Avoid Duplicate Styles

If multiple pages need the same component, add it to ModulesCommon.css.

### 5. Maintain Accessibility

- Use semantic HTML elements
- Ensure sufficient color contrast
- Provide descriptive alt text for icons
- Test with keyboard navigation

## Common Patterns

### Pattern: Module List Page

```html
{% extends 'base_generic.html' %} {% block css %}
<link rel="stylesheet" href="{% static 'css/ModulesCommon.css' %}" />
<link rel="stylesheet" href="{% static 'css/ConceptModulesPage.css' %}" />
{% endblock %} {% block css-container %} concept-modules-page {% endblock %} {%
block content %}
<div class="concept-modules-parent">
    <b class="concept-modules">Page Title</b>
    <!-- Grid of modules -->
</div>
{% endblock %}
```

### Pattern: Individual Module/Quiz Page

```html
{% extends 'base_generic.html' %} {% block css %}
<link rel="stylesheet" href="{% static 'css/ModulesCommon.css' %}" />
{% endblock %} {% block css-container %} concept-module-page {% endblock %} {%
block content %}
<div class="module-container">
    <header class="module-header">
        <div class="module-breadcrumb">
            <a href="...">Back</a> / <span>Current Page</span>
        </div>
        <h1 class="module-title">Page Title</h1>
    </header>

    <div class="module-content">
        <ol class="progress-list">
            <!-- List items -->
        </ol>
    </div>
</div>
{% endblock %}
```

## Troubleshooting

### Issue: Whitespace at Bottom of Page

**Cause**: Page wrapper missing or has incorrect `min-height`

**Solution**: Ensure template has `css-container` block with appropriate wrapper class:

```html
{% block css-container %} concept-module-page {% endblock %}
```

### Issue: Missing Styles

**Cause**: CSS file not imported or wrong classes used

**Solution**:

1. Import ModulesCommon.css in template
2. Verify class names match ModulesCommon.css components
3. Check browser DevTools Console for CSS 404 errors

### Issue: Content Not Centered

**Cause**: Incorrect or missing inner container

**Solution**: Wrap content in `.module-container`:

```html
<div class="module-container">
    <!-- Your content -->
</div>
```

## Migration Guide

### Migrating from Old CSS to New Architecture

1. **Identify the page type** (module list, quiz list, individual module, etc.)
2. **Choose appropriate wrapper class** from ModulesCommon.css
3. **Update template `css-container` block** to use wrapper class
4. **Replace old component classes** with ModulesCommon.css equivalents
5. **Import ModulesCommon.css** in template CSS block
6. **Remove obsolete CSS files** after migration complete
7. **Test responsiveness** on mobile, tablet, desktop

### Example Migration: quiz_list.html

**Before**:

```html
{% block css %}
<link rel="stylesheet" href="{% static 'css/ConceptModule.css' %}" />
{% endblock %} {% block css-container %}concept-module{% endblock %} {% block
content %}
<div class="sub-modules-overview-parent">
    <b class="artificial-intelligence">{{ module.name }}</b>
    <ol class="progress-in-module1">
        ...
    </ol>
</div>
{% endblock %}
```

**After**:

```html
{% block css %}
<link rel="stylesheet" href="{% static 'css/ModulesCommon.css' %}" />
{% endblock %} {% block css-container %}concept-module-page{% endblock %} {%
block content %}
<div class="module-container">
    <header class="module-header">
        <h1 class="module-title">{{ module.name }}</h1>
    </header>
    <div class="module-content">
        <ol class="progress-list">
            ...
        </ol>
    </div>
</div>
{% endblock %}
```

## Maintenance

### When to Update This Documentation

- Adding new page wrapper classes
- Creating new shared components in ModulesCommon.css
- Changing CSS custom property values
- Modifying responsive breakpoints
- Adding new CSS files to the architecture

### Code Review Checklist

- [ ] Uses CSS custom properties (variables)
- [ ] Applies appropriate page wrapper class
- [ ] No hardcoded colors or spacing values
- [ ] Imports ModulesCommon.css when using shared components
- [ ] Responsive design tested on mobile, tablet, desktop
- [ ] No duplicate CSS rules across files
- [ ] Semantic HTML elements used
- [ ] Accessibility considerations addressed
