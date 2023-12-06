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
        Mocks the requests.get() method to avoid actual API calls during testing.
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

        # assert at least 1 player and 1 stat have been created, since the script creates a random number of them.
        self.assertEqual(Game.objects.count(), 1)
        self.assertGreaterEqual(Player.objects.count(), 1)
        self.assertGreaterEqual(Stat.objects.count(), 1)

        player = Player.objects.first()
        stat = Stat.objects.first()
        game = Game.objects.first()

        self.assertEqual(stat.player, player)
        self.assertEqual(player.nickname, "test_user")
        self.assertEqual(player.profile_image, "https://example.com/test_image.jpg")
        self.assertEqual(stat.player, player)
        self.assertIsNotNone(stat.creation_date)
        self.assertIsNotNone(stat.score)
        self.assertIn(player, game.players.all())
        self.assertIsNotNone(game.start_timestamp)
        self.assertIsNotNone(game.finish_timestamp)
        self.assertIn(game.winner, game.players.all())

    @patch('game_stats.management.commands.simulate_stats.requests.get')
    def test_simulate_stats_exception_handling(self, mock_requests_get):
        """
        Tests the simulate_stats command exception handling.
        Mocks the requests.get() method to avoid actual API calls during testing.
        """
        mock_requests_get.side_effect = requests.exceptions.RequestException("Mocked API error")

        # run simulate_stats script
        command = Command()
        command.handle()

        # assert no data has been inserted in the database, due to an exception.
        self.assertEqual(Player.objects.count(), 0)
        self.assertEqual(Stat.objects.count(), 0)
        self.assertEqual(Game.objects.count(), 0)
