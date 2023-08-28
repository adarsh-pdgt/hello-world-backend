# Third Party Stuff
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

# Hello World Stuff
from hello_world.base.utils.urls import reverse

User = get_user_model()


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("auth-register")

        self.required_keys = {
            "email",
            "password"
        }
        self.expected_keys = {
            "id",
            "first_name",
            "last_name",
            "email",
            "auth_token"
        }

        self.user_data = {
            "first_name": "sample",
            "last_name": "user",
            "email": "hello@example.com",
            "password": "localhost"
        }

    def test_user_registration_required_fields(self):
        response = self.client.post(self.url, data=None, format="json")
        self.assertEqual(response.status_code, 400)

        # Check error-type, error-fields and error-message in response
        self.assertEqual(response.data["error_type"], "ValidationError")
        self.assertSetEqual(
            self.required_keys, set(error["field"] for error in response.data["errors"])
        )
        self.assertSetEqual(
            {"This field is required."},
            set(error["message"] for error in response.data["errors"]),
        )

    def test_user_registration(self):
        self.assertEqual(User.objects.count(), 0)

        response = self.client.post(self.url, data=self.user_data, format="json")
        self.assertEqual(response.status_code, 201)

        # Check all expected keys are present in response
        self.assertSetEqual(self.expected_keys, set(response.data.keys()))

        # Check user instance is created in DB
        self.assertEqual(User.objects.count(), 1)
        user = User.objects.first()

        # Check correct data is saved in DB
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])
        self.assertEqual(user.email, self.user_data["email"])

        # Check correct data is sent in response
        self.assertEqual(self.user_data["first_name"], response.data["first_name"])
        self.assertEqual(self.user_data["last_name"], response.data["last_name"])
        self.assertEqual(self.user_data["email"], response.data["email"])
