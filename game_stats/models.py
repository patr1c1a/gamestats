from django.db import models


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
    score = models.IntegerField()

    def __str__(self):
        return f"(ID: {self.pk}). PLAYER: {self.player.nickname}. SCORE: {self.score}. CREATED: {self.creation_date}."


class Game(models.Model):
    """
    Details on a game involving 0 to 10 players.
    """
    players = models.ManyToManyField(Player, related_name='games')
    start_timestamp = models.DateTimeField(auto_now_add=True)
    finish_timestamp = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"(ID: {self.pk}). PLAYERS: {', '.join([str(player.nickname) for player in self.players.all()])}. " \
               f"START: {self.start_timestamp}. FINISH: {self.finish_timestamp}. WINNER: {self.winner.nickname}"
