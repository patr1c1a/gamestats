from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from game_stats.models import Game, Player
from django.utils import timezone


class StatViewsTest(TestCase):
	def setUp(self):
		# Create test data for stats
		self.player1 = Player.objects.create(nickname="test_player1")
		self.player2 = Player.objects.create(nickname="test_player2")
		self.game1 = Game.objects.create(start_timestamp=timezone.now(),
		                                 finish_timestamp=timezone.now() + timezone.timedelta(minutes=1))
		self.game1.players.set([self.player1, self.player2])
		self.game1.winner = self.player1

		self.game2 = Game.objects.create(start_timestamp=timezone.now(),
		                                 finish_timestamp=timezone.now() + timezone.timedelta(minutes=1))
		self.client = APIClient()

	def test_get_games(self):
		# Tests that all games are returned
		response = self.client.get('/games/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), Game.objects.count())

	def test_get_stat_detail(self):
		# Tests retrieving a specific game by its id
		response = self.client.get(f'/games/{self.game1.id}/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Check start date
		self.assertEqual(response.data['start_timestamp'][:10], str(self.game1.start_timestamp)[:10])
		# Check start time
		self.assertEqual(response.data['start_timestamp'][11:19], str(self.game1.start_timestamp)[11:19])

		# Check finish date
		self.assertEqual(response.data['finish_timestamp'][:10], str(self.game1.finish_timestamp)[:10])
		# Check finish time
		self.assertEqual(response.data['finish_timestamp'][11:19], str(self.game1.finish_timestamp)[11:19])
