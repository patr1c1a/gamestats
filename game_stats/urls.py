from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats.views import *

urlpatterns = [
   path("players/", PlayerList.as_view(), name="player-list-or-create"),
   path("players/<int:pk>/", PlayerDetail.as_view(), name="player-by-id"),
   path("stats/", StatList.as_view(), name="stat-list-or-create"),
   path("stats/<int:pk>/", StatDetail.as_view(), name="stat-by-id"),
   path("games/", GameList.as_view(), name="game-list-or-create"),
   path("games/<int:pk>/", GameDetail.as_view(), name="game-by-id"),
   path("stats/ranking/", StatRankingView.as_view(), name="top-10-scores"),
   path("users/", UserListCreateView.as_view(), name="user-list-or-create"),
   path("users/<int:pk>/", UserRetrieveUpdateDestroyView.as_view(), name="user-by-id"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
