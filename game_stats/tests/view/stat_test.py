from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from game_stats.models import Stat, Player
from django.utils import timezone


class StatViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.player1 = Player.objects.create(nickname="stat_view_test_player1")
		self.stat1 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=10)
		self.stat2 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=5)
		self.stat3 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=1)
		self.client = APIClient()

	def test_get_stats(self):
		"""
		Tests the /stats/ endpoint by validating that stats added during test setUp are returned, asserting their
		scores and player nicknames.
		"""
		response = self.client.get('/stats/')
		returned_stats = [stat for stat in response.data["results"]]
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(self.stat1.score, returned_stats[0]["score"])
		self.assertEqual(self.stat1.player.nickname, returned_stats[0]["player"]["nickname"])
		self.assertEqual(self.stat2.score, returned_stats[1]["score"])
		self.assertEqual(self.stat2.player.nickname, returned_stats[1]["player"]["nickname"])
		self.assertEqual(self.stat3.score, returned_stats[2]["score"])
		self.assertEqual(self.stat3.player.nickname, returned_stats[2]["player"]["nickname"])

	def test_get_stat_detail(self):
		"""
		Tests the stats/<int:pk>/ endpoint by retrieving a specific stat by its id.
		"""
		response = self.client.get(f'/stats/{self.stat1.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['player']['id'], self.player1.id)
		self.assertEqual(response.data['score'], self.stat1.score)
		# Check date
		self.assertEqual(response.data['creation_date'][:10], str(self.stat1.creation_date)[:10])
		# Check time
		self.assertEqual(response.data['creation_date'][11:19], str(self.stat1.creation_date)[11:19])
