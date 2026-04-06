from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class RegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')

    def test_register_page_loads(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_valid_registration_creates_user(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertEqual(UserModel.objects.count(), 1)
        self.assertEqual(UserModel.objects.first().username, 'testuser')

    def test_duplicate_email_rejected(self):
        UserModel.objects.create_user(
            username='existing',
            email='dupe@example.com',
            password='Pass1234!'
        )
        response = self.client.post(self.register_url, {
            'username': 'newuser',
            'email': 'dupe@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertFormError(
            response,
            'form',
            'email',
            'An account with this email already exists.'
        )

    def test_short_username_rejected(self):
        response = self.client.post(self.register_url, {
            'username': 'ab',
            'email': 'short@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertFormError(
            response,
            'form',
            'username',
            'Username must be at least 3 characters long.'
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_edit_profile_requires_login(self):
        response = self.client.get(reverse('accounts:edit-profile'))
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={reverse('accounts:edit-profile')}"
        )