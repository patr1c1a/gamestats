import random
import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from game_stats.models import Player, Stat, Game
from django.db import transaction


class Command(BaseCommand):
    """
    Simulates random Stats, Games, and Players and insert into database.
    """

    help = "Simulate random Stats, Games, and Players and insert into the database."

    def handle(self, *args, **options):
        """
        Handles the command execution.
        Generates random data for Player, Stat, and Game models and inserts it into the database.
        """
        with transaction.atomic():
            try:
                print(self.style.SUCCESS("Simulating statistics, games, and players..."))

                # simulate Player data
                players = self.generate_random_players()

                # simulate Game data
                winner = random.choice(players) if players else None
                game = Game()
                game.save()
                game.players.set(players)
                game.winner = winner
                game.save()

                # simulate Stat data
                player_data = self.generate_random_player_data()
                new_player = random.choice(players) if players else Player.objects.create(
                    nickname=player_data["nickname"], profile_image=player_data["profile_image"])

                Stat.objects.create(
                    player=new_player,
                    creation_date=timezone.now(),
                    score=random.randint(0, 100),
                    game=game if players else None)

                print(self.style.SUCCESS("Statistics, games, and players simulation completed."))

            except Exception as e:
                print(self.style.ERROR(f"An error occurred: {str(e)}"))

    def generate_random_player_data(self) -> dict:
        """
        Generates random player data by calling the randomuser.me API.

        Returns:
        dict: Dictionary containing "nickname" and "profile_image" fields.
        """
        try:
            response = requests.get("https://randomuser.me/api/")
            response.raise_for_status()
            data = response.json()["results"][0]
            return {
                "nickname": data["login"]["username"],
                "profile_image": data["picture"]["large"],
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error calling randomuser.me API: {str(e)}")

    def generate_random_players(self) -> list:
        """
        Generates a list of random players.

        Returns:
        list: List of Player instances.
        """
        try:
            num_players = random.randint(0, 10)
            players = []

            for _ in range(num_players):
                player_data = self.generate_random_player_data()
                player, _ = Player.objects.get_or_create(nickname=player_data["nickname"],
                                                         profile_image=player_data["profile_image"])
                players.append(player)

            return players

        except Exception as e:
            raise Exception(f"Error generating random players: {str(e)}")
