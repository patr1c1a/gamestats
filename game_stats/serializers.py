from rest_framework import serializers
from .models import Player, Stat, Game
from django.contrib.auth.models import User


class PlayerSerializer(serializers.ModelSerializer):
    """
    Serializer for the Player model.
    """
    class Meta:
        model = Player
        fields = "__all__"

    def validate_nickname(self, value):
        """
        Validates that the nickname only contains letters, numbers and underscores.
        """
        if not (value.replace("_", "").isalnum()) or not (value.isascii()):
            raise serializers.ValidationError(
                "Nickname can only contain letters, numbers, and underscores."
            )
        return value


class GameSerializer(serializers.ModelSerializer):
    """
    Serializer for the Game model.
    """
    class Meta:
        model = Game
        fields = "__all__"

    def validate(self, data):
        """
        Validates that the winner is included in the "players" list.
        """
        players = data['players']
        winner = data['winner'] if 'winner' in data else None
        if winner and winner not in players:
            raise serializers.ValidationError("Winner must be included in the players list.")
        return data

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole object for the
        `winner` field instead of just the primary key by mapping the field to its serialized value.
        """
        representation = super().to_representation(instance)
        players_instances = instance.players.all()
        if players_instances:
            representation["players"] = [PlayerSerializer(player).data for player in players_instances]
        else:
            representation["players"] = []
        winner_instance = instance.winner
        if winner_instance is not None:
            representation["winner"] = PlayerSerializer(winner_instance).data
        else:
            representation["winner"] = None
        return representation


class StatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Stat model.
    """
    class Meta:
        model = Stat
        fields = "__all__"

    def validate(self, data):
        """
        Validates that the player is included in the Game.
        """
        player = data['player']
        game = data['game'] if 'game' in data else None
        if game and player not in game.players.all():
            raise serializers.ValidationError("Player must be included in the game's players list.")
        return data

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole objects for the
        `player` and `game` fields instead of just the primary key by mapping the field
        to its serialized value. Also shows creation_date in the "%Y-%m-%d %H:%M:%S" format.
        """
        representation = super().to_representation(instance)
        representation["player"] = PlayerSerializer(instance.player).data
        creation_date = instance.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        representation["creation_date"] = creation_date
        representation["game"] = GameSerializer(instance.game).data
        return representation


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
