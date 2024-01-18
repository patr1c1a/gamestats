from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from game_stats.models import Player


class PlayerViewsTest(TestCase):
    def setUp(self):
        """
        Creates test data. Logs in as an admin (is_staff=True) user.
        """
        self.user1 = User.objects.create(username="test_user1", password="test_password", is_staff=True)
        self.user2 = User.objects.create(username="test_user2", password="test_password")
        self.user3 = User.objects.create(username="test_user3", password="test_password")
        self.player1 = Player.objects.create(user=self.user1, nickname="player_view_test_player1")
        self.player2 = Player.objects.create(user=self.user2, nickname="player_view_test_player2")
        self.player3 = Player.objects.create(user=self.user3, nickname="player_view_test_player3")

        self.access_token = str(AccessToken.for_user(self.user1))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_get_players(self):
        """
        Tests GET to /players/ endpoint by validating that nicknames of all players added during test setUp are returned.
        """
        response = self.client.get(reverse("player-list-or-create"))
        returned_nicknames = [player["nickname"] for player in response.data["results"]]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.player1.nickname, returned_nicknames)
        self.assertIn(self.player2.nickname, returned_nicknames)
        self.assertIn(self.player3.nickname, returned_nicknames)

    def test_get_player_detail(self):
        """
        Tests GET to /players/<int:pk>/ endpoint by retrieving a specific player by its id.
        """
        response = self.client.get(reverse("player-by-id", args=[self.player1.id]), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nickname"], self.player1.nickname)

    def test_get_player_no_trailing_slash(self):
        """
        Tests GET to /players/<int:pk> (no trailing slash) endpoint by retrieving a specific player by its id.
        """
        response = self.client.get(f"/players/{self.player1.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_player(self):
        """
        Tests POST to /players/ to create a new player.
        """
        data = {
            "user": User.objects.create(username="test_user4", password="test_password").id,
            "nickname": "player_view_test_player4",
        }
        response = self.client.post(
            reverse("player-list-or-create"), data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_player(self):
        """
        Tests PATCH to /players/<int:pk>/ endpoint by updating a specific player.
        """
        updated_data = {"nickname": "player_view_test_nickname_changed"}
        response = self.client.patch(
            reverse("player-by-id", args=[self.player2.id]),
            data=updated_data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check database:
        self.player2.refresh_from_db()
        self.assertEqual(self.player2.nickname, "player_view_test_nickname_changed")

    def test_delete_player(self):
        """
        Tests DELETE to /players/<int:pk>/ endpoint by deleting a specific player.
        """
        response = self.client.delete(reverse("player-by-id", args=[self.player2.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check database:
        with self.assertRaises(Player.DoesNotExist):
            Player.objects.get(id=self.player2.id)
