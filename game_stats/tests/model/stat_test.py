from MySQLdb._mysql import IntegrityError
from django.test import TestCase
from game_stats.models import Stat, Player
from django.core.exceptions import ValidationError


class StatModelTest(TestCase):
	def setUp(self):
		# Create a Player to associate Stat to
		self.player = Player.objects.create(nickname="test_player")

	def test_stat_creation(self):
		"""
	    Tests that a Stat can be created with all its fields.
		"""
		stat = Stat.objects.create(
			player=self.player,
			score=10
		)
		self.assertEqual(stat.player.nickname, "test_player")
		self.assertEqual(stat.score, 10)

	def test_delete_stat(self):
		"""
		Tests that Stat can be deleted.
		"""
		stat = Stat.objects.create(
			player=self.player,
			score=10
		)
		stat.delete()
		with self.assertRaises(Stat.DoesNotExist):
			Stat.objects.get(id=stat.id)

	def test_player_no_score(self):
		"""
	    Tests that a Stat can be created with no score.
		"""
		stat = Stat.objects.create(
			player=self.player
		)
		self.assertEqual(stat.player.nickname, "test_player")
