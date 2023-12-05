from django.db import models


class Player(models.Model):
    nickname = models.CharField(max_length=255)
    profile_image = models.URLField()

    def __str__(self):
        return f'{self.nickname} - {self.profile_image}'

class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()

    def __str__(self):
        return f'{self.creation_date} - {self.score}'
