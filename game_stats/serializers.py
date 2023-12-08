from rest_framework import serializers
from .models import Player, Stat, Game


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"

    def validate_nickname(self, value):
        """
        Validate that the nickname only contains letters, numbers and underscores.
        """
        if not (value.replace("_", "").isalnum()) or not (value.isascii()):
            raise serializers.ValidationError(
                "Nickname can only contain letters, numbers, and underscores."
            )
        return value


class StatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stat
        fields = "__all__"

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole object for the
        `player` field instead of just the primary key by mapping the field to its serialized value.
        Also shows date in the "%Y-%m-%d %H:%M:%S" format.
        """
        representation = super().to_representation(instance)
        representation["player"] = PlayerSerializer(instance.player).data
        creation_date = instance.creation_date.strftime("%Y-%m-%d %H:%M:%S")
        representation["creation_date"] = creation_date
        return representation


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = "__all__"

    def to_representation(self, instance):
        """
        Overrides the `to_representation` method to display the whole object for the
        `winner` field instead of just the primary key by mapping the field to its serialized value.
        Also shows timestamps in the "%Y-%m-%d %H:%M:%S" format.
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

        start_timestamp = instance.start_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        representation["start_timestamp"] = start_timestamp

        finish_timestamp = instance.finish_timestamp.strftime("%Y-%m-%d %H:%M:%S")
        representation["finish_timestamp"] = finish_timestamp

        return representation
