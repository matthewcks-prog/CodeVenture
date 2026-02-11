"""
Management command to seed the database with initial learning modules and sample data.

Usage:
    python manage.py seed_data
    python manage.py seed_data --clear  # Clear existing data first
"""
import logging
from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from LearningResource.models import LearningModule, SubModule, VideoTutorial

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Seeds the database with initial learning modules and sample data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing learning data before seeding',
        )
        parser.add_argument(
            '--admin',
            action='store_true',
            help='Create admin superuser (username: admin, password: superuser)',
        )

    def handle(self, *args, **options):
        """Main command handler."""
        self.stdout.write('=' * 70)
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))
        self.stdout.write('=' * 70)

        try:
            with transaction.atomic():
                # Create admin user if requested
                if options['admin']:
                    self._create_admin_user()

                # Clear existing data if requested
                if options['clear']:
                    self._clear_data()

                # Seed learning modules
                self._seed_learning_modules()

            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 70))
            self.stdout.write(self.style.SUCCESS('[SUCCESS] Database seeding completed successfully!'))
            self.stdout.write(self.style.SUCCESS('=' * 70))
            
        except Exception as e:
            logger.error(f"Error during database seeding: {str(e)}", exc_info=True)
            self.stdout.write(self.style.ERROR(f'[ERROR] {str(e)}'))
            raise

    def _create_admin_user(self):
        """Create or update admin superuser."""
        self.stdout.write('\n[1/2] Creating admin user...')
        
        username = 'admin'
        password = 'superuser'
        email = 'admin@codeventure.com'
        
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'  [WARNING] Admin user already exists: {username}'))
            
            # Update to ensure it's a superuser
            if not user.is_superuser or not user.is_staff:
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'  [OK] Updated admin user permissions'))
                
        except User.DoesNotExist:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created admin user: {username}'))
        
        self.stdout.write(f'    Username: {username}')
        self.stdout.write(f'    Password: {password}')
        self.stdout.write(f'    Email: {email}')

    def _clear_data(self):
        """Clear existing learning data."""
        self.stdout.write('\nClearing existing data...')
        
        submodule_count = SubModule.objects.count()
        video_count = VideoTutorial.objects.count()
        module_count = LearningModule.objects.count()
        
        SubModule.objects.all().delete()
        VideoTutorial.objects.all().delete()
        LearningModule.objects.all().delete()
        
        self.stdout.write(self.style.WARNING(
            f'  [OK] Deleted {module_count} modules, {submodule_count} submodules, '
            f'{video_count} videos'
        ))

    def _seed_learning_modules(self):
        """Seed learning modules with submodules."""
        self.stdout.write('\n[2/2] Seeding learning modules...')
        
        modules_created = 0
        submodules_created = 0
        
        # Basic Modules - Essential for beginners
        basic_module, created = LearningModule.objects.get_or_create(
            name='Basic Modules',
            defaults={
                'short_name': 'basics',
                'description': 'Fundamental programming concepts for beginners. Start your coding journey here!',
                'thumbnail': 'https://images.unsplash.com/photo-1516116216624-53e697fedbea?w=400'
            }
        )
        if created:
            modules_created += 1
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created module: {basic_module.name}'))
        else:
            self.stdout.write(f'  [INFO] Module already exists: {basic_module.name}')
        
        # Create submodules for Basic Modules
        basic_submodules = [
            {
                'name': 'Introduction to Programming',
                'difficulty_level': 'Basic',
                'description': 'Learn what programming is and why it\'s important. Understand how computers execute instructions.',
                'video_name': 'Intro to Programming',
                # https://www.youtube.com/watch?v=zOjov-2OZ0E
                'video_id': 'zOjov-2OZ0E',
            },
            {
                'name': 'Variables and Data Types',
                'difficulty_level': 'Basic',
                'description': 'Understand how to store and manipulate data using variables. Learn about different data types.',
                'video_name': 'Variables and Data Types',
                # https://www.youtube.com/watch?v=LKFrQXaoSMQ
                'video_id': 'LKFrQXaoSMQ',
            },
            {
                'name': 'Control Flow',
                'difficulty_level': 'Basic',
                'description': 'Master if statements, loops, and decision-making in your programs.',
                'video_name': 'Control Flow',
                # https://www.youtube.com/watch?v=Zp5MuPOtsSY
                'video_id': 'Zp5MuPOtsSY',
            },
            {
                'name': 'Functions',
                'difficulty_level': 'Basic',
                'description': 'Learn to write reusable code with functions. Understand parameters and return values.',
                'video_name': 'Functions',
                # https://www.youtube.com/watch?v=89cGQjB5R4M
                'video_id': '89cGQjB5R4M',
            },
        ]
        
        prev_submodule = None
        for idx, sub_data in enumerate(basic_submodules):
            # update_or_create so existing records get the latest video_id
            video, _ = VideoTutorial.objects.update_or_create(
                name=sub_data['video_name'],
                defaults={'video_id': sub_data['video_id']},
            )
            
            submodule, created = SubModule.objects.get_or_create(
                name=sub_data['name'],
                parent_module=basic_module,
                defaults={
                    'difficulty_level': sub_data['difficulty_level'],
                    'description': sub_data['description'],
                    'video': video,
                    'prev_submodule': prev_submodule
                }
            )
            
            # Link previous submodule to this one
            if prev_submodule:
                prev_submodule.next_submodule = submodule
                prev_submodule.save()
            
            prev_submodule = submodule
            
            if created:
                submodules_created += 1
        
        self.stdout.write(f'    [OK] Created {len(basic_submodules)} submodules for Basic Modules')
        
        # Python Fundamentals
        python_module, created = LearningModule.objects.get_or_create(
            name='Python Fundamentals',
            defaults={
                'short_name': 'python',
                'description': 'Deep dive into Python programming. Learn syntax, data structures, and best practices.',
                'thumbnail': 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400'
            }
        )
        if created:
            modules_created += 1
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created module: {python_module.name}'))
        
        python_submodules = [
            {
                'name': 'Python Syntax Basics',
                'difficulty_level': 'Basic',
                'description': 'Learn Python\'s clean and readable syntax. Master indentation and basic structure.',
                'video_name': 'Python Fundamentals Part 1',
                # https://www.youtube.com/watch?v=fWjsdhR3z3c
                'video_id': 'fWjsdhR3z3c',
            },
            {
                'name': 'Lists and Dictionaries',
                'difficulty_level': 'Intermediate',
                'description': 'Master Python\'s powerful built-in data structures for organizing information.',
                'video_name': 'Python Fundamentals Part 2',
                # https://www.youtube.com/watch?v=Gx5qb1uHss4
                'video_id': 'Gx5qb1uHss4',
            },
        ]
        
        prev_submodule = None
        for sub_data in python_submodules:
            video, _ = VideoTutorial.objects.update_or_create(
                name=sub_data['video_name'],
                defaults={'video_id': sub_data['video_id']},
            )
            
            submodule, created = SubModule.objects.get_or_create(
                name=sub_data['name'],
                parent_module=python_module,
                defaults={
                    'difficulty_level': sub_data['difficulty_level'],
                    'description': sub_data['description'],
                    'video': video,
                    'prev_submodule': prev_submodule
                }
            )
            
            if prev_submodule:
                prev_submodule.next_submodule = submodule
                prev_submodule.save()
            
            prev_submodule = submodule
            
            if created:
                submodules_created += 1
        
        self.stdout.write(f'    [OK] Created {len(python_submodules)} submodules for Python Fundamentals')
        
        # Web Development
        web_module, created = LearningModule.objects.get_or_create(
            name='Web Development',
            defaults={
                'short_name': 'web',
                'description': 'Build modern websites and web applications. Learn HTML, CSS, JavaScript, and frameworks.',
                'thumbnail': 'https://images.unsplash.com/photo-1547658719-da2b51169166?w=400'
            }
        )
        if created:
            modules_created += 1
            self.stdout.write(self.style.SUCCESS(f'  [OK] Created module: {web_module.name}'))
        
        web_submodules = [
            {
                'name': 'HTML & CSS Basics',
                'difficulty_level': 'Basic',
                'description': 'Create and style web pages. Learn the building blocks of the web.',
                'video_name': 'Web Development Fundamentals Part 1',
                # https://www.youtube.com/watch?v=hu-q2zYwEYs&list=PL4cUxeGkcC9ivBf_eKCPIAYXWzLlPAm6G
                'video_id': 'hu-q2zYwEYs',
            },
            {
                'name': 'JavaScript Essentials',
                'difficulty_level': 'Intermediate',
                'description': 'Add interactivity to your websites. Master the language of the web.',
                'video_name': 'Web Development Fundamentals Part 2',
                # https://www.youtube.com/watch?v=zFZrkCIc2Oc&list=...
                'video_id': 'zFZrkCIc2Oc',
            },
        ]
        
        prev_submodule = None
        for sub_data in web_submodules:
            video, _ = VideoTutorial.objects.update_or_create(
                name=sub_data['video_name'],
                defaults={'video_id': sub_data['video_id']},
            )
            
            submodule, created = SubModule.objects.get_or_create(
                name=sub_data['name'],
                parent_module=web_module,
                defaults={
                    'difficulty_level': sub_data['difficulty_level'],
                    'description': sub_data['description'],
                    'video': video,
                    'prev_submodule': prev_submodule
                }
            )
            
            if prev_submodule:
                prev_submodule.next_submodule = submodule
                prev_submodule.save()
            
            prev_submodule = submodule
            
            if created:
                submodules_created += 1
        
        self.stdout.write(f'    [OK] Created {len(web_submodules)} submodules for Web Development')
        
        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'  Summary:'))
        self.stdout.write(f'    - Modules created: {modules_created}')
        self.stdout.write(f'    - Submodules created: {submodules_created}')
        self.stdout.write(f'    - Total modules: {LearningModule.objects.count()}')
        self.stdout.write(f'    - Total submodules: {SubModule.objects.count()}')
