from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from game_stats.models import Player, Game


class GameModelTest(TestCase):
    def setUp(self):
        # Create Players to associate Game to
        self.player1 = Player.objects.create(nickname="test_player1")
        self.player2 = Player.objects.create(nickname="test_player2")
        self.player3 = Player.objects.create(nickname="test_player3")

    def test_game_creation(self):
        """
        Tests that a Game can be created with all its fields.
        """
        game = Game(
            start_timestamp=timezone.now(),
            finish_timestamp=timezone.now() + timezone.timedelta(minutes=1),
        )
        game.save()
        game.players.add(self.player1, self.player2, self.player3)
        game.winner = self.player1

        self.assertEqual(game.winner, self.player1)
        self.assertEqual(
            set(game.players.all()), {self.player1, self.player2, self.player3}
        )

    def test_game_delete(self):
        """
        Tests that a Game can be deleted.
        """
        game = Game(
            start_timestamp=timezone.now(),
            finish_timestamp=timezone.now() + timezone.timedelta(minutes=1),
        )
        game.save()
        game.players.add(self.player1, self.player2, self.player3)
        game.winner = self.player1

        game.delete()
        with self.assertRaises(Game.DoesNotExist):
            Game.objects.get(id=game.id)

    def test_game_winner_not_in_players_list(self):
        """
        Tests that creating a Game with a winner not in the players list raises a ValidationError.
        """
        game = Game(
            start_timestamp=timezone.now(),
            finish_timestamp=timezone.now() + timezone.timedelta(minutes=1),
            winner=self.player1,
        )
        with self.assertRaises(ValidationError) as context:
            game.save()
        self.assertIn(
            "Winner must be in the players list.",
            context.exception.error_dict["winner"][0],
        )
