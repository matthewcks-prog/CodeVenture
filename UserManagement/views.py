"""
User Management Views
Handles authentication, registration, and profile management with proper error handling.
"""
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction

from .models import Student, Teacher, Parent
from .forms import StudentCreationForm, ParentCreationForm, BasicRegistrationForm

logger = logging.getLogger(__name__)

def login_view(request):
    """
    Handle user login with comprehensive validation and error handling.
    
    Security features:
    - Rate limiting should be implemented at middleware level
    - Prevents user enumeration by not revealing if username exists
    - Logs failed login attempts for security monitoring
    """
    page = 'login'
    
    # Redirect authenticated users to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        # Validate input presence
        if not username or not password:
            messages.error(request, 'Both username and password must be provided.')
            logger.warning(f"Login attempt with missing credentials from IP: {request.META.get('REMOTE_ADDR')}")
            return render(request, 'login_register.html', {'page': page})

        try:
            # Authenticate user
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                logger.info(f"Successful login for user: {username}")
                
                # Redirect to next URL if specified, otherwise home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                # Don't reveal if user exists or password is wrong (prevent user enumeration)
                messages.error(request, 'Invalid username or password.')
                logger.warning(f"Failed login attempt for username: {username}")
                
        except Exception as e:
            logger.error(f"Login error for user {username}: {str(e)}", exc_info=True)
            messages.error(request, 'An error occurred during login. Please try again.')
    
    context = {'page': page}
    return render(request, 'login_register.html', context)


def logout_user(request):
    """
    Handle user logout with proper session cleanup.
    Clears all messages and session data before logout.
    """
    try:
        # Clear any pending messages
        storage = messages.get_messages(request)
        storage.used = True
        
        # Log the logout event
        if request.user.is_authenticated:
            logger.info(f"User logged out: {request.user.username}")
        
        logout(request)
        messages.success(request, 'You have been successfully logged out.')
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}", exc_info=True)
    
    return redirect('home')


def register_user(request, user_type=None):
    """
    Register a new user with specified role (student, parent, teacher).
    
    Uses database transactions to ensure atomicity - either all profile
    data is created or none of it is, preventing orphaned records.
    
    Args:
        request: HTTP request object
        user_type: Type of user account ('student', 'parent', or 'teacher')
        
    Raises:
        Http404: If invalid user_type is provided
    """
    # Validate user type
    VALID_USER_TYPES = ['student', 'parent', 'teacher']
    if user_type not in VALID_USER_TYPES:
        logger.warning(f"Invalid user type requested: {user_type}")
        raise Http404("User Type not found")

    # Redirect if already authenticated
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('home')

    form = BasicRegistrationForm()

    if request.method == 'POST':
        form = BasicRegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                # Use atomic transaction to ensure data consistency
                with transaction.atomic():
                    # Create user account
                    user = form.save(commit=False)
                    user.email = user.email.lower()  # Normalize email
                    user.save()
                    
                    # Create corresponding profile based on user type
                    profile = None
                    if user_type == 'student':
                        profile = Student.objects.create(user=user)
                    elif user_type == 'parent':
                        profile = Parent.objects.create(user=user)
                    elif user_type == 'teacher':
                        profile = Teacher.objects.create(user=user)
                    
                    logger.info(f"New {user_type} user created: {user.username}")
                    
                    # Log in the newly created user
                    login(request, user)
                    messages.success(
                        request,
                        f'Welcome {user.first_name}! Please complete your profile.'
                    )
                    
                    # Redirect to profile completion
                    return redirect('complete_profile')
                    
            except ValidationError as e:
                logger.warning(f"Validation error during registration: {str(e)}")
                messages.error(request, 'Please correct the errors below.')
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}", exc_info=True)
                messages.error(
                    request,
                    'An error occurred during registration. Please try again.'
                )
        else:
            # Form validation failed
            logger.warning(f"Invalid registration form submission for {user_type}")
            messages.error(request, 'Please correct the errors in the form.')

    context = {
        'form': form,
        'user_type': user_type,
        'page': 'register'
    }
    return render(request, 'login_register.html', context)


