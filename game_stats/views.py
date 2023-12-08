from rest_framework import generics
from .models import Player, Stat, Game
from .serializers import PlayerSerializer, StatSerializer, GameSerializer


class PlayerList(generics.ListCreateAPIView):
	"""
	API endpoint that allows players to be viewed or created.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer


class PlayerDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	API endpoint that allows a single player to be viewed, updated, or deleted.
	"""
	queryset = Player.objects.all()
	serializer_class = PlayerSerializer


class StatList(generics.ListCreateAPIView):
	"""
	API endpoint that allows stats to be viewed or created.
	"""
	queryset = Stat.objects.all()
	serializer_class = StatSerializer


class StatDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	API endpoint that allows a single stat to be viewed, updated, or deleted.
	"""
	queryset = Stat.objects.all()
	serializer_class = StatSerializer


class GameList(generics.ListCreateAPIView):
	"""
	API endpoint that allows games to be viewed or created.
	"""
	queryset = Game.objects.all()
	serializer_class = GameSerializer


class GameDetail(generics.RetrieveUpdateDestroyAPIView):
	"""
	API endpoint that allows a single game to be viewed, updated, or deleted.
	"""
	queryset = Game.objects.all()
	serializer_class = GameSerializer
