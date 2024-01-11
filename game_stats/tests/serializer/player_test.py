from django.test import TestCase
from game_stats.serializers import PlayerSerializer
from django.contrib.auth.models import User


class PlayerSerializerTest(TestCase):

    def test_valid_nickname(self):
        """
        Tests that a player created with a valid nickname is valid.
        """
        user = User.objects.create(username='test_user1', password='test_password')
        data = {"user": user.id, "nickname": "test_player"}
        serializer = PlayerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_nickname(self):
        """
        Tests that a player created with an invalid nickname raises an error.
        """
        user = User.objects.create(username='test_user2', password='test_password')
        data = {"user": user.id, "nickname": "test player"}
        serializer = PlayerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Nickname can only contain letters, numbers, and underscores.", serializer.errors["nickname"])
