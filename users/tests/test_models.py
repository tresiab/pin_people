from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTests(TestCase):
    def setUp(self):
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
        self.assertEqual(str(self.user), "testuser")
