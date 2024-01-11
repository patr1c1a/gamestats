from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase


class UserRegistrationViewTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.client = APIClient()

	def test_user_registration_success(self):
		"""
		Tests the /signup/ endpoint by validating that user signup with valid data succeeds.
		"""
		data = {
			"username": "test_user",
			"email": "testuser@example.com",
			"password": "test_password",
			"first_name": "Test",
			"last_name": "User"
		}
		response = self.client.post("/signup/", data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		user_exists = User.objects.filter(username="test_user").exists()
		self.assertTrue(user_exists)
