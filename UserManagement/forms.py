"""
User Management Forms.

StudentCreationForm uses a text-based date input with calendar picker support
to avoid Safari/macOS issues where native type="date" blocks keyboard input.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Student, Parent, Teacher


# ISO date format for backend and frontend consistency (accessibility, APIs).
BIRTHDAY_INPUT_FORMAT = '%Y-%m-%d'


class DateTextInput(forms.DateInput):
    """Date input that renders as type="text" for Mac/Safari keyboard entry."""
    input_type = 'text'


class BasicRegistrationForm(UserCreationForm):
    # Extend UserCreationForm to include additional fields (email, first_name, last_name).
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')


class StudentCreationForm(forms.ModelForm):
    # Form for creating or updating student profiles.
    # Birthday: explicit type="text" + calendar picker (Flatpickr) for cross-platform
    # reliability (Safari/macOS native date input blocks keyboard entry).
    birthday = forms.DateField(
        input_formats=[BIRTHDAY_INPUT_FORMAT],
        help_text='Use the calendar to pick a date, or enter YYYY-MM-DD.',
        widget=DateTextInput(
            format=BIRTHDAY_INPUT_FORMAT,
            attrs={
                'placeholder': 'YYYY-MM-DD',
                'class': 'date-picker-input',
                'autocomplete': 'bday',
            },
        ),
    )
    coding_experience = forms.ChoiceField(choices=Student.EXPERIENCE_CHOICES)
    parent_email = forms.EmailField(required=False)

    class Meta:
        model = Student
        fields = ('birthday', 'coding_experience', 'parent_email')


class ParentCreationForm(forms.ModelForm):
    # Form for creating or updating parent profiles.
    children_email = forms.EmailField(required=False)

    class Meta:
        model = Parent
        fields = ('children_email',)
