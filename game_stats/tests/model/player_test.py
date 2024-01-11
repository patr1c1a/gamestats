from django.test import TestCase
from game_stats.models import Player
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class PlayerModelTest(TestCase):

	def setUp(self):
		self.user = User.objects.create(username="test_user", password="test_password")
		self.player = Player.objects.create(
			user=self.user,
			nickname="test_player",
			profile_image="https://example.com/image.jpg"
		)

	def test_player_creation(self):
		"""
	    Tests that a Player can be created with all its fields.
		"""

		self.assertEqual(self.player.nickname, "test_player")
		self.assertEqual(self.player.profile_image, "https://example.com/image.jpg")
		self.assertEqual(self.player.user.username, "test_user")

	def test_delete_player(self):
		"""
		Tests that Player can be deleted.
		"""
		self.player.delete()
		with self.assertRaises(Player.DoesNotExist):
			Player.objects.get(id=self.player.id)

	def test_player_no_profile_image(self):
		"""
	    Tests that a Player can be created with no profile image.
		"""
		player = Player.objects.create(
			nickname="test_player",
			user=User.objects.create(username="test_user2", password="test_password")
		)
		self.assertEqual(player.nickname, "test_player")

	def test_player_no_nickname(self):
		"""
		Tests that creating a Player without a nickname raises a ValidationError.
		"""
		player = Player(
			profile_image="https://example.com/image.jpg",
			user=User.objects.create(username="test_user3", password="test_password")
		)
		with self.assertRaises(ValidationError) as context:
			player.full_clean()
		self.assertIn('nickname', context.exception.error_dict)


	def test_player_no_user(self):
		"""
		Tests that creating a Player without a user raises a ValidationError.
		"""
		player = Player(
			nickname="test_player",
		)
		with self.assertRaises(ValidationError) as context:
			player.full_clean()
		self.assertIn('user', context.exception.error_dict)

	def test_player_invalid_nickname(self):
		"""
	    Tests that a Player nickname can only contain letters, numbers and underscores.
		"""
		self.player.nickname = "test player"

		with self.assertRaises(ValidationError) as context:
			self.player.save()

		self.assertIn(
			"Nickname can only contain letters, numbers and underscores.",
			context.exception.messages,
		)
