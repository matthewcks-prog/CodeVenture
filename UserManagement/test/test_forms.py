"""
Tests for UserManagement forms.

Validates birthday field behavior: widget type, input format, validation,
and compatibility with calendar picker (Flatpickr) and manual entry.
"""
import pytest
from django import forms

from UserManagement.forms import (
    BIRTHDAY_INPUT_FORMAT,
    StudentCreationForm,
    ParentCreationForm,
    BasicRegistrationForm,
)


# -----------------------------------------------------------------------------
# StudentCreationForm — birthday field (Mac/Safari fix: text + calendar)
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_student_creation_form_birthday_valid_iso():
    """Birthday accepts ISO date YYYY-MM-DD."""
    data = {
        'birthday': '2010-05-15',
        'coding_experience': 'No experience',
    }
    form = StudentCreationForm(data=data)
    assert form.is_valid(), form.errors
    assert str(form.cleaned_data['birthday']) == '2010-05-15'


@pytest.mark.django_db
def test_student_creation_form_birthday_invalid_format():
    """Birthday rejects non-ISO formats (e.g. MM/DD/YYYY)."""
    data = {
        'birthday': '05/15/2010',
        'coding_experience': 'No experience',
    }
    form = StudentCreationForm(data=data)
    assert not form.is_valid()
    assert 'birthday' in form.errors


@pytest.mark.django_db
def test_student_creation_form_birthday_empty():
    """Birthday is required."""
    data = {
        'birthday': '',
        'coding_experience': 'No experience',
    }
    form = StudentCreationForm(data=data)
    assert not form.is_valid()
    assert 'birthday' in form.errors


@pytest.mark.django_db
def test_student_creation_form_birthday_invalid_date():
    """Birthday rejects invalid date strings."""
    data = {
        'birthday': 'not-a-date',
        'coding_experience': 'No experience',
    }
    form = StudentCreationForm(data=data)
    assert not form.is_valid()
    assert 'birthday' in form.errors


def test_student_creation_form_birthday_widget_type_text():
    """Birthday widget uses type="text" for Mac/Safari keyboard entry."""
    form = StudentCreationForm()
    widget = form.fields['birthday'].widget
    assert getattr(widget, 'input_type', widget.attrs.get('type')) == 'text'


def test_student_creation_form_birthday_widget_has_date_picker_class():
    """Birthday widget has class for Flatpickr binding."""
    form = StudentCreationForm()
    widget = form.fields['birthday'].widget
    assert 'date-picker-input' in widget.attrs.get('class', '')


def test_student_creation_form_birthday_input_format():
    """Birthday uses single ISO format for consistency."""
    assert BIRTHDAY_INPUT_FORMAT == '%Y-%m-%d'


# -----------------------------------------------------------------------------
# Other forms — smoke checks
# -----------------------------------------------------------------------------


@pytest.mark.django_db
def test_parent_creation_form_valid():
    """ParentCreationForm accepts optional children_email."""
    form = ParentCreationForm(data={'children_email': ''})
    assert form.is_valid()


@pytest.mark.django_db
def test_basic_registration_form_required_fields():
    """BasicRegistrationForm requires username, email, passwords."""
    form = BasicRegistrationForm(data={})
    assert not form.is_valid()
    assert 'username' in form.errors or 'password1' in form.errors
