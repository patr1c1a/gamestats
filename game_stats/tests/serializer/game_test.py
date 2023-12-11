from django.test import TestCase
from game_stats.models import Player, Game
from game_stats.serializers import GameSerializer, PlayerSerializer


class GameSerializerTest(TestCase):
    def setUp(self):
        """
        Creates test data.
        """
        self.player1 = Player.objects.create(nickname="test_player1")
        self.player2 = Player.objects.create(nickname="test_player2")
        self.player3 = Player.objects.create(nickname="test_player3")
        self.game = {
            "players": [self.player1.id, self.player2.id],
            "winner": self.player1.id,
        }

    def test_validate_winner_not_in_players(self):
        """
        Tests that validation raises an error when the winner is not included in the players list.
        """
        self.game["winner"] = self.player3.id
        serializer = GameSerializer(data=self.game)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertEqual(serializer.errors["non_field_errors"][0], "Winner must be included in the players list.")

    def test_to_representation(self):
        """
        Tests that the representation of fields matches the serialized data.
        """
        game = Game.objects.create(winner=self.player1)
        game.players.set([self.player1, self.player2])
        serializer = GameSerializer(instance=game)
        self.assertEqual(serializer.data["players"], [PlayerSerializer(self.player1).data, PlayerSerializer(self.player2).data])
        self.assertEqual(serializer.data["winner"], PlayerSerializer(self.player1).data)

