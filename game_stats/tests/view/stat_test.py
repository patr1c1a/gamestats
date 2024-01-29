from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken
from game_stats.models import Stat, Player, User
from django.utils import timezone


class StatViewsTest(TestCase):
	def setUp(self):
		"""
		Creates test data.
		"""
		self.user1 = User.objects.create(username="test_user1", password="test_password", is_staff=True)
		self.user2 = User.objects.create(username="test_user2", password="test_password")
		self.player1 = Player.objects.create(user=self.user1, nickname="stat_view_test_player1")
		self.player2 = Player.objects.create(user=self.user2, nickname="stat_view_test_player2")
		self.stat1 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=10)
		self.stat2 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=5)
		self.stat3 = Stat.objects.create(player=self.player1, creation_date=timezone.now(), score=1)

		self.access_token = str(AccessToken.for_user(self.user1))
		self.client = APIClient()
		self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

	def test_get_stats(self):
		"""
		Tests GET to /stats/ endpoint by validating that stats added during test setUp() are returned, asserting their
		scores and player nicknames.
		"""
		response = self.client.get(reverse("stat-list-or-create"))
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
		Tests GET to stats/<int:pk>/ endpoint by retrieving a specific stat by its id.
		"""
		response = self.client.get(reverse("stat-by-id", args=[self.stat1.id]), format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["player"]["id"], self.player1.id)
		self.assertEqual(response.data["score"], self.stat1.score)
		# Check date
		self.assertEqual(response.data["creation_date"][:10], str(self.stat1.creation_date)[:10])
		# Check time
		self.assertEqual(response.data["creation_date"][11:19], str(self.stat1.creation_date)[11:19])

	def test_get_stat_no_trailing_slash(self):
		"""
		Tests GET to /stats/<int:pk> (no trailing slash) endpoint by retrieving a specific stat by its id.
		"""
		response = self.client.get(f"/stats/{self.stat1.id}")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["id"], self.stat1.id)

	def test_create_stat(self):
		"""
		Tests POST to /stats/ to create a new stat.
		"""
		data = {"player": self.player2.id, "creation_date": timezone.now(), "score": 90}
		response = self.client.post(reverse("stat-list-or-create"), data=data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_update_game(self):
		"""
		Tests PATCH to /stats/<int:pk>/ endpoint by updating a specific stat.
		"""
		updated_data = {"score": 80}
		response = self.client.patch(reverse("stat-by-id", args=[self.stat1.id]), data=updated_data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# Check database:
		self.stat1.refresh_from_db()
		self.assertEqual(self.stat1.score, 80)

	def test_delete_stat(self):
		"""
		Tests DELETE to /stats/<int:pk>/ endpoint by deleting a specific stat.
		"""
		response = self.client.delete(reverse("stat-by-id", args=[self.stat1.id]))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		# Check database:
		with self.assertRaises(Stat.DoesNotExist):
			Stat.objects.get(id=self.stat1.id)
