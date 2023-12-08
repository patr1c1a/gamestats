from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Player(models.Model):
    """
    A single player.
    """
    nickname = models.CharField(max_length=255)
    profile_image = models.URLField()

    def __str__(self):
        return f"(ID: {self.pk}). NICKNAME: {self.nickname}. AVATAR: {self.profile_image}"


class Stat(models.Model):
    """
    Statistics on a single player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField()

    def __str__(self):
        return f"(ID: {self.pk}). PLAYER: {self.player.nickname}. SCORE: {self.score}. CREATED: {self.creation_date}."


class Game(models.Model):
    """
    Details about a game involving 0 to 10 players.
    """
    players = models.ManyToManyField(Player, related_name='players')
    start_timestamp = models.DateTimeField(auto_now_add=True)
    finish_timestamp = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # If start_timestamp is not set, set it to the current date and time
        if not self.start_timestamp:
            self.start_timestamp = timezone.now()

        super().save(*args, **kwargs)

        # Check if the winner is in the list of players after the instance is saved
        if self.winner and self.winner not in self.players.all():
            raise ValidationError({
                'winner': ValidationError('Winner must be in the players list.', code='invalid'),
            })

        # Check that finish date is later than start date.
        if self.finish_timestamp and self.start_timestamp and self.finish_timestamp <= self.start_timestamp:
            raise ValidationError("Finish date must be later than start date.")

    def __str__(self):
        winner = self.winner.nickname if self.winner else 'No winner yet'
        return f"(ID: {self.pk}). START: {self.start_timestamp}. FINISH: {self.finish_timestamp}. WINNER: {winner}"