@login_required(login_url='/login/')
def complete_profile(request):
    """
    Allow authenticated users to complete their profile information.
    
    Handles different profile types (Student, Parent, Teacher) with
    appropriate forms and validation. Uses transactions for data integrity.
    """
    user = request.user

    # Determine user type and appropriate form
    if hasattr(user, 'student'):
        form_class = StudentCreationForm
        user_type = 'student'
    elif hasattr(user, 'parent'):
        form_class = ParentCreationForm
        user_type = 'parent'
    elif hasattr(user, 'teacher'):
        # Teachers don't need additional profile info
        messages.info(request, 'Your account is ready to use!')
        return redirect('home')
    else:
        # User has no profile type set, redirect to role selection
        logger.warning(f"User {user.username} has no profile type")
        messages.warning(request, 'Please select your role to continue.')
        return redirect('choose_user_type')

    if request.method == 'POST':
        form = form_class(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    if user_type == 'student':
                        # Update student profile
                        student = user.student
                        student.birthday = form.cleaned_data.get('birthday')
                        student.coding_experience = form.cleaned_data.get('coding_experience')
                        student.parent_email = form.cleaned_data.get('parent_email')
                        student.profile_completed = True

                        # Attempt to link parent if email provided
                        parent_email = form.cleaned_data.get('parent_email')
                        if parent_email:
                            try:
                                parent = Parent.objects.get(
                                    user__email__iexact=parent_email.lower()
                                )
                                student.parent = parent
                                logger.info(f"Linked student {user.username} to parent {parent.user.username}")
                            except ObjectDoesNotExist:
                                messages.warning(
                                    request,
                                    f'No parent account found with email: {parent_email}. '
                                    'You can link later when they create an account.'
                                )
                            except Parent.MultipleObjectsReturned:
                                logger.error(f"Multiple parents found with email: {parent_email}")
                                messages.error(request, 'Multiple accounts found with that email.')

                        student.save()
                        messages.success(request, 'Profile completed successfully!')
                        logger.info(f"Student profile completed: {user.username}")

                    elif user_type == 'parent':
                        # Update parent profile
                        parent = user.parent
                        parent.profile_completed = True
                        children_email = form.cleaned_data.get('children_email')
                        
                        if children_email:
                            try:
                                student = Student.objects.get(
                                    user__email__iexact=children_email.lower()
                                )
                                student.parent = parent
                                student.save()
                                logger.info(f"Linked parent {user.username} to student {student.user.username}")
                                messages.success(
                                    request,
                                    f'Successfully linked to student: {student.user.get_full_name()}'
                                )
                            except ObjectDoesNotExist:
                                messages.warning(
                                    request,
                                    f'No student account found with email: {children_email}. '
                                    'You can link later when they create an account.'
                                )
                            except Student.MultipleObjectsReturned:
                                logger.error(f"Multiple students found with email: {children_email}")
                                messages.error(request, 'Multiple accounts found with that email.')
                        
                        parent.save()
                        messages.success(request, 'Profile completed successfully!')
                        logger.info(f"Parent profile completed: {user.username}")

                    return redirect('home')
                    
            except ValidationError as e:
                logger.warning(f"Validation error in profile completion: {str(e)}")
                messages.error(request, 'Please correct the errors below.')
            except Exception as e:
                logger.error(f"Error completing profile for {user.username}: {str(e)}", exc_info=True)
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = form_class()

    context = {
        'form': form,
        'user_type': user_type,
        'page': 'complete_profile'
    }
    return render(request, 'login_register.html', context)


def choose_user_type(request):
    """
    Allow users to select or change their role (student, parent, teacher).
    
    For new users: redirects to registration with selected role
    For existing users: changes their role (useful for OAuth users without role)
    """
    if request.method != 'POST':
        return render(request, 'SelectRoleForm.html')

    selected_role = request.POST.get('role', '').strip().lower()
    
    # Validate role selection
    VALID_ROLES = ['student', 'parent', 'teacher']
    if selected_role not in VALID_ROLES:
        messages.error(request, 'Please select a valid role.')
        return render(request, 'SelectRoleForm.html')

    # For unauthenticated users, redirect to registration
    if not request.user.is_authenticated:
        return redirect('register_user', user_type=selected_role)

    # For authenticated users (e.g., OAuth users), create/update role
    try:
        with transaction.atomic():
            user = request.user
            
            # Remove existing roles (allows role switching)
            if hasattr(user, 'student'):
                user.student.delete()
                logger.info(f"Removed student role for {user.username}")
            if hasattr(user, 'parent'):
                user.parent.delete()
                logger.info(f"Removed parent role for {user.username}")
            if hasattr(user, 'teacher'):
                user.teacher.delete()
                logger.info(f"Removed teacher role for {user.username}")

            # Create new role
            if selected_role == 'student':
                Student.objects.create(user=user)
                logger.info(f"Created student role for {user.username}")
                messages.success(request, 'Student account created! Please complete your profile.')
                return redirect('complete_profile')
            elif selected_role == 'parent':
                Parent.objects.create(user=user)
                logger.info(f"Created parent role for {user.username}")
                messages.success(request, 'Parent account created! Please complete your profile.')
                return redirect('complete_profile')
            elif selected_role == 'teacher':
                Teacher.objects.create(user=user)
                logger.info(f"Created teacher role for {user.username}")
                messages.success(request, 'Teacher account created!')
                return redirect('home')
                
    except Exception as e:
        logger.error(f"Error setting user role for {user.username}: {str(e)}", exc_info=True)
        messages.error(request, 'An error occurred while setting your role. Please try again.')
        return render(request, 'SelectRoleForm.html')

    # Fallback return
    return render(request, 'SelectRoleForm.html')

