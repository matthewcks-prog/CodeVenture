from django.test import TestCase, RequestFactory
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount, SocialLogin, SocialApp
from WelcomePage.adapter import CustomSocialAccountAdapter, _derive_username_from_data
from UserManagement.models import Student


class CustomSocialAccountAdapterTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adapter = CustomSocialAccountAdapter()
        # Create a user without a role
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        # Ensure Site and SocialApp exist for pre_social_login linking (connect needs them)
        site, _ = Site.objects.get_or_create(pk=settings.SITE_ID, defaults={"domain": "testserver", "name": "Test"})
        app, _ = SocialApp.objects.get_or_create(
            provider="google",
            defaults={"name": "Google", "client_id": "test-id", "secret": "test-secret"},
        )
        if site not in app.sites.all():
            app.sites.add(site)

    def test_get_login_redirect_url_no_role(self):
        """Test redirection to role selection if user has no role."""
        request = self.factory.get('/accounts/google/login/')
        request.user = self.user

        url = self.adapter.get_login_redirect_url(request)
        # Verify it redirects to choose_user_type
        self.assertEqual(url, reverse('choose_user_type'))

    def test_get_login_redirect_url_with_role(self):
        """Test standard redirection if user has a role."""
        # Add a role to the user
        Student.objects.create(user=self.user)

        request = self.factory.get('/accounts/google/login/')
        request.user = self.user

        url = self.adapter.get_login_redirect_url(request)
        # Should return default redirect (home or next)
        self.assertNotEqual(url, reverse('choose_user_type'))

    def test_pre_social_login_links_existing_user(self):
        """Test that pre_social_login links a social account to an existing user by email."""
        request = self.factory.get('/accounts/google/login/')

        # Scenario: User is NOT logged in, but exists in DB.
        from django.contrib.auth.models import AnonymousUser
        request.user = AnonymousUser()

        # Mock a social login instance
        account = SocialAccount(provider='google', uid='12345')
        # important: extra_data must contain the email matching self.user
        account.extra_data = {'email': 'test@example.com'}
        sociallogin = SocialLogin(account=account)
        sociallogin.user = None

        # Verify user is not linked yet
        self.assertFalse(SocialAccount.objects.filter(user=self.user).exists())

        # call method
        self.adapter.pre_social_login(request, sociallogin)

        # Verify linkage by checking DB
        self.assertTrue(SocialAccount.objects.filter(user=self.user, uid='12345', provider='google').exists())

    def test_populate_username_generates_username(self):
        """Test that populate_username generates a username from email if missing."""
        user = User()
        user.email = "newuser@example.com"
        user.username = "" # Missing username

        # Call populate_username
        self.adapter.populate_username(None, user)

        # Verify username is generated
        self.assertEqual(user.username, "newuser")

        # Verify it handles conflicts (simple check, full unique logic is in allauth)
        User.objects.create(username="newuser")
        user.username = ""
        self.adapter.populate_username(None, user)
        self.assertNotEqual(user.username, "newuser")
        self.assertTrue(user.username.startswith("newuser"))

    def test_populate_user_sets_username_from_email(self):
        """Test that populate_user derives username from email when provider doesn't supply it."""
        request = self.factory.get('/accounts/google/login/')
        from allauth.socialaccount.models import SocialLogin
        from allauth.socialaccount.models import SocialAccount
        from django.contrib.auth import get_user_model
        User = get_user_model()
        account = SocialAccount(provider='google', uid='99999')
        account.extra_data = {'email': 'googleuser@example.com', 'given_name': 'Google', 'family_name': 'User'}
        sociallogin = SocialLogin(account=account)
        sociallogin.user = User()
        sociallogin.user.email = 'googleuser@example.com'
        sociallogin.user.first_name = 'Google'
        sociallogin.user.last_name = 'User'
        sociallogin.user.username = ''
        data = {'email': 'googleuser@example.com', 'first_name': 'Google', 'last_name': 'User'}
        user = self.adapter.populate_user(request, sociallogin, data)
        self.assertTrue(user.username)
        self.assertIn('googleuser', user.username.lower())

    def test_derive_username_from_data(self):
        """Test _derive_username_from_data helper."""
        self.assertEqual(_derive_username_from_data({'email': 'user@domain.com'}), 'user')
        self.assertEqual(_derive_username_from_data({'first_name': 'John', 'last_name': 'Doe'}), 'JohnDoe')
        self.assertEqual(_derive_username_from_data({}), 'user')
