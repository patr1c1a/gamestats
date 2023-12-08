from django.test import TestCase
from game_stats.models import Stat
from game_stats.serializers import StatSerializer, PlayerSerializer


class StatSerializerTest(TestCase):
    def setUp(self):
        # Test data
        self.player = {"nickname": "test_player"}
        player_serializer = PlayerSerializer(data=self.player)
        player_serializer.is_valid()
        self.player_pk = player_serializer.save().pk

        self.stat = {"player": self.player_pk, "score": 10}

    def test_representation(self):
        serializer = StatSerializer(data=self.stat)
        self.assertTrue(serializer.is_valid())
        stat = serializer.save()
        self.assertEqual(Stat.objects.count(), 1)
        self.assertEqual(stat.score, self.stat["score"])
        self.assertEqual(stat.player.pk, self.player_pk)
