from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from django.test import TestCase


class UserViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.user1 = User.objects.create(username="test_user1", password="test_password", is_staff=True)
		self.user2 = User.objects.create(username="test_user2", password="test_password", is_staff=False)
		self.user3 = User.objects.create(username="test_user3", password="test_password", is_staff=False)
		self.access_token = str(AccessToken.for_user(self.user1))
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

	def test_get_users(self):
		"""
		Tests GET to /users/ endpoint by validating that usernames of all users added during test setUp are returned.
		"""
		response = self.client.get(reverse("user-list-or-create"))
		returned_usernames = []
		for user in response.data:
			returned_usernames.append(user["username"])
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn(self.user1.username, returned_usernames)
		self.assertIn(self.user2.username, returned_usernames)

	def test_get_user_detail(self):
		"""
		Tests GET to /users/<int:pk>/ endpoint by retrieving a specific user by its id.
		"""
		response = self.client.get(reverse("user-by-id", args=[self.user1.id]), format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["username"], self.user1.username)

	def test_get_user_no_trailing_slash(self):
		"""
		Tests GET to /users/<int:pk> (no trailing slash) endpoint by retrieving a specific user by its id.
		"""
		response = self.client.get(f"/users/{self.user1.id}")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["username"], self.user1.username)

	def test_user_registration_success(self):
		"""
		Tests POST to /users/ endpoint by validating that user signup with valid data succeeds.
		"""
		data = {
			"username": "test_user",
			"email": "testuser@example.com",
			"password": "test_password",
			"first_name": "Test",
			"last_name": "User"
		}
		response = self.client.post(reverse("user-list-or-create"), data=data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		user_exists = User.objects.filter(username="test_user").exists()
		self.assertTrue(user_exists)

	def test_update_user(self):
		"""
		Tests PATCH to /users/<int:pk>/ endpoint by updating a specific user.
		"""
		updated_data = {"is_staff": True}
		response = self.client.patch(reverse("user-by-id", args=[self.user2.id]), data=updated_data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Check database:
		self.user2.refresh_from_db()
		self.assertEqual(self.user1.is_staff, True)

	def test_delete_user(self):
		"""
		Tests DELETE to /users/<int:pk>/ endpoint by deleting a specific user.
		"""
		response = self.client.delete(reverse("user-by-id", args=[self.user3.id]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		# Check database:
		with self.assertRaises(User.DoesNotExist):
			User.objects.get(id=self.user3.id)
