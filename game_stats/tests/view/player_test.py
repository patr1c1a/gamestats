from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from game_stats.models import Player


class PlayerViewsTest(TestCase):
    def setUp(self):
        """
        Creates test data.
        """
        self.player1 = Player.objects.create(nickname="test_player1")
        self.player2 = Player.objects.create(nickname="test_player2")
        self.player3 = Player.objects.create(nickname="test_player3")
        self.client = APIClient()

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
