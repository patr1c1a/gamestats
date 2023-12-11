from django.test import TestCase
from game_stats.models import Stat, Player, Game
from game_stats.serializers import StatSerializer
import re


class StatSerializerTest(TestCase):
    def setUp(self):
        """
        Creates test data.
        """
        self.player = Player.objects.create(nickname="test_player")
        self.game = Game.objects.create()
        self.game.players.add(self.player)
        self.stat = {"player": self.player.id, "score": 10, "game": self.game.id}
        self.other_player = Player.objects.create(nickname="other_player")

    def test_representation(self):
        """
        Tests that the representation of fields matches the serialized data.
        """
        serializer = StatSerializer(data=self.stat)
        self.assertTrue(serializer.is_valid())
        stat = serializer.save()
        self.assertEqual(Stat.objects.count(), 1)
        self.assertEqual(stat.score, self.stat["score"])
        date_format_regex = re.compile(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        self.assertTrue(date_format_regex.match(serializer.data["creation_date"]))
        self.assertEqual(stat.player.id, self.stat["player"])
        self.assertEqual(stat.game.id, self.stat["game"])

    def test_validate_player_not_in_game(self):
        """
        Tests that validation raises an error when the player is not included in the game's players list.
        """
        self.stat["player"] = self.other_player.id
        serializer = StatSerializer(data=self.stat)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(
            serializer.errors["non_field_errors"][0],
            "Player must be included in the game's players list.",
        )
