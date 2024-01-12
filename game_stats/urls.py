from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from game_stats.views import *

urlpatterns = [
   path("players/", PlayerListCreate.as_view(), name="player-list-or-create"),
   path("players/<int:pk>/", PlayerRetrieveUpdateDestroy.as_view(), name="player-by-id"),
   path("stats/", StatListCreate.as_view(), name="stat-list-or-create"),
   path("stats/<int:pk>/", StatRetrieveUpdateDestroy.as_view(), name="stat-by-id"),
   path("games/", GameListCreate.as_view(), name="game-list-or-create"),
   path("games/<int:pk>/", GameRetrieveUpdateDestroy.as_view(), name="game-by-id"),
   path("stats/ranking/", StatRankingView.as_view(), name="top-10-scores"),
   path("users/", UserListCreate.as_view(), name="user-list-or-create"),
   path("users/<int:pk>/", UserRetrieveUpdateDestroy.as_view(), name="user-by-id"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
