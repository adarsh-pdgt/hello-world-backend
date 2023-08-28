# Third Party Stuff
from rest_framework.test import APITestCase

# Hello World Stuff
from hello_world.base.utils.urls import reverse
from hello_world.users.tests.factories import create_user


class UserDetailsTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("me")

        self.user = create_user(email="test@example.com")

        self.expected_keys = {
            "id",
            "first_name",
            "last_name",
            "email"
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

    def test_get_current_user_api(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        # Check expected keys in response
        self.assertSetEqual(self.expected_keys, set(response.data.keys()))

        # Check user data is correctly sent in response
        self.assertEqual(str(self.user.id), response.data["id"])
        self.assertEqual(self.user.first_name, response.data["first_name"])
        self.assertEqual(self.user.last_name, response.data["last_name"])
        self.assertEqual(self.user.email, response.data["email"])
