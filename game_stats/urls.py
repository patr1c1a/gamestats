from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats.views import *

urlpatterns = [
   path("players/", PlayerList.as_view(), name="player-list"),
   path("players/<int:pk>/", PlayerDetail.as_view(), name="player-by-id"),
   path("stats/", StatList.as_view(), name="stat-list"),
   path("stats/<int:pk>/", StatDetail.as_view(), name="stat-by-id"),
   path("games/", GameList.as_view(), name="game-list"),
   path("games/<int:pk>/", GameDetail.as_view(), name="game-by-id"),
   path("stats/ranking/", StatRankingView.as_view(), name="top-10-scores"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
