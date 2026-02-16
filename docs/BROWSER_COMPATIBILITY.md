# Browser and device compatibility

CodeVenture auth and profile forms are built to work on **Safari/macOS**, **iOS**, **Chrome/Firefox/Edge**, and **all common viewport sizes**. This document describes the approach and what to preserve when changing forms or CSS.

## Form input behavior (“can’t type” fix)

### Problem

Users on some devices (notably Safari/macOS and some mobile browsers) reported being unable to type in sign-up or login fields. Typical causes:

- An overlay or stacking context capturing focus or pointer events.
- `user-select` or touch behavior preventing focus/keyboard.
- Relying on Django’s default form output (`as_p`) without explicit input structure and attributes.

### Approach

1. **Defensive CSS** (`UserManagement/static/css/login_register.css`):
   - `.login-container`: `position: relative; z-index: 1` so the form sits above any stray overlay.
   - `.login-form`: `touch-action: manipulation` so taps focus inputs immediately (no 300 ms delay on iOS).
   - All inputs/textarea/select inside `.login-container`: `user-select: text` (and `-webkit-user-select: text`) so typing is never blocked.
   - Text/email/password inputs: `-webkit-appearance: none; appearance: none` so WebKit doesn’t apply native overlays that block the keyboard.

2. **Explicit form markup**:
   - **Login**: Manual HTML with `autocomplete="username"` and `autocomplete="current-password"`.
   - **Registration**: Template renders each field with `.input-group`, proper `id`/`for`, `autocomplete`, and placeholders (no `form.as_p` for this form).
   - **Complete profile**: Fields rendered in a loop with the same `.input-group` structure so the same CSS and behavior apply.

3. **Viewport**: Base template uses `meta name="viewport" content="initial-scale=1, width=device-width"` without disabling zoom (accessibility).

When adding or changing auth/profile forms, keep these patterns so behavior stays consistent across devices.

---

## Birthday (date of birth) field

The student profile **birthday** field is implemented as a **text input plus calendar picker** (Flatpickr), not a native `input type="date"`.

### Why

- On **Safari/macOS**, the native date input often blocks keyboard entry; only the system picker or autofill works. This caused “can’t type” reports for the birthday field.
- A plain text input (`type="text"`) ensures typing works on all platforms. The calendar picker is added only on the complete-profile (student) page for better UX.

### Implementation

- **Backend:** `UserManagement.forms.StudentCreationForm` uses a `DateInput` subclass with `input_type = 'text'` and `attrs={'class': 'date-picker-input', ...}`; the server accepts ISO format `YYYY-MM-DD`.
- **Frontend:** On the complete-profile page for students, Flatpickr is loaded (CDN) and bound to `#id_birthday` with `dateFormat: 'Y-m-d'` and `allowInput: true` so both calendar and manual entry work.

### Maintenance

- Do not switch the birthday field back to a native `type="date"` without verifying keyboard entry on Safari/macOS.
- If replacing Flatpickr, keep the input as `type="text"` and preserve the `YYYY-MM-DD` value for the server.
