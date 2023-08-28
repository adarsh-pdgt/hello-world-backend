# Third Party Stuff
from rest_framework.test import APITestCase

# Hello World Stuff
from hello_world.base.utils.urls import reverse
from hello_world.users.tests.factories import create_user


class UserLoginTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth-login")
        self.user = create_user(email="test@example.com", password="test")

        self.request_data = {"email": self.user.email, "password": "test"}
        self.expected_keys = {
            "id",
            "first_name",
            "last_name",
            "email",
            "auth_token"
        }

    def test_user_login(self):
        response = self.client.post(self.url, data=self.request_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(self.expected_keys, set(response.data.keys()))
