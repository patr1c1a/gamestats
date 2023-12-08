from django.test import TestCase
from game_stats.models import Player
from django.core.exceptions import ValidationError


class PlayerModelTest(TestCase):
	def test_player_creation(self):
		"""
	    Tests that a Player can be created with all its fields.
		"""
		player = Player.objects.create(
			nickname="test_player",
			profile_image="https://example.com/image.jpg"
		)
		self.assertEqual(player.nickname, "test_player")
		self.assertEqual(player.profile_image, "https://example.com/image.jpg")

	def test_delete_player(self):
		"""
		Tests that Player can be deleted.
		"""
		player = Player.objects.create(
			nickname="test_player",
			profile_image="https://example.com/image.jpg"
		)
		player.delete()
		with self.assertRaises(Player.DoesNotExist):
			Player.objects.get(id=player.id)

	def test_player_no_profile_image(self):
		"""
	    Tests that a Player can be created with no profile image.
		"""
		player = Player.objects.create(
			nickname="test_player",
		)
		self.assertEqual(player.nickname, "test_player")

	def test_player_no_nickname(self):
		"""
		Tests that creating a Player without a nickname raises a ValidationError.
		"""
		player = Player(
			profile_image="https://example.com/image.jpg"
		)
		with self.assertRaises(ValidationError) as context:
			player.full_clean()
		self.assertIn('nickname', context.exception.error_dict)
