from django.test import TestCase
from game_stats.serializers import PlayerSerializer


class PlayerSerializerTest(TestCase):
    def test_valid_nickname(self):
        """
        Tests that a player created with a valid nickname is valid.
        """
        data = {"nickname": "test_player"}
        serializer = PlayerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_nickname(self):
        """
        Tests that a player created with an invalid nickname raises an error.
        """
        data = {"nickname": "test player"}
        serializer = PlayerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Nickname can only contain letters, numbers, and underscores.", serializer.errors["nickname"])
