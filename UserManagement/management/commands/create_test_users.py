"""
Management command to create test users for each role.

Usage:
    python manage.py create_test_users
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from UserManagement.models import Student, Parent, Teacher
from datetime import date

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates test users for student, parent, and teacher roles'

    def handle(self, *args, **options):
        """Main command handler."""
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('Creating test users...'))
        self.stdout.write('=' * 70)

        try:
            with transaction.atomic():
                # Create student user
                student_user = self._create_student()
                
                # Create parent user
                parent_user = self._create_parent()
                
                # Create teacher user
                teacher_user = self._create_teacher()

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write(self.style.SUCCESS('[SUCCESS] All test users created successfully!'))
            self.stdout.write(self.style.SUCCESS('=' * 70))
            
            # Display credentials
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('Test User Credentials:'))
            self.stdout.write('')
            self.stdout.write('[STUDENT]')
            self.stdout.write(f'  Username: student')
            self.stdout.write(f'  Password: student123')
            self.stdout.write(f'  Email: student@codeventure.com')
            self.stdout.write('')
            self.stdout.write('[PARENT]')
            self.stdout.write(f'  Username: parent')
            self.stdout.write(f'  Password: parent123')
            self.stdout.write(f'  Email: parent@codeventure.com')
            self.stdout.write('')
            self.stdout.write('[TEACHER]')
            self.stdout.write(f'  Username: teacher')
            self.stdout.write(f'  Password: teacher123')
            self.stdout.write(f'  Email: teacher@codeventure.com')
            self.stdout.write('')
            
        except Exception as e:
            logger.error(f"Error creating test users: {str(e)}", exc_info=True)
            self.stdout.write(self.style.ERROR(f'[ERROR] {str(e)}'))
            raise

    def _create_student(self):
        """Create a test student user."""
        self.stdout.write('\n[1/3] Creating student user...')
        
        username = 'student'
        password = 'student123'
        email = 'student@codeventure.com'
        
        try:
            # Check if user already exists
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'  [WARNING] User already exists: {username}'))
            
            # Ensure student profile exists
            if not hasattr(user, 'student'):
                student = Student.objects.create(
                    user=user,
                    birthday=date(2010, 1, 1),
                    coding_experience='beginner',
                    profile_completed=True
                )
                self.stdout.write(self.style.SUCCESS(f'  [OK] Added student profile to existing user'))
            else:
                self.stdout.write(f'  [INFO] Student profile already exists')
                
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='Student'
            )
            
            # Create student profile
            student = Student.objects.create(
                user=user,
                birthday=date(2010, 1, 1),
                coding_experience='beginner',
                profile_completed=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created student user: {username}'))
        
        return user

    def _create_parent(self):
        """Create a test parent user."""
        self.stdout.write('\n[2/3] Creating parent user...')
        
        username = 'parent'
        password = 'parent123'
        email = 'parent@codeventure.com'
        
        try:
            # Check if user already exists
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'  [WARNING] User already exists: {username}'))
            
            # Ensure parent profile exists
            if not hasattr(user, 'parent'):
                parent = Parent.objects.create(
                    user=user,
                    profile_completed=True
                )
                self.stdout.write(self.style.SUCCESS(f'  [OK] Added parent profile to existing user'))
            else:
                self.stdout.write(f'  [INFO] Parent profile already exists')
                
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='Parent'
            )
            
            # Create parent profile
            parent = Parent.objects.create(
                user=user,
                profile_completed=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created parent user: {username}'))
        
        return user

    def _create_teacher(self):
        """Create a test teacher user."""
        self.stdout.write('\n[3/3] Creating teacher user...')
        
        username = 'teacher'
        password = 'teacher123'
        email = 'teacher@codeventure.com'
        
        try:
            # Check if user already exists
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'  [WARNING] User already exists: {username}'))
            
            # Ensure teacher profile exists
            if not hasattr(user, 'teacher'):
                teacher = Teacher.objects.create(
                    user=user
                )
                self.stdout.write(self.style.SUCCESS(f'  [OK] Added teacher profile to existing user'))
            else:
                self.stdout.write(f'  [INFO] Teacher profile already exists')
                
        except User.DoesNotExist:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name='Test',
                last_name='Teacher'
            )
            
            # Create teacher profile
            teacher = Teacher.objects.create(
                user=user
            )
            
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created teacher user: {username}'))
        
        return user
