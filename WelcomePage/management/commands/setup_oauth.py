"""
Django management command to set up Google OAuth
Run with: python manage.py setup_oauth
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

User = get_user_model()


class Command(BaseCommand):
    help = 'Set up Google OAuth and create superuser'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("CodeVenture Production Setup")
        self.stdout.write("=" * 60)
        self.stdout.write("")
        
        # 1. Create superuser
        self.stdout.write("1. Creating superuser account...")
        try:
            if User.objects.filter(username='admin').exists():
                self.stdout.write(self.style.WARNING("   Superuser 'admin' already exists"))
                user = User.objects.get(username='admin')
            else:
                user = User.objects.create_superuser(
                    username='admin',
                    email='superuser@gmail.com',
                    password='Admin123!'
                )
                self.stdout.write(self.style.SUCCESS("   Superuser created successfully!"))
                self.stdout.write("      Username: admin")
                self.stdout.write("      Email: superuser@gmail.com")
                self.stdout.write("      Password: Admin123!")
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   Error creating superuser: {e}"))
            return
        
        # 2. Get or create Site
        self.stdout.write("")
        self.stdout.write("2. Configuring site...")
        try:
            site, created = Site.objects.get_or_create(
                id=1,
                defaults={
                    'domain': 'codeventure-ez4m.onrender.com',
                    'name': 'CodeVenture'
                }
            )
            if not created:
                site.domain = 'codeventure-ez4m.onrender.com'
                site.name = 'CodeVenture'
                site.save()
            self.stdout.write(self.style.SUCCESS(f"   Site configured: {site.domain}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   Error configuring site: {e}"))
            return
        
        # 3. Create Google OAuth app
        self.stdout.write("")
        self.stdout.write("3. Setting up Google OAuth...")
        
        # Get OAuth credentials from environment variables
        google_client_id = os.environ.get('GOOGLE_OAUTH_CLIENT_ID')
        google_client_secret = os.environ.get('GOOGLE_OAUTH_CLIENT_SECRET')
        
        if not google_client_id or not google_client_secret:
            self.stdout.write(self.style.WARNING("   Skipping: GOOGLE_OAUTH_CLIENT_ID or GOOGLE_OAUTH_CLIENT_SECRET not set"))
            self.stdout.write("   Set these environment variables to enable Google OAuth")
            return
        
        try:
            google_app, created = SocialApp.objects.get_or_create(
                provider='google',
                defaults={
                    'name': 'Google OAuth',
                    'client_id': google_client_id,
                    'secret': google_client_secret,
                }
            )
            
            if not created:
                # Update existing
                google_app.name = 'Google OAuth'
                google_app.client_id = google_client_id
                google_app.secret = google_client_secret
                google_app.save()
                self.stdout.write(self.style.SUCCESS("   Google OAuth app updated"))
            else:
                self.stdout.write(self.style.SUCCESS("   Google OAuth app created"))
            
            # Link to site
            if site not in google_app.sites.all():
                google_app.sites.add(site)
                self.stdout.write(self.style.SUCCESS("   Google OAuth linked to site"))
            else:
                self.stdout.write(self.style.SUCCESS("   Google OAuth already linked to site"))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"   Error setting up Google OAuth: {e}"))
            return
        
        self.stdout.write("")
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("Setup completed successfully!"))
        self.stdout.write("=" * 60)
        self.stdout.write("")
        self.stdout.write("Next steps:")
        self.stdout.write("1. Visit: https://codeventure-ez4m.onrender.com/admin/")
        self.stdout.write("2. Login with:")
        self.stdout.write("   Username: admin")
        self.stdout.write("   Password: Admin123!")
        self.stdout.write("")
        self.stdout.write("3. Google OAuth should now work on your site!")
        self.stdout.write("=" * 60)
