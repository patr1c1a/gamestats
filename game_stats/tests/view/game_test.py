from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from game_stats.models import Game, Player


class GameViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.player1 = Player.objects.create(nickname="game_view_test_player1")
		self.player2 = Player.objects.create(nickname="game_view_test_player2")
		self.game1 = Game.objects.create()
		self.game1.players.set([self.player1, self.player2])
		self.game1.winner = self.player1
		self.game2 = Game.objects.create()
		self.game2.players.set([])
		self.client = APIClient()

	def test_get_games(self):
		"""
		Tests the /games/ endpoint to validate that all games are returned.
		"""
		response = self.client.get('/games/')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), Game.objects.count())

	def test_get_game_detail(self):
		"""
		Tests the games/<int:pk>/ endpoint by retrieving a specific game by its id.
		"""
		response = self.client.get(f"/games/{self.game1.id}/")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
