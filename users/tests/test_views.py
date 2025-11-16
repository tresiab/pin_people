import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class LoginViewTest(TestCase):

    def setUp(self):
        """
        Create test user.
        """
        self.user = User.objects.create_user(username="testuser", password="secret123")
        self.login_url = reverse("login")

    def test_login_page_loads(self):
        """
        Login page should load correctly with GET.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_success(self):
        """
        Login with valid credentials should redirect to home.
        """
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "secret123",
            },
        )
        self.assertRedirects(response, reverse("location"))

    def test_login_failure(self):
        """
        Login with invalid credentials should return error.
        """
        response = self.client.post(
            self.login_url,
            {
                "username": "testuser",
                "password": "wrongpass",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password.")


class LogoutViewTest(TestCase):

    def setUp(self):
        """
        Create and login a test user.
        """
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")

    def test_logout_view_logs_out_user(self):
        """
        Test that accessing the logout view logs out the user
        and redirects to the expected page.
        """
        response = self.client.post(reverse("logout"))

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))

        # After logout the user should no longer be authenticated
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_view_requires_login(self):
        """
        Test that logout works gracefully even when the user is not logged in.
        """
        self.client.logout()
        response = self.client.post(reverse("logout"))

        # Still should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("login"))


class RegisterViewTests(TestCase):

    def test_get_register_view(self):
        """
        Test that GET request to the registration view return a 200 OK status
        and renders the correct registration template with an empty form.
        """
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIsInstance(response.context["form"], CustomUserCreationForm)

    def test_post_valid_register_view(self):
        """
        Test that a valid POST request successfully creates a new user
        and redirects to the login page.
        """
        form_data = {
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        }
        response = self.client.post(reverse("register"), form_data)

        # Ensure user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Ensure redirect to login
        self.assertRedirects(response, reverse("login"))

    def test_post_invalid_register_view(self):
        """
        Test that a valid POST request re-render the form with errors
        and does not create a new user.
        """
        form_data = {
            "username": "newuser",
            "password1": "strongpassword123",
            "password2": "differentpassword",
        }
        response = self.client.post(reverse("register"), form_data)

        # Should return the same page with form errors
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertFalse(User.objects.filter(username="newuser").exists())
        self.assertTrue(response.context["form"].errors)


class LocationViewTests(TestCase):

    def setUp(self):
        """
        Create test users.
        """
        self.user1 = User.objects.create_user(
            username="user1", password="password123", latitude=-34.08, longitude=18.86
        )
        self.user2 = User.objects.create_user(username="user2", password="password123", latitude=None, longitude=None)
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpass", latitude=-33.93, longitude=18.42
        )

    def test_location_view_requires_login(self):
        """
        The view should redirect to login if not authenticated.
        """
        url = reverse("location")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_location_view_with_logged_in_user(self):
        """
        Test that logged in users can access the view and receive the correct context.
        """
        self.client.login(username="user1", password="password123")
        url = reverse("location")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/location.html")

        # Check context keys
        self.assertIn("users_json", response.context)
        self.assertIn("logged_in_user_id", response.context)
        self.assertIn("is_superuser", response.context)

        # Verify logged in user ID
        self.assertEqual(response.context["logged_in_user_id"], self.user1.id)

        # Verify the superuser flag
        self.assertFalse(response.context["is_superuser"])

        # Verify users_json contains only the users with coordinates
        users_data = json.loads(response.context["users_json"])
        self.assertEqual(len(users_data), 2)
        self.assertTrue(all("latitude" in u and "longitude" in u for u in users_data))

        # Verify usernames
        usernames = [u["username"] for u in users_data]
        self.assertIn("user1", usernames)
        self.assertIn("admin", usernames)
        self.assertNotIn("user2", usernames)


class ProfileViewTests(TestCase):

    def setUp(self):
        """
        Create test users.
        """
        self.user1 = User.objects.create_user(username="user1", password="password123")
        self.user2 = User.objects.create_user(username="user2", password="password123")
        self.superuser = User.objects.create_superuser(username="admin", password="adminpass")

    def test_own_profile_access(self):
        """
        Test that regular users can view their own profiles.
        """
        self.client.login(username="user1", password="password123")
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["user"], self.user1)

    def test_superuser_can_view_any_profile(self):
        """
        Test that superuser can view any user's profile.
        """
        self.client.login(username="admin", password="adminpass")
        url = reverse("user_detail", args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile.html")
        self.assertEqual(response.context["user"], self.user1)

    def test_regular_user_cannot_view_other_profile(self):
        """
        Test that a regular user cannot view another user's profile.
        """
        self.client.login(username="user1", password="password123")
        url = reverse("user_detail", args=[self.user2.id])
        response = self.client.get(url)
        self.assertContains(response, "You are not allowed to view this profile.", status_code=403)

    def test_anonymous_user_redirect_to_login(self):
        """
        Test that an anonymous user is redirected to login.
        """
        url = reverse("profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)


class ProfileChangeViewTests(TestCase):

    def setUp(self):
        """
        Create test users.
        """
        self.user1 = User.objects.create_user(username="user1", password="password123", email="user1@example.com")
        self.user2 = User.objects.create_user(username="user2", password="password123", email="user2@example.com")
        self.superuser = User.objects.create_superuser(
            username="admin", password="adminpass", email="admin@example.com"
        )

    def test_anonymous_user_redirected_to_login(self):
        """
        Test that anonymous users are redirected to login pages.
        """
        url = reverse("profile_change")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_regular_user_can_edit_own_profile_get(self):
        """
        Test that a regular user can view their own profile change page (GET).
        """
        self.client.login(username="user1", password="password123")
        url = reverse("profile_change")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_change.html")
        self.assertIsInstance(response.context["form"], CustomUserChangeForm)
        self.assertEqual(response.context["user"], self.user1)

    def test_regular_user_can_edit_own_profile_post(self):
        """
        Test that a regular user can update their own profile (POST).
        """
        self.client.login(username="user1", password="password123")
        url = reverse("profile_change")
        data = {"username": "user1_updated", "email": "user1_new@example.com"}
        response = self.client.post(url, data)

        self.user1.refresh_from_db()
        self.assertEqual(self.user1.username, "user1_updated")
        self.assertEqual(self.user1.email, "user1_new@example.com")

        self.assertRedirects(response, reverse("user_detail", args=[self.user1.id]))

    def test_regular_user_cannot_edit_another_user(self):
        """
        Test that a regular user cannot edit someone else's profile.
        """
        self.client.login(username="user1", password="password123")
        url = reverse("user_change", args=[self.user2.id])
        response = self.client.get(url)

        self.assertContains(
            response,
            "You are not allowed to edit this profile.",
            status_code=403,
        )

    def test_superuser_can_edit_any_user(self):
        """
        Test that a superuser can edity eany user's profile.
        """
        self.client.login(username="admin", password="adminpass")
        url = reverse("user_change", args=[self.user1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/profile_change.html")
        self.assertEqual(response.context["user"], self.user1)
        self.assertIsInstance(response.context["form"], CustomUserChangeForm)
