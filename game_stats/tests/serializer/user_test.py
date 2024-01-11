from django.test import TestCase
from game_stats.serializers import UserSerializer


class UserSerializerTest(TestCase):

	def test_valid_serializer(self):
		"""
		Tests that a user created with valid data is valid.
		"""
		data = {
			"username": "testuser",
			"email": "testuser@example.com",
			"password": "testpassword",
			"first_name": "Test",
			"last_name": "User"
		}
		serializer = UserSerializer(data=data)
		self.assertTrue(serializer.is_valid())
		user = serializer.save()
		self.assertEqual(user.username, "testuser")
		self.assertNotEqual(user.password, "testpassword")  # Password should be hashed
		self.assertEqual(user.first_name, "Test")
		self.assertEqual(user.last_name, "User")

	def test_invalid_serializer(self):
		"""
		Tests that a user created with invalid data is invalid.
		"""
		data = {
			"username": "invalid username",
			"email": "invalidemail",
			"password": "testpassword",
		}
		serializer = UserSerializer(data=data)
		self.assertFalse(serializer.is_valid())
