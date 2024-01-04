from django.test import TestCase
from unittest.mock import patch
from game_stats.models import Player, Stat, Game
from game_stats.management.commands.simulate_stats import Command
import requests


class SimulateStatsTests(TestCase):
    """
    Tests for the simulate_stats management command.
    """
    @patch('game_stats.management.commands.simulate_stats.requests.get')
    def test_simulate_stats_command(self, mock_requests_get):
        """
        Tests the simulate_stats command by running it and asserting the expected database records.
        Mocks the requests.get() method to generate a new player without actual API calls during testing.
        """
        mock_response = {
            'results': [{
                'login': {'username': 'test_user'},
                'picture': {'large': 'https://example.com/test_image.jpg'},
            }]
        }
        mock_requests_get.return_value.json.return_value = mock_response

        # run simulate_stats script
        command = Command()
        command.handle()

        # assert at least 1 player, 1 game and 1 stat have been created.
        self.assertGreaterEqual(Player.objects.count(), 1)
        self.assertEqual(Game.objects.count(), 1)
        self.assertGreaterEqual(Stat.objects.count(), 1)

        player = Player.objects.first()
        game = Game.objects.first()
        stat = Stat.objects.first()

        self.assertEqual(player.nickname, "test_user")
        self.assertEqual(player.profile_image, "https://example.com/test_image.jpg")
        self.assertIn(game.winner, game.players.all())
        self.assertEqual(stat.player, player)
        self.assertEqual(stat.game, game)
        self.assertIsNotNone(stat.creation_date)
        self.assertIsNotNone(stat.score)

    @patch('game_stats.management.commands.simulate_stats.requests.get')
    def test_simulate_stats_exception_handling(self, mock_requests_get):
        """
        Tests the simulate_stats command exception handling.
        Mocks the requests.get() method to generate a new player without actual API calls during testing.
        """
        mock_requests_get.side_effect = requests.exceptions.RequestException("Mocked API error")

        # run simulate_stats script
        command = Command()
        command.handle()

        # assert no data has been inserted in the database, due to an exception.
        self.assertEqual(Player.objects.count(), 0)
        self.assertEqual(Stat.objects.count(), 0)
        self.assertEqual(Game.objects.count(), 0)

    @patch('game_stats.management.commands.simulate_stats.requests.get')
    @patch('game_stats.management.commands.simulate_stats.Command.generate_random_players')
    def test_simulate_stats_with_zero_players(self, mock_generate_random_players, mock_requests_get):
        """
        Tests the simulate_stats command when the players list in the Game object is empty.
        Mocks the requests.get() method to generate a new player without actual API calls during testing.
        Mocks the generate_random_players() method in the script to return an empty list of players.
        """
        mock_requests_get.return_value.json.return_value = {
            'results': [{
                'login': {'username': 'test_user'},
                'picture': {'large': 'https://example.com/test_image.jpg'},
            }]
        }
        mock_generate_random_players.return_value = []

        command = Command()
        command.handle()

        stat = Stat.objects.latest('id')

        self.assertEqual(Player.objects.count(), 1)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(Stat.objects.count(), 1)
        self.assertIsNotNone(stat.player)
        self.assertEqual(stat.player.nickname, "test_user")
        self.assertEqual(stat.player.profile_image, "https://example.com/test_image.jpg")
