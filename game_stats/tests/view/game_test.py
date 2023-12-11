from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from game_stats.models import Game, Player


class GameViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.player1 = Player.objects.create(nickname="test_player1")
		self.player2 = Player.objects.create(nickname="test_player2")
		self.game1 = Game.objects.create()
		self.game1.players.set([self.player1, self.player2])
		self.game1.winner = self.player1
		self.game2 = Game.objects.create()
		self.game2.players.set([])
		self.client = APIClient()

	def test_get_games(self):
		"""
		Tests that all games are returned
		"""
		response = self.client.get('/stats/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), Game.objects.count())

	def test_get_game_detail(self):
		"""
		Tests retrieving a specific game by its id.
		"""
		response = self.client.get(f"/games/{self.game1.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
