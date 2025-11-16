from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from users.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CustomUserCreationFormTests(TestCase):

    def test_form_valid_data_creates_user(self):
        """
        Form with valid username and passwords should create a user.
        """
        form_data = {
            "username": "newuser",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "newuser")
        self.assertTrue(user.check_password("complexpassword123"))
        self.assertIsInstance(user, User)

    def test_form_invalid_password_mismatch(self):
        """
        Form with mismatched passwords should be invalid.
        """
        form_data = {
            "username": "newuser",
            "password1": "password123",
            "password2": "differentpassword",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_form_invalid_missing_username(self):
        """
        Form without a username should be invalid.
        """
        form_data = {
            "username": "",
            "password1": "password123",
            "password2": "password123",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CustomUserChangeFormTests(TestCase):

    def setUp(self):
        """
        Create a test user.
        """
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            phone_number="1234567890",
            address="123 Main St",
            latitude=-34.0,
            longitude=18.0,
        )

    def test_form_initialization(self):
        """
        Form should initialize correctly with a user instance.
        """
        form = CustomUserChangeForm(instance=self.user)
        self.assertEqual(form.initial["username"], self.user.username)
        self.assertEqual(form.initial["email"], self.user.email)
        self.assertEqual(form.initial["first_name"], self.user.first_name)
        self.assertEqual(form.initial["last_name"], self.user.last_name)
        self.assertEqual(form.initial["phone_number"], self.user.phone_number)
        self.assertEqual(form.initial["address"], self.user.address)
        self.assertEqual(form.initial["latitude"], self.user.latitude)
        self.assertEqual(form.initial["longitude"], self.user.longitude)

    def test_form_valid_data_updates_user(self):
        """
        Form with valid data should update the user.
        """
        data = {
            "username": "updateduser",
            "password": self.user.password,  # leave password unchanged
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "phone_number": "+27 83 123 1234",
            "address": "456 Elm St",
            "latitude": -33.9,
            "longitude": 18.4,
        }
        form = CustomUserChangeForm(data=data, instance=self.user)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "updateduser")
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "User")
        self.assertEqual(user.phone_number, "+27 83 123 1234")
        self.assertEqual(user.address, "456 Elm St")
        self.assertEqual(user.latitude, Decimal("-33.9"))
        self.assertEqual(user.longitude, Decimal("18.4"))

    def test_form_invalid_missing_username(self):
        """
        Form with missing username should be invalid.
        """
        data = {
            "username": "",
            "password": self.user.password,
            "email": "updated@example.com",
        }
        form = CustomUserChangeForm(data=data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)
