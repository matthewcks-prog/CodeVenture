from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from allauth.socialaccount.models import SocialAccount, SocialLogin
from WelcomePage.adapter import CustomSocialAccountAdapter
from UserManagement.models import Student

class CustomSocialAccountAdapterTest(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.adapter = CustomSocialAccountAdapter()
        # Create a user without a role
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')

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
