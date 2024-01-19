from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from game_stats.models import Game, Player, User


class GameViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data. Logs in as an admin (is_staff=True) user.
		"""
		self.user1 = User.objects.create(username="test_user1", password="test_password", is_staff=True)
		self.user2 = User.objects.create(username="test_user2", password="test_password")
		self.player1 = Player.objects.create(user=self.user1, nickname="game_view_test_player1")
		self.player2 = Player.objects.create(user=self.user2, nickname="game_view_test_player2")
		self.game1 = Game.objects.create()
		self.game1.players.set([self.player1, self.player2])
		self.game1.winner = self.player1
		self.game2 = Game.objects.create()
		self.game2.players.set([])

		self.access_token = str(AccessToken.for_user(self.user1))
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

	def test_get_games(self):
		"""
		Tests GET to /games/ endpoint by validating that nicknames of all players added during test setUp are returned.
		"""
		response = self.client.get(reverse("game-list-or-create"))
		returned_nicknames = []
		for game in response.data["results"]:
			for player in game.get("players"):
				returned_nicknames.append(player["nickname"])
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn(self.player1.nickname, returned_nicknames)
		self.assertIn(self.player2.nickname, returned_nicknames)

	def test_get_game_detail(self):
		"""
		Tests GET to /games/<int:pk>/ endpoint by retrieving a specific game by its id.
		"""
		response = self.client.get(reverse("game-by-id", args=[self.game1.id]), format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], self.game1.id)

	def test_get_game_no_trailing_slash(self):
		"""
		Tests GET to /games/<int:pk> (no trailing slash) endpoint by retrieving a specific game by its id.
		"""
		response = self.client.get(f"/games/{self.game1.id}")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], self.game1.id)

	def test_create_game(self):
		"""
		Tests POST to /games/ to create a new game.
		"""
		data = {"players": [self.player1.id, self.player2.id], "winner": self.player1.id}
		response = self.client.post(reverse("game-list-or-create"), data=data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_game(self):
		"""
		Tests PATCH to /games/<int:pk>/ endpoint by updating a specific game.
		"""
		updated_data = {"winner": self.player2.id}
		response = self.client.patch(reverse("game-by-id", args=[self.game1.id]), data=updated_data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Check database:
		self.game1.refresh_from_db()
		self.assertEqual(self.game1.winner, self.player2)

	def test_delete_game(self):
		"""
		Tests DELETE to /games/<int:pk>/ endpoint by deleting a specific game.
		"""
		response = self.client.delete(reverse("game-by-id", args=[self.game1.id]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		# Check database:
		with self.assertRaises(Game.DoesNotExist):
			Game.objects.get(id=self.game1.id)
