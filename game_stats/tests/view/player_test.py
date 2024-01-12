from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from game_stats.models import Player


class PlayerViewsTest(TestCase):
    def setUp(self):
        """
        Creates test data.
        """
        self.user1 = User.objects.create(username='test_user1', password='test_password')
        self.user2 = User.objects.create(username='test_user2', password='test_password')
        self.user3 = User.objects.create(username='test_user3', password='test_password')
        self.player1 = Player.objects.create(user=self.user1, nickname="player_view_test_player1")
        self.player2 = Player.objects.create(user=self.user2, nickname="player_view_test_player2")
        self.player3 = Player.objects.create(user=self.user3, nickname="player_view_test_player3")

        self.access_token = str(AccessToken.for_user(self.user1))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_get_players(self):
        """
        Tests the /players/ endpoint by validating that nicknames of all players added during test setUp are returned.
        """
        response = self.client.get("/players/")
        returned_nicknames = [player["nickname"] for player in response.data["results"]]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.player1.nickname, returned_nicknames)
        self.assertIn(self.player2.nickname, returned_nicknames)
        self.assertIn(self.player3.nickname, returned_nicknames)

    def test_get_player_detail(self):
        """
        Tests the players/<int:pk>/ endpoint by retrieving a specific player by its id.
        """
        response = self.client.get(f"/players/{self.player1.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], self.player1.nickname)
