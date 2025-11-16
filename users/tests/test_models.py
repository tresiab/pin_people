from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):

    def setUp(self):
        """
        Create a test user.
        """
        self.user = User.objects.create(
            username="testuser",
            password="testpassword",
            is_superuser=False,
            is_staff=False,
            is_active=True,
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone_number="0831231234",
            address="221B Baker Street",
            latitude=Decimal("-34.080000"),
            longitude=Decimal("18.860000"),
        )

    def test_user_str(self):
        """
        Test that the __str__ method of the User model
        returns the username as its string representation.
        """
        self.assertEqual(str(self.user), "testuser")

    def test_to_dms(self):
        """
        Test that the to_dms() function correctly converts
        latitude and longitude values into formatted
        degrees–minutes–seconds (DMS) strings with the proper
        directional indicators (N/S/E/W).
        """
        self.assertEqual(self.user.to_dms(self.user.latitude), "34°4'48\"S")
        self.assertEqual(self.user.to_dms(self.user.latitude, "lat"), "34°4'48\"S")
        self.assertEqual(self.user.to_dms(self.user.longitude, "lon"), "18°51'36\"E")

    def test_position_property(self):
        """
        Test that the User model's position property returns
        the correctly formatted latitude and longitude string
        in degrees–minutes–seconds (DMS) format.
        """
        self.assertEqual(self.user.position, "34°4'48\"S 18°51'36\"E")
