# Third Party Stuff
from rest_framework.test import APITestCase

# Hello World Stuff
from hello_world.base.utils.urls import reverse
from hello_world.users.tests.factories import create_user


class UserPasswordChangeTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth-password-change")

        self.current_password = "password1"
        self.new_password = "paSswOrd2.#$"

        # Create user
        self.user = create_user(
            email="test@example.com", password=self.current_password
        )

        self.request_data = {
            "current_password": self.current_password,
            "new_password": self.new_password,
        }
        self.expected_keys = {
            "id",
            "first_name",
            "last_name",
            "email",
            "auth_token",
        }

    def test_authentication(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 401)

        # Check response data
        self.assertEqual(response.data["error_type"], "NotAuthenticated")
        self.assertEqual(len(response.data["errors"]), 1)
        self.assertEqual(
            response.data["errors"][0]["message"],
            "Authentication credentials were not provided.",
        )

    def test_user_password_change(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(self.url, self.request_data, format="json")
        self.assertEqual(response.status_code, 204)

        # Logout User
        self.client.logout()

        # Check new password is set or not
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(self.new_password))

        # Test login with new password
        self.url = reverse("auth-login")
        request_data = {"email": self.user.email, "password": self.new_password}

        response = self.client.post(self.url, request_data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(self.expected_keys, set(response.data.keys()))
