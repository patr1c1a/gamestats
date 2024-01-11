from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class Player(models.Model):
    """
    A single player.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=255)
    profile_image = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check that nickname only contains alphanumeric or underscore characters.
        if not (str(self.nickname).replace('_', '').isalnum()) or not (str(self.nickname).isascii()):
            raise ValidationError("Nickname can only contain letters, numbers and underscores.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"(ID: {self.pk}). NICKNAME: {self.nickname}. AVATAR: {self.profile_image}. REAL NAME: {self.user.first_name + self.user.last_name}"


class Game(models.Model):
    """
    Details about a game involving 0 to 10 players.
    """
    players = models.ManyToManyField(Player, related_name='players')
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        winner = self.winner.nickname if self.winner else 'No winner.'
        return f"(ID: {self.pk}). WINNER: {winner}"


class Stat(models.Model):
    """
    Statistics on a single player.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"(ID: {self.pk}). PLAYER: {self.player.nickname}. SCORE: {self.score}. CREATED: {self.creation_date}." \
               f"GAME: {self.game}"
